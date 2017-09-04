#!/usr/bin/env python3
# -*-coding: utf-8 -*-
"""
Create on Tue Aug 8 09:22:00 2017

@author: Tristan Song
"""

import codecs
import platform
import time
import random
from communitySearch import Fetcher

def main():
    # 读取所有proxy pool
    proxyLists = []
    with open('./proxyPool.csv', 'r') as f:
        for line in f.readlines():
            line = line.strip().split('://')
            proxyLists.append({line[0]: line[1]})

    # 读取所有User_Agents
    User_Agents = []
    with open('./User_Agents.csv', 'r') as f:
        for line in f.readlines():
            User_Agents.append(line.strip())
    """
    print('Start crawling all URLs...')

    # 获得所有小区的搜索网址
    startTime = time.time()
    with codecs.open('./常州_小区.csv', 'r', 'utf-8') as f1:
        for line in f1.readlines():
            searchItem = line.split(',')[0]
            pNext = 1 # 是否有下一页，1则继续，0则停止
            pageNo = 0
            pageURLs = []
            while pNext:
                pageNo += 1
                user_agent = random.choice(User_Agents)
                proxy = random.choice(proxyLists)
                if platform.system() == 'Darwin':
                    print('Community: %s, page: %d'%(searchItem.encode('utf-8'), pageNo))
                else:
                    print('Community: %s, page: %d'%(searchItem, pageNo))
                page = pageURL(searchItem, pageNo, user_agent, proxy)
                pNext, pageLists = page.pageLists()
                pageURLs.extend(pageLists)
            print('Community search done! Start to write URLs to file...')
            if platform.system() == 'Darwin':
                with open('./pageURLs.csv', 'ab+') as f2:
                    for url in pageURLs:
                        f2.write((url + '\n').encode('utf-8'))
            else:
                with open('./pageURLs.csv', 'a+') as f2:
                    for url in pageURLs:
                        f2.write(url + '\n')
            print('Community URLs writing done!')
        print('All commnity searching done!')
    endTime = time.time()
    print('All URLs crawled! Time Consumption: %.fmin'%float((endTime - startTime)/60))
    """

    #***********************************************************************#
    #********由于网页的不规范，存在小区名为暂无的情况，故边搜边爬********#
    #***********************************************************************#
    # 调用所有网页网址，提取数据并保存
    print('Start parsing all data...')

    startTime = time.time()
    allURLs = []
    failURLs = []
    problemURLs = []
    with codecs.open('./pageURLs.csv', 'r') as f:
        for line in f.readlines():
            allURLs.append(line.strip())
    if platform.system() == 'Darwin':
        file = codecs.open('./results.csv', 'ab+')
    else:
        file = codecs.open('./results.csv', 'a+')
    f = Fetcher(5)
    # 初始所有爬取列表
    for url in allURLs:
        user_agent = random.choice(User_Agents)
        proxy = random.choice(proxyLists)
        f.push((url, user_agent, proxy))
        while f.taskLeft():
            ans = f.get()
            # 成功读取信息
            if ans[0] == 1:
                if platform.system() == 'Darwin':
                    for i in ans[1]:
                        file.write((i+',').encode('utf'))
                    file.write('\n'.encode('utf-8'))
                else:
                    for i in ans[1]:
                        file.write(i+',')
                    file.write('\n')
            # 网页未打开，放入失败列表，后续继续爬取
            elif ans[0] == 0:
                failURLs.append(ans[1])
            # 网页已打开，但没有内容
            else:
                problemURLs.append(ans[1])
    print('爬取失败列表：%d'%len(failURLs))
    print('存在解析列表：%d'%len(problemURLs))
    """
    # 继续爬取失败列表
    while len(failURLs)>50:
        newFail = []
        for url in failURLs:
            f.push((url, user_agent, proxy))
            while f.taskLeft:
                ans = f.get()
                # 成功读取信息
                if ans[0] == 1:
                    if platform.system() == 'Darwin':
                        for i in ans[1]:
                            file.write((i+',').encode('utf'))
                        file.write('\n'.encode('utf-8'))
                    else:
                        for i in ans[1]:
                            file.write(i+',')
                        file.write('\n')
                # 网页未打开，放入失败列表，后续继续爬取
                elif ans[0] == 0:
                    newFail.append(ans[1])
                # 网页已打开，但没有内容
                else:
                    pass
        failURLs = newFail
    """
    file.close()

    endTime = time.time()
    print('All data parsed! Time Consumption: %.fmin'%float((endTime - startTime)/60))

if __name__ == '__main__':
    main()
