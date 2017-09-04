#!/usr/bin/env python3
# -*-coding: utf-8 -*-
"""
Created on Tue Aug 8 09:53:00 2017

@author: Tristan Song
"""

from threading import Thread, Lock
from queue import Queue
import urllib.request
from urllib.parse import quote
from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import platform
import random


# 读取搜索页面的所有房源网址并返回，通过是否有下一页确定是否继续
class pageURL(object):
    def __init__(self, searchItem, pageNo, user_agent, proxy):
        self.searchItem = searchItem
        self.pageNo = pageNo
        self.user_agent = user_agent
        self.proxy = proxy

    def pageLists(self):
        # 安居客房源，按照最新排序
        baseURL = 'https://cz.anjuke.com/sale/o5-p'
        url = baseURL + str(self.pageNo) + 'rd1/?kw=' + quote(self.searchItem, encoding='utf-8') + '#filtersort'
        header = {}
        header['User-Agent'] = self.user_agent
        proxy_support = urllib.request.ProxyHandler(self.proxy)
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        req = Request(url, headers=header)
        # 网站编码不统一，charset标明utf-8，但使用decode('utf-8')总是出现无法解码情况
        html = urlopen(req).read()
        bsObj = BeautifulSoup(html, 'lxml')
        pageLists = []
        items = bsObj.find_all('li', class_='list-item')
        for item in items:
            page = item.find('a', class_='houseListTitle')
            pageLists.append(page['href'])
        # 查看是否还有下一页
        pNext = bsObj.find('a', class_='aNxt')
        try:
            pNext['href']
            return 1, pageLists
        except TypeError as e:
            print('Search end! No more pages')
            return 0, pageLists


class Fetcher:
    def __init__(self, threads):
        self.lock = Lock()
        self.q_req = Queue()
        self.q_ans = Queue()
        self.threads = threads
        for i in range(self.threads):
            t = Thread(target=self.threadGet)
            t.setDaemon(True)
            t.start()
        self.running = 0

    def __del__(self):
        self.q_req.join()
        self.q_ans.join()

    def taskLeft(self):
        return self.q_req.qsize() + self.q_ans.qsize() + self.running

    def push(self, req):
        return self.q_req.put(req)

    def get(self):
        return self.q_ans.get()

    def threadGet(self):
        while True:
            req = self.q_req.get()
            url = req[0]
            user_agent = req[1]
            proxy = req[2]
            header = {}
            header['User-Agent'] = user_agent
            proxy_support = urllib.request.ProxyHandler(proxy)
            opener = urllib.request.build_opener(proxy_support)
            urllib.request.install_opener(opener)
            #time.sleep(random.uniform(2,5))
            req = Request(url, headers=header)
            with self.lock:
                self.running += 1
            try:
                # 3 types
                # 0: url not opened, will be put into fail lists
                # 1: url parsed, success
                # 2: url opened but no data
                html = urlopen(req).read()
                ans = self.urlParse(html)
                if ans == 'fail':
                    print("'%s' opened, but some parse problem!"%url)
                    ans = (2, url)
            except urllib.error.HTTPError as e:
                print("'%s' not opened, will be parsed later!"%url)
                ans = (0, url)
            self.q_ans.put(ans)
            with self.lock:
                self.running -= 1
            self.q_req.task_done()

    def urlParse(self, html):
        bsObj = BeautifulSoup(html, 'lxml')
        try:
            # 获取房源简要信息：总价、户型、面积
            basicInfo = re.findall("(\d+)[\u4e00-\u9fa5]", bsObj.find('div', class_='basic-info clearfix').get_text())
            price = basicInfo[0]
            livingRoom = basicInfo[1]
            sittingRoom = basicInfo[2]
            area = basicInfo[3]
            
            # 获取房源详细信息：年代、朝向、楼层、装修、首付、中介
            houseInfo_1 = bsObj.find('div', class_='first-col detail-col').get_text().split('\uff1a')
            community = houseInfo_1[1].split()[0]
            buildYear = houseInfo_1[3].split()[0]
            houseInfo_2 = bsObj.find('div', class_='second-col detail-col').get_text().split()
            direction = houseInfo_2[-2].split('\uff1a')[-1]
            floor = houseInfo_2[-1].split('\uff1a')[-1]
            # 楼层, 存在高、中、低，或者没有
            floor_1 = re.findall("(\u9ad8|\u4e2d|\u4f4e)", floor)
            if floor_1 == []:
                floor_1 = '无'
            else:
                floor_1 = floor_1[0]
            floor_2 = re.findall("(\d+)", floor)[0]
            houseInfo_3 = bsObj.find('div', class_='third-col detail-col').get_text().split()
            decoration = houseInfo_3[0].split('\uff1a')[-1]
            downPay = re.findall("([0-9\.]+)", houseInfo_3[-2])[0]
            # 中介公司没有
            broker = bsObj.find('div', class_='broker-company').get_text().split()
            if len(broker) > 1:
                company = broker[0].split('\uff1a')[1]
            else:
                company = broker[0]
            ans = (1, [community, price, livingRoom, sittingRoom, area, buildYear, direction, floor_1, floor_2, decoration, downPay, company])
            return ans
        except AttributeError as e:
            return 'fail'
