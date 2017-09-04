#!/usr/bin/env python3
# -*-coding: utf-8 -*-
"""
Created on Thur Aug 17 14:31:00 2017

@author: TristanSong
"""

from trafficAPI import trafficAPI
import platform
import codecs

def main():
    """
    LINES  = ['B1', 'H1', 'B2', 'H2', 'B10', 'B11', 'B12', 'B13', 'B15', 'B16', 'B19', 'B22', 'B23']
    if platform.system() == 'Darwin':
        with open('./bus_stations.csv', 'wb') as f:
            for line in LINES:
                api = trafficAPI('lines', line)
                ans = api.search()
                f.write((line + ';').encode('utf-8'))
                f.write((ans + '\n').encode('utf-8'))
    else:
        with open('./bus_stations.csv', 'w') as f:
            for line in LINES:
                api = trafficAPI('lines', line)
                ans = api.search()
                f.write(line + ';')
                f.write(ans + '\n')
    """
    stats = []
    with codecs.open('./bus_stations.csv', 'r') as f:
        for line in f.readlines():
            line = line.strip().split(';')
            for i in range(1, len(line)):
                if line[i] not in stats:
                    stats.append(line[i])

    if platform.system() == 'Darwin':
        with open('./stats_coord.csv', 'wb') as f:
            for stat in stats:
                api = trafficAPI('stats', stat)
                ans = api.search()
                f.write((stat+':'+ans+'\n').encode('utf-8'))
    else:
        with open('./stats_coord.csv', 'w') as f:
            for stat in stats:
                api = trafficAPI('stats', stat)
                ans = api.search()
                print(ans)
                f.write(stat+':'+ans+'\n')
    

if __name__ == '__main__':
    main()
