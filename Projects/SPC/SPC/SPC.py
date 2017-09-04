#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
Created on Wed Mar 8 10:06:00 2017

@author: Tristan Song
"""

import tkinter as tk
from tkinter import ttk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style
import matplotlib.animation as animation
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import FormatStrFormatter
import os
import sys
import re
import pandas as pd
import platform
matplotlib.use("TkAgg")


VERY_LARGE = ("Arial", 16)
LARGE_FONT = ("Arial", 12)
NORMAL_FONT = ("Arial", 10)
SMALL_FONT = ("Arial", 8)
SHOW_QUANT = 50

# 处理matplotlib显示中文字体问题
if "Windows" in platform.platform():
    font_set1 = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=16)
    font_set2 = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=10)

style.use("ggplot")
fig = Figure(figsize=(10, 6), dpi=100)
a = fig.add_subplot(2, 1, 1)
b = fig.add_subplot(2, 1, 2, sharex=a)


# Set default volumeDir and cfVolume for the default Frame
volumeDir = os.path.join(os.getcwd(), "NOVA-5kg")
cfVolume = "NOVA-5kg"
# Create the .txt to store file list and result
fileList = ["5kg_file.txt", "5kg_result.txt", "500g_file.txt", "500g_result.txt", "300g_file.txt", "300g_result.txt"]
for file in fileList:
    if not os.path.exists(os.path.join(os.getcwd(), file)):
        f = open(os.path.join(os.getcwd(), file), "w")
        f.close()

def popup_msg(msg):
    popup = tk.Tk()
    popup.geometry("480x320")
    popup.wm_title("Warning!")
    label = ttk.Label(popup, text=msg, font=NORMAL_FONT)
    label.pack()
    button = ttk.Button(popup, text="OK", command=popup.destroy)
    button.pack()
    popup.mainloop()

def get_quantity(window, entry):
    global SHOW_QUANT
    SHOW_QUANT = int(entry.get())
    window.destroy()
    
def show_quantity():

    quantity = tk.Tk()
    quantity.geometry("480x320")
    quantity.wm_title("请输入显示数量!")
    entry = tk.Entry(quantity, textvariable="请输入显示数量！")
    entry.pack()
    button1 = ttk.Button(quantity, text="OK", command=lambda: get_quantity(quantity, entry))
    button1.pack()
    quantity.mainloop()


def get_volumeDir(volume):
    global volumeDir
    global cfVolume
    cfVolume = volume
    volumeDir = os.path.join(os.getcwd(), volume)


def get_file_list():
    # get the new added file, so extract the data only once in func "get_result"
    newFile = []

    # get the new added file
    if cfVolume == "NOVA-5kg":
        f = open("./5kg_file.txt", "r")
    if cfVolume == "NOVA-500g":
        f = open("./500g_file.txt", "r")
    if cfVolume == "NOVA-300g":
        f = open("./300g_file.txt", "r")
    storeList = f.read().strip().split("\n")
    for file in os.listdir(volumeDir):
        if cfVolume in file and file not in storeList:
            newFile.append(file)
    f.close()

    # add the new file to file list, even though newFile is None
    if cfVolume == "NOVA-5kg":
        f = open("./5kg_file.txt", "a")
    if cfVolume == "NOVA-500g":
        f = open("./500g_file.txt", "a")
    if cfVolume == "NOVA-300g":
        f = open("./300g_file.txt", "a")
    for new in newFile:
        f.write(new + "\n")
    f.close()

    return newFile


def get_result():
    # For the right now, only collect the markNo, thickness, collect more result later
    thicknessLine = [15, 18, 22, 26, 37, 40, 44, 48]  # The line location of thickness in the file

    # add the new result into result
    newFile = get_file_list()
    if newFile != []:
        for new in newFile:
            with open("./"+cfVolume+"/"+new, "r", encoding="gbk") as f:
                data = f.readlines()
                thickness = []
                volume = re.split('\\s+', data[3].strip())[-1]
                cnc = re.split('\\s+', data[7].strip())[-1]
                markNo = re.split('\\s+', data[7].strip())[-2]
                measureTime = re.split("\\s+", data[5].strip())  # The date in the file
                #measureTime = datetime.strptime(measureTime[-2] + measureTime[-1], "%Y/%m/%d%H:%M")
                for line in thicknessLine:
                    b = re.split("\\s+", data[line - 1].strip())
                    thickness.append(float(b[5]))
                #thickness.sort() # no need to sort

                if cfVolume == "NOVA-5kg":
                    f = open("./5kg_result.txt", "a")
                if cfVolume == "NOVA-500g":
                    f = open("./500g_result.txt", "a")
                if cfVolume == "NOVA-300g":
                    f = open("./300g_result.txt", "a")
                f.write(volume + "," + cnc + "," + markNo + ",")
                for thick in thickness:
                    f.write(str(thick) + ",")
                f.write(measureTime[-2] + " " + measureTime[-1] + "\n")
                f.close()


def animate(i):
    get_result()

    columns = ["volume", "cnc", "mark", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "time"]
    if cfVolume == "NOVA-5kg":
        result = pd.read_table("./5kg_result.txt", sep=",", names=columns)
        U = 0.5
        T = 0.06
    if cfVolume == "NOVA-500g":
        result = pd.read_table("./500g_result.txt", sep=",", names=columns)
        U = 0.3
        T = 0.06
    if cfVolume == "NOVA-300g":
        print("not defined!")
        pass
        #result = pd.read_table("./300g_result.txt", sep=",", names=columns)
        #U = None
        #T = None

    if result["time"].count()+1 < 20:
        print("数据量小于20组！")
        data = result.sort_values(by="time")
    #elif result["time"].count()+1 < 50:
    #    data = result.sort_values(by="time")
    else:
        data = result.sort_values(by="time").tail(SHOW_QUANT)

    data = data.iloc[:, [-9, -8, -7, -6]]
    sigma = data.values.std(ddof=1)
    data_mean = data.mean().mean()
    UCL = U + 3*sigma
    LCL = U - 3*sigma
    xrange = data.max(axis=1) - data.min(axis=1)
##    R = xrange.mean()
##    CL = data.mean().mean()
##    UCL = CL + 0.729 * R
##    LCL = CL - 0.729 * R
    # sigma = data.values.std(ddof=1)
    # X = data.mean().mean()
    # Ca = (X - U)/(T/2)
    # Cp = T/sigma/6
    # Cpk = Cp*(1-abs(Ca))

    length = len(data)
    x = list(range(len(data)))

    if cfVolume == "NOVA-5kg":
        limit_up = [0.530]*length
        limit_mid = [0.500]*length
        limit_down = [0.470]*length
    elif cfVolume == "NOVA-500g":
        limit_up = [0.330]*length
        limit_mid = [0.300]*length
        limit_down = [0.270]*length
    else:
        # nova-300g
        pass
    UCL = [UCL]*length
    LCL = [LCL]*length
    data_mean = [data_mean]*length

    a.clear()
    b.clear()
    a.yaxis.set_major_formatter(FormatStrFormatter("%.3f"))
    b.yaxis.set_major_formatter(FormatStrFormatter("%.3f"))
    a.set_title("%s关键尺寸SPC过程控制图"%cfVolume, fontproperties=font_set1)
    #a.set_title("%s关键尺寸SPC过程控制图(Cpk=%.3f)"%(cfVolume, Cpk), fontproperties=font_set)
    a.set_ylabel("壁厚/mm", fontproperties=font_set2)
    b.set_ylabel("极差/mm", fontproperties=font_set2)
    a.plot(x, limit_up, linestyle="-", color="r", label=u"公差上限")
    a.plot(x, limit_mid, linestyle="--", color="g", label=u"公差中值")
    a.plot(x, limit_down, linestyle="-", color="r", label=u"公差下限")
    a.plot(x, data_mean, linestyle="-", color="y", label=u"数据中值")
    a.plot(x, UCL, linestyle="-", color="b", label=u"上控制限")
    a.plot(x, LCL, linestyle="-", color="b", label=u"下控制限")
    a.plot(x, data.mean(axis=1), marker="o", color="r", label=u"实测值")
    # a.plot(x, data["t1"], marker="*", color="g", label=u"最小值")
    a.legend(loc="upper left", prop=font_set2)

    b.set_ylim([0, 0.06])
    b.plot(x, xrange, marker="o", color="r", label=u"极差")
    b.legend(loc="upper left", prop=font_set2)


class SPC(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #tk.Tk.iconbitmap(self, default="client_icon.ico") # change the icon format to ico, which can show correctly
        #self.geometry("1280x720")
        #self.resizable(False, False)
        self.wm_title("POLC QM&CNC NOVA精益生产线SPC过程控制图")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        menubar = tk.Menu(self)
        self.config(menu=menubar)

        volumemenu = tk.Menu(menubar, tearoff=0)
        volumemenu.add_command(label="NOVA-5kg", font=NORMAL_FONT,
                               command=lambda :get_volumeDir("NOVA-5kg"))
        volumemenu.add_command(label="NOVA-500g", font=NORMAL_FONT,
                               command=lambda :get_volumeDir("NOVA-500g"))
        volumemenu.add_command(label="NOVA-300g", font=NORMAL_FONT,
                               command=lambda :get_volumeDir("NOVA-300g"))
        volumemenu.add_separator()
        volumemenu.add_command(label="退出", font=NORMAL_FONT,
                               command=self.quit)
        menubar.add_cascade(label="容量", menu=volumemenu, font=NORMAL_FONT)

        showmenu = tk.Menu(menubar, tearoff=0)
        showmenu.add_command(label="显示数量", font=NORMAL_FONT,
                             command=lambda :show_quantity())
        menubar.add_cascade(label="显示", menu=showmenu, font=NORMAL_FONT)

        savemenu = tk.Menu(menubar, tearoff=0)
        savemenu.add_command(label="NOVA-5kg保存", font=NORMAL_FONT,
                             command=lambda :popup_msg("Not support yet!"))
        savemenu.add_command(label="NOVA-500g保存", font=NORMAL_FONT,
                             command=lambda :popup_msg("Not support yet!"))
        savemenu.add_command(label="NOVA-300g保存", font=NORMAL_FONT,
                             command=lambda :popup_msg("Not support yet!"))
        menubar.add_cascade(label="保存", menu=savemenu, font=NORMAL_FONT)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_separator()
        helpmenu.add_command(label="版本", font=NORMAL_FONT,
                             command=lambda :popup_msg("Version: 1.0"))
        helpmenu.add_command(label="关于", font=NORMAL_FONT,
                             command=lambda :popup_msg("Author: Tristan Song"))
        menubar.add_cascade(label="帮助", menu=helpmenu, font=NORMAL_FONT)

        self.frames = {}
        for F in (StartPage, GraphPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, height=5, font=LARGE_FONT,
                         text="""本程序仅适用于POLC QM&CNC部门的NOVA精益产线SPC生产过程控制！""")
        label.pack()
        button1 = ttk.Button(self, text="同意",
                             command=lambda :controller.show_frame(GraphPage))
        button2 = ttk.Button(self, text="不同意",
                             command=self.quit)
        button1.pack()
        button2.pack()


class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #label = tk.Label(self, text="NOVA-5kg关键尺寸SPC过程控制图", font=VERY_LARGE)
        #label.pack(side="top")

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side="bottom", fill="both", expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side="bottom", fill="both", expand=True)


app = SPC()
ani = animation.FuncAnimation(fig, animate, interval=3000) #interval millisecond
app.mainloop()
