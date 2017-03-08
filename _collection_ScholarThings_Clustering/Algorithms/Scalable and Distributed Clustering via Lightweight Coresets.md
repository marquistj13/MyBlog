--- 
title: Scalable and Distributed Clustering via Lightweight Coresets
date:   2017-02-28
---


* content
{:toc}


来自：苏黎世联邦理工学院，名校啊

终于看到和DNN无关的clustering文章了，没有那么多detail的烦恼，好激动。
最近几天一直陷到DNN的文献里边了，心情不爽啊，赶紧搞个纯聚类的压压惊。

啊啊，看不懂啊
我看到了各种bound……
看到第三页就没法看了……

搜了一下，发现[作者主页](https://las.inf.ethz.ch/people/olivier-bachem)，啊就是NIPS16 拿到oral的那个！搞出来一个 Fast and Provably Good Seedings for k-Means

算了先看实验吧
看到人家用了四个数据集，exicited！
>1. KDD — 145’751 samples with 74 features measuring the match between a protein and a native sequence
(KDD Cup, 2004).
1. CSN — 7GB of cellphone accelerometer data processed into 80’000 observations and 17 features
(Faulkner et al., 2011).
1. MSYP — 90 features from 515’345 songs of the Million Song datasets used for predicting the year of songs
(Bertin-Mahieux et al., 2011).
1.  CODRNA — 8 features from 488’565 RNA input sequence pairs (Uzilov et al., 2006).


人家用了1.5TB memory，上G的数据集才明显看出来效果（里头用了抽样），看样子一个好的结果的确得有各种付出和机遇。

文章的主体其实在第三章就有了，就是 _Definition 1 (Lightweight coreset for k-Means)_ ,形式很简单，后边第四、五章貌似就是为这一章服务的。


