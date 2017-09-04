#!/usr/bin/env python3
# -*-coding: utf-8 -*-
"""
Created on Tue Aug 8 11:09:00 2017

@author: TristanSong
"""
import urllib.request
from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import socket
import os
import platform

class proxyPool(object):
    def __init__(self, directory, pageNum=1):
        self.directory = directory
        self.pageNum = pageNum

    def checkDirectory(self):
        # If directory not exists, create it.
        if not os.path.exists(self.directory):
            print(self.directory + 'does not exist, will be created.')
            os.makedirs(self.directory)
        fileName = self.directory + 'proxyPool' + '.csv'
        if os.path.exists(fileName):
            print(fileName + ' already exists, will be cleared for storing.')
            with open(fileName, 'w') as f:
                f.close()
        return fileName

    def checkProxy(self, ip_temp):
        socket.setdefaulttimeout(3)
        url =  'http://ip.chinaz.com/getip.aspx'
        proxy_support = urllib.request.ProxyHandler(ip_temp)
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        try:
            html = urlopen(url)
            if html:
                return True
            else:
                return False
        except Exception as e:
            return False

    def getProxy(self):
        fileName = self.checkDirectory()
        User_Agent = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
        header = {}
        header['User-Agent'] = User_Agent
        baseURL = 'http://www.xicidaili.com/nn/'
        for page in range(1, self.pageNum+1):
            print('downloading page %d...'%page)
            url = baseURL + str(page)
            req = Request(url, headers=header)
            html = urlopen(req)
            bsObj = BeautifulSoup(html, 'html.parser')
        
            ips = bsObj.findAll('tr')
            for i in range(1, len(ips)):
                ip = ips[i]
                tds = ip.findAll('td')
                ip_temp = {}
                ip_temp['addr'] = tds[1].contents[0]
                ip_temp['port'] = tds[2].contents[0]
                ip_temp['type'] = tds[5].contents[0]

                proxy_host = {ip_temp['type']: ip_temp['type'] + '://' + ip_temp['addr'] + ':' + ip_temp['port']}
                if self.checkProxy(proxy_host):
                    if platform.system() == 'Darwin':
                        with open(fileName, 'ab+') as f:
                            f.write((proxy_host[ip_temp['type']] + '\n').encode('utf-8'))
                    else:
                        with open(fileName, 'a+') as f:
                            f.write(proxy_host[ip_temp['type']] + '\n')
        print('Downloading complete!')
