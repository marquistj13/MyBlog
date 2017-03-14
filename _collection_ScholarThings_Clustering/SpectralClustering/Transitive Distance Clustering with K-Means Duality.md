--- 
title: Transitive Distance Clustering with K-Means Duality
date:   2017-03-14
---



* content
{:toc}

## Meta
一篇CVPR14，作者在valse的演讲视频在[专题侠客群论剑-20151223](http://valse.mmcheng.net/p20151223/) 。
我是看了视频之后再看论文的，只看论文的话貌似有点摸不着头脑。

作者在视频中隐晦地提到，选坑很重要，作者用Transitive Distance也是有贵人相助，看来机遇很重要，啊。

这篇文章基于二作的一篇07年的文章 [Clustering with Transitive Distance and K-Means Duality](https://arxiv.org/abs/0711.3594),即transitive distance和k-means duality这个概念的运用。本文即可认为是这篇文章的拓展（其实看摘要蛮像的，这两篇文章有很高的重复率）。

我发现谱聚类的效果挺好的，此坑可入啊。
由这篇文章发现的两个可看的东西：
1. On Spectral Clustering: Analysis and an algorithm
2. 一篇博客：[谱聚类算法概述](https://www.zybuluo.com/hainingwyx/note/593818)

## Abstract
首先，硬扯上spectral clustering，降低了复杂度。
目前对谱聚类不太了解，难道只要用上graph就算谱聚类？

算法特点：用上了一个_Transitive Distance_，还有其 _k-means duality_ 特性。

## Introduction
指导聚类算法design的一个根本原则
>__Consistency__. Data within the same cluster are close to each other, while data in different clusters are relatively far away

层次聚类(the hierarchy approach)是bottom-up的，因此完全取决于local data structure，很容易出现multi-scale clusters的error。

k-means and EM 假设的数据分布太简单了（Euclidean / Mahananobis distances）因此无法hold 住data with manifold or irregularly shaped clusters

谱聚类很好啊，但eigendecompostion的复杂度太高 $O(n^3)$. 因此得解决scalability
problem。

本文的算法规避了eigendecomposition ，因此降到了$O(n^2)$
此算法的 __philosophy__ 和 _Kernel k-means: spectral clustering and normalized cuts（where spectral clustering is unified to the kernel k-means framework）_ 一样，但上面这篇文章还得解eigenproblem。

本文的贡献是三点： efficiency，straightforwardness，flexibility。
flexibility就是易扩展，efficiency就是运算复杂度低了。
straightforwardness不太好理解，就是规避了discrete-to-continuous relaxations这么一个步骤。

## 文章内容
transitive distance的概念古已有之
![](TransitiveDistanceClustering\定义.png)
很明显，它定义在另外一个距离 $d(.,.)$ 之上，这个 $d(.,.)$ 可以是欧氏距离，也可以是卡方距离（6.4节的图像分割用的用到了）。

有人证明了transitive distance是一种ultrametric，然后本文搞出一个Theorem 1（证明在附录A）
![](TransitiveDistanceClustering\定理1.png)

这个定理的underlying intuition很简单，就是在影射后的新空间 $V'$ ，可以直接用Kmeans，即比原空间 $V$ 的聚类更容易。
即我们得到了一个具有良好特性的 kernel mapping。

但问题来了，正如通常的kernel trick，这个影射之后啊，咱只有点与点之间在新空间的距离（即距离矩阵），没有其绝对坐标啦，这还咋玩儿。
（啊，用kernel kmeans的套路不行么？）

作者用k-means duality特性来解决此问题。
即直接将距离矩阵的行进行距离即可（看视频是这么说的，论文的这一部分没有看懂啊）

第五节试算法描述部分要构造一个minimum spanning tree。

## 实验部分
好多奇形怪状的形状，还有 Iris and Ionosphere datasets。

对于Image segmentation，先搞superpixel（用G. Mori. Guiding Model Search Using Segmentation. ICCV, 2005.的方法），用 $\chi^2$ distance.
