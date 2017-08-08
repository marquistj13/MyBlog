---
layout: post
title:  TensorFlow之Broadcasting
categories: 深度学习
tag: [Tensorflow]
---

* content
{:toc}


## 理论部分
### 为啥需要broadcast
当具有不同rank（就是总的维数）的array进行运算的时候就需要Broadcasting了。
broadcast的本质：__将低rank的array重复特定次数__，且两个array的原始rank必须能够match
（ _注意：_这个复制，指的是其余维度数据都复制一遍）

### Principles：tf和numpy的不同
尽量避免 implicit and "magical" features，即那些，定义起来简单，但又很多假设，不便于长期维护的机制

因此tf必须 _显示指定broadcast的细节_

### Broadcasting a lower-rank array onto a higher-rank array
首先，标量与array之间的broadcast不需要显示指定

对于低维向高维array broadcast，就需要 __显示指定一个 broadcasting tuple，这个tuple钦定了高维array的哪些维度match到低维array__

举个例子，在tf中，以下操作是不允许的：
```py
|1 2 3| + |7 8 9|
|4 5 6|
```
__除非你钦定一个broadcasting tuple__，实际上这个tuple只能是 `(1)`,这样：
```py
||7 8 9| ==> |7 8 9|
            |7 8 9|
```


另一个case：adding a 3-element vector (dimension (3)) to a 3x3 matrix (dimensions (3,3)). 
按照第1个dimension，就是让这个vector和矩阵的第一个维度 _对齐_，那么就按行复制
```py
|7 8 9| ==> |7 8 9|
            |7 8 9|
            |7 8 9|
```
按照第0 dimension，就是将这个vector和矩阵的行 _对齐_
```py
|7| ==> |7 7 7|
 |8|     |8 8 8|
 |9|     |9 9 9|
```

__如果没法对齐，那么就没法按照该维度进行broadcast__

例如一个`MxNxPxQ`的array，和一个维度为`T`的vector运算，可能有以下组合
```py
          MxNxPxQ

dim 3:          T
dim 2:        T
dim 1:      T
dim 0:    T
```
但要想能够这么算，我们必须得要求T和对应的维度的数字一样（如与P一样）
```py
|7| ==> |7 7 7|
 |8|     |8 8 8|
 |9|     |9 9 9|
```
再换一个例子：To match a TxV matrix onto the MxNxPxQ array,我们必须制定两个 __对齐维度__
```py
          MxNxPxQ
dim 2,3:      T V
dim 1,2:    T V
dim 0,3:  T     V
etc...
```


### Broadcasting similar-rank arrays with degenerate dimensions （就是某一个dimension为1）
说清楚一点就是：broadcasting two arrays that have the same rank but different dimension sizes. 
这时候就和numpy很相似了，就得要求两个array是compatible
>Two arrays are compatible when all their dimensions are compatible. Two dimensions are compatible if:
1. They are equal, or
1. One of them is 1 (a "degenerate" dimension)

例如：
>(2,1) and (2,3) broadcast to (2,3).
(1,2,5) and (7,2,5) broadcast to (7,2,5)
(7,2,5) and (7,1,5) broadcast to (7,2,5)
(7,2,5) and (7,2,6) are incompatible and cannot be broadcast.


当然，(2,1) and (1,3) broadcast to (2,3). 

### Broadcast composition
就是以上两种broadcast的复合。
例如：
```py
|1 2 3 4| + [5 6]    // [5 6] is a 1x2 matrix, not a vector.
```
一个为4，一个为1x2,一个是一维的，一个是两维的，这时候broadcasting tuple只能是(0),即，将4变成4xM,很明显，M为2：
```py
|1 1| + [5 6]
|2 2|
|3 3|
|4 4|
```
然后再进行"degenerate dimension broadcasting" ，将1x2变成4x2:
```py
|1 1| + |5 6|     |6  7|
|2 2| + |5 6|  =  |7  8|
|3 3| + |5 6|     |8  9|
|4 4| + |5 6|     |9 10|
```

## 应用部分
我也不知道那个所谓的 broadcasting tuple在哪个函数指定，下面就介绍一个比较偏向degenerate dimensions的例子吧。

对于kmeans问题，假设我有10个二维数据，即 `x` 为 `10x2`, 要聚成三个cluster，在聚类过程中，我们要根据初始化或计算出来的三个center来确定哪些点应该属于哪一个cluster，好了三个center记为 `c`,维度为`3x2`

