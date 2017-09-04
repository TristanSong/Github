#!/usr/env/bin python3
# -*-coding:utf-8 -*-
'''
Created on Wed Mar 10 10:32:00 2017

@author: Tristan Song
'''

import tkinter as tk
from tkinter import ttk
import os, sys
from datetime import datetime
import shutil

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


def auto_move():
    moveList = []
    with open("./0000_Move.txt", "r") as f:
        for line in f.readlines():
            if line.strip() != "":
                moveList.append(line.strip())

    today = datetime.now()
    today = today.strftime("%Y-%m-%d")
    if not os.path.exists(r"./%s/"%today):
        os.makedirs(r"./%s/"%today)

    rawList = os.listdir()
    fileList = []
    for file in rawList:
        if ".txt" in file:
            fileList.append(file)
    
    if moveList == [""]:
        print("请输入待拷贝的钢号！")
        sys.exit()

    n = 0
    fail = []
    for move in moveList:
        for file in fileList:
            if move in file:
                shutil.copy("%s"%file, "./%s"%today)
                n += 1
            else:
                fail.append(move)
    fail = set(fail)
    with open("./0000_Move_Failure.txt", "w+") as data:
        for f in fail:
            data.write(f+"\n")
    if n < len(moveList):
        popup_msg("输入%s只钢号，成功拷贝%s只！\n请打开0000_Move_Failure.txt文件查看未拷贝钢号！"%(len(moveList), n))
    else:
        popup_msg("输入%s只钢号，成功拷贝%s只！"%(len(moveList), n))
    


class StartPage(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self)

        self.wm_title('NOVA三坐标txt测量结果自动拷贝至日期')
        #self.iconbitmap(bitmap='client_icon.ico')
        self.geometry("640x480")
        self.resizable(0, 0)

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)

        label = tk.Label(container, font=LARGE_FONT, text="""
        **********************************************************
        请将弹性体钢号输入至"0000_Move.txt"文件中并保存，
        程序会将对应的三坐标结果文件拷贝至创建日期内！
        未拷贝的钢号会自动输出至0000_Move_Failure.txt文件中，请注意查看！
        **********************************************************""")
        label.pack(side='top', fill="both", expand=True)

        button = tk.Button(container, text='复制', font=LARGE_FONT, command=auto_move)
        button.pack(side='bottom')

app = StartPage()
app.mainloop()
