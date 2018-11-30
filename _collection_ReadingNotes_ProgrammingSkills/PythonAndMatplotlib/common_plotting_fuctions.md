---
title:  绘图常用参考函数
date:   2017-11-1
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

### contour 图
代码来源：http://gluon.mxnet.io/chapter02_supervised-learning/perceptron.html
```python
# plot contour plots on a [-3,3] x [-3,3] grid
def plotscore(w,d):
    xgrid = np.arange(-3, 3, 0.02)
    ygrid = np.arange(-3, 3, 0.02)
    xx, yy = np.meshgrid(xgrid, ygrid)
    zz = nd.zeros(shape=(xgrid.size, ygrid.size, 2))
    zz[:,:,0] = nd.array(xx)
    zz[:,:,1] = nd.array(yy)
    vv = nd.dot(zz,w) + b
    CS = plt.contour(xgrid,ygrid,vv.asnumpy())
    plt.clabel(CS, inline=1, fontsize=10)
```

理解这个函数的关键有两个
* `np.meshgrid` 的输出
* zz为什么要扩展维度。

关键是 `np.meshgrid` 的输出，它有两种index的方法 `Cartesian (‘xy’, default) or matrix (‘ij’) indexing `
默认是笛卡尔的，即对于输入` x1, x2,..., ‘xn’`,输出的shape为：`(N1, N2, N3,...Nn)`,好了铺垫到此结束，举个例子(这个例子从 [numpy.meshgrid](https://docs.scipy.org/doc/numpy/reference/generated/numpy.meshgrid.html)改编。)：
```python
import numpy as np
x = np.arange(-5, 5, 0.1)
y = np.arange(-5, 5, 0.2)
xx, yy = np.meshgrid(x, y)
print(x.shape,y.shape)
print(xx.shape,yy.shape)
(100,) (50,)
(50, 100) (50, 100)
```
官网说了，
>`meshgrid` is very useful to evaluate functions on a grid.

即，可以这么玩：
```python
import matplotlib.pyplot as plt
zz = np.sin(xx**2 + yy**2) / (xx**2 + yy**2)
h = plt.contourf(xx,yy,zz)
plt.show()
```

好了，回到咱们上面的contour 图的例子，为什么要先对xx和yy增维度呢？

再看一个例子：

```python
x = np.arange(-5, 5, 1)
y = np.arange(-5, 5, 2)
xx, yy = np.meshgrid(x, y)
print(x.shape,y.shape)
print(xx.shape,yy.shape)
(10,) (5,)
(5, 10) (5, 10)

print(xx,'\n',yy)

[[-5 -4 -3 -2 -1  0  1  2  3  4]
 [-5 -4 -3 -2 -1  0  1  2  3  4]
 [-5 -4 -3 -2 -1  0  1  2  3  4]
 [-5 -4 -3 -2 -1  0  1  2  3  4]
 [-5 -4 -3 -2 -1  0  1  2  3  4]] 
 [[-5 -5 -5 -5 -5 -5 -5 -5 -5 -5]
 [-3 -3 -3 -3 -3 -3 -3 -3 -3 -3]
 [-1 -1 -1 -1 -1 -1 -1 -1 -1 -1]
 [ 1  1  1  1  1  1  1  1  1  1]
 [ 3  3  3  3  3  3  3  3  3  3]]

zz = np.zeros(shape=(y.size, x.size, 2))
zz[:,:,0] = xx
zz[:,:,1] = yy
print(zz.shape)
print(zz)

(5, 10, 2)
[[[-5. -5.]
  [-4. -5.]
  [-3. -5.]
  [-2. -5.]
  [-1. -5.]
  [ 0. -5.]
  [ 1. -5.]
  [ 2. -5.]
  [ 3. -5.]
  [ 4. -5.]]

 [[-5. -3.]
  [-4. -3.]
  [-3. -3.]
  [-2. -3.]
  [-1. -3.]
  [ 0. -3.]
  [ 1. -3.]
  [ 2. -3.]
  [ 3. -3.]
  [ 4. -3.]]

 [[-5. -1.]
  [-4. -1.]
  [-3. -1.]
  [-2. -1.]
  [-1. -1.]
  [ 0. -1.]
  [ 1. -1.]
  [ 2. -1.]
  [ 3. -1.]
  [ 4. -1.]]

 [[-5.  1.]
  [-4.  1.]
  [-3.  1.]
  [-2.  1.]
  [-1.  1.]
  [ 0.  1.]
  [ 1.  1.]
  [ 2.  1.]
  [ 3.  1.]
  [ 4.  1.]]

 [[-5.  3.]
  [-4.  3.]
  [-3.  3.]
  [-2.  3.]
  [-1.  3.]
  [ 0.  3.]
  [ 1.  3.]
  [ 2.  3.]
  [ 3.  3.]
  [ 4.  3.]]]
```
一目了然啊
