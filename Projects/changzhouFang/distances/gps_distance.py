#!/usr/bin/env python3
# -*-coding: utf-8 -*-
"""
Created on Mon Aug 28 10:45:00 2017

@author: TristanSong
"""

import numpy as np
import platform
import codecs

def distance(x1, y1, x2, y2):
    R =  6378.137 # 地球半径
    # 转化为rad
    radLat1 = np.deg2rad(x1)
    radLng1 = np.deg2rad(y1)
    radLat2 = np.deg2rad(x2)
    radLng2 = np.deg2rad(y2)
    a = radLat1 - radLat2
    b = radLng1 - radLng2
    s = 2*np.arcsin(np.sqrt(np.power(np.sin(a/2), 2) + np.cos(radLat1)*np.cos(radLat2)*np.power(np.sin(b/2), 2)))
    return int(1000*s*R)

def main():
    # 计算小区到BRT、地铁、公园
    file_d = './小区_METRO.csv'
    file_1 = './常州_小区.csv'
    file_2 = './metro.csv'

    if platform.system() == 'Windows':
        file_result = open(file_d, 'wb')

        # 读取所有目标站点，形成词典
        targetDict = {}
        with open(file_2, 'rb') as f:
            for line in f.readlines():
                line = line.decode('utf-8').strip().split(',')
                if line[0] not in targetDict:
                    targetDict[line[0]] = [float(line[1]), float(line[2])]

        with open(file_1, 'rb') as f:
            for line in f.readlines():
                line = line.decode('utf-8').strip().split(',')
                line[1] = float(line[1]) # 纬度
                line[2] = float(line[2]) # 经度

                # 小区与所有目标站点的距离
                tempDict = {}
                for k in targetDict:
                    # 注意经纬度对应(经度、纬度)
                    tempDict[k] = distance(line[2], line[1], targetDict[k][0], targetDict[k][1])
                # 存储最小距离及站点
                min_d = min(tempDict.items(), key=lambda x: x[1])
                file_result.write((line[0] + ',' + str(min_d[1]) + ',' + min_d[0] + ',' + line[4] + '\n').encode('utf-8'))
        f_result.close()
    
if __name__ == '__main__':
    main()
