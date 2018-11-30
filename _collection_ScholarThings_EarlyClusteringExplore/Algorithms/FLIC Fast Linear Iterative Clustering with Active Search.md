--- 
title:  FLIC Fast Linear Iterative Clustering with Active Search
date:   2017-03-8
---



* content
{:toc}

## Meta
作者Ming-Ming Cheng貌似很牛啊，在paper上有 [个人主页](http://mmcheng.net/cmm/)，在这里发现了Valse这个很强大的组织，不过貌似程老师自己也维持了一个界面（貌似不更新了，还是直接搜 valse吧），我找到了 [专题侠客群论剑-20151223](http://valse.mmcheng.net/p20151223/) 这个界面。里边有两位搞聚类的牛人的paper介绍视频，其中cmu的 [禹之鼎](http://www.contrib.andrew.cmu.edu/~yzhiding/publications.htm)介绍的是cvpr14的一篇文章Transitive Distance Clustering with K-Means Duality （这篇文章用了 [BSDS300](https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/) 这个图像分割的数据集）及其后续AAAI16： On Order-Constrained Transitive Distance Clustering 很值得看啊。
好了，看一下本文吧。
首先，定一下领域，本文关心的算法用于生成图像的Superpixels，即作为over-segmentation tools。
基于Simple Linear Iterative Clustering (SLIC) 。

得到superpixel之后就可以做image segmentation了。


我感觉这篇文章不用细看了……

## intro
先不细看了。

## Preliminaries
就是介绍SLIC了（这一部分可作为小的积累性知识。）

本文算法的不同之处在于active search。

SLIC-based algorithms的特点：
>each search region is fixed in the assignment step of a single loop, and the region continuity information of neighboring pixels is largely ignored when allocating pixels to superpixels. Separately performing the assignment step and the update step also leads to a delayed feedback of pixel label change.







