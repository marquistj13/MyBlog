---
title:  绘图常用参考函数
---


* content
{:toc}


### 散点图
这个模板很好，稍事修改即可。
```py
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

%matplotlib inline
def ScatterPlot(X, Y, assignments=None, centers=None):
  if assignments is None:
    assignments = [0] * len(X)
  fig = plt.figure(figsize=(14,8))
  cmap = ListedColormap(['red', 'green', 'blue', 'magenta'])
  plt.scatter(X, Y, c=assignments, cmap=cmap)
  if centers is not None:
    plt.scatter(centers[:, 0], centers[:, 1], c=range(len(centers)), 
                marker='+', s=400, cmap=cmap)  
  plt.xlabel('Height (in)')
  plt.ylabel('Weight (lbs)')
  plt.show()
```

这样可以在聚类前和聚类后都能用这个函数画图了，`assignment` 就是类标。
