#!/usr/bin/env python3
# -*-coding: utf-8 -*-
"""
Created on Thur Aug 10 09:45:00 2017

@author: TristanSong
"""

import pymysql
import os
import re
from datetime import datetime
import tkinter as tk
from tkinter import ttk

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

# 录入数据
def get_result():
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='')
    cur = conn.cursor()
    cur.execute('CREATE DATABASE IF NOT EXISTS nova_spc')
    cur.execute('USE nova_spc')
    
    fileLists = os.listdir()
    for file in fileLists:
        if '.txt' in file:
                thicknessLine = [15, 18, 22, 26, 37, 40, 44, 48]  # 壁厚在文件中位置
                with open(file, 'r', encoding='gbk') as f:
                    data = f.readlines()
                    t = []
                    volume = re.split('\\s+', data[3].strip())[-1] # 弹性体容量
                    cnc = re.split('\\s+', data[7].strip())[-1] # 机床号
                    markNo = re.split('\\s+', data[7].strip())[-2] # 钢号
                    measureTime = re.split("\\s+", data[5].strip()) # 测量时间
                    measureTime = datetime.strptime(measureTime[-2] + measureTime[-1], "%Y/%m/%d%H:%M")
                    for line in thicknessLine: # 壁厚数据
                        b = re.split("\\s+", data[line - 1].strip())
                        t.append(float(b[5]))

                # 数据库中是否有‘容量_机床’表，没有则创建
                tableName = volume.split('-')[-1] + '_' + cnc
                cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='nova_spc'")
                tableLists = cur.fetchall()
                if tableName not in tableLists:
                    sql = 'CREATE TABLE IF NOT EXISTS ' + tableName + ' (markNo INT NOT NULL PRIMARY KEY, m_time DATETIME NOT NULL, \
t1 FLOAT(4, 3) NOT NULL, t2 FLOAT(4, 3) NOT NULL, t3 FLOAT(4, 3) NOT NULL, t4 FLOAT(4, 3) NOT NULL, \
t5 FLOAT(4, 3) NOT NULL, t6 FLOAT(4, 3) NOT NULL, t7 FLOAT(4, 3) NOT NULL, t8 FLOAT(4, 3) NOT NULL)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4'
                    cur.execute(sql)
                # 录入数据至表中
                sql = 'INSERT INTO ' + tableName + ' (markNo, t1, t2, t3, t4, t5, t6, t7, t8, m_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                cur.execute(sql, (markNo, t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], measureTime))

    cur.close()
    conn.commit()
    conn.close()
    popup_msg('数据录入完成！')

if __name__ == '__main__':
    app = tk.Tk()
    app.wm_title('NOVA SPC数据自动录入程序')
    app.geometry('640x480')
    app.resizable(0, 0)

    label = tk.Label(app, font=LARGE_FONT, text="""
NOVA SPC数据自动录入程序

本程序用于将NOVA三坐标检测结果自动录入数据库中
数据录入成功后，会出现弹窗提示：数据录入完成
*******注意：每次仅放入最新检测结果*******
*******否则会报错，并且没有弹窗弹出*******""")
    label.pack(side='top', fill="both", expand=True)
    button = tk.Button(app, text='开始录入', font=LARGE_FONT, command=get_result)
    button.pack(side='bottom')
    app.mainloop()
    

