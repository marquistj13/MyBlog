--- 
title: The blind men and the elephant on meeting the problem of multiple truths in data from clustering and pattern mining perspectives
date:   2017-6-6
---

## Meta
本文讨论了聚类中的子空间聚类和pattern mining的关系。
为了上升主题，题目搞成了聚类和pattern mining，所谓盲人摸象，就是好几个盲人，每个人摸到的同一个象的部分不一样，得到了部分“truth”，聚类和pattern mining就是俩盲人。

## 聚类法简介
先说Subspace clustering。
这哥们儿难在不知道各个子空间的维度是啥（即每个子空间可能都不一样）。咋办，就得去搜索，去learn。作者还提到了一类axis-parallel subspaces。
好了，两种搜索方法1. top-down search：先搜索 full-dimensional space。2. bottom-up search：搜索空间很大。

然后提到了Ensemble clustering，Alternative (or: constraint) clustering，以及Multiview clustering。啊不想看了。

## Pattern mining—considering the same elephant?
好了本文的另一半：Pattern mining及其与子空间聚类的联系开始了。
pattern mining也是exploratory data mining的一个branch，它的目标是发现 recurring
structures，即重复的结构，至于它和子空间聚类的关系，一图胜千言：
![](.\Theblindmen\illustration.png)
左图： Traditional pattern mining returns patterns, sets of attributes
最右图：Traditional clustering returns object groups, or clusters
中图：Modern pattern mining以及subspace clustering的结果

注：作者提到本文所指的pattern mining指的是出现比较频繁的item。
