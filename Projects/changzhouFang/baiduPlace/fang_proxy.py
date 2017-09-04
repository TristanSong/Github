#!/usr/bin/env python3
# -*-coding: utf-8 -*-
"""
Create on Tue Aug 8 09:22:00 2017

@author: Tristan Song
"""

import time
from baiduPlaceAPI import baiduPlaceAPI
from proxyPool import proxyPool

def main():
    file_dir = './'
    
    # 调用百度地图API，查询小区及GPS坐标
    print('Start downloading commnunity...')
    place = baiduPlaceAPI(query='中学', directory=file_dir)
    place.placeSearch()
    """
    # 爬取可用的proxy
    print('Start downloading proxy pools...')
    ips = proxyPool(directory=file_dir, pageNum=2)
    ips.getProxy()
    """
if __name__ == '__main__':
    main()
