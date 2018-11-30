--- 
title:  Multilevel Clustering viaWasserstein Means
date:   2017-11-2
---



* content
{:toc}

## 前述
本文偏统计

## 摘要
multilevel clustering的概念：
simultaneously partition data in each group and discover grouping patterns among groups in a potentially large hierarchically structured corpus of data.

## intro
很多data存在multilevel structure。
例如可以将word组成document，document又可以组成corpora

我们可能既对partitioning the data in each group (to obtain local clusters) and partitioning a collection of data groups (to obtain global clusters).

层级聚类得到的tree-structed clustering并不能用于discovering the nested structure of multilevel data.


本文从纯优化的角度来搞。we shall take a purely optimization approach.
怪不得我看不懂啊。

如果要同时用K-means clustering在global level (among groups), and local level (within each group),进行聚类，那么可以通过将Wasserstein distances的概念加到目标函数中，然后再搞这个joint optimization problem来实现。

本文的目标：is to formulate this optimization precisely, to develop algorithms for solving the optimization problem efficiently, and to make sense of the obtained solutions in terms of statistical consistency.

具体的不想看了。