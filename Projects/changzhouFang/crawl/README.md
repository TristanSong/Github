crawl_1.py
---

为第一版本，先爬取所有二手房源的地址，以便统一爬取具体信息，后弃之。

生成文件：
- pageURLs.csv(后期已删除)

crawl_2.py
---

调用communitySearch.py,  myThread.py通过多线程直接爬取信息

**需从baiduPlace文件夹下拷贝常州_小区.csv至当前目录，后期发现使用代理IP仍出现验证码问题，期间为了避免出现问题，采用每次爬取几个小区方式（故目录内存在常州_小区_0.csv，results_1.csv临时文件），最终使用模拟人工点击网页方式爬虫**

生成文件：
- results.csv