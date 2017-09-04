SPC.py
---

第一版本，主要使用tkinter, matplotlib，从NOVA-5kg等子文件夹中读取txt文件，提取其中数值，将结果保存至**_resutls.txt文件，然后显示在matplotlib中，并不完美。

SPC_html.py
---

读取根目录下的txt文件，提取其中结果，并将结果根据‘容量-机床’保存至相应数据库内，灵活性较高。

SPC文件夹
---

读取SPC_html.py保存至数据库的结果，使用echarts显示在html网页中。

**所有生成的exe可执行文件已删除，windows下可使用pyinstaller生成程序。**