一种方法就是 [此页面](https://learningtensorflow.com/lesson6/)的例子：
```py
def assign_to_nearest(samples, centroids):
    # Finds the nearest centroid for each sample

    # START from http://esciencegroup.com/2016/01/05/an-encounter-with-googles-tensorflow/
    expanded_vectors = tf.expand_dims(samples, 0)
    expanded_centroids = tf.expand_dims(centroids, 1)
    distances = tf.reduce_sum( tf.square(
               tf.subtract(expanded_vectors, expanded_centroids)), 2)
    mins = tf.argmin(distances, 0)
    # END from http://esciencegroup.com/2016/01/05/an-encounter-with-googles-tensorflow/
    nearest_indices = mins
    return nearest_indices
```

怎么理解呢？为啥要将`10x2`的`x`经过`tf.expand_dims`变成`1x10x2`,`3x2`的`c`变成`3x1x2`？反过来可以么？我们一步步来解释。

### 维度扩展部分
先看需求。
为了找出一个点聚类哪个center更近，我们肯定得算出这个点到所有center的距离，说到这，我们就要联想到broadcast的本质：__将低rank的array重复特定次数__。
根据上面这个需求，这些点得复制三次，同时，每一个center得重复10次

__在理解这些“重复”或“复制”的过程中一定要谨记以下两点：__
1. `10x2`扩展维度变成`1x10x2`之后，数据量不变，即还是20个数值，我们在其shape中加1，其实总的数字数目不变
2. 在某一个dimension为1的dimension处复制该array的时候，其余所有dimension的数据都要复制一遍，也就是说，该array的所有数字都要复制一遍

太空洞了，举例说话：

```py
import tensorflow as tf
import numpy as np
sess = tf.Session()
x=tf.constant(np.ones((10,2)))
sess.run(x)
c=tf.constant(np.array([[0,0],[1,0],[0,0]],dtype=float))
sess.run(c)
```

可以看到x和c分别为：
```py
array([[ 1.,  1.],
       [ 1.,  1.],
       [ 1.,  1.],
       [ 1.,  1.],
       [ 1.,  1.],
       [ 1.,  1.],
       [ 1.,  1.],
       [ 1.,  1.],
       [ 1.,  1.],
       [ 1.,  1.]])
和
array([[ 0.,  0.],
       [ 1.,  0.],
       [ 0.,  0.]])
```
经过维度扩展之后为:
```py
x_e=tf.expand_dims(x,dim=0)
sess.run(x_e)
c_e=tf.expand_dims(c,dim=1)
sess.run(c_e)
array([[[ 1.,  1.],
        [ 1.,  1.],
        [ 1.,  1.],
        [ 1.,  1.],
        [ 1.,  1.],
        [ 1.,  1.],
        [ 1.,  1.],
        [ 1.,  1.],
        [ 1.,  1.],
        [ 1.,  1.]]])
和
array([[[ 0.,  0.]],

       [[ 1.,  0.]],

       [[ 0.,  0.]]])
```
其shape为：
```py
print(x_e.shape)
print(c_e.shape)
(1, 10, 2)
(3, 1, 2)
```
二者进行运算的时候就会有broadcast，即都变成`(3x10x2)`
我们可以从其运算结果验证这俩array（tf里叫做tensor）是如何在相应dimension进行复制的：
```py
sess.run(tf.subtract(x_e,c_e))
array([[[ 1.,  1.],
        [ 1.,  1.],
        [ 1.,  1.],
        [ 1.,  1.],
        [ 1.,  1.],
        [ 1.,  1.],
        [ 1.,  1.],
        [ 1.,  1.],
        [ 1.,  1.],
        [ 1.,  1.]],

       [[ 0.,  1.],
        [ 0.,  1.],
        [ 0.,  1.],
        [ 0.,  1.],
        [ 0.,  1.],
        [ 0.,  1.],
        [ 0.,  1.],
        [ 0.,  1.],
        [ 0.,  1.],
        [ 0.,  1.]],

       [[ 1.,  1.],
        [ 1.,  1.],
        [ 1.,  1.],
        [ 1.,  1.],
        [ 1.,  1.],
        [ 1.,  1.],
        [ 1.,  1.],
        [ 1.,  1.],
        [ 1.,  1.],
        [ 1.,  1.]]])
```
很明显，对于x，从`10x2`扩展维度变到`1x10x2`,然后复制成`3x10x2`,我们可以根据以上结果看出来，是这么复制的，即`10x2`的数据复制三遍，
同理，对于center，即c，从`3x1x2`复制成`3x10x2`,其实就是将每一个center点复制10遍，要仔细体会。

### argmin部分
我们看一下原问题的
```py
distances = tf.reduce_sum( tf.square(
               tf.subtract(expanded_vectors, expanded_centroids)), 2)
mins = tf.argmin(distances, 0)
```
部分。
翻译成我们上面的具体数值例子就是：
```py
t0=tf.subtract(tf.expand_dims(x,dim=0),tf.expand_dims(c,dim=1))
s0=tf.reduce_sum(tf.square(t0),2)
sess.run(s0)
array([[ 2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.],
       [ 1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.],
       [ 2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.]])
```
然后
```py
sess.run(tf.argmin(s0,0))
array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=int64)
```

很容易理解，`s0=tf.reduce_sum(tf.square(t0),2)`,就是按照第2个dimension求和，该dimension就没了，argmin也是同理。

### 反过来扩展维度也是可以的
即：
```py
t1=tf.subtract(tf.expand_dims(x,dim=1),tf.expand_dims(c,dim=0))
s1=tf.reduce_sum(tf.square(t1),2)
sess.run(s1)
array([[ 2.,  1.,  2.],
       [ 2.,  1.,  2.],
       [ 2.,  1.,  2.],
       [ 2.,  1.,  2.],
       [ 2.,  1.,  2.],
       [ 2.,  1.,  2.],
       [ 2.,  1.,  2.],
       [ 2.,  1.,  2.],
       [ 2.,  1.,  2.],
       [ 2.,  1.,  2.]])
sess.run(tf.argmin(s1,1))
array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=int64)
```
结果是一样的。
即，每一个数复制三遍，从`10x1x2`变到`10x3x2`
每一个center点复制10遍，即从`1x3x2`到`10x3x2`
