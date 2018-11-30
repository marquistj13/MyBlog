--- 
title:  A novel density-based fuzzy clustering algorithm for low dimensional feature space
date:   2017-5-19
---



* content
{:toc}

## Meta
核心内容很简单，但包装的很玄乎，不值得细看

##  主题思想
将特征空间分成很多格点（缺陷不言自明），然后数一下各个格点的密度（怎么数？就是类似于每一个格点都有一个隶属度值，累加然后归一化，很简单的intuition），好了再利用一个现成的图论算法：Connected-Components Labeling对一些连通区域赋给一个唯一的label（在公式9上面的Step 4: Clusters detection and location）。


##  至于为啥能够和 Active Learning Method (ALM)联系起来，也是很简单的
其一，根据图1，人家ALM有一个分而治之的步骤，即将大问题分成小问题，每一个小问题提取特征，最后根据这些个特征进行决策
其二，本文的算法能够凑到这个ALM的框架中，即将大的特征空间分成小的格点，每一个格点数一下密度，最后利用这些密度特征feed进Connected-Components Labeling得到label。

Remark：作者对于Connected-Components Labeling介绍比较少，我也不想了解啦。


##  总评
意义不大
