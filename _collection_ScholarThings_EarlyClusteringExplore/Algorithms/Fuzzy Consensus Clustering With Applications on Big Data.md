--- 
title:  Fuzzy Consensus Clustering With Applications on Big Data
date:   2017-12-5
---



* content
{:toc}

## 前言
在有监督领域，弱分类器可以组合成强分类器
对于无监督聚类，从基本分区搞一个consensus分区也是同样的道理(fuzzy consensus partition from multiple fuzzy basic partitions)

本文就是搞这个的，而且是fuzzy的版本。

## 方法总览
对于有目标函数的consensus 聚类，其实就是一个组合优化问题。
令 $\pi_i$ 作为某一个基本分区（例如用FCM或KMeans得到）， $\pi$ 是我们要求的 consensus分区。
优化的目标函数可以定义为：
$$\max_{\pi}{\sum_i^r\omega_iU(\pi,\pi_i)}$$

其中， $\omega_i$ 是用户自定义的权值。 
$U$ 可以认为是损失函数， consensus 聚类领域称其为Utility Function。

这个式子如何去解呢。
本文将其转化为最小化问题。

## 具体实现
作者搞了一大坨的Utility Function定义之后，得到了 (26) 式，即和FCM差不多的式子。可以迭代的形式，还证明了收敛性。

## 实验
uci的几个数据集，还是老样子，一点都不提数据的预处理，直接就给结果了。
数据集在表5，还有wine。

在表6中，结果表示，从多个FCM分区（跑了好多次FCM得到很多分区）中得到的consensus分区，结果的确比原分区好。

在Spark上实现以后，用集群处理上G的数据，128 GB of RAM，配置吓尿了，结果还行，但无比较，所以不知道真正的好坏。

## 评价
以我的视角来说，遗憾有2：
1. 结果不够形象。 从多个弱分区得到一个分区，那么原分区的缺陷是否能避免？原来非线性的hold不住，结果分区估计也不行吧，矮子里边拔将军？
2. 实验结果不可重复，毫无预处理，聚类文献的通病？

## 展望
弱分区的组合不应该如此吧？ 非得如此生硬地组合么？
我感觉可以更fuzzy地解决这个组合问题，而非硬生生地从坏的里边找好的。

