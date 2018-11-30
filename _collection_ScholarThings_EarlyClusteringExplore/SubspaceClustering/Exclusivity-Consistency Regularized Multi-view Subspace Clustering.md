--- 
title: Exclusivity-Consistency Regularized Multi-view Subspace Clustering
date:   2017-11-1
---



* content
{:toc}

## 前言
本文的算法利用了不同representation的互补信息，怎么实现的呢，就是在子空间聚类的目标函数里加两项
1. a novel position-aware exclusivity term
1. a consistency term

## Intro
碰巧能够利用互补信息，当然要说一下 这种 multiple views的好处了。 

In practice, we often face data in multiple views. Different views characterize different and partly independent information about the data.

这些view最终目的还是要capture the rich information from multiple data cues as well as the complementary information among different cues, thus will be beneficial to clustering.

## problem formulation
首先是子空间聚类的目标函数：
![](ExclusivityConsistencyRegularized\formula1.png)

一通倒腾之后，定义了一个Representation Exclusivity和Indicator Consistency的概念，然后加到目标函数中
![](ExclusivityConsistencyRegularized\formula9.png)

## 优化算法
有了目标函数，就得优化了
看着挺麻烦的，先不看了