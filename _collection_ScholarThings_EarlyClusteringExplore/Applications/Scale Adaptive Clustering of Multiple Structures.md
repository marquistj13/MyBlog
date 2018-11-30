--- 
title: Scale Adaptive Clustering of Multiple Structures
date:   2017-10-31
---


* content
{:toc}

## 前言
对于一个noisy dataset，如何才能分割成 Multiple Inlier Structures 呢？
这就需要我们先定义好优化问题，然后再搞一个Robust Estimator。

可惜，由于我对cv圈的基本套路不很熟悉，这篇文章只能看个大概。
很多_经验性的步骤啊_，不得要领。

## intro
作者声称，CNN在identify 复杂pattern的时候，只能给出qualitative categorizations instead of parameterizations of the models. 即给出模型的定性分类，而非参数化？
训练时间长，要求数据多，因此采用老的方法。

本文的算法和RANSAC很像。

作者提出的估计器有三个步骤：
scale estimation, mean shift based structure recovery, and strength based inlier classification. 

卖点是只需要指定很少的参数。


还有一个领域相关的东西：这个问题的解决都需要很多trial，本文算法的唯一参数就是随机采样的trial的次数

## STRUCTURE INITIALIZATION
根据经验性的intuition进行堆积木

首先是Carrier Vectors的概念，其实就是第一个intuition了：
>CV中的非线性目标函数可以transform成高维中的linear relation。

用熟悉的话就是，这些输入特征互相乘一下就行了，一个例子就是 $x=\left[x,  y,  x^\prime , y^\prime,  x x^\prime ,  x y^\prime ,  y x^\prime,   y y^\prime \right]^\top$

那么The linearized function of the carriers is
$x_{i}^\top \theta - \alpha \simeq 0 ~~~ i = 1,\ldots,n_{in}$

其中这个截距 $\alpha$ 需要估计出来。

然后是Carrier Vector协方差矩阵的一阶逼近，即Jacobian matrix，不知道干啥的哈哈。


最后是Mahalanobis Distances，也是各种经验性的东西，不知道干啥。


## ESTIMATION OF MULTIPLE STRUCTURES
### 首先是scale 的估计，即Mahalanobis Distances的 $\hat\sigma$
一大坨的经验性的东西，不想看。
结果就是公式13了：
$\hat\sigma = \max_{\eta=\epsilon,\ldots,\eta_t}  k_{t_\eta}$

### Mean Shift Based Structure Recovery
这一步的Mean Shift也没看懂，目测就是将截距给搞一搞，即对于每一次trial，所有点通过Carrier Vector之后变成一个标量截距，然后将这些截距聚类，得到截距空间的mode
这就是截距的估计了吧。

### Strength Based Classification
就是定义一个指标
$s = \frac{n_{in}}{\hat \sigma^{tls}}.$
来表征structure的线性空间的density，你的density大，就能首先检测出来。

## 最后的算法就是3.6节的算法框图。
暂时不想细究了。
