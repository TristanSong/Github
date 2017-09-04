#!/usr/bin/env python3
# -*-coding: utf-8 -*-
"""
Created on Mon Aug 28 16:50 2017

@author: TristanSong
"""

def main():
    with open('./学区.csv', 'rb') as f:
        schoolDict = {}
        for line in f.readlines():
            line = line.decode('utf-8').strip().split(',')
            k = line[0]
            line.pop(0)
            schoolDict[k] = line

    filename = './小区_SCHOOL.csv'
    f_result = open(filename, 'wb')
    f_result.write(('小区,行政区,').encode('utf-8'))
    for k in schoolDict:
        f_result.write((k+',').encode('utf-8'))
    f_result.write(('\n').encode('utf-8'))
    
    with open('./常州_小区.csv', 'rb') as f:
        for line in f.readlines():
            line = line.decode('utf-8').strip().split(',')
            ans = []
            ans.extend([line[0], line[4]])
            for k in schoolDict:
                if line[0] in schoolDict[k]:
                    ans.append(1)
                else:
                    ans.append(0)
            for i in ans:
                f_result.write((str(i)+',').encode('utf-8'))
            f_result.write(('\n').encode('utf-8'))
    f_result.close()
        
if __name__ == '__main__':
    main()
