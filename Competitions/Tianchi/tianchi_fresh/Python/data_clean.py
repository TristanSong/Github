#!/usr/bin/env python3
# -*-coding: utf-8 -*-
"""
Created on Sun May 21 17:17:27 2017

@author: TristanSong
"""

with open("data.csv", "w") as f:
    f.write("user_id,item_id,behavior_type,day\n")
    data = open("/Volumes/macOS_HD/Python/TianChi/tianchi_fresh/tianchi_fresh_comp_train_user.csv", "r")
    for line in data.readlines():
        line = line.strip().split(",")
        if "2014-12-18" in line[5]:
            f.write(line[0]+","+line[1]+","+line[2]+","+'30'+"\n")
        if "2014-12-17" in line[5]:
            f.write(line[0]+","+line[1]+","+line[2]+","+"29"+"\n")
        if "2014-12-16" in line[5]:
            f.write(line[0]+","+line[1]+","+line[2]+","+"28"+"\n")
    data.close()
