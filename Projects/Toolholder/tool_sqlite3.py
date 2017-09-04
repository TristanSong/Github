#!/usr/env/bin python3
# -*-coding:utf-8 -*-
'''
Created on Mon Mar 13 23:24:41 2017

@author: Tristan Song
'''

import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime
import threading
import os
import shutil
import xlwt

SUPER_LARGE = 16
LARGE_FONT = ("Arial", 14)
NORM_FONT = ("Arial", 12)
SMALL_FONT = ("Arial", 10)
COLOR_1 = "#B0B0B0"
COLOR_2 = "#90EE90"
ADMIN_USER = "10014320"
ADMIN_PWD = "polc_CNC"
LOGIN_PERSON = ""

# Create the worker database if not exist
conn = sqlite3.connect("toolholder_db.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS worker_list "
            "(id_card VARCHAR(10) NOT NULL PRIMARY KEY, "
            "worker_id VARCHAR(10) NOT NULL UNIQUE, "
            "worker_name VARCHAR(20) NOT NULL)")
# To set a default foreign key for toolholder, when nobody lend the toolholder
cur.execute("REPLACE INTO worker_list "
            "VALUES (?, ?, ?)",
            ("0000", "0000", "0000"))
# Have set the default value for tool_cnc, but why need to set it again when insert necessarily???????????
cur.execute("CREATE TABLE IF NOT EXISTS toolholder_list "
            "(tool_id VARCHAR(10) NOT NULL PRIMARY KEY, "
            "tool_dm NUMERIC(6, 3) NOT NULL, "
            "tool_type VARCHAR(10) NOT NULL, "
            "tool_note VARCHAR(50), "
            "tool_cnc INTEGER NOT NULL DEFAULT 0, "
            "tool_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, "
            "tool_worker NOT NULL REFERENCES worker_list(worker_id))")
cur.close()
conn.commit()
conn.close()


