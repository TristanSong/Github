import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

style.use("fivethirtyeight")

web_stats = {"Day": [1, 2, 3, 4, 5, 6],
             "Visitors": [43, 45, 65, 56, 98, 90],
             "Bounce Rate": [42, 35, 65, 67, 56, 89]}

df = pd.DataFrame(web_stats)
df.set_index("Day", inplace=True)

df.plot()
plt.show()
