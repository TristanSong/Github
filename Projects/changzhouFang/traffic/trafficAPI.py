#!/usr/bin/env python3
# -*-coding: utf-8 -*-
"""
Created on Thur Aug 17 13:48:00 2017

@author: TristanSong
"""

import re
from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup

class trafficAPI(object):
    def __init__(self, searchType, item, city='常州', app_key = 'f41c8afccc586de03a99c86097e98ccb'):
        # 2 searchType: stats, lines
        self.searchType = searchType
        self.item = item.upper()
        self.city = city
        self.app_key = app_key

    def search(self):
        types = ['stats', 'lines']
        if self.searchType not in  types:
            print('请输入正确搜索选项：stats or lines?')
            exit
        baseURL = 'http://openapi.aibang.com/bus/'
        url = baseURL + self.searchType + '?app_key=' + self.app_key + '&city=' + \
              quote(self.city) + '&q=' + quote(self.item)
        html = urlopen(url).read()
        bsObj = BeautifulSoup(html, 'lxml')

        # 判断搜索类型为：线路/站点
        if self.searchType == 'lines':
            lines = []
            stats = []
            all_lines = bsObj.find_all('name')
            all_stats = bsObj.find_all('stats')
            for line in all_lines:
                lines.append(line.get_text())
            for stat in all_stats:
                stats.append(stat.get_text())
            for i in range(len(lines)):
                if self.item in lines[i]:
                    ans = stats[i]
                    break
            return ans
        elif self.searchType == 'stats':
            result_num = bsObj.find('result_num').get_text()
            if result_num == '0':
                print('No value found!')
                return 'fail'
            ans = bsObj.find('xy').get_text()
            return ans
        else:
            pass
