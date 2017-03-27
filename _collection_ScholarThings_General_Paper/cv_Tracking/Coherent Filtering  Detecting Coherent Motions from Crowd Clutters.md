--- 
title:  Coherent Filtering  Detecting Coherent Motions from Crowd Clutters
date:   2017-3-27
---



* content
{:toc}

## Meta
Bolei Zhou大神的ECCV 2012，人家几乎每年都能发顶会，环境好，实力强，好羡慕

## Abstract
所谓Coherent motions就是描述collective movements of individuals in crowd。

理解Coherent motion对应的规律（underlying priors），并且从背景噪声中检测出来是难点啊 

本文搞出一个prior，即Coherent Neighbor Invariance
其实就是发现了一个video的连续几帧中，有几个规律，然后利用这几个规律来设计算法

本文的算法能够很好滴区分 coherent and incoherent motions

## Related Works
作者列出了一大堆算法，指出了，这些算法都需要特定的假设

并且Crowd motion有很多种：
为了数运动的数目，有人搞算法去检测independent motion
有人用李代数来学习global motion patterns of crowds
有人用spectral clustering to group long-term dense trajectories for the segmentation of moving objects in video.
在3D motion segmentation中，在仿射变换的假设下，还有Generalized Principal Component Analysis (GPCA) [16] and RANSAC [15]


本文develop a general coherent motion technique which can be well
applied to the various problems discussed above

## 本文的算法
思想不难

过了n帧之后，一个点周围的K个最近的点，能够一直存在的，肯定在减少，但是这些一直在它周围存在的点钟，coherent的点，即和它运动一致的点的比例是增加的
（最近点的定义看图1，该prior的效果看图2）

另外，一直保持最近点的点中，它们的速度相关性一般会保持比较高的值

这就是本文的先验。

## 试验
有Synthetic Data

在4.1的结尾，有Ncuts, K-means, and Mean-shift的方法对比，即图6

4.2还有 Hopkins155 Database

