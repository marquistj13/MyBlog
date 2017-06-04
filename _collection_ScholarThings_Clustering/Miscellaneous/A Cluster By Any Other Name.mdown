--- 
title: A Cluster By Any Other Name
date:   2017-6-4
---


* content
{:toc}

## 前言
给你一堆点，它们能不能组成一个cluster？ 这个 _degree of clusterness_ 怎么去算？
本文（一篇小会议论文）就是要通过实验得到这么一个计算方法（哦，两个）。

至于一堆点能不能构成一个cluster，很显然，只有存在好多cluster的时候，一个cluster才有意义。作者将此问题称为： _This was sort of an “I may not know how to define one, but I’ll know it when I see it” type response._

## 内容
本文思路很简单。
给定一堆点，分成好多种情形去摆放。即很密集，稍微松一点，最后完全随机。很明显它们的clusterness是逐渐减小的。
怎么获取这个clusterness呢？用PCM当C=1时，即P1M进行聚类，将所有隶属度去均值，就得到一个特征值。再将这个特征值“动起来”，即通过改变P1M的 $eta$ ，得到不同的特征值，然后将这个 特征值- $eta$ 变化曲线画出来就能看出来了，然后再根据这个曲线定义clusterness的定义了。

作者的另一个方法 Vat clusterness也是同理，即让一个参数动起来，计算特征值，最后找出经验公式。

## 综评
这个定义clusterness的非常根本的问题有啥意义？
作者的隐含意思就是对于每一个聚类算法，咱们都应该可以搞出一个对应的衡量clusterness的指标，但是单个指标又不可靠，如Fig.6对于两个cluster的情形，上面定义的俩指标都不可靠，作者提议需要融合这俩指标，所以啊问题没那么简单。
话又说回来了，定义clusterness有啥用，还不是落入古典“聚类”的俗套？
