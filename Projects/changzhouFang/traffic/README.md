BRT
---
trafficAPI：根据已知线路/站点条件下，搜索线路对应的站点或站点对应的GPS坐标

生成文件：
- bus_stations.csv：根据线路搜索对应所有站点
- stats_coord.csv：根据站点搜索所有的坐标

地铁
---

手工从百度地图坐标识别查找，暂时还没找到直接的库调用，幸好只有44站

- metro_1.csv：地铁1号线
- metro_2.csv：地铁2号线
- metro.csv：所有站点