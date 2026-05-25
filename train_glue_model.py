"""
train_glue_model.py
====================
Train mô hình học sâu (Keras) phân loại keo: OK vs NG (nhị phân).

    NG = không có keo  /  lệch đường keo  /  ít keo   (gộp chung 1 lớp)
    OK = keo đạt yêu cầu

Dùng transfer learning với MobileNetV2 (nhẹ + nhanh, hợp dây chuyền AOI),
huấn luyện 2 pha: (1) đóng băng backbone luyện đầu phân loại, (2) fine-tune
mở khoá vài lớp cuối với learning rate thấp.

TƯƠNG THÍCH với hàm AI() trong AOIE41EU_V6_glue.py (không cần sửa app):
    - input 224x224, ảnh chia /255.0  (model TỰ map [0,1] -> [-1,1] bên trong)
    - output sigmoid 1 giá trị = xác suất OK  ->  prediction[0][0]
    - giữ nguyên ngưỡng pred > 0.3 là OK

CẤU TRÚC THƯ MỤC DỮ LIỆU (nhãn gán theo tên folder; alphabet -> NG=0, OK=1):

    dataset/
        NG/      <- ảnh: không keo, lệch đường keo, ít keo (gộp chung)
        OK/      <- ảnh: keo đạt

Cài đặt:
    pip install "tensorflow>=2.9" numpy

Train:
    python train_glue_model.py --data_dir dataset --epochs 25 --out glue_model.h5

Dự đoán thử 1 ảnh (mô phỏng đúng hàm AI()):
    python train_glue_model.py --predict glue_model.h5 --image img/1.png
"""

import argparse
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

IMG_SIZE = (224, 224)
CLASS_NAMES = ["NG", "OK"]          # index 0 = NG, index 1 = OK (khớp pred = P(OK))
AUTOTUNE = tf.data.AUTOTUNE


# --------------------------------------------------------------------------- #
# Dữ liệu
# --------------------------------------------------------------------------- #
def build_datasets(data_dir, batch_size, val_split, seed):
    train_ds = keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=val_split,
        subset="training",
        seed=seed,
        image_size=IMG_SIZE,
        batch_size=batch_size,
        label_mode="binary",
        class_names=CLASS_NAMES,
    )
    val_ds = keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=val_split,
        subset="validation",
        seed=seed,
        image_size=IMG_SIZE,
        batch_size=batch_size,
        label_mode="binary",
        class_names=CLASS_NAMES,
    )
    return train_ds, val_ds


def compute_class_weight(train_ds):
    """Cân bằng dữ liệu khi số ảnh NG/OK chênh lệch (trọng số nghịch đảo tần suất)."""
    counts = np.zeros(2, dtype=np.int64)
    for _, labels in train_ds.unbatch():
        counts[int(labels.numpy().item())] += 1
    total = int(counts.sum())
    weights = {i: (total / (2.0 * c)) if c > 0 else 1.0 for i, c in enumerate(counts)}
    print(f"Số ảnh train mỗi lớp: NG={counts[0]}, OK={counts[1]}  ->  class_weight={weights}")
    return weights


def make_augmenter():
    """Augmentation NHẸ, giữ nguyên nhãn (xoay/dịch nhỏ + đổi sáng/tương phản
    để chịu được biến động ánh sáng — vốn rất lớn ở ảnh thực tế)."""
    return keras.Sequential(
        [
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.04),
            layers.RandomZoom(0.10),
            layers.RandomTranslation(0.05, 0.05),
            layers.RandomBrightness(0.20),     # chạy trên thang [0,255]
            layers.RandomContrast(0.20),
        ],
        name="augment",
    )


def prepare(ds, augmenter=None):
    """Augment (chỉ khi train) trên thang [0,255] -> rồi chuẩn hoá /255.0 -> [0,1]."""
    if augmenter is not None:
        ds = ds.map(lambda x, y: (augmenter(x, training=True), y), num_parallel_calls=AUTOTUNE)
    ds = ds.map(lambda x, y: (x / 255.0, y), num_parallel_calls=AUTOTUNE)
    return ds.prefetch(AUTOTUNE)


