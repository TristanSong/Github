#/usr/bin/env python3
# -*-coding:utf-8 -*-

import pandas as pd
import datetime
from pandas_datareader import data, wb
import matplotlib.pyplot as plt
from matplotlib import style

style.use("fivethirtyeight")

start = datetime.datetime(2017, 1, 1)
end = datetime.datetime(2017, 3, 28)

df = data.DataReader("XOM", "yahoo", start ,end)

df["High"].plot()
plt.show()

