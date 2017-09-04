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
from communitySearch import pageURL, Fetcher

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

    print('Start crawling all URLs...')
    startTime = time.time()
    
    f_community = codecs.open('./常州_小区_1.csv', 'r', 'utf-8')
    if platform.system() == 'Darwin':
        f_results = codecs.open('./results_1.csv', 'ab+')
    else:
        f_results = codecs.open('./results_1.csv', 'a+')
    failURLs = []
    problemURLs = []
    for line in f_community.readlines():
        searchItem = line.split(',')[0]
        pNext = 1 # 是否有下一页，1则继续，0则停止
        pageNo = 0
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
            
            f = Fetcher(10)
            for url in pageLists:
                user_agent = random.choice(User_Agents)
                proxy = random.choice(proxyLists)
                f.push((url, user_agent, proxy))
                while f.taskLeft():
                    ans = f.get()
                    # 成功读取信息
                    if ans[0] == 1:
                        if platform.system() == 'Darwin':
                            f_results.write((searchItem+',').encode('utf-8'))
                            for i in ans[1]:
                                f_results.write((i+',').encode('utf'))
                            f_results.write('\n'.encode('utf-8'))
                        else:
                            f_results.write(searchItem+',')
                            for i in ans[1]:
                                f_results.write(i+',')
                            f_results.write('\n')
                    # 网页未打开，放入失败列表，后续继续爬取
                    elif ans[0] == 0:
                        failURLs.append(ans[1])
                    # 网页已打开，但没有内容
                    else:
                        problemURLs.append(ans[1])
        time.sleep(random.randint(30, 60))
        print('Community: %s writing done!'%searchItem.encode('utf-8'))

    """
    # 继续爬取失败列表
    while len(failURLs)>50:
        newFail = []
        for url in failURLs:
            user_agent = random.choice(User_Agents)
            proxy = random.choice(proxyLists)
            f.push((url, user_agent, proxy))
            while f.taskLeft:
                ans = f.get()
                # 成功读取信息
                if ans[0] == 1:
                    if platform.system() == 'Darwin':
                        f_results.write((searchItem+',').encode('utf-8'))
                        for i in ans[1]:
                            f_results.write((i+',').encode('utf'))
                        f_results.write('\n'.encode('utf-8'))
                    else:
                        f_results.write(searchItem+',')
                        for i in ans[1]:
                            f_results.write(i+',')
                        f_results.write('\n')
                # 网页未打开，放入失败列表，后续继续爬取
                elif ans[0] == 0:
                    newFail.append(ans[1])
                # 网页已打开，但没有内容
                else:
                    pass
        failURLs = newFail
    """
    f_results.close()
    f_community.close()
    
    print('All commnity searching & saving done!')
    endTime = time.time()
    print('All URLs crawled! Time Consumption: %.fmin'%float((endTime - startTime)/60))


if __name__ == '__main__':
    main()
