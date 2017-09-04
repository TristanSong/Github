#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
Created on Wed Jun 6 17:09:00 2017

@author: TristanSong
"""

import sqlite3
import csv

conn = sqlite3.connect("./toolholder_db.db")
cur = conn.cursor()

cur.execute("SELECT * FROM worker_list ORDER BY id_card")
workers = cur.fetchall()
with open("./worker_list.csv", "w", encoding="utf-8") as f:
    writer = csv.writer(f)
    for worker in workers:
        writer.writerow(worker)

cur.execute("SELECT * FROM toolholder_list ORDER BY tool_id")
toolholders = cur.fetchall()
with open("./toolholder_list.csv", "w", encoding="utf-8") as f:
    writer = csv.writer(f)
    for toolholder in toolholders:
        writer.writerow(toolholder)

cur.close()
conn.close()
