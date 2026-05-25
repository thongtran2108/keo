import os
import cv2
import csv
import sys
import time
import tkinter
import datetime
from datetime import datetime
from lib import *
import numpy as np
from INI import Ini
import customtkinter
from Tooltip import ToolTip
from SDmodule.SDCam import *
from PIL import Image, ImageTk
from tkinter import messagebox
from keras.models import load_model
from keras.utils import load_img, img_to_array
import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports
import threading
import requests
customtkinter.set_appearance_mode('dark')

#region
with open("sysEU/login.ini", "w") as f:
    f.write("False")
path_area_1 = open("area/area1_p1.ini", "r")
path_area_2 = open("area/area2_p1.ini", "r")
path_area_3 = open("area/area3_p1.ini", "r")
path_area_4 = open("area/area4_p1.ini", "r")
path_area_ct = open("area/area_ct.ini", "r")

area_1 = path_area_1.readlines()
area_2 = path_area_2.readlines()
area_3 = path_area_3.readlines()
area_4 = path_area_4.readlines()
areact = path_area_ct.readlines()

min_area1 = int(area_1[0])
min_area2 = int(area_2[0])
min_area3 = int(area_3[0])
min_area4 = int(area_4[0])
min_area_ct = int(areact[0])

max_area1 = int(area_1[1])
max_area2 = int(area_2[1])
max_area3 = int(area_3[1])
max_area4 = int(area_4[1])
max_area_ct = int(areact[1])

path_area_12 = open("area/area1_p2.ini", "r")
path_area_22 = open("area/area2_p2.ini", "r")
path_area_32 = open("area/area3_p2.ini", "r")
path_area_42 = open("area/area4_p2.ini", "r")
path_area_ct2 = open("area/area_ct2.ini", "r")

area_12 = path_area_12.readlines()
area_22= path_area_22.readlines()
area_32 = path_area_32.readlines()
area_42 = path_area_42.readlines()
areact2 = path_area_ct2.readlines()

min_area12 = int(area_12[0])
min_area22 = int(area_22[0])
min_area32 = int(area_32[0])
min_area42 = int(area_42[0])
min_area_ct2 = int(areact2[0])

max_area12 = int(area_12[1])
max_area22 = int(area_22[1])
max_area32 = int(area_32[1])
max_area42 = int(area_42[1])
max_area_ct2 = int(areact2[1])

path_area_13 = open("area/area1_p3.ini", "r")
path_area_23 = open("area/area2_p3.ini", "r")
path_area_33 = open("area/area3_p3.ini", "r")
path_area_43 = open("area/area4_p3.ini", "r")
path_area_ct3 = open("area/area_ct3.ini", "r")

area_13 = path_area_13.readlines()
area_23= path_area_23.readlines()
area_33 = path_area_33.readlines()
area_43 = path_area_43.readlines()
areact3 = path_area_ct3.readlines()

min_area13 = int(area_13[0])
min_area23 = int(area_23[0])
min_area33 = int(area_33[0])
min_area43 = int(area_43[0])
min_area_ct3 = int(areact3[0])

max_area13 = int(area_13[1])
max_area23 = int(area_23[1])
max_area33 = int(area_33[1])
max_area43 = int(area_43[1])
max_area_ct3 = int(areact3[1])

path_area_14 = open("area/area1_p4.ini", "r")
path_area_24 = open("area/area2_p4.ini", "r")
path_area_34 = open("area/area3_p4.ini", "r")
path_area_44 = open("area/area4_p4.ini", "r")
path_area_ct4 = open("area/area_ct4.ini", "r")

area_14 = path_area_14.readlines()
area_24= path_area_24.readlines()
area_34 = path_area_34.readlines()
area_44 = path_area_44.readlines()
areact4 = path_area_ct4.readlines()

min_area14 = int(area_14[0])
min_area24 = int(area_24[0])
min_area34 = int(area_34[0])
min_area44 = int(area_44[0])
min_area_ct4 = int(areact4[0])

max_area14 = int(area_14[1])
max_area24 = int(area_24[1])
max_area34 = int(area_34[1])
max_area44 = int(area_44[1])
max_area_ct4 = int(areact4[1])

