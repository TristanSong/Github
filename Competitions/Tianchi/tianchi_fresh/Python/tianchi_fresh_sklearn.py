#!/usr/bin/env python3
# -*-coding:utf-8 -*0
"""
Created on Sun May 21 18:04:05 2017

@author: TristanSong
"""

import numpy as np
import pandas as pd
import math
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

f = open("data.csv", "r")
data = f.readlines()

train_day29 = []
offline_candidate30 = []
online_candidate31 = []

for line in data:
    array = line.strip().split(",")
    if array[0]=="user_id":
        continue
    day = int(array[-1])
    uid = (array[0], array[1], day+1)
    if day==29:
        train_day29.append(uid)
    if day==30:
        offline_candidate30.append(uid)
    if day==31:
        online_candidate31.append(uid)

train_day29 = list(set(train_day29))
offline_candidate30 = list(set(offline_candidate30))
online_candidate31 = list(set(online_candidate31))

print("*****"*7)
print("Train Item number:", len(train_day29))
print("Offline Candidate Item number:", len(offline_candidate30))
print("*****"*7)

# feature
ui_dict = [{}for i in range(4)]
for line in data:
    array = line.strip().split(",")
    if array[0]=="user_id":
        continue
    day = int(array[-1])
    uid = (array[0], array[1], day)
    type = int(array[-2]) - 1
    if uid in ui_dict[type]:
        ui_dict[type][uid] += 1
    else:
        ui_dict[type][uid] = 1

# label
ui_buy = {}
for line in data:
    array = line.strip().split(",")
    if array[0]=="user_id":
        continue
    day = int(array[-1])
    uid = (array[0], array[1], day)
    if array[-2]=="4":
        ui_buy[uid] = 1

# train X, y
X = np.zeros((len(train_day29), 4))
y = np.zeros((len(train_day29), ))
id = 0
for uid in train_day29:
    last_uid = (uid[0], uid[1], uid[2]-1)
    for i in range(4):
        X[id][i] = math.log1p(ui_dict[i][last_uid] if last_uid in ui_dict[i] else 0)
    y[id] = 1 if uid in ui_buy else 0
    id += 1

print("*****"*7)
print("X= ", X)
print("-----"*7)
print("y= ", y)
print("Train number:", len(y), "Positive number:", sum(y))

# predict X, y for offline_candidate30
pX = np.zeros((len(offline_candidate30), 4))
id = 0
for uid in offline_candidate30:
    last_uid = (uid[0], uid[1], uid[2]-1)
    for i in range(4):
        pX[id][i] = math.log1p(ui_dict[i][last_uid] if last_uid in ui_dict[i] else 0)
    id += 1

# predict X, y for online_candidate31



# training
model = LogisticRegression()
#model = DecisionTreeClassifier()
model.fit(X, y)

# evaluate
py = model.predict_proba(pX)
npy = []
for a in py:
    npy.append(a[1])
py = npy
print("pX= ", pX)

# combine
lx = zip(offline_candidate30, py)
print("*****"*7)
lx = sorted(lx, key=lambda x:x[1], reverse=True)
print("*****"*7)

wf = open("ans.csv", "w")
wf.write("user_id,item_id\n")
for i in range(437):
    item = lx[i]
    wf.write("%s,%s\n"%(item[0][0], item[0][1]))

wf.close()
f.close()
