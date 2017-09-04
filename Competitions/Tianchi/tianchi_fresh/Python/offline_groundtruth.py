#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
Created on Sun May 21 23:10:19 2017

@author: TristanSong
"""

with open("offline_groundtruth.csv", "w") as f:
    f.write("user_id,item_id\n")
    data = open("/Volumes/macOS_HD/Python/TianChi/tianchi_fresh/tianchi_fresh_comp_train_user.csv", "r")
    for line in data.readlines():
        line = line.strip().split(",")
        if "2014-12-18" in line[5] and line[2]=="4":
            f.write(line[0]+","+line[1])
    data.close()
    