class Toolholder(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # ico format can show correctly. When on Mac, the "default" need to be "bitmap", also "self" to "tk.Tk"
        tk.Tk.iconbitmap(self, bitmap="client_icon.ico")
        self.geometry("600x320")
        self.resizable(False, False)
        self.wm_title("POLC QM&CNC刀柄管理系统")

        menu_bar = tk.Menu(self, tearoff=0)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="管理员", command=lambda: self.showFrame(AdminLogin))
        file_menu.add_command(label="员工", command=lambda :self.showFrame(WorkerLogin))
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=lambda: tk.Tk.destroy(self))
        menu_bar.add_cascade(label="文件", menu=file_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="帮助", command=lambda :myThread(popupMsg, ("Not support yet!", )))
        help_menu.add_separator()
        help_menu.add_command(label="版本", command=lambda :myThread(popupMsg, ("Version: 0.1", )))
        help_menu.add_command(label="关于", command=lambda :myThread(popupMsg, ("Author: Tristan Song/宋寒", )))
        menu_bar.add_cascade(label="帮助", menu=help_menu)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (WorkerLogin, AdminLogin, WorkerPage, AdminPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.showFrame(WorkerLogin)

    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class WorkerLogin(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = ttk.Label(self, text="请扫描工号卡！")
        label.pack()
        self.id_card = tk.Entry(self, show="*")
        self.id_card.pack()
        button = ttk.Button(self, text="登陆", command=self.infoCheck)
        button.pack()

        self.id_card.focus_set()

    def infoCheck(self):
        conn = sqlite3.connect("toolholder_db.db")
        cur = conn.cursor()
        cur.execute("SELECT id_card "
                    "FROM worker_list "
                    "WHERE id_card=?", (self.id_card.get(), ))
        values = cur.fetchone()
        cur.close()
        conn.commit()
        conn.close()

        if values == None or values[0] == "":
            popupMsg("暂时没有您的信息，请联系管理员！")
        else:
            global LOGIN_PERSON
            LOGIN_PERSON = self.id_card.get()
            self.controller.showFrame(WorkerPage)


class AdminLogin(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        id_label = ttk.Label(self, text="名称：")
        id_label.grid(row=0, column=0)
        name_label = ttk.Label(self, text="密码：")
        name_label.grid(row=1, column=0)
        self.id_input = ttk.Entry(self, width=10, show="*")
        self.id_input.grid(row=0, column=1)
        self.name_input = ttk.Entry(self, width=10, show="*")
        self.name_input.grid(row=1, column=1)

        self.id_input.focus_set()

        login_button = ttk.Button(self, text="登陆", command=self.infoCheck)
        login_button.grid(row=2, column=0, columnspan=2)

    def infoCheck(self):
        if self.id_input.get() == ADMIN_USER and self.name_input.get() == ADMIN_PWD:
            global LOGIN_PERSON
            LOGIN_PERSON = "0000"
            self.controller.showFrame(AdminPage)
        else:
            popupMsg("请输入正确的管理员信息！")


class WorkerPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        ################################################################################################################
        # borrow and return
        b_r_canvas = tk.Canvas(self, bg=COLOR_1, height=300, width=180)
        b_r_canvas.place(x=0, y=0, anchor="nw")

        b_r_label = ttk.Label(b_r_canvas, text="借刀＆还刀")
        b_r_label.place(x=70, y=0, anchor="nw")

        b_r_msg_label = ttk.Label(b_r_canvas, text="""借刀：请使用扫描枪扫描刀柄上
           二维码，并输入使用机床！
还刀：扫描刀柄上二维码即可！""")
        b_r_msg_label.place(x=0, y=180, anchor="nw")

        borrow_label = ttk.Label(b_r_canvas, text="刀柄号：", width=7)
        borrow_label.place(x=10, y=20, anchor="nw")
        self.borrow_entry = ttk.Entry(b_r_canvas, width=18)
        self.borrow_entry.place(x=62, y=20, anchor="nw")

        cnc_label = ttk.Label(b_r_canvas, text="机床：", width=7)
        cnc_label.place(x=10, y=50, anchor="nw")
        self.cnc_entry = ttk.Entry(b_r_canvas, width=18)
        self.cnc_entry.place(x=62, y=50, anchor="nw")

        #retrun_label = ttk.Label(b_r_canvas, text="还刀柄：", width=7)
        #retrun_label.place(x=10, y=80, anchor="nw")
        #self.return_entry = ttk.Entry(b_r_canvas, width=18)
        #self.return_entry.place(x=62, y=80, anchor="nw")

        open_button = ttk.Button(b_r_canvas, text="开锁", width=8)
        open_button.place(x=0, y=140, anchor="nw")
        borrow_button = ttk.Button(b_r_canvas, text="借刀", width=8)
        borrow_button.place(x=60, y=140, anchor="nw")
        return_button = ttk.Button(b_r_canvas, text="还刀", width=8)
        return_button.place(x=120, y=140, anchor="nw")

        open_button.config(command=lambda: myThread(openLock, ()))
        borrow_button.config(command=lambda :myThread(lendTool, (self.borrow_entry.get(), self.cnc_entry.get())))
        return_button.config(command=lambda :myThread(returnTool, (self.borrow_entry.get(), )))

        ################################################################################################################
        # search
        search_canvas = tk.Canvas(self, bg=COLOR_1, height=300, width=180)
        search_canvas.place(x=200, y=0, anchor="nw")

        search_msg_label = ttk.Label(search_canvas, text="""支持以下查询：
1，根据二维码编号查找
2，根据类型、直径模糊搜索
      如：输入(铣刀，10)即可查询
      所有(铣刀，直径10~11)刀具！
查询结果存放在results.txt中""")
        search_msg_label.place(x=0, y=180, anchor="nw")

        search_label = ttk.Label(search_canvas, text="查刀")
        search_label.place(x=80, y=0, anchor="nw")

        tool_no_label = ttk.Label(search_canvas, text="编号：", width=5)
        tool_no_label.place(x=10, y=20, anchor="nw")
        self.tool_no_entry = ttk.Entry(search_canvas, width=20)
        self.tool_no_entry.place(x=50, y=20, anchor="nw")

        tool_type_label = ttk.Label(search_canvas, text="类型：", width=5)
        tool_type_label.place(x=10, y=50, anchor="nw")
        self.tool_type_entry = ttk.Entry(search_canvas, width=20)
        self.tool_type_entry.place(x=50, y=50, anchor="nw")
        """
        # 用Listbox太过麻烦，故直接使用Entry
        self.search_type_scroll = ttk.Scrollbar(search_canvas)
        self.search_type_scroll.place(x=160, y=50, anchor="nw")
        self.search_type_list = tk.Listbox(search_canvas, yscrollcommand=self.search_type_scroll.set, height=3, width=17, selectmode="SINGLE")
        self.search_type_list.place(x=50, y=50, anchor="nw")
        for i in ["铣刀", "镗刀", "铰刀", "钻头"]:
            self.search_type_list.insert("end", i)
        self.search_type_scroll.config(command=self.search_type_list.yview)
        """

        tool_dm_label = ttk.Label(search_canvas, text="直径：", width=5)
        tool_dm_label.place(x=10, y=80, anchor="nw")
        self.tool_dm_entry = ttk.Entry(search_canvas, width=20)
        self.tool_dm_entry.place(x=50, y=80, anchor="nw")

        search_note_label = ttk.Label(search_canvas, text="备注：", width=5)
        search_note_label.place(x=10, y=110, anchor="nw")
        self.search_note_text = ttk.Entry(search_canvas, width=20)
        self.search_note_text.place(x=50, y=110, anchor="nw")

        search_button = ttk.Button(search_canvas, text="查询", width=8)
        search_button.place(x=70, y=140, anchor="nw")
        search_button.config(command=lambda :myThread(searchToolholder, (self.tool_no_entry.get(), self.tool_dm_entry.get(), self.tool_type_entry.get())))


class AdminPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        ################################################################################################################
        # worker database canvas
        worker_canvas = tk.Canvas(self, bg=COLOR_2, height=300, width=180)
        worker_canvas.place(x=400, y=0, anchor="nw")

        worker_label = ttk.Label(worker_canvas, text="员工信息管理", width=15)
        worker_label.place(x=50, y=0, anchor="nw")
        worker_msg_label = ttk.Label(worker_canvas, text="""工卡：ID卡，扫描即可                    
工号：员工工号                    
姓名：员工姓名                    """)
        worker_msg_label.place(x=0, y=180, anchor="nw")

        id_card_label = ttk.Label(worker_canvas, text="工卡：", width=5)
        id_card_label.place(x=10, y=20, anchor="nw")
        self.id_card_entry = ttk.Entry(worker_canvas, width=20)
        self.id_card_entry.place(x=50, y=20, anchor="nw")

        id_label = ttk.Label(worker_canvas, text="工号：", width=5)
        id_label.place(x=10, y=50, anchor="nw")
        self.id_entry = ttk.Entry(worker_canvas, width=20)
        self.id_entry.place(x=50, y=50, anchor="nw")

        name_label = ttk.Label(worker_canvas, text="姓名：", width=5)
        name_label.place(x=10, y=80, anchor="nw")
        self.name_entry = ttk.Entry(worker_canvas, width=20)
        self.name_entry.place(x=50, y=80, anchor="nw")

        add_button = ttk.Button(worker_canvas, text="增加", width=8)
        add_button.place(x=15, y=140, anchor="nw")
        del_button = ttk.Button(worker_canvas, text="删除", width=8)
        del_button.place(x=100, y=140, anchor="nw")
        add_button.config(command=lambda :myThread(addWorker, (self.id_card_entry.get(), self.id_entry.get(), self.name_entry.get())))
        del_button.config(command=lambda :myThread(delWorker, (self.id_card_entry.get(), )))

        ################################################################################################################
        # toolholder database canvas
        tool_canvas = tk.Canvas(self, bg=COLOR_2, height=300, width=180)
        tool_canvas.place(x=200, y=0, anchor="nw")

        toolholder_label = ttk.Label(tool_canvas, text="刀柄管理")
        toolholder_label.place(x=70, y=0, anchor="nw")
        search_msg_label = ttk.Label(tool_canvas, text="""支持以下查询：
1，根据二维码编号查找
2，根据类型、直径模糊搜索
      如：输入(铣刀，10)即可查询
      所有(铣刀，直径10~11)刀具！
查询结果存放在results.txt中""")
        search_msg_label.place(x=0, y=180, anchor="nw")

        tool_no_label = ttk.Label(tool_canvas, text="编号：", width=5)
        tool_no_label.place(x=10, y=20, anchor="nw")
        self.tool_no_entry = ttk.Entry(tool_canvas, width=20)
        self.tool_no_entry.place(x=50, y=20, anchor="nw")

        tool_type_label = ttk.Label(tool_canvas, text="类型：", width=5)
        tool_type_label.place(x=10, y=50, anchor="nw")
        self.tool_type_entry = ttk.Entry(tool_canvas, width=20)
        self.tool_type_entry.place(x=50, y=50, anchor="nw")
        """
        # 用Listbox太过麻烦，故直接使用Entry
        self.tool_type_scroll = ttk.Scrollbar(tool_canvas)
        self.tool_type_scroll.place(x=160, y=50, anchor="nw")
        self.tool_type_list = tk.Listbox(tool_canvas, yscrollcommand=self.tool_type_scroll.set, height=3, width=17, selectmode="SINGLE")
        self.tool_type_list.place(x=50, y=50, anchor="nw")
        for i in ["铣刀", "镗刀", "铰刀", "钻头"]:
            self.tool_type_list.insert("end", i)
        self.tool_type_scroll.config(command=self.tool_type_list.yview)
        """

        tool_dm_label = ttk.Label(tool_canvas, text="直径：", width=5)
        tool_dm_label.place(x=10, y=80, anchor="nw")
        self.tool_dm_entry = ttk.Entry(tool_canvas, width=20)
        self.tool_dm_entry.place(x=50, y=80, anchor="nw")

        tool_note_label = ttk.Label(tool_canvas, text="备注：", width=5)
        tool_note_label.place(x=10, y=110, anchor="nw")
        self.tool_note_entry = ttk.Entry(tool_canvas, width=20)
        self.tool_note_entry.place(x=50, y=110, anchor="nw")

        tool_add_button = ttk.Button(tool_canvas, text="增加", width=8)
        tool_add_button.place(x=5, y=140, anchor="nw")
        tool_del_button = ttk.Button(tool_canvas, text="删除", width=8)
        tool_del_button.place(x=65, y=140, anchor="nw")
        tool_search_button = ttk.Button(tool_canvas, text="查询", width=8)
        tool_search_button.place(x=125, y=140, anchor="nw")

        tool_add_button.config(command=lambda :myThread(addToolholder, (self.tool_no_entry.get(), self.tool_dm_entry.get(), self.tool_type_entry.get(), self.tool_note_entry.get())))
        tool_del_button.config(command=lambda :myThread(delToolholder, (self.tool_no_entry.get(), )))
        tool_search_button.config(command=lambda :myThread(searchToolholder, (self.tool_no_entry.get(), self.tool_dm_entry.get(), self.tool_type_entry.get())))

        ################################################################################################################
        # borrow and return
        b_r_canvas = tk.Canvas(self, bg=COLOR_2, height=300, width=180)
        b_r_canvas.place(x=0, y=0, anchor="nw")

        b_r_label = ttk.Label(b_r_canvas, text="借刀＆还刀")
        b_r_label.place(x=70, y=0, anchor="nw")
        b_r_msg_label = ttk.Label(b_r_canvas, text="""借刀：请使用扫描枪扫描刀柄上
           二维码，并输入使用机床！
还刀：扫描刀柄上二维码即可！""")
        b_r_msg_label.place(x=0, y=180, anchor="nw")

        borrow_label = ttk.Label(b_r_canvas, text="刀柄号：", width=7)
        borrow_label.place(x=10, y=20, anchor="nw")
        self.borrow_entry = ttk.Entry(b_r_canvas, width=18)
        self.borrow_entry.place(x=62, y=20, anchor="nw")

        cnc_label = ttk.Label(b_r_canvas, text="机床：", width=7)
        cnc_label.place(x=10, y=50, anchor="nw")
        self.cnc_entry = ttk.Entry(b_r_canvas, width=18)
        self.cnc_entry.place(x=62, y=50, anchor="nw")

        #return_label = ttk.Label(b_r_canvas, text="还刀柄：", width=7)
        #return_label.place(x=10, y=80, anchor="nw")
        #self.return_entry = ttk.Entry(b_r_canvas, width=18)
        #self.return_entry.place(x=62, y=80, anchor="nw")

        open_button = ttk.Button(b_r_canvas, text="开锁", width=8)
        open_button.place(x=0, y=140, anchor="nw")
        borrow_button = ttk.Button(b_r_canvas, text="借刀", width=8)
        borrow_button.place(x=60, y=140, anchor="nw")
        return_button = ttk.Button(b_r_canvas, text="还刀", width=8)
        return_button.place(x=120, y=140, anchor="nw")


        open_button.config(command=lambda: myThread(openLock, ()))
        borrow_button.config(command=lambda :myThread(lendTool, (self.borrow_entry.get(), self.cnc_entry.get())))
        return_button.config(command=lambda :myThread(returnTool, (self.borrow_entry.get(),)))
        """
        # search
        search_canvas = tk.Canvas(self, bg=COLOR_2, height=200, width=180)
        search_canvas.place(x=400, y=200, anchor="nw")

        search_label = ttk.Label(search_canvas, text="查刀")
        search_label.place(x=80, y=0, anchor="nw")

        search_no_label = ttk.Label(search_canvas, text="编号：", width=5)
        search_no_label.place(x=10, y=20, anchor="nw")
        self.search_no_entry = ttk.Entry(search_canvas, width=20)
        self.search_no_entry.place(x=50, y=20, anchor="nw")

        search_dm_label = ttk.Label(search_canvas, text="直径：", width=5)
        search_dm_label.place(x=10, y=110, anchor="nw")
        self.search_dm_entry = ttk.Entry(search_canvas, width=20)
        self.search_dm_entry.place(x=50, y=110, anchor="nw")

        search_type_label = ttk.Label(search_canvas, text="类型：", width=5)
        search_type_label.place(x=10, y=50, anchor="nw")

        self.search_type_scroll = ttk.Scrollbar(search_canvas)
        self.search_type_scroll.place(x=160, y=50, anchor="nw")
        self.search_type_list = tk.Listbox(search_canvas, yscrollcommand=self.search_type_scroll.set, height=3, width=17, selectmode="SINGLE")
        self.search_type_list.place(x=50, y=50, anchor="nw")
        for i in ["铣刀", "镗刀", "铰刀", "钻头"]:
            self.search_type_list.insert("end", i)
        self.search_type_scroll.config(command=self.search_type_list.yview)

        search_note_label = ttk.Label(search_canvas, text="备注：", width=5)
        search_note_label.place(x=10, y=140, anchor="nw")
        self.search_note_text = tk.Text(search_canvas, width=18, height=2)
        self.search_note_text.place(x=50, y=140, anchor="nw")

        search_button = ttk.Button(search_canvas, text="查询", width=10)
        search_button.place(x=70, y=175, anchor="nw")
        """


def myThread(Target, Args=()):
    th = threading.Thread(target=Target, args=Args)
    th.setDaemon(True)
    th.start()
    

def openLock():
    os.system('bth.exe')


def popupMsg(msg):
    window = tk.Tk()
    window.wm_title("!")
    label1 = ttk.Label(window, text=msg)
    label1.pack(side="top", fill="both", expand=True)
    button1 = ttk.Button(window, text="OK", command=window.destroy)
    button1.pack(side="top", fill="x", expand=True)
    window.mainloop()


def addWorker(id_card, worker_id, worker_name):

    if id_card == "":
        popupMsg("请将工号卡放置于读卡器上！")
    elif worker_id == "":
        popupMsg("请输入工号！")
    elif worker_name == "":
        popupMsg("请输入员工姓名！")

    conn = sqlite3.connect("toolholder_db.db")
    cur = conn.cursor()
    cur.execute("SELECT id_card "
                "FROM worker_list "
                "WHERE id_card=?", (id_card, ))
    values = cur.fetchone()

    if values == None:
        cur.execute("INSERT INTO worker_list "
                    "VALUES (?, ?, ?)", (id_card, worker_id, worker_name))
        popupMsg("(%s, %s)已添加!"%(worker_id, worker_name))
    else:
        popupMsg("此卡已注册！")

    cur.close()
    conn.commit()
    conn.close()

    shutil.copy("./toolholder_db.db", r"\\cn11smfg\MFG\POLC\POLC-CNC")


# not working for the right now, because when using REFERENCE, need to delete the corresponding info
def delWorker(id_card):
    if id_card == "":
        popupMsg("请将工号卡放置于读卡器上！")

    conn = sqlite3.connect("toolholder_db.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM worker_list "
                "WHERE id_card=?", (id_card, ))
    values = cur.fetchone()

    if values == None:
        popupMsg("此人还未注册！")
    else:
        cur.execute("DELETE FROM worker_list "
                    "WHERE id_card=?", (id_card,))
        popupMsg("(%s, %s)已删除"%(values[1], values[2]))

    cur.close()
    conn.commit()
    conn.close()
    
    shutil.copy("./toolholder_db.db", r"\\cn11smfg\MFG\POLC\POLC-CNC")


def addToolholder(tool_id, tool_dm, tool_type, tool_note):
    if tool_id == "":
        popupMsg("请扫描刀柄二维码！")
    elif tool_dm == "":
        popupMsg("请输入刀柄直径！")
    elif tool_type == "":
        popupMsg("请选择刀柄类型！")
    elif tool_note == "":
        popupMsg("请输入刀柄描述！")

    conn = sqlite3.connect("toolholder_db.db")
    cur = conn.cursor()
    cur.execute("SELECT tool_id "
                "FROM toolholder_list "
                "WHERE tool_id=?", (tool_id, ))
    values = cur.fetchone()

    if values == None:
        cur.execute("INSERT INTO toolholder_list "
                    "(tool_id, tool_dm, tool_type, tool_note, tool_cnc, tool_time, tool_worker) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (tool_id, float(tool_dm), tool_type, tool_note, 0, datetime.now(), "0000"))
        popupMsg("刀柄添加完成")
    else:
        popupMsg("此刀柄已添加！")

    cur.close()
    conn.commit()
    conn.close()
    
    shutil.copy("./toolholder_db.db", r"\\cn11smfg\MFG\POLC\POLC-CNC")
    

def delToolholder(tool_id):
    if tool_id == "":
        popupMsg("请扫描刀柄二维码！")

    conn = sqlite3.connect("toolholder_db.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM toolholder_list "
                "WHERE tool_id=?", (tool_id, ))
    values = cur.fetchone()

    if values == None:
        popupMsg("查无此刀柄！")
    else:
        cur.execute("DELETE FROM toolholder_list "
                    "WHERE tool_id=?", (tool_id, ))
        popupMsg("(%s, %s)已删除"%(values[0], values[1]))

    cur.close()
    conn.commit()
    conn.close()

    shutil.copy("./toolholder_db.db", r"\\cn11smfg\MFG\POLC\POLC-CNC")


def searchToolholder(tool_id, tool_dm, tool_type):
    conn = sqlite3.connect("toolholder_db.db")
    cur = conn.cursor()

    if tool_id == "" and tool_dm == "" and tool_type == "":
        popupMsg("请至少输入一条搜索项！")

    if tool_id !="":
        cur.execute("SELECT * FROM toolholder_list "
                    "WHERE tool_id=?", (tool_id, ))
    else:
        if tool_dm != "" and tool_type != "":
            cur.execute("SELECT * FROM toolholder_list "
                        "WHERE tool_dm LIKE ? AND tool_type LIKE ?", (tool_dm+'%', tool_type+'%'))
        else:
            popupMsg("请输入合理的搜索信息！")

    values = cur.fetchall()
    if values == None:
        popupMsg("查无此刀柄！")
    else:
        row_0 = [u"刀柄号", u"直径", u"类型", u"备注", u"使用机床", u"借还时间", u"使用员工"]
        # save results to .txt file
        with open("results.txt", "w") as f:
            for line in row_0:
                f.write(line+",")
            f.write("\n")
            
            for line in values:
                for i in line:
                    f.write(str(i) + ", ")
                f.write("\n")
        """
        # save results to .xlsx file
        f = xlwt.Workbook()
        sheet_1 = f.add_sheet(u"刀柄查询", cell_overwrite_ok=True)
        for j in range(0, len(row_0)):
            sheet_1.write(0, j, row_0[j])

        row = 1
        for line in values:
            for j in range(0, 5):
                sheet_1.write(i, j, str(line[j]))
    
        f.save("results.xls")
        """
     
        popupMsg("查询完成，请打开results.txt文件！")

    cur.close()
    conn.commit()
    conn.close()


def lendTool(tool_id, cnc_no):
    if tool_id == "":
        popupMsg("请扫描刀柄二维码！")
    if cnc_no == "":
        popupMsg("请输入机床号！")

    conn = sqlite3.connect("toolholder_db.db")
    cur = conn.cursor()
    cur.execute("UPDATE toolholder_list "
                "SET tool_cnc=?, tool_time=?, tool_worker=? "
                "WHERE tool_id=?",
                (cnc_no, datetime.now(), LOGIN_PERSON, tool_id))
    popupMsg("已完成借刀流程！")

    cur.close()
    conn.commit()
    conn.close()

    shutil.copy("./toolholder_db.db", r"\\cn11smfg\MFG\POLC\POLC-CNC")
    

def returnTool(tool_id):
    if tool_id == "":
        popupMsg("请扫描刀柄二维码！")

    conn = sqlite3.connect("toolholder_db.db")
    cur = conn.cursor()
    cur.execute("UPDATE toolholder_list "
                "SET tool_cnc=?, tool_time=?, tool_worker=? "
                "WHERE tool_id=?",
                (0, datetime.now(), LOGIN_PERSON, tool_id))
    popupMsg("已完成还刀流程！")

    cur.close()
    conn.commit()
    conn.close()

    shutil.copy("./toolholder_db.db", r"\\cn11smfg\MFG\POLC\POLC-CNC")
    

app = Toolholder()
app.mainloop()