# --------------------------------------------------------------------------- #
# Mô hình
# --------------------------------------------------------------------------- #
def build_model():
    inputs = keras.Input(shape=IMG_SIZE + (3,))        # ảnh đã /255.0 -> [0,1]
    x = layers.Rescaling(2.0, offset=-1.0)(inputs)     # [0,1] -> [-1,1] cho MobileNetV2
    base = keras.applications.MobileNetV2(
        input_shape=IMG_SIZE + (3,),
        include_top=False,
        weights="imagenet",
    )
    base.trainable = False
    x = base(x, training=False)                        # BatchNorm luôn ở chế độ inference
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(1, activation="sigmoid")(x)  # = P(OK)
    return keras.Model(inputs, outputs, name="glue_ok_ng"), base


def compile_model(model, lr):
    model.compile(
        optimizer=keras.optimizers.Adam(lr),
        loss="binary_crossentropy",
        metrics=[
            "accuracy",
            keras.metrics.Precision(name="precision"),
            keras.metrics.Recall(name="recall"),
            keras.metrics.AUC(name="auc"),
        ],
    )


def unfreeze_top(base, n_layers=40):
    """Mở khoá ~n lớp cuối của backbone để fine-tune, giữ BatchNorm đóng băng."""
    base.trainable = True
    for layer in base.layers[:-n_layers]:
        layer.trainable = False
    for layer in base.layers:
        if isinstance(layer, layers.BatchNormalization):
            layer.trainable = False


# --------------------------------------------------------------------------- #
# Đánh giá
# --------------------------------------------------------------------------- #
def evaluate(model, ds, threshold):
    y_true, y_prob = [], []
    for x, y in ds:
        y_prob.extend(model.predict(x, verbose=0).ravel().tolist())
        y_true.extend(y.numpy().ravel().tolist())
    y_true = np.array(y_true, dtype=int)
    y_pred = (np.array(y_prob) >= threshold).astype(int)

    tp = int(((y_pred == 1) & (y_true == 1)).sum())   # OK đoán đúng OK
    tn = int(((y_pred == 0) & (y_true == 0)).sum())   # NG đoán đúng NG
    fp = int(((y_pred == 1) & (y_true == 0)).sum())   # NG bị đoán OK  (LỌT LỖI - nguy hiểm)
    fn = int(((y_pred == 0) & (y_true == 1)).sum())   # OK bị đoán NG  (rớt oan)

    acc = (tp + tn) / max(len(y_true), 1)
    prec_ng = tn / max(tn + fn, 1)        # độ chính xác khi báo NG
    rec_ng = tn / max(tn + fp, 1)         # tỉ lệ bắt được NG (recall của NG)

    print("\n================  ĐÁNH GIÁ TRÊN VALIDATION  ================")
    print(f"  Ngưỡng quyết định OK: pred >= {threshold}")
    print(f"  Accuracy : {acc:.4f}")
    print(f"  Confusion matrix:")
    print(f"                 Đoán NG     Đoán OK")
    print(f"     Thực NG  |   {tn:6d}      {fp:6d}   <- {fp} ca LỌT LỖI (NG bị cho qua)")
    print(f"     Thực OK  |   {fn:6d}      {tp:6d}   <- {fn} ca rớt oan")
    print(f"  Bắt lỗi NG (recall NG): {rec_ng:.4f} | Chính xác khi báo NG: {prec_ng:.4f}")
    print("  Lưu ý: tăng ngưỡng -> bắt được nhiều NG hơn nhưng dễ rớt oan OK; giảm thì ngược lại.")
    print("============================================================\n")


