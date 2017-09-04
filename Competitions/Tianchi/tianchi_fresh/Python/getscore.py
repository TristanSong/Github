#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
Created on Sun May 21 23:10:19 2017

@author: TristanSong
"""

import sys

st = open("offline_groundtruth.csv")
const = st.readlines()

answer = []
for a in const:
    if a[0]=="u":
        continue
    answer.append(a)
answer = set(answer)

f = open(sys.argv[1])
con = f.readlines()
you = []
for a in con:
    if a[0]=="u":
        continue
    you.append(a)
you = set(you)

inter = answer&you

print("Hit number:", len(inter))
if len(inter) > 0:
    a = len(answer)
    b = len(you)
    c = len(inter)
    R = 1.0*c/a*100
    P = 1.0*c/b*100
    F1 = 2.0*R*P/(R+P)
    print("F1/P/R %.2f%%/%.2f%%/%.2f%%\n"%(F1, P, R))
