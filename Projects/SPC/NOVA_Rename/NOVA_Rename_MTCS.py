#!/usr/env/bin python3
# -*-coding:utf-8 -*-
'''
Created on Wed Mar 10 10:32:00 2017

@author: Tristan Song
'''

import tkinter as tk
from tkinter import ttk
import os
import re

LARGE_FONT = ('Verdana', 12)

# Show popup message
def popup_msg(msg):
    popup = tk.Tk()
    popup.wm_title('Warning!')
    popup.geometry('300x100')
    label = tk.Label(popup, text=msg)
    label.pack(side='top', fill='both', expand=True)
    command = ttk.Button(popup, text='OK', command=popup.destroy)
    command.pack(side='bottom')
    popup.mainloop()


def auto_rename():
    rawList = os.listdir()
    fileList = []

    # Pick the NOVA***.txt file
    for i in range(len(rawList)):
        if ".txt" in rawList[i]:
        #if 'NOVA' in rawList[i] and '.txt' in rawList[i]:
            fileList.append(rawList[i])

    if fileList == []:
        popup_msg('该文件夹内没有找到NOVA的三坐标txt检测文件！')
        exit()

    for file in fileList:
        with open(file, 'r') as f:
            data = f.readlines()
            volume = str(re.split('\\s+', data[3].strip())[-1])
            cnc = str(re.split('\\s+', data[7].strip())[-1])
            markNo = str(re.split('\\s+', data[7].strip())[-2])
##        os.rename(file,  volume + "_" + cnc + "_" +  markNo + '.txt')
        os.rename(file, markNo + '.txt')
            
    popup_msg('重命名完成！')

class StartPage(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self)

        self.wm_title('NOVA重命名for MTCS')
        #self.iconbitmap(bitmap='client_icon.ico')
        self.geometry("640x480")
        self.resizable(0, 0)

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)

        label = tk.Label(container, font=LARGE_FONT, text="""
        **********************************************************

        NOVA重命名
        
        **********************************************************
        本程序用于将txt文件重命名为"编号.txt"
        请将本程序置于待更名的NOVA三坐标txt测量结果文件夹内，
        程序自动读取钢号并重命名！
        **********************************************************
        更改前：NOVA-5kg******.txt
        更改后：4825.txt
        **********************************************************""")
        label.pack(side='top', fill="both", expand=True)

        button = tk.Button(container, text='开始重命名', font=LARGE_FONT, command=auto_rename)
        button.pack(side='bottom')


app = StartPage()
app.mainloop()