# --------------------------------------------------------------------------- #
# Dự đoán 1 ảnh (mô phỏng đúng hàm AI() trong app)
# --------------------------------------------------------------------------- #
def predict_image(model_path, image_path, threshold):
    model = keras.models.load_model(model_path)
    img = keras.utils.load_img(image_path, target_size=IMG_SIZE)
    arr = keras.utils.img_to_array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)
    p = float(model.predict(arr, verbose=0)[0][0])
    label = "OK" if p > threshold else "NG"
    print(f"{image_path}  ->  P(OK)={p:.4f}  =>  {label}  (ngưỡng {threshold})")
    return p


# --------------------------------------------------------------------------- #
# Train
# --------------------------------------------------------------------------- #
def train(args):
    raw_train, raw_val = build_datasets(args.data_dir, args.batch_size, args.val_split, args.seed)
    class_weight = compute_class_weight(raw_train)

    train_ds = prepare(raw_train, make_augmenter())
    val_ds = prepare(raw_val)

    model, base = build_model()

    early = keras.callbacks.EarlyStopping(
        monitor="val_loss", patience=6, restore_best_weights=True, verbose=1
    )

    # ---- Pha 1: đóng băng backbone, luyện đầu phân loại ----
    print("\n>>> PHA 1: luyện đầu phân loại (backbone đóng băng)")
    compile_model(model, lr=1e-3)
    reduce_lr = keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss", factor=0.5, patience=3, min_lr=1e-6, verbose=1
    )
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=args.epochs,
        class_weight=class_weight,
        callbacks=[early, reduce_lr],
    )

    # ---- Pha 2: fine-tune vài lớp cuối ----
    if not args.no_finetune and args.fine_tune_epochs > 0:
        print("\n>>> PHA 2: fine-tune các lớp cuối của backbone (LR thấp)")
        unfreeze_top(base, n_layers=args.unfreeze_layers)
        compile_model(model, lr=1e-5)
        model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=args.fine_tune_epochs,
            class_weight=class_weight,
            callbacks=[
                keras.callbacks.EarlyStopping(
                    monitor="val_loss", patience=6, restore_best_weights=True, verbose=1
                )
            ],
        )

    evaluate(model, val_ds, args.threshold)

    model.save(args.out)
    print(f"Đã lưu model: {args.out}")
    print(f"-> Trỏ 'train_model' trong file cấu hình sys của app tới '{args.out}' là dùng được ngay.")


# --------------------------------------------------------------------------- #
def parse_args():
    p = argparse.ArgumentParser(description="Train model phán keo OK/NG (Keras).")
    p.add_argument("--data_dir", default="dataset", help="Thư mục dữ liệu chứa NG/ và OK/")
    p.add_argument("--epochs", type=int, default=25, help="Số epoch pha 1")
    p.add_argument("--fine_tune_epochs", type=int, default=12, help="Số epoch pha 2 (fine-tune)")
    p.add_argument("--unfreeze_layers", type=int, default=40, help="Số lớp cuối mở khoá khi fine-tune")
    p.add_argument("--no_finetune", action="store_true", help="Bỏ qua pha fine-tune")
    p.add_argument("--batch_size", type=int, default=16)
    p.add_argument("--val_split", type=float, default=0.2)
    p.add_argument("--seed", type=int, default=123)
    p.add_argument("--threshold", type=float, default=0.3, help="Ngưỡng P(OK) để coi là OK (khớp app)")
    p.add_argument("--out", default="glue_model.h5", help="Đường dẫn lưu model")
    # chế độ dự đoán thử
    p.add_argument("--predict", metavar="MODEL", help="Đường dẫn model để dự đoán thử")
    p.add_argument("--image", help="Ảnh cần dự đoán (đi kèm --predict)")
    return p.parse_args()


def main():
    args = parse_args()
    if args.predict:
        if not args.image:
            raise SystemExit("Cần --image khi dùng --predict")
        predict_image(args.predict, args.image, args.threshold)
    else:
        train(args)


if __name__ == "__main__":
    main()
