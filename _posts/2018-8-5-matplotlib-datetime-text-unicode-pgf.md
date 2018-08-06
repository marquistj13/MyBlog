---
layout: post
title:  matplotlib 技巧之 使用 unicode 以及 保存为pgf时使用datetime
categories: [编辑器等文档工具]
tag: [Python,Matplotlib]
---

* content
{:toc}

## 序言

## 使用 datetime
在 [Date tick labels](https://matplotlib.org/gallery/text_labels_and_annotations/date.html) 中介绍了如何使用 python 的 datetime.datetime 对象作为 xaxis 的  tick locators and formatters。

由于历史原因，matplotlib 会首先将datetime转换为距离 `0001-01-01 00:00:00 UTC` 的天数 plus one day，比较坑的是，如果我没理解错的话，将 datetime.datetime 对象 作为tick locating and formatting 的时候，matplotlib 会自动给我们转换，但是其他时候我们必须得手动使用matplotlib.dates.date2num and matplotlib.dates.num2date进行转换，要不然就可能出现莫名其妙的错误。

对于如下例子：
```python
# -*- coding: utf-8 -*-
import matplotlib as mpl
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.font_manager import FontProperties
x_date_string= np.array(['2007/1/1', '2007/1/2', '2007/1/3', '2007/1/4', '2007/1/5'])
x=map(lambda x_in:dt.datetime.strptime(x_in, "%Y/%m/%d"),x_date_string)
np.random.seed(0)
y=np.random.random_sample(5)
fig, ax = plt.subplots(figsize=(8,5))
# plot figure
ax.plot(x, y, '.-', markersize= 8)
# set Locator
dayLoc = mdates.DayLocator(interval=1) # every day
ax.xaxis.set_major_locator(dayLoc)
dayFmt = mdates.DateFormatter('%y/%m/%d')
ax.xaxis.set_major_formatter(dayFmt)
# add text
#ax.text(mdates.date2num(dt.datetime.strptime("2007/1/1", "%Y/%m/%d")), 0.5, u"哈哈", fontproperties = FontProperties('SimHei',  size= 'xx-large'))
ax.text(dt.datetime.strptime("2007/1/1", "%Y/%m/%d"), 0.5, u"哈哈", fontproperties = FontProperties('SimHei',  size= 'xx-large'))
ax.set_xlabel(u"€, ü", fontsize = 20)
fig.autofmt_xdate()
plt.savefig("pgf_test.pdf")
plt.savefig("pgf_test.pgf")
```
此时，默认使用的是 Qt5Agg backend，因此，此时可以生成 pdf，但无法生成 pgf。

回忆一下上面我们提到，除了tick相关的datetime会自动转换为matplotlib的距离，其他的都需要我们自己转换，此时，只要将上述代码的 `dt.datetime.strptime("2007/1/1", "%Y/%m/%d")` 变为： `mdates.date2num(dt.datetime.strptime("2007/1/1", "%Y/%m/%d"))` 即可。

## 使用Unicode
在上述例子中，汉字等Unicode的显示通过设置 `fontproperties = FontProperties('SimHei',  size= 'xx-large')` 来实现。

## pgf 的使用
在生成的pgf文件的头部，说明了如何将此pgf文件嵌入latex文档，即要么直接`\input{<filename>.pgf}`(和主文档在同一个目录)，
或者 （主文档和pgf文档不在一个目录的时候）`\usepackage{import}`  然后 `\import{<path to file>}{<filename>.pgf}`。

在 [Typesetting With XeLaTeX/LuaLaTeX](https://matplotlib.org/users/pgf.html) 介绍了如何将Matplotlib的backend调成pgf backend，即：
```python
import matplotlib as mpl
mpl.use("pgf")
```
还可以指定其preamble：
```python
pgf_with_custom_preamble = {
    "font.family": "serif", # use serif/main font for text elements
    "text.usetex": True,    # use inline math for ticks
    "pgf.rcfonts": False,   # don't setup fonts from rc parameters
    "pgf.preamble": [
         "\\usepackage{units}",         # load additional packages
         "\\usepackage{metalogo}",
         "\\usepackage{unicode-math}",  # unicode math setup
         r"\setmathfont{xits-math.otf}",
         r"\setmainfont{DejaVu Serif}", # serif font via preamble
         ]
}
```
这些preamble还应该加到你的tex文件中，且只能用xelatex编译你的tex了。

__注意：__ 上述链接中说了，在pgf backend时，`plt.savefig('figure.pdf')` 生成的pdf是编译得到的，且默认是matplotlib使用 `xelatex` 编译生成pdf的（当然你的系统里应该装了texlive等tex环境才能这么用）。
因此，如果用默认的Qt5Agg backend生成的pdf插入tex文件，用xelatex编译时，可能会提示broken pdf file，此时只能用pdflatex编译你的tex文件；
而我们用 pgf backend 编译生成的pdf由于是用xelatex编译生成的，因此将其插入tex文件时，该tex文件是可以使用xelatex编译的。


虽然可以将pgf文件直接插入到tex中，但我还是倾向于将图片存为pdf文件，再插入tex。
（使用pgf时可能会有各种preamble的问题，且肯定会影响速度）

## datetime的细节
在本页最上面的代码中，
将 `'2007/1/1'` 字符串转换为 datetime.datetime 对象是通过 `dt.datetime.strptime('2007/1/1', "%Y/%m/%d")` 实现的。注意由于 `'2007/1/1'` 中有斜杠，因此 `"%Y/%m/%d"` 也得有。

另外，locator 的设置也值得借鉴：
```python
# set Locator
dayLoc = mdates.DayLocator(interval=1) # every day
ax.xaxis.set_major_locator(dayLoc)
dayFmt = mdates.DateFormatter('%y/%m/%d')
ax.xaxis.set_major_formatter(dayFmt)
```