drawing = False
point0 = None
point1 = None
#endregion

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("TESLA")
        # self.geometry("1944x1080")
        # self.state('zoomed')
        self.attributes('-fullscreen', True)
        self.title("- ❤️T🍀 -")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)  
        # load images with light and dark mode image
        self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(self.image_path, "tesla.png")), size=(60, 40))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(self.image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(self.image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(self.image_path, "home_dark.png")),
                                               dark_image=Image.open(os.path.join(self.image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(self.image_path, "chat_dark.png")),
                                               dark_image=Image.open(os.path.join(self.image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(self.image_path, "add_user_dark.png")),
                                                dark_image=Image.open(os.path.join(self.image_path, "add_user_light.png")), size=(20, 20))
        self.camera_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(self.image_path, "camera.png")),
                                           size=(30, 30))
        self.power_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(self.image_path, "power.png")),
                                           size=(30, 30))
        self.logout_images = customtkinter.CTkImage(light_image=Image.open(os.path.join(self.image_path, "logout.png")),
                                           size=(30, 30))
        self.material_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(self.image_path, "material.png")),
                                                dark_image=Image.open(os.path.join(self.image_path, "material.png")), size=(30, 30))

          # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="TESLA", image=self.logo_image,
                                                                    compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=(10, 30), pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="MES",
                                                            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                        image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Setting",
                                                            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                        image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")
        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Material",
                                                            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                        image=self.material_image, anchor="w", command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=16, column=0, padx=20, pady=20, sticky="s")
        self.appearance_mode_menu.set('Dark')
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

                # create home frame
        self.home_frame = customtkinter.CTkFrame(self,corner_radius=0, fg_color="transparent")
                
        self.canvas_1 = customtkinter.CTkCanvas(self.home_frame, bg = "white", width = 550, height = 350)
        self.canvas_1.grid(row = 0, column = 0, columnspan = 3,padx = (10, 10), pady = (50, 10))
        self.lbl_canvas1 = customtkinter.CTkLabel(self.canvas_1, text= 'Position 1', fg_color= 'transparent', font= customtkinter.CTkFont('Times New Roman', 22, 'normal'), text_color= 'black')
        self.lbl_canvas1.grid(row = 0, column = 0, columnspan = 3, rowspan = 2, padx = (10, 600), pady = (10, 415))

        self.canvas_2 = customtkinter.CTkCanvas(self.home_frame, bg = "white", width = 550, height = 350)
        self.canvas_2.grid(row = 0, column = 3, columnspan = 3,padx = (10, 10), pady = (50, 10))
        self.lbl_canvas2 = customtkinter.CTkLabel(self.canvas_2, text= 'Position 2', fg_color= 'transparent', font= customtkinter.CTkFont('Times New Roman', 22, 'normal'), text_color= 'black')
        self.lbl_canvas2.grid(row = 0, column = 0, columnspan = 3, rowspan = 2, padx = (10, 600), pady = (10, 415))

        self.canvas_3 = customtkinter.CTkCanvas(self.home_frame, bg = "white", width = 550, height = 350)
        self.canvas_3.grid(row = 1, column = 0, columnspan = 3,padx = (10, 10), pady = (10, 100))
        self.lbl_canvas3 = customtkinter.CTkLabel(self.canvas_3, text= 'Position 3', fg_color= 'transparent', font= customtkinter.CTkFont('Times New Roman', 22, 'normal'), text_color= 'black')
        self.lbl_canvas3.grid(row = 0, column = 0, columnspan = 3, rowspan = 2, padx = (10, 600), pady = (10, 415))

        self.canvas_4 = customtkinter.CTkCanvas(self.home_frame, bg = "white", width = 550, height = 350)
        self.canvas_4.grid(row = 1, column = 3, columnspan = 3,padx = (10, 10), pady = (10, 100))
        self.lbl_canvas4 = customtkinter.CTkLabel(self.canvas_4, text= 'Position 4', fg_color= 'transparent', font= customtkinter.CTkFont('Times New Roman', 22, 'normal'), text_color= 'black')
        self.lbl_canvas4.grid(row = 0, column = 0, columnspan = 2, rowspan = 2, padx = (10, 600), pady = (10, 415))

        self.notification = customtkinter.CTkTextbox(self.home_frame,width=280, height= 1050, fg_color= 'transparent', text_color= ("black", "white"), font= customtkinter.CTkFont('Times New Roman', 15, 'normal'))
        self.notification.grid(row = 0, column = 6, rowspan = 25, padx = 10, pady =10)
        self.notification.tag_config("1", foreground ="green")
        self.notification.tag_config("2", foreground ="red")

                # create second frame
        self.sys = Ini('sysEU/sys.ini')
        self.scan_COM = self.sys.find('SCAN')
        self.menban_COM = self.sys.find('SCAN_MENBAN')
        self.number_COM = self.sys.find('SCAN_NUMBER')
        self.on_SFC = self.sys.find('on_SFC')
        self.sn_link1 = self.sys.find('sn_link1')
        self.sn_link2 = self.sys.find('sn_link2')
        self.save_img = self.sys.find('save_img')
        self.url_post = self.sys.find('POST')
        self.station_name_SFC = self.sys.find('station_name')
        self.tokken_SFC = self.sys.find('tokken')
        self.start_scan = self.sys.find('start_scan')
        self.start_AOI = self.sys.find('start_AOI')
        self.complete_AOI = self.sys.find('complete_AOI')
        self.start_pos = self.sys.find('start_pos')
        # self.url_material1 = self.sys.find('material1')
        self.url_material2 = self.sys.find('material2')
        self.name_staffid = self.sys.find('staffid')
        self.url_save_img = self.sys.find('save_img')
        self.ip_plc = self.sys.find('ip_plc')
        self.log = self.sys.find('add_log')
        self.select_program = self.sys.find('select_program')
        
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.Path_MES = customtkinter.CTkEntry(self.second_frame, width=200, height= 10, fg_color= 'white', text_color= "black", placeholder_text_color = 'black')
        self.Path_MES.grid(row = 0, column = 0, padx = (50, 10), pady = (50, 10))
        self.Path_MES.insert(tkinter.END, str(self.sn_link1))
        self.tooltip = ToolTip(self.Path_MES)
        self.Path_MES.bind("<Enter>", self.tooltip.show_tooltip)
        self.Path_MES.bind("<Leave>", self.tooltip.hide_tooltip)
        self.Path_MES2 = customtkinter.CTkEntry(self.second_frame, width=200, height= 10, fg_color= 'white', text_color= "black", placeholder_text_color = 'black')
        self.Path_MES2.grid(row = 0, column = 3, padx = (50, 10), pady = (50, 10))
        self.Path_MES2.insert(tkinter.END, str(self.sn_link2))
        self.tooltip = ToolTip(self.Path_MES2)
        self.Path_MES2.bind("<Enter>", self.tooltip.show_tooltip)
        self.Path_MES2.bind("<Leave>", self.tooltip.hide_tooltip)
        self.Path_MES_stname = customtkinter.CTkEntry(self.second_frame, width=200, height= 10, fg_color= 'white', text_color= "black", placeholder_text_color = 'black')
        self.Path_MES_stname.grid(row = 0, column = 9, padx = (50, 10), pady = (50, 10))
        self.Path_MES_stname.insert(tkinter.END, str(self.station_name_SFC))
        self.tooltip = ToolTip(self.Path_MES_stname)
        self.Path_MES_stname.bind("<Enter>", self.tooltip.show_tooltip)
        self.Path_MES_stname.bind("<Leave>", self.tooltip.hide_tooltip)
        self.Path_MES_tokken = customtkinter.CTkEntry(self.second_frame, width=200, height= 10, fg_color= 'white', text_color= "black", placeholder_text_color = 'black')
        self.Path_MES_tokken.grid(row = 0, column = 7, padx = (50, 10), pady = (50, 10))
        self.Path_MES_tokken.insert(tkinter.END, str(self.tokken_SFC))
        self.tooltip = ToolTip(self.Path_MES_tokken)
        self.Path_MES_tokken.bind("<Enter>", self.tooltip.show_tooltip)
        self.Path_MES_tokken.bind("<Leave>", self.tooltip.hide_tooltip)
        self.Path_MES_POST = customtkinter.CTkEntry(self.second_frame, width=200, height= 10, fg_color= 'white', text_color= "black", placeholder_text_color = 'black')
        self.Path_MES_POST.grid(row = 0, column = 5, padx = (50, 10), pady = (50, 10))
        self.Path_MES_POST.insert(tkinter.END, str(self.url_post))
        self.tooltip = ToolTip(self.Path_MES_POST)
        self.Path_MES_POST.bind("<Enter>", self.tooltip.show_tooltip)
        self.Path_MES_POST.bind("<Leave>", self.tooltip.hide_tooltip)
        self.Path_url_image = customtkinter.CTkEntry(self.second_frame, width=200, height= 10, fg_color= 'white', text_color= "black", placeholder_text_color = 'black')
        self.Path_url_image.grid(row = 2, column = 5, padx = (50, 10), pady = (50, 10))
        self.Path_url_image.insert(tkinter.END, str(self.url_save_img))
        self.tooltip = ToolTip(self.Path_url_image)
        self.Path_url_image.bind("<Enter>", self.tooltip.show_tooltip)
        self.Path_url_image.bind("<Leave>", self.tooltip.hide_tooltip)

        self.lbl_com_scan = customtkinter.CTkLabel(self.second_frame, text = 'SCAN PRODUCT', font= customtkinter.CTkFont('Times New Roman', 14, 'normal'))
        self.lbl_com_scan.grid(row = 3, column = 0, padx = (10, 10), pady = (100, 0))
        self. available_ports = list(serial.tools.list_ports.comports())
        self.com = []
        for i in self.available_ports:
            self.com.append(str(i.device))
        self.btn_com_scan = customtkinter.CTkOptionMenu(self.second_frame,values=[i for i in self.com], fg_color = ['gray','white'], text_color = 'black',command=self.select_com)
        self.btn_com_scan.grid(row = 4, column = 0,padx = (10, 10), pady = (10, 10))
        self.btn_com_scan.set(str(self.scan_COM))
        self.btn_refresh_com = customtkinter.CTkButton(self.second_frame, width=50, height= 10, text= 'Refresh', command= self.refresh_com)
        self.btn_refresh_com.grid(row = 4, column = 1,padx = (10, 10), pady = (10, 10))

        self.lbl_com_scan_K = customtkinter.CTkLabel(self.second_frame, text = 'SCAN KHUÔN', font= customtkinter.CTkFont('Times New Roman', 14, 'normal'))
        self.lbl_com_scan_K.grid(row = 5, column = 0, padx = (10, 10), pady = (10, 0))
        self.available_port_K = list(serial.tools.list_ports.comports())
        self.com_K = []
        for i_K in self.available_port_K:
            self.com_K.append(str(i_K.device))
        self.btn_com_scan_K = customtkinter.CTkOptionMenu(self.second_frame,values=[i for i in self.com_K], fg_color = ['gray','white'], text_color = 'black',command=self.select_com_N)
        self.btn_com_scan_K.grid(row = 6, column = 0,padx = (10, 10), pady = (10, 10))
        self.btn_com_scan_K.set(str(self.number_COM))
        self.btn_setting_com = customtkinter.CTkButton(self.second_frame, width=50, height= 10, text= 'More', command= self.setting_scan)
        self.btn_setting_com.grid(row = 6, column = 1,padx = (10, 10), pady = (10, 10))

        self.lbl_com_scan_M = customtkinter.CTkLabel(self.second_frame, text = 'SCAN MENBAN', font= customtkinter.CTkFont('Times New Roman', 14, 'normal'))
        self.lbl_com_scan_M.grid(row = 7, column = 0, padx = (10, 10), pady = (10, 0))
        self.available_port_M = list(serial.tools.list_ports.comports())
        self.com_M = []
        for i_M in self.available_port_M:
            self.com_M.append(str(i_M.device))
        self.btn_com_scan_M = customtkinter.CTkOptionMenu(self.second_frame,values=[i for i in self.com_M], fg_color = ['gray','white'], text_color = 'black',command=self.select_com_M)
        self.btn_com_scan_M.grid(row = 8, column = 0,padx = (10, 10), pady = (10, 10))
        self.btn_com_scan_M.set(str(self.menban_COM))

        self.lbl_com_scan_T = customtkinter.CTkLabel(self.second_frame, text = 'TEST SCAN', font= customtkinter.CTkFont('Times New Roman', 14, 'normal'))
        self.lbl_com_scan_T.grid(row = 3, column = 3, padx = (10, 40), pady = (100, 0))
        self.available_port_T = list(serial.tools.list_ports.comports())
        self.com_T = []
        for i_T in self.available_port_T:
            self.com_T.append(str(i_T.device))
        self.btn_com_scan_T = customtkinter.CTkOptionMenu(self.second_frame,values=[i for i in self.com_T], fg_color = ['gray','white'], text_color = 'black', command=self.select_com_T)
        self.btn_com_scan_T.grid(row = 4, column = 3,padx = (10, 10), pady = (10, 10))

        self.btn_on_scan = customtkinter.CTkButton(self.second_frame, width=50, height= 10, text= 'ON SCAN', command= lambda: self.try_scan(ON_OFF=True))
        self.btn_on_scan.grid(row = 4, column = 4,padx = (10, 10), pady = (10, 10))

        self.btn_off_scan = customtkinter.CTkButton(self.second_frame, width=50, height= 10, text= 'OFF SCAN', command= lambda: self.try_scan(ON_OFF=False))
        self.btn_off_scan.grid(row = 5, column = 4,padx = (10, 10), pady = (10, 10))

        self.btn_save_snlink1 = customtkinter.CTkButton(self.second_frame, width=50, height= 10, text= 'sn_link1', command = lambda: self.get_entry('sn_link1', self.Path_MES))
        self.btn_save_snlink1.grid(row = 0, column = 1, padx = (0, 10), pady = (50, 10))
        self.btn_save_snlink2 = customtkinter.CTkButton(self.second_frame, width=50, height= 10, text= 'sn_link2', command = lambda: self.get_entry('sn_link2', self.Path_MES2))
        self.btn_save_snlink2.grid(row = 0, column = 4, padx = (0, 10), pady = (50, 10))
        self.btn_save_stationName = customtkinter.CTkButton(self.second_frame, width=50, height= 10, text= 'Station name', command = lambda: self.get_entry('station_name', self.Path_MES_stname))
        self.btn_save_stationName.grid(row = 0, column = 10, padx = (0, 10), pady = (50, 10))
        self.btn_save_tokken = customtkinter.CTkButton(self.second_frame, width=50, height= 10, text= 'Tokken', command = lambda: self.get_entry('tokken', self.Path_MES_tokken))
        self.btn_save_tokken.grid(row = 0, column = 8, padx = (0, 10), pady = (50, 10))
        self.btn_save_post = customtkinter.CTkButton(self.second_frame, width=50, height= 10, text= 'URL post', command = lambda: self.get_entry('POST', self.Path_MES_POST))
        self.btn_save_post.grid(row = 0, column = 6, padx = (0, 10), pady = (50, 10))
        self.btn_url_image = customtkinter.CTkButton(self.second_frame, width=50, height= 10, text= 'URL images', command = lambda: self.get_entry('save_img', self.Path_url_image))
        self.btn_url_image.grid(row = 2, column = 6, padx = (0, 10), pady = (50, 10))

        self.start_scan_MES= customtkinter.CTkEntry(self.second_frame, width=200, height= 10, fg_color= 'white', text_color= "black", placeholder_text_color = 'black')
        self.start_scan_MES.grid(row = 1, column = 0, padx = (50, 10), pady = (50, 10))
        self.start_scan_MES.insert(tkinter.END, str(self.start_scan))
        self.start_AOI_MES = customtkinter.CTkEntry(self.second_frame, width=200, height= 10, fg_color= 'white', text_color= "black",placeholder_text_color = 'black')
        self.start_AOI_MES.grid(row = 1, column = 3, padx = (50, 10), pady = (50, 10))
        self.start_AOI_MES.insert(tkinter.END, str(self.start_AOI))
        self.complete_AOI_MES = customtkinter.CTkEntry(self.second_frame, width=200, height= 10, fg_color= 'white', text_color= "black", placeholder_text_color = 'black')
        self.complete_AOI_MES.grid(row = 1, column = 5, padx = (50, 10), pady = (50, 10))
        self.complete_AOI_MES.insert(tkinter.END, str(self.complete_AOI))
        self.start_pos_MES = customtkinter.CTkEntry(self.second_frame, width=200, height= 10, fg_color= 'white', text_color= "black", placeholder_text_color = 'black')
        self.start_pos_MES.grid(row = 1, column = 7, padx = (50, 10), pady = (50, 10))
        self.start_pos_MES.insert(tkinter.END, str(self.start_pos))
        self.ip_PLC = customtkinter.CTkEntry(self.second_frame, width=200, height= 10, fg_color= 'white', text_color= "black", placeholder_text_color = 'black')
        self.ip_PLC.grid(row = 1, column = 9, padx = (50, 10), pady = (50, 10))
        self.ip_PLC.insert(tkinter.END, str(self.ip_plc))

        self.btn_start_scan = customtkinter.CTkButton(self.second_frame, width=50, height= 10, text= 'start scan', command = lambda: self.get_entry('start_scan', self.start_scan_MES))
        self.btn_start_scan.grid(row = 1, column = 1, padx = (0, 10), pady = (50, 10))
        self.btn_start_AOI = customtkinter.CTkButton(self.second_frame, width=50, height= 10, text= 'start AOI', command = lambda: self.get_entry('start_AOI', self.start_AOI_MES))
        self.btn_start_AOI.grid(row = 1, column = 4, padx = (0, 10), pady = (50, 10))
        self.btn_complete_AOI = customtkinter.CTkButton(self.second_frame, width=50, height= 10, text= 'complete AOI', command = lambda: self.get_entry('complete_AOI', self.complete_AOI_MES))
        self.btn_complete_AOI.grid(row = 1, column = 6, padx = (0, 10), pady = (50, 10))
        self.btn_start_pos = customtkinter.CTkButton(self.second_frame, width=50, height= 10, text= 'Start pos', command = lambda: self.get_entry('start_pos', self.start_pos_MES))
        self.btn_start_pos.grid(row = 1, column = 8, padx = (0, 10), pady = (50, 10))
        self.btn_ip_plc = customtkinter.CTkButton(self.second_frame, width=50, height= 10, text= 'IP PLC', command = lambda: self.get_entry('ip_plc', self.ip_PLC))
        self.btn_ip_plc.grid(row = 1, column = 10, padx = (0, 10), pady = (50, 10))

        self.on_off_SFC = customtkinter.CTkSwitch(self.second_frame, text = "ON/OFF SFC", command = self.state_on_off_SFC)
        self.on_off_SFC.grid(row = 2, column = 0, padx = (50, 10), pady = (50, 10))

        self.staffid = customtkinter.CTkEntry(self.second_frame, width=200, height= 10, fg_color= 'white', text_color= "black", placeholder_text_color = 'black')
        self.staffid.grid(row = 2, column = 3,padx = (50, 10), pady = (50, 10))
        self.staffid.insert(tkinter.END, str(self.name_staffid))
        self.btn_staffid = customtkinter.CTkButton(self.second_frame, width=50, height= 10, text= 'Employee ID', command = lambda: self.get_entry('staffid', self.staffid))
        self.btn_staffid.grid(row = 2, column = 4, padx = (0, 10), pady = (50, 10))
        
                # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
                # select default frame

        #endregion

        self.notf = customtkinter.CTkRadioButton(self.home_frame, text = 'Camera', state= tkinter.DISABLED)
        self.notf.grid(row = 1, column = 0, padx = (10, 250), pady = (500, 10))

        self.notf1 = customtkinter.CTkRadioButton(self.home_frame, text = 'SFC', state= tkinter.DISABLED)
        self.notf1.grid(row = 1, column = 0, padx = (10, 50), pady = (500, 10))

        self.notf2 = customtkinter.CTkRadioButton(self.home_frame, text = 'PLC', state= tkinter.DISABLED)
        self.notf2.grid(row = 1, column = 0, padx = (150, 10), pady = (500, 10))


        self.times = datetime.now().strftime('%H:%M:%S')

        self.four_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.material2 = customtkinter.CTkEntry(self.four_frame, width=700, height= 10, fg_color= 'white', text_color= "black", placeholder_text_color = 'black')
        self.material2.grid(row = 3, column = 0, columnspan = 9,padx = (50, 10), pady = (50, 10))
        self.material2.insert(tkinter.END, str(self.url_material2))
        self.tooltip = ToolTip(self.material2)
        self.material2.bind("<Enter>", self.tooltip.show_tooltip)
        self.material2.bind("<Leave>", self.tooltip.hide_tooltip)
        # self.material2 = customtkinter.CTkEntry(self.four_frame, width=700, height= 10, fg_color= 'white', text_color= "black", placeholder_text_color = 'black')
        # self.material2.grid(row = 4, column = 0, columnspan = 9,padx = (50, 10), pady = (50, 10))
        # self.material2.insert(tkinter.END, str(self.url_material2))
        # self.tooltip = ToolTip(self.material2)
        # self.material2.bind("<Enter>", self.tooltip.show_tooltip)
        # self.material2.bind("<Leave>", self.tooltip.hide_tooltip)

        self.btn_material2 = customtkinter.CTkButton(self.four_frame, width=50, height= 10, text= 'Material Glur', command = lambda: self.get_entry('material2', self.material2, check_glur = True))
        self.btn_material2.grid(row = 3, column = 0, columnspan = 9, padx = (850, 10), pady = (50, 10))
        # self.btn_material2 = customtkinter.CTkButton(self.four_frame, width=50, height= 10, text= 'material2', command = lambda: self.get_entry('material2', self.material2))
        # self.btn_material2.grid(row = 4, column = 0, columnspan = 9, padx = (850, 10), pady = (50, 10))

        self.btn_test_AOI1 = customtkinter.CTkButton(self.navigation_frame, corner_radius=10, text="AOI 1",
                                                     text_color=("gray10", "gray90"), hover_color=("green", "green"),
                                                image=self.camera_image, anchor="w", command = lambda: self.AOI('img/1.png', 1))
        self.btn_test_AOI1.grid(row = 7, column = 0, padx = 10, pady = 10)
        self.btn_test_AOI2 = customtkinter.CTkButton(self.navigation_frame, corner_radius=10, text="AOI 2",
                                                            text_color=("gray10", "gray90"), hover_color=("green", "green"),
                                                        image=self.camera_image, anchor="w", command = lambda: self.AOI('img/2.png', 2))
        self.btn_test_AOI2.grid(row = 8, column = 0, padx = 10, pady = 10)
        self.btn_test_AOI3 = customtkinter.CTkButton(self.navigation_frame, corner_radius=10, text="AOI 3",
                                                            text_color=("gray10", "gray90"), hover_color=("green", "green"),
                                                        image=self.camera_image, anchor="w", command = lambda: self.AOI('img/3.png', 3))
        self.btn_test_AOI3.grid(row = 9, column = 0, padx = 10, pady = 10)
        self.btn_test_AOI4 = customtkinter.CTkButton(self.navigation_frame, corner_radius=10, text="AOI 4",
                                                            text_color=("gray10", "gray90"), hover_color=("green", "green"),
                                                        image=self.camera_image, anchor="w", command = lambda: self.AOI('img/4.png', 4))
        self.btn_test_AOI4.grid(row = 10, column = 0, padx = 10, pady = 10)

        self.btn_test = customtkinter.CTkButton(self.navigation_frame, corner_radius=10, text="Shut Down",
                                                            text_color=("gray10", "gray90"), hover_color=("red", "red"), image=self.power_image, anchor="w",
                                                        command = self.shutdow)
        self.btn_test.grid(row = 11, column = 0, padx = 10, pady = 10)

        self.btn_logout = customtkinter.CTkButton(self.navigation_frame, corner_radius=10, text="Logout",
                                                            text_color=("gray10", "black"), hover_color=("red", "red"), image=self.logout_images, anchor="w", fg_color='white',
                                                        command = self.logout)
        self.cap = SDCapture(color= True)

        self.lbl_select_program = customtkinter.CTkLabel(self.second_frame, text = 'Select Program', font= customtkinter.CTkFont('Times New Roman', 14, 'normal'))
        self.lbl_select_program.grid(row = 5, column = 3, padx = (10, 10), pady = (10, 0))
        self.option_program = customtkinter.CTkOptionMenu(self.second_frame,values=["M3Y",  "E41 NA", "E41 EU"], fg_color = ['gray','white'], text_color = 'black',command=self.fuc_select_program)
        self.option_program.grid(row = 6, column = 3, padx = (10, 10), pady = (10, 10))
        self.option_program.set(str(self.select_program).replace("_",  " "))

        self.select_frame_by_name("home")

        self.lbl_Times = customtkinter.CTkLabel(self.home_frame, text = '', font= customtkinter.CTkFont('Times New Roman', 14, 'normal'))
        self.lbl_Times.grid(row = 1, column = 0, columnspan = 6, padx = (1000, 10), pady = (500, 0))

        if self.cap.startGrabbing():
            self.notification.insert("0.0", f"\n{self.times}: Đã kết nối Camera!", "1")
            self.notf.select()
            self.notf.configure(text_color_disabled = 'green', fg_color= 'green')
        else:
            self.notification.insert("0.0", f"\n{self.times}: Không kết nối được Camera!!", "2")
            self.notf.select()
            self.notf.configure(text_color_disabled = 'red', fg_color= 'red')

        self.red = (0, 0 , 255)
        self.green = (0, 255, 0)

        self.model = load_model(self.sys.find('train_model'))
        self.notification.insert("0.0", f"\n{self.times}: Program - {self.sys.find('select_program').replace('_', ' ')}", "1")

        state_on = customtkinter.BooleanVar(self, value=True)
        state_off = customtkinter.BooleanVar(self, value=False)
        if self.on_SFC == True:
            self.on_off_SFC.configure(variable=state_on)
        else:
            self.on_off_SFC.configure(variable=state_off)
        self.canvas_1.bind("<Button-1>", self.loggin_frame1)
        self.canvas_2.bind("<Button-1>", self.loggin_frame2)
        self.canvas_3.bind("<Button-1>", self.loggin_frame3)
        self.canvas_4.bind("<Button-1>", self.loggin_frame4)
    
    def fuc_select_program(self, value):
        if value == "M3Y":
            messagebox.showinfo('❤️T🍀', 'Select M3Y mode')
            self.withdraw()
            os.system("python mainm3y.py")
            self.destroy()
        elif value == "E41 NA":
            messagebox.showinfo('❤️T🍀', 'Select E41 NA mode')
            self.withdraw()
            os.system("python main.py")
            self.destroy()
        elif value == "E41 EU":
            messagebox.showinfo('❤️T🍀', 'Select E41 EU mode')
    
    def try_scan(self, ON_OFF:bool):
        self.sys.replace('True', 'superlead_config')
        self.scan_COM_T = self.sys.find('SCAN_TEST')
        time.sleep(0.1)
        self.times = datetime.datetime.now().strftime('%H:%M:%S')
        ser = serial.Serial(self.scan_COM_T, 115200, timeout=1)
        if ON_OFF == True:
            if ser.isOpen():
                ser.write(bytearray(b'T'))
            else:
                ser.open()
                ser.write(bytearray(b'T'))
            data = ser.readline(50)
            data = str(data)[2:-1]
            if len(data) > 0:
                self.notification.insert("0.0", f"\n{self.times}: {str(data)}", "1")
        else:
            if ser.isOpen():
                ser.write(bytearray(b'STOP'))
            else:
                ser.open()
                ser.write(bytearray(b'STOP'))
        self.sys.replace('False', 'superlead_config')
    
    def setting_scan(self):
        r = messagebox.askquestion('❤️T🍀', 'Bạn có muốn mở SuperLead Config?')
        if r ==  'yes':
            self.sys.replace('True', 'superlead_config')
            time.sleep(2)
            os.system('"C:\\Program Files (x86)\\SuperLead\\SuperConfig\\SuperConfig.exe"')
            self.sys.replace('False', 'superlead_config')
        else:
            pass

    def state_on_off_SFC(self):
        if self.on_SFC == True:
            self.on_SFC = False
            self.sys.replace('False', 'on_SFC')
            messagebox.showwarning("❤️T🍀", "SFC đã tắt!")
        else:
            self.on_SFC = True
            self.sys.replace('True', 'on_SFC')
            messagebox.showwarning("❤️T🍀", "SFC đã bật!")
    
    def get_entry(self, data_find, entry_get, check_glur = False):
        data = entry_get.get()
        if check_glur:
            js = {"sn": r"{}".format(str(data))}
            req = requests.post(f"http://10.222.48.213:8888/v2/pass/mes/tsc/checkGlue/TSC-VN/tsc_vn1/agp", json=js)
            if req.json().get('code') == 200:
                self.sys.replace(data, data_find)
                messagebox.showinfo('❤️T🍀', 'Mã keo kiểm tra: Pass')
                self.sys.replace('True', 'change_save')
            else:
                messagebox.showerror('❤️T🍀', str(req.json().get('msg')))
        else:
            if data == '':
                messagebox.showerror('❤️T🍀', 'Lưu không thành công!')
            else:
                self.sys.replace(data, data_find)
                messagebox.showinfo('❤️T🍀', 'Lưu thành công!')
                self.sys.replace('True', 'change_save')
        
    def scan_material(self):
        contain_material1 = self.sys.find('contain_material1')
        contain_material1 = contain_material1.split(',')
        contain_material2 = self.sys.find('contain_material2')
        contain_material2 = contain_material2.split(',')
        scan_COM = self.sys.find('SCAN')
        ser_product = serial.Serial(scan_COM, 115200, 8, timeout = 1)
        while True:
            if ser_product.isOpen():
                ser_product.write(bytearray(b'\x02\xF4\x03'))
            else:
                ser_product.open()
                ser_product.write(bytearray(b'\x02\xF4\x03'))
            data = ser_product.readline(100)
            data_scan = str(data)[2:-1]
            value_material = data_scan
            if len(value_material) > 0:
                ser_product.close()
                for x in contain_material1:
                    if value_material.__contains__(x):
                        self.material1.delete(0,tkinter.END)
                        self.material1.insert(tkinter.END, str(value_material))
                        value_material = value_material.split('\n')
                        self.sys.replace(value_material, 'material1')
                        break
  
                for y in contain_material2:
                    if value_material.__contains__(y):
                        value_material = value_material[12:]
                        self.material2.delete(0,tkinter.END)
                        self.material2.insert(tkinter.END, str(value_material))
                        value_material = value_material.split('\n')
                        self.sys.replace(value_material, 'material2')
                        break
                break
    
    def refresh(self):
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 
    
    def select_com(self, value):
        for i in self.available_ports:
            if value == str(i.device):
                self.sys.replace(str(i.device), 'SCAN')
                messagebox.showinfo('❤️T🍀', 'Select COM Product {}'.format(str(i.device)))

    def select_com_M(self, value):
        for i in self.available_ports:
            if value == str(i.device):
                self.sys.replace(str(i.device), 'SCAN_MENBAN')
                messagebox.showinfo('❤️T🍀', 'Select COM Menban {}'.format(str(i.device)))
    
    def select_com_N(self, value):
        for i in self.available_ports:
            if value == str(i.device):
                self.sys.replace(str(i.device), 'SCAN_NUMBER')
                messagebox.showinfo('❤️T🍀', 'Select COM Khuôn {}'.format(str(i.device)))
    
    def select_com_T(self, value):
        for i in self.available_ports:
            if value == str(i.device):
                self.sys.replace(str(i.device), 'SCAN_TEST')

    def refresh_com(self):
        self. available_ports = list(serial.tools.list_ports.comports())
        self.com = []
        for i in self.available_ports:
            self.com.append(str(i.device))
        self.btn_com_scan.configure(values=[i for i in self.com])
        self.btn_com_scan_K.configure(values=[i for i in self.com])
        self.btn_com_scan_M.configure(values=[i for i in self.com])
        self.btn_com_scan_T.configure(values=[i for i in self.com])

    def shutdow(self):
        r = messagebox.askquestion("❤️T🍀", "Bạn có muốn đóng chương trình không!")
        if r == 'no':
            pass
            # os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 
        else:
            print("\nThe program will be closed...")
            self.cap.closeCamera()
            sys.exit()
    
    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        check_login = open("sysEU/login.ini", "r")
        check_login = check_login.readlines()
        check_login = check_login[0]
        if check_login == "True":
            self.select_frame_by_name("frame_2")
        else:
            os.system("python loginEU.py")
            check_login = open("sysEU/login.ini", "r")
            check_login = check_login.readlines()
            check_login = check_login[0]
            if check_login == "True":
                self.select_frame_by_name("frame_2")
                self.btn_logout.grid(row = 6, column = 0, padx = 10, pady = 10)
            else:
                pass

    def frame_3_button_event(self):
        check_login = open("sysEU/login.ini", "r")
        check_login = check_login.readlines()
        check_login = check_login[0]
        if check_login == "True":
            self.select_frame_by_name("frame_3")
        else:
            os.system("python loginEU.py")
            check_login = open("sysEU/login.ini", "r")
            check_login = check_login.readlines()
            check_login = check_login[0]
            if check_login == "True":
                self.select_frame_by_name("frame_3")
                self.btn_logout.grid(row = 6, column = 0, padx = 10, pady = 10)
            else:
                pass
    
    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def logout(self):
        with open("sysEU/login.ini", "w") as f:
                f.write("False")
        self.select_frame_by_name("home")
        self.btn_logout.grid_forget()
    
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        
        if name == "frame_4":
            self.four_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.four_frame.grid_forget()
            
    def select_roi(self, path_img, path_file_roi1, path_file_roi2, path_file_roi3, path_file_roi4, path_file_roi_center):
        try:
            img = cv2.imread(path_img)
            ROIs = cv2.selectROIs("Select Rois",img)
            r = messagebox.askquestion("❤️T🍀", "Bạn có muốn lưu không!")
            if r == 'yes':
                ##### Luu cac toa do cua ROI vao file##########
                with open(path_file_roi1, "w") as file:
                    file.write(str(ROIs[0][0])+"\n")
                    file.write(str(ROIs[0][1])+"\n")
                    file.write(str(ROIs[0][2])+"\n")
                    file.write(str(ROIs[0][3]))

                with open(path_file_roi2, "w") as file:
                    file.write(str(ROIs[1][0])+"\n")
                    file.write(str(ROIs[1][1])+"\n")
                    file.write(str(ROIs[1][2])+"\n")
                    file.write(str(ROIs[1][3]))
                
                with open(path_file_roi3, "w") as file:
                    file.write(str(ROIs[2][0])+"\n")
                    file.write(str(ROIs[2][1])+"\n")
                    file.write(str(ROIs[2][2])+"\n")
                    file.write(str(ROIs[2][3]))
                
                with open(path_file_roi4, "w") as file:
                    file.write(str(ROIs[3][0])+"\n")
                    file.write(str(ROIs[3][1])+"\n")
                    file.write(str(ROIs[3][2])+"\n")
                    file.write(str(ROIs[3][3]))

                # with open(path_file_roi_center, "w") as file:
                #     file.write(str(ROIs[4][0])+"\n")
                #     file.write(str(ROIs[4][1])+"\n")
                #     file.write(str(ROIs[4][2])+"\n")
                #     file.write(str(ROIs[4][3]))
                #     messagebox.showinfo('Notification', 'Succesfully!')
            else:
                pass
            cv2.destroyAllWindows()
        except:
            messagebox.askretrycancel('❤️T🍀', 'ERROR! Thiếu vùng kiểm tra')
            while True:
                frame = self.cap.read()
                frame = cv2.resize(frame, (880, 680))
                cv2.imwrite(path_img, frame)
                break
            img = cv2.imread(path_img)
            ROIs = cv2.selectROIs("Select Rois",img)
            r = messagebox.askquestion("❤️T🍀", "Bạn có muốn lưu không!")
            if r == 'yes': 
                ##### Luu cac toa do cua ROI vao file##########
                with open(path_file_roi1, "w") as file:
                    file.write(str(ROIs[0][0])+"\n")
                    file.write(str(ROIs[0][1])+"\n")
                    file.write(str(ROIs[0][2])+"\n")
                    file.write(str(ROIs[0][3]))

                with open(path_file_roi2, "w") as file:
                    file.write(str(ROIs[1][0])+"\n")
                    file.write(str(ROIs[1][1])+"\n")
                    file.write(str(ROIs[1][2])+"\n")
                    file.write(str(ROIs[1][3]))
                
                with open(path_file_roi3, "w") as file:
                    file.write(str(ROIs[2][0])+"\n")
                    file.write(str(ROIs[2][1])+"\n")
                    file.write(str(ROIs[2][2])+"\n")
                    file.write(str(ROIs[2][3]))
                
                with open(path_file_roi4, "w") as file:
                    file.write(str(ROIs[3][0])+"\n")
                    file.write(str(ROIs[3][1])+"\n")
                    file.write(str(ROIs[3][2])+"\n")
                    file.write(str(ROIs[3][3]))

                with open(path_file_roi_center, "w") as file:
                    file.write(str(ROIs[3][0])+"\n")
                    file.write(str(ROIs[3][1])+"\n")
                    file.write(str(ROIs[3][2])+"\n")
                    file.write(str(ROIs[3][3]))
                    messagebox.showinfo('❤️T🍀', 'Thành công!')
            else:
                pass
            cv2.destroyAllWindows()

    def get_data_area(self, entry1, entry2, path_save):
        r = messagebox.askquestion("❤️T🍀", "Do you want save!")
        if r == 'yes':
            try:
                ghd = entry1.get()
                ghd = int(ghd)
                ght = entry2.get()
                ght = int(ght)
                with open(path_save,"w",encoding='utf-8') as file:
                    file.write(str(ghd)+"\n")
                    file.write(str(ght)+"\n")
                # messagebox.OK  = 'ok'
                messagebox.showinfo('❤️T🍀', 'Succesfully!')
            except:
                messagebox.showerror('❤️T🍀', 'ERROR!') 
        else:
            pass     

    def contours(self, roi, mask, black = False):
        if black == True:
            mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY_INV)[1]
        self.contourss, self.hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) 
        if len(self.contourss) >= 1:
            self.contours_max = max(self.contourss, key = cv2.contourArea)
            self.area = cv2.contourArea(self.contours_max)
            cv2.drawContours(roi,[self.contours_max], -1 ,(0,255,0), 2)
        else:
            self.area = 0
        return self.area
    
    def draw_contours(self, roi, mask,color, black = False):
        if black == True:
            mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY_INV)[1]
        self.contoursss, self.hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) 
        if len(self.contoursss) >= 1:
            self.contours_max = max(self.contoursss, key = cv2.contourArea)
            cv2.drawContours(roi,[self.contours_max], -1 , color, 2)

    def add_log(self, mess: str):
        self.times_log = datetime.now()
        self.text_file = self.times_log.strftime("%Y%m%d")
        self.path_file_save = "log/" + self.text_file + '.txt'
        with open(self.path_file_save,  'a', encoding= 'utf-8') as f:
            f.writelines([mess])

    def AI(self,  image):
        img = load_img(image, target_size=(224, 224))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0

        # D? ?o¨¢n
        prediction = self.model.predict(img_array)
        confidence = prediction[0][0]
        return confidence

    def filterNoise_contours(self,img,mask_name,p,hsv_link,name_side, check_bw=False):
        hsv_file = open(f'sys_new/hsv/{hsv_link}/{name_side}.csv',"r",encoding='utf-8')
        roi_hsv = hsv_file.readlines()
        min_h = int(roi_hsv[0])
        min_s = int(roi_hsv[1])
        min_v = int(roi_hsv[2])
        max_h = int(roi_hsv[3])
        max_s = int(roi_hsv[4])
        max_v = int(roi_hsv[5])
        # erode
        er_file = open(f'sys_new/settingnoise/{p}/erode_{name_side}.ini',"r",encoding='utf-8')
        get_er = er_file.readlines()
        param_er = int(get_er[0])
        # dilate
        di_file = open(f'sys_new/settingnoise/{p}/dilate_{name_side}.ini',"r",encoding='utf-8')
        get_di = di_file.readlines()
        param_di = int(get_di[0])
        # blur
        bl_file = open(f'sys_new/settingnoise/{p}/blur_{name_side}.ini',"r",encoding='utf-8')
        get_bl = bl_file.readlines()
        param_bl = int(get_bl[0])

        # morph
        morph_file = open(f'sys_new/settingnoise/{p}/morph_{name_side}.ini',"r",encoding='utf-8')
        get_morph = morph_file.readlines()
        param_morph = get_morph[0]
        morph_ker_file = open(f'sys_new/settingnoise/{p}/morph_kernel_{name_side}.ini',"r",encoding='utf-8')
        get_morph_ker = morph_ker_file.readlines()
        param_morph_ker = int(get_morph_ker[0])
        if check_bw == True:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)[1]
            cv2.imwrite(f'img/{p}_mask/{mask_name}.png', ret)
            contours, _ = cv2.findContours(ret, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            area = self.calculateArea(contours) 
            return area
        else:
            if param_bl>0:
                img = cv2.medianBlur(img,param_bl)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            low = np.array([min_h,min_s,min_v])
            high = np.array([max_h,max_s,max_v])
            mask = cv2.inRange(hsv,low,high)
            if param_er>0:
                mask = cv2.erode(mask,(param_er,param_er))
            if param_di>0:
                mask = cv2.dilate(mask,(param_di,param_di))
            if param_morph_ker>0:
                if param_morph == "MORPH_CLOSE":
                    morph = cv2.MORPH_CLOSE
                else:
                    morph = cv2.MORPH_OPEN
                mask = cv2.morphologyEx(mask,morph,kernel=np.ones((param_morph_ker,param_morph_ker),np.uint8))
            cv2.imwrite(f'img/{p}_mask/{mask_name}.png',mask)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            area = self.calculateArea(contours) 
            return area
    
    def calculateArea(self,contours):
        totalArea1 = 0
        for cnt in contours:
            area1 = cv2.contourArea(cnt)
            totalArea1 += area1
        return totalArea1
    def show_loading(self):
        self.loading_window = customtkinter.CTkToplevel(self)
        self.loading_window.title("Đang tải dữ liệu...")
        self.loading_window.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self.loading_window.attributes("-alpha", 0.92)
        self.loading_window.configure(fg_color="#000000")  # nền đen trong mờ

        # Nền mờ phủ toàn màn hình
        overlay = customtkinter.CTkFrame(self.loading_window, fg_color="#000000")
        overlay.pack(fill="both", expand=True)

        # Frame loading chính giữa
        frame = customtkinter.CTkFrame(overlay, corner_radius=20, fg_color=("#f5f5f5", "#2b2b2b"))
        frame.place(relx=0.5, rely=0.5, anchor="center")

        label = customtkinter.CTkLabel(frame, text="Đang tải, vui lòng chờ...", font=("Segoe UI", 20))
        label.pack(pady=(25, 10))

        # Lấy màu nền cho Canvas
        bg_color = "#f5f5f5" if customtkinter.get_appearance_mode() == "Light" else "#2b2b2b"

        # Spinner xoay
        canvas = customtkinter.CTkCanvas(frame, width=100, height=100, bg=bg_color, highlightthickness=0)
        canvas.pack(pady=5)
        arc = canvas.create_arc(10, 10, 90, 90, start=0, extent=90, width=6, style="arc", outline="#1E90FF")

        # Thanh tiến trình
        progressbar = customtkinter.CTkProgressBar(frame, width=300, height=10)
        progressbar.pack(pady=(10, 25))
        progressbar.set(0)
        # --- Hiệu ứng xoay ---
        def rotate_spinner():
            angle = 0
            while True:
                try:
                    canvas.itemconfig(arc, start=angle)
                    angle = (angle + 10) % 360
                    time.sleep(0.03)
                except:
                    break  # Dừng khi cửa sổ bị đóng

        # --- Thanh tiến trình chạy qua lại ---
        def animate_progress():
            while True:
                try:
                    for i in range(100):
                        progressbar.set(i / 100)
                        time.sleep(0.02)
                    for i in reversed(range(100)):
                        progressbar.set(i / 100)
                        time.sleep(0.02)
                except:
                    break

        threading.Thread(target=rotate_spinner, daemon=True).start()
        threading.Thread(target=animate_progress, daemon=True).start()
    
    def close_loading(self):
        if self.loading_window:
            self.loading_window.destroy()
            self.loading_window = None
    
    def loggin_frame1(self,even):
        check_login = open("sysEU/login.ini", "r")
        check_login = check_login.readlines()
        check_login = check_login[0]
        if check_login == "True":
            self.show_loading()
            threading.Thread(target=self.run_setting_script_p1, daemon=True).start()
        else:
            os.system("python loginEU.py")
            check_login = open("sysEU/login.ini", "r")
            check_login = check_login.readlines()
            check_login = check_login[0]
            if check_login == "True":
                self.show_loading()
                threading.Thread(target=self.run_setting_script_p1, daemon=True).start()
                self.btn_logout.grid(row = 6, column = 0, padx = 10, pady = 10)
            else:
                pass
    
    def loggin_frame2(self,even):
        check_login = open("sysEU/login.ini", "r")
        check_login = check_login.readlines()
        check_login = check_login[0]
        if check_login == "True":
            self.show_loading()
            threading.Thread(target=self.run_setting_script_p2, daemon=True).start()
        else:
            os.system("python loginEU.py")
            check_login = open("sysEU/login.ini", "r")
            check_login = check_login.readlines()
            check_login = check_login[0]
            if check_login == "True":
                self.show_loading()
                threading.Thread(target=self.run_setting_script_p2, daemon=True).start()
                self.btn_logout.grid(row = 6, column = 0, padx = 10, pady = 10)
            else:
                pass
    def loggin_frame3(self,even):
        check_login = open("sysEU/login.ini", "r")
        check_login = check_login.readlines()
        check_login = check_login[0]
        if check_login == "True":
            self.show_loading()
            threading.Thread(target=self.run_setting_script_p3, daemon=True).start()
        else:
            os.system("python loginEU.py")
            check_login = open("sysEU/login.ini", "r")
            check_login = check_login.readlines()
            check_login = check_login[0]
            if check_login == "True":
                self.show_loading()
                threading.Thread(target=self.run_setting_script_p3, daemon=True).start()
                self.btn_logout.grid(row = 6, column = 0, padx = 10, pady = 10)
            else:
                pass
    def loggin_frame4(self,even):
        check_login = open("sysEU/login.ini", "r")
        check_login = check_login.readlines()
        check_login = check_login[0]
        if check_login == "True":
            self.show_loading()
            threading.Thread(target=self.run_setting_script_p4, daemon=True).start()
        else:
            os.system("python loginEU.py")
            check_login = open("sysEU/login.ini", "r")
            check_login = check_login.readlines()
            check_login = check_login[0]
            if check_login == "True":
                self.show_loading()
                threading.Thread(target=self.run_setting_script_p4, daemon=True).start()
                self.btn_logout.grid(row = 6, column = 0, padx = 10, pady = 10)
            else:
                pass

    def run_setting_script_p1(self):
        os.system("python detail_Aoi/settingAoip1.py")
        self.after(0, self.close_loading)
    def run_setting_script_p2(self):
        os.system("python detail_Aoi/settingAoip2.py")
        self.after(0, self.close_loading)
    def run_setting_script_p3(self):
        os.system("python detail_Aoi/settingAoip3.py")
        self.after(0, self.close_loading)
    def run_setting_script_p4(self):
        os.system("python detail_Aoi/settingAoip4.py")
        self.after(0, self.close_loading)

    def coordinate_calculate(self,img,p,position):
        # coordinate
        coordinate_file = open(f"sys_new/coordinate/{p}/coordinate.ini",'r')
        coordinate_file = coordinate_file.readlines()
        xco = int(coordinate_file[0])
        yco = int(coordinate_file[1])
        wco = int(coordinate_file[2])
        hco = int(coordinate_file[3])
        coordinate_left = open(f"sys_new/coordinate/{p}/left.ini",'r')
        coordinate_left = coordinate_left.readlines()
        xcol = int(coordinate_left[0])
        ycol = int(coordinate_left[1])
        coordinate_top = open(f"sys_new/coordinate/{p}/top.ini",'r')
        coordinate_top = coordinate_top.readlines()
        xcot = int(coordinate_top[0])
        ycot = int(coordinate_top[1])
        coordinate_right = open(f"sys_new/coordinate/{p}/right.ini",'r')
        coordinate_right = coordinate_right.readlines()
        xcor = int(coordinate_right[0])
        ycor = int(coordinate_right[1])
        coordinate_center = open(f"sys_new/coordinate/{p}/center.ini",'r')
        coordinate_center = coordinate_center.readlines()
        xcoc = int(coordinate_center[0])
        ycoc = int(coordinate_center[1])
        coordinate_bottom = open(f"sys_new/coordinate/{p}/bottom.ini",'r')
        coordinate_bottom = coordinate_bottom.readlines()
        xcob = int(coordinate_bottom[0])
        ycob = int(coordinate_bottom[1])
        # coordinate out
        coordinate_left_out = open(f"sys_new/coordinate/{p}/left_out.ini",'r')
        coordinate_left_out = coordinate_left_out.readlines()
        xcol_out = int(coordinate_left_out[0])
        ycol_out = int(coordinate_left_out[1])
        coordinate_top_out = open(f"sys_new/coordinate/{p}/top_out.ini",'r')
        coordinate_top_out = coordinate_top_out.readlines()
        xcot_out = int(coordinate_top_out[0])
        ycot_out = int(coordinate_top_out[1])
        coordinate_right_out = open(f"sys_new/coordinate/{p}/right_out.ini",'r')
        coordinate_right_out = coordinate_right_out.readlines()
        xcor_out = int(coordinate_right_out[0])
        ycor_out = int(coordinate_right_out[1])
        coordinate_bottom_out = open(f"sys_new/coordinate/{p}/bottom_out.ini",'r')
        coordinate_bottom_out = coordinate_bottom_out.readlines()
        xcob_out = int(coordinate_bottom_out[0])
        ycob_out = int(coordinate_bottom_out[1])
        crop_fil = img[yco:yco+hco, xco:xco+wco]
        template = cv2.imread('match_temp.png')
        target_Y = yco
        target_X = xco
        try:
            result = cv2.matchTemplate(crop_fil, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            print(f"Bounding rect trên ảnh gốc: {xco+max_loc[0]}, {max_loc[1]+yco}")
            print("tuong dong C: ",max_val)
            print("toa do C: ",max_loc)
            target_Y = max_loc[1]+yco
            target_X = max_loc[0]+xco
        except:
            print('khong co')
            target_Y = yco
            target_X = xco
        
        roi_files = [f"sys_new/roi/{position}/left.ini", f"sys_new/roi/{position}/top.ini", f"sys_new/roi/{position}/right.ini", f"sys_new/roi/{position}/bottom.ini",f"sys_new/roi/{position}/center.ini",
                     f"sys_new/roi/{position}/left_out.ini", f"sys_new/roi/{position}/top_out.ini", f"sys_new/roi/{position}/right_out.ini", f"sys_new/roi/{position}/bottom_out.ini"]
        roi_coords = []

        for roi_file in roi_files:
            with open(roi_file, "r") as f:
                roi = [int(line) for line in f.readlines()]
                roi_coords.append(roi)

        d1_r1, d2_r1, d3_r1, d4_r1 = roi_coords[0]
        d1_r2, d2_r2, d3_r2, d4_r2 = roi_coords[1]
        d1_r3, d2_r3, d3_r3, d4_r3 = roi_coords[2]
        d1_r4, d2_r4, d3_r4, d4_r4 = roi_coords[3]
        d1_r5, d2_r5, d3_r5, d4_r5 = roi_coords[4]
        d1_r6, d2_r6, d3_r6, d4_r6 = roi_coords[5]#left
        d1_r7, d2_r7, d3_r7, d4_r7 = roi_coords[6]#top
        d1_r8, d2_r8, d3_r8, d4_r8 = roi_coords[7]#right
        d1_r9, d2_r9, d3_r9, d4_r9 = roi_coords[8]#bottom
        with open(f"sys_new/roi/{position}/left.ini", "w") as file:
            file.write(str(target_X-xcol)+"\n")
            file.write(str(target_Y-ycol)+"\n")
            file.write(str(d3_r1)+"\n")
            file.write(str(d4_r1))
        with open(f"sys_new/roi/{position}/top.ini", "w") as file:
            file.write(str(target_X-xcot)+"\n")
            file.write(str(target_Y-ycot)+"\n")
            file.write(str(d3_r2)+"\n")
            file.write(str(d4_r2))
        with open(f"sys_new/roi/{position}/right.ini", "w") as file:
            file.write(str(target_X-xcor)+"\n")
            file.write(str(target_Y-ycor)+"\n")
            file.write(str(d3_r3)+"\n")
            file.write(str(d4_r3))
        with open(f"sys_new/roi/{position}/bottom.ini", "w") as file:
            file.write(str(target_X-xcob)+"\n")
            file.write(str(target_Y-ycob)+"\n")
            file.write(str(d3_r4)+"\n")
            file.write(str(d4_r4))
        with open(f"sys_new/roi/{position}/center.ini", "w") as file:
            file.write(str(target_X-xcoc)+"\n")
            file.write(str(target_Y-ycoc)+"\n")
            file.write(str(d3_r5)+"\n")
            file.write(str(d4_r5))
        # outline
        self.a = target_X-xcol_out
        self.cal = target_X-xcol_out
        print(self.cal)
        if self.a < 0:
            self.a = 0
        with open(f"sys_new/roi/{position}/left_out.ini", "w") as file:
            file.write(str(self.a)+"\n")
            file.write(str(target_Y-ycol_out)+"\n")
            file.write(str(d3_r6)+"\n")
            file.write(str(d4_r6))
        with open(f"sys_new/roi/{position}/top_out.ini", "w") as file:
            file.write(str(target_X-xcot_out)+"\n")
            file.write(str(target_Y-ycot_out)+"\n")
            file.write(str(d3_r7)+"\n")
            file.write(str(d4_r7))
        with open(f"sys_new/roi/{position}/right_out.ini", "w") as file:
            file.write(str(target_X-xcor_out)+"\n")
            file.write(str(target_Y-ycor_out)+"\n")
            file.write(str(d3_r8)+"\n")
            file.write(str(d4_r8))
        with open(f"sys_new/roi/{position}/bottom_out.ini", "w") as file:
            file.write(str(target_X-xcob_out)+"\n")
            file.write(str(target_Y-ycob_out)+"\n")
            file.write(str(d3_r9)+"\n")
            file.write(str(d4_r9))

    def AOI(self, path_img: str,number_kh):
        if number_kh ==1:
            self.canvas_1.delete('all')
        elif number_kh ==2:
            self.canvas_2.delete('all')
        elif number_kh ==3:
            self.canvas_3.delete('all')
        else:
            self.canvas_4.delete('all')
        times = datetime.now().strftime('%H:%M:%S')
        try:
            self.result = 0
            if number_kh ==1:
                self.btn_test_AOI1.configure(fg_color = 'green')
            elif number_kh ==2:
                self.btn_test_AOI2.configure(fg_color = 'green')
            elif number_kh ==3:
                self.btn_test_AOI3.configure(fg_color = 'green')
            else:
               self.btn_test_AOI4.configure(fg_color = 'green')
            
            frame = self.cap.read()
            frame = cv2.resize(frame, (880, 680))
            cv2.imwrite(path_img, frame)
            img = cv2.imread(path_img)
            cv2.imwrite(f'temp{number_kh}.jpg',img)
            pred =  self.AI(f"temp{number_kh}.jpg")
            path_area_1 = open(f"area/area1_p{number_kh}.ini", "r")
            path_area_2 = open(f"area/area2_p{number_kh}.ini", "r")
            path_area_3 = open(f"area/area3_p{number_kh}.ini", "r")
            path_area_4 = open(f"area/area4_p{number_kh}.ini", "r")
            path_area_5 = open(f"area/area5_p{number_kh}.ini", "r")
            path_area_left = open(f"area/outL_p{number_kh}.ini", "r")
            path_area_top = open(f"area/outT_p{number_kh}.ini", "r")
            path_area_right = open(f"area/outR_p{number_kh}.ini", "r")
            path_area_bottom = open(f"area/outB_p{number_kh}.ini", "r")

            area_1 = path_area_1.readlines()
            area_2 = path_area_2.readlines()
            area_3 = path_area_3.readlines()
            area_4 = path_area_4.readlines()
            area_5 = path_area_5.readlines()
            area_L = path_area_left.readlines()
            area_T = path_area_top.readlines()
            area_R = path_area_right.readlines()
            area_B = path_area_bottom.readlines()

            min_area1 = int(area_1[0])
            min_area2 = int(area_2[0])
            min_area3 = int(area_3[0])
            min_area4 = int(area_4[0])
            min_area5 = int(area_5[0])
            min_area_ol = int(area_L[0])
            min_area_ot = int(area_T[0])
            min_area_or = int(area_R[0])
            min_area_ob = int(area_B[0])

            max_area1 = int(area_1[1])
            max_area2 = int(area_2[1])
            max_area3 = int(area_3[1])
            max_area4 = int(area_4[1])
            max_area5 = int(area_5[1])
            max_area_ol = int(area_L[1])
            max_area_ot = int(area_T[1])
            max_area_or = int(area_R[1])
            max_area_ob = int(area_B[1])
            self.coordinate_calculate(img,f'p{number_kh}',f'position{number_kh}')
            roi_files = [f"sys_new/roi/position{number_kh}/left.ini", f"sys_new/roi/position{number_kh}/top.ini", f"sys_new/roi/position{number_kh}/right.ini", f"sys_new/roi/position{number_kh}/bottom.ini",f"sys_new/roi/position{number_kh}/center.ini",
                         f"sys_new/roi/position{number_kh}/left_out.ini", f"sys_new/roi/position{number_kh}/top_out.ini", f"sys_new/roi/position{number_kh}/right_out.ini", f"sys_new/roi/position{number_kh}/bottom_out.ini"]
            roi_coords = []
            for roi_file in roi_files:
                with open(roi_file, "r") as f:
                    roi = [int(line) for line in f.readlines()]
                    roi_coords.append(roi)

            d1_r1, d2_r1, d3_r1, d4_r1 = roi_coords[0]
            d1_r2, d2_r2, d3_r2, d4_r2 = roi_coords[1]
            d1_r3, d2_r3, d3_r3, d4_r3 = roi_coords[2]
            d1_r4, d2_r4, d3_r4, d4_r4 = roi_coords[3]
            d1_r5, d2_r5, d3_r5, d4_r5 = roi_coords[4]
            d1_r6, d2_r6, d3_r6, d4_r6 = roi_coords[5]#left
            d1_r7, d2_r7, d3_r7, d4_r7 = roi_coords[6]#top
            d1_r8, d2_r8, d3_r8, d4_r8 = roi_coords[7]#right
            d1_r9, d2_r9, d3_r9, d4_r9 = roi_coords[8]#bottom

            cal_w = 0
            if self.cal <0:
                cal_w = d3_r6+self.cal
            else:
                cal_w = d3_r6

            roi1 = img[d2_r1:d2_r1+d4_r1, d1_r1:d1_r1+d3_r1]
            roi2 = img[d2_r2:d2_r2+d4_r2, d1_r2:d1_r2+d3_r2]
            roi3 = img[d2_r3:d2_r3+d4_r3, d1_r3:d1_r3+d3_r3]
            roi4 = img[d2_r4:d2_r4+d4_r4, d1_r4:d1_r4+d3_r4]
            roi5 = img[d2_r5:d2_r5+d4_r5, d1_r5:d1_r5+d3_r5]
            roi6 = img[d2_r6:d2_r6+d4_r6, d1_r6:d1_r6+cal_w]
            roi7 = img[d2_r7:d2_r7+d4_r7, d1_r7:d1_r7+d3_r7]
            roi8 = img[d2_r8:d2_r8+d4_r8, d1_r8:d1_r8+d3_r8]
            roi9 = img[d2_r9:d2_r9+d4_r9, d1_r9:d1_r5+d3_r9]
            
            area1 = self.filterNoise_contours(roi1,'mask_left',f'p{number_kh}',f'position{number_kh}','left')
            area2 = self.filterNoise_contours(roi2,'mask_top',f'p{number_kh}',f'position{number_kh}','top')
            area3 = self.filterNoise_contours(roi3,'mask_right',f'p{number_kh}',f'position{number_kh}','right')
            area4 = self.filterNoise_contours(roi4,'mask_bottom',f'p{number_kh}',f'position{number_kh}','bottom')
            area5 = self.filterNoise_contours(roi5,'mask_center',f'p{number_kh}',f'position{number_kh}','center')
            area6 = self.filterNoise_contours(roi6,'mask_left_out',f'p{number_kh}',f'position{number_kh}','left_out')
            area7 = self.filterNoise_contours(roi7,'mask_top_out',f'p{number_kh}',f'position{number_kh}','top_out')
            area8 = self.filterNoise_contours(roi8,'mask_right_out',f'p{number_kh}',f'position{number_kh}','right_out')
            area9 = self.filterNoise_contours(roi9,'mask_bottom_out',f'p{number_kh}',f'position{number_kh}','bottom_out')

            temps = []
            arr_ng=[]

            if pred >0.3:
                if area1 <= max_area1 and area1 >= min_area1:
                    temp1 = 1
                    temps.append(temp1)
                    self.notification.insert("0.0", f"\n{times}:  Vùng 1 khuôn #{number_kh} OK: {area1}", "1")
                    if self.log == True:
                        self.add_log(f"\n{times}:  Vùng 1 khuôn #{str(number_kh)} OK: {str(area1)}")
                
                    cv2.rectangle(img,(d1_r1, d2_r1), (d1_r1+d3_r1, d2_r1+d4_r1),(0,255,0),2)
                else: 
                    self.notification.insert("0.0", f"\n{times}: Vùng 1 khuôn #{number_kh} NG: {area1}", "2")
                    if self.log == True:
                        self.add_log(f"\n{times}:  Vùng 1 khuôn #{str(number_kh)} NG: {str(area1)}")
                    temp1 = 10
                    temps.append(temp1)
                    arr_ng.append('temp1')
                
                if area2 >= min_area2 and area2 <= max_area2:
                    temp2 = 1
                    temps.append(temp2)
                
                    self.notification.insert("0.0", f"\n{times}:  Vùng 2 khuôn #{number_kh} OK: {area2}", "1")
                    if self.log == True:
                        self.add_log(f"\n{times}:  Vùng 2 khuôn #{str(number_kh)} OK: {str(area2)}")
                    cv2.rectangle(img,(d1_r2, d2_r2), (d1_r2+d3_r2, d2_r2+d4_r2),(0,255,0),2)
                else:
                    temp2 = 10
                    temps.append(temp2)
                    self.notification.insert("0.0", f"\n{times}:  Vùng 2 khuôn #{number_kh} NG: {area2}", "2")
                    if self.log == True:
                        self.add_log(f"\n{times}:  Vùng 2 khuôn #{str(number_kh)} NG: {str(area2)}")
                    arr_ng.append('temp2')


                if area3 <= max_area3 and area3 >= min_area3:
                    temp3 = 1
                    temps.append(temp3)
                    
                    self.notification.insert("0.0", f"\n{times}:  Vùng 3 khuôn #{number_kh} OK: {area3}", "1")
                    if self.log == True:
                        self.add_log(f"\n{times}:  Vùng 3 khuôn #{str(number_kh)} OK: {str(area3)}")
                    cv2.rectangle(img,(d1_r3, d2_r3), (d1_r3+d3_r3, d2_r3+d4_r3),(0,255,0),2)
                else:
                    temp3 = 10
                    temps.append(temp3)
                
                    self.notification.insert("0.0", f"\n{times}:  Vùng 3 khuôn #{number_kh} NG: {area3}", "2")
                    if self.log == True:
                        self.add_log(f"\n{times}:  Vùng 3 khuôn #{str(number_kh)} NG: {str(area3)}")
                    arr_ng.append('temp3')

                if area4 <= max_area4 and area4 >= min_area4:
                    temp4 = 1
                    temps.append(temp4)
                
                    self.notification.insert("0.0", f"\n{times}:  Vùng 4 khuôn #{number_kh} OK: {area4}", "1")
                    if self.log == True:
                        self.add_log(f"\n{times}:  Vùng 4 khuôn #{str(number_kh)} OK: {str(area4)}")
                    cv2.rectangle(img,(d1_r4, d2_r4), (d1_r4+d3_r4, d2_r4+d4_r4),(0,255,0),2)
                else:
                    temp4 = 10
                    temps.append(temp4)
                    self.notification.insert("0.0", f"\n{times}:  Vùng 4 khuôn #{number_kh} NG: {area4}", "2")
                    if self.log == True:
                        self.add_log(f"\n{times}:  Vùng 4 khuôn #{str(number_kh)} NG: {str(area4)}")
                    arr_ng.append('temp4')
                
                if area5 <= max_area5 and area5 >= min_area5:
                    temp5 = 1
                    temps.append(temp5)
                
                    self.notification.insert("0.0", f"\n{times}:  Vùng 5 khuôn #{number_kh} OK: {area5}", "1")
                    if self.log == True:
                        self.add_log(f"\n{times}:  Vùng 5 khuôn #{str(number_kh)} OK: {str(area5)}")
                    cv2.rectangle(img,(d1_r5, d2_r5), (d1_r5+d3_r5, d2_r5+d4_r5),(0,255,0),2)
                else:
                    temp5 = 10
                    temps.append(temp5)
                    self.notification.insert("0.0", f"\n{times}:  Vùng 5 khuôn #{number_kh} NG: {area5}", "2")
                    if self.log == True:
                        self.add_log(f"\n{times}:  Vùng 5 khuôn #{str(number_kh)} NG: {str(area5)}")
                    arr_ng.append('temp5')
                
                if area6 <= max_area_ol and area6 >= min_area_ol:
                    temp6 = 1
                    temps.append(temp6)
                
                    self.notification.insert("0.0", f"\n{times}:  Vùng ngoài trái khuôn #{number_kh} OK: {area6}", "1")
                    if self.log == True:
                        self.add_log(f"\n{times}:  Vùng ngoài trái khuôn #{str(number_kh)} OK: {str(area6)}")
                    cv2.rectangle(img,(d1_r6, d2_r6), (d1_r6+cal_w, d2_r6+d4_r6),(0,255,0),2)
                else:
                    temp6 = 10
                    temps.append(temp6)
                    self.notification.insert("0.0", f"\n{times}:  Vùng ngoài trái khuôn #{number_kh} NG: {area6}", "2")
                    if self.log == True:
                        self.add_log(f"\n{times}:  Vùng ngoài trái khuôn #{str(number_kh)} NG: {str(area6)}")
                    arr_ng.append('temp6')
                
                if area7 <= max_area_ot and area7 >= min_area_ot:
                    temp7 = 1
                    temps.append(temp7)
                    self.notification.insert("0.0", f"\n{times}:  Vùng ngoài trên khuôn #{number_kh} OK: {area7}", "1")
                    if self.log == True:
                        self.add_log(f"\n{times}:  Vùng ngoài trên khuôn #{str(number_kh)} OK: {str(area7)}")
                    cv2.rectangle(img,(d1_r7, d2_r7), (d1_r7+d3_r7, d2_r7+d4_r7),(0,255,0),2)
                else:
                    temp7 = 10
                    temps.append(temp7)
                    self.notification.insert("0.0", f"\n{times}:  Vùng ngoài trên khuôn #{number_kh} NG: {area7}", "2")
                    if self.log == True:
                        self.add_log(f"\n{times}:  Vùng ngoài trên khuôn #{str(number_kh)} NG: {str(area7)}")
                    arr_ng.append('temp7')
                
                if area8 <= max_area_or and area8 >= min_area_or:
                    temp8 = 1
                    temps.append(temp8)
                    self.notification.insert("0.0", f"\n{times}:  Vùng ngoài phải khuôn #{number_kh} OK: {area8}", "1")
                    if self.log == True:
                        self.add_log(f"\n{times}:  Vùng ngoài phải khuôn #{str(number_kh)} OK: {str(area8)}")
                    cv2.rectangle(img,(d1_r8, d2_r8), (d1_r8+d3_r8, d2_r8+d4_r8),(0,255,0),2)
                else:
                    temp8 = 10
                    temps.append(temp8)
                    self.notification.insert("0.0", f"\n{times}:  Vùng ngoài phải khuôn #{number_kh} NG: {area8}", "2")
                    if self.log == True:
                        self.add_log(f"\n{times}:  Vùng ngoài phải khuôn #{str(number_kh)} NG: {str(area8)}")
                    arr_ng.append('temp8')
                
                if area9 <= max_area_ob and area9 >= min_area_ob:
                    temp9 = 1
                    temps.append(temp9)
                    self.notification.insert("0.0", f"\n{times}:  Vùng ngoài dưới khuôn #{number_kh} OK: {area9}", "1")
                    if self.log == True:
                        self.add_log(f"\n{times}:  Vùng ngoài dưới khuôn #{str(number_kh)} OK: {str(area9)}")
                    cv2.rectangle(img,(d1_r9, d2_r9), (d1_r9+d3_r9, d2_r9+d4_r9),(0,255,0),2)
                else:
                    temp9 = 10
                    temps.append(temp9)
                    self.notification.insert("0.0", f"\n{times}:  Vùng ngoài dưới khuôn #{number_kh} NG: {area9}", "2")
                    if self.log == True:
                        self.add_log(f"\n{times}:  Vùng ngoài dưới khuôn #{str(number_kh)} NG: {str(area9)}")
                    arr_ng.append('temp9')
                
                for i in arr_ng:
                    if i =='temp1':
                        cv2.rectangle(img,(d1_r1, d2_r1), (d1_r1+d3_r1, d2_r1+d4_r1),(0,0,255),2)
                    if i =='temp2':
                        cv2.rectangle(img,(d1_r2, d2_r2), (d1_r2+d3_r2, d2_r2+d4_r2),(0,0,255),2)
                    if i =='temp3':
                        cv2.rectangle(img,(d1_r3, d2_r3), (d1_r3+d3_r3, d2_r3+d4_r3),(0,0,255),2)
                    if i =='temp4':
                        cv2.rectangle(img,(d1_r4, d2_r4), (d1_r4+d3_r4, d2_r4+d4_r4),(0,0,255),2)
                    if i =='temp5':
                        cv2.rectangle(img,(d1_r5, d2_r5), (d1_r5+d3_r5, d2_r5+d4_r5),(0,0,255),2)
                    if i =='temp6':
                        cv2.rectangle(img,(d1_r6, d2_r6), (d1_r6+cal_w, d2_r6+d4_r6),(0,0,255),2)
                    if i =='temp7':
                        cv2.rectangle(img,(d1_r7, d2_r7), (d1_r7+d3_r7, d2_r7+d4_r7),(0,0,255),2)
                    if i =='temp8':
                        cv2.rectangle(img,(d1_r8, d2_r8), (d1_r8+d3_r8, d2_r8+d4_r8),(0,0,255),2)
                    if i =='temp9':
                        cv2.rectangle(img,(d1_r9, d2_r9), (d1_r9+d3_r9, d2_r9+d4_r9),(0,0,255),2)
                
                self.notification.insert("0.0", f"\n{times}: Dự đoán keo khuôn #{number_kh} OK: {pred}", "1")
                if self.log == True:
                    self.add_log(f"\n{times}: Dự đoán keo khuôn #{(str(number_kh))} OK: {str(pred)}")
                if all(temp == 1 for temp in temps):
                    cv2.putText(img, "OK", org=(700,70), fontFace=cv2.FONT_HERSHEY_COMPLEX, \
                            fontScale=3, color= (0,255,0), thickness=2)
                    self.result = 1              
                else:
                    cv2.putText(img, "NG", org=(700,70), fontFace=cv2.FONT_HERSHEY_COMPLEX, \
                            fontScale=3, color= (0,0,255), thickness=2)
                    self.result = 10
            else:
                self.notification.insert("0.0", f"\n{times}: Dự đoán keo khuôn #{number_kh} NG: {pred}", "2")
                if self.log == True:
                    self.add_log(f"\n{times}: Dự đoán keo khuôn #{str(number_kh)} NG: {str(pred)}")
                cv2.putText(img, "NG", org=(700,70), fontFace=cv2.FONT_HERSHEY_COMPLEX, \
                        fontScale=3, color= (0,0,255), thickness=2)
                cv2.rectangle(img,(d1_r1, d2_r1), (d1_r1+d3_r1, d2_r1+d4_r1),(0,0,255),2)
                cv2.rectangle(img,(d1_r2, d2_r2), (d1_r2+d3_r2, d2_r2+d4_r2),(0,0,255),2)
                cv2.rectangle(img,(d1_r3, d2_r3), (d1_r3+d3_r3, d2_r3+d4_r3),(0,0,255),2)
                cv2.rectangle(img,(d1_r4, d2_r4), (d1_r4+d3_r4, d2_r4+d4_r4),(0,0,255),2)
                cv2.rectangle(img,(d1_r5, d2_r5), (d1_r5+d3_r5, d2_r5+d4_r5),(0,0,255),2)
                cv2.rectangle(img,(d1_r6, d2_r6), (d1_r6+d3_r6, d2_r6+d4_r6),(0,0,255),2)
                cv2.rectangle(img,(d1_r7, d2_r7), (d1_r7+d3_r7, d2_r7+d4_r7),(0,0,255),2)
                cv2.rectangle(img,(d1_r8, d2_r8), (d1_r8+d3_r8, d2_r8+d4_r8),(0,0,255),2)
                cv2.rectangle(img,(d1_r9, d2_r9), (d1_r9+d3_r9, d2_r9+d4_r9),(0,0,255),2)
                self.result = 10

            self.img_1 = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            if number_kh ==1:
                self.img_1 = cv2.resize(self.img_1, (self.canvas_1.winfo_width(), self.canvas_1.winfo_height()))
                self.photo1 = ImageTk.PhotoImage(image=Image.fromarray(self.img_1))
                self.canvas_1.create_image(0,0,image = self.photo1,anchor = tkinter.NW)
                self.btn_test_AOI1.configure(fg_color=['#3B8ED0','#1F6AA5'])
            elif number_kh ==2:
                self.img_1 = cv2.resize(self.img_1 ,(self.canvas_2.winfo_width(), self.canvas_2.winfo_height()))
                self.photo2 = ImageTk.PhotoImage(image=Image.fromarray(self.img_1))
                self.canvas_2.create_image(0,0,image = self.photo2,anchor = tkinter.NW)
                self.btn_test_AOI2.configure(fg_color=['#3B8ED0','#1F6AA5'])
            elif number_kh ==3:
                self.img_1 = cv2.resize(self.img_1 ,(self.canvas_3.winfo_width(), self.canvas_3.winfo_height()))
                self.photo3 = ImageTk.PhotoImage(image=Image.fromarray(self.img_1))
                self.canvas_3.create_image(0,0,image = self.photo3,anchor = tkinter.NW)
                self.btn_test_AOI3.configure(fg_color=['#3B8ED0','#1F6AA5'])
            else:
                self.img_1 = cv2.resize(self.img_1 ,(self.canvas_4.winfo_width(), self.canvas_4.winfo_height()))
                self.photo4 = ImageTk.PhotoImage(image=Image.fromarray(self.img_1))
                self.canvas_4.create_image(0,0,image = self.photo4,anchor = tkinter.NW)
                self.btn_test_AOI4.configure(fg_color=['#3B8ED0','#1F6AA5'])
            

        except Exception as ex:
            print(f"Error Position {number_kh}: {ex}")
            self.notification.insert("0.0", f"\n{times}:  Error Position {number_kh}: {ex}")
            if self.log == True:
                self.add_log(f"\n{times}:  Error Position {number_kh}: {str(ex)}")