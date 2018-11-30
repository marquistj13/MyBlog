--- 
title: 涉及到maximum margin clustering的论文及其它Deep Clustering的资料
date:   2017-03-2
---



* content
{:toc}


## 先介绍maximum margin clustering的论文
###  首先是 _Data-Driven Fuzzy Modeling Using Deep Learning_ 
这是一篇大杂烩，各种乱七八糟的东西都糅合到一块儿了，如deep learning, probability theory, fuzzy modeling, and extreme learning machines。
其中从RBM得到的隐含特征进行聚类用的就是A probability based clustering method。
这个聚类算法的 __目标函数__ 借鉴了 _Deep learning with nonparametric clustering_ 的。
我们知道，目标函数是精华啊

###  Deep learning with nonparametric clustering
我又忘了nonparametric的含义……
这篇文章的重点估计也是这个聚类的目标函数吧，就是公式4.
它前面也是一大坨RBM，都是套路啊。

### maximum margin clustering
搜索Nonparametric maximum margin clustering的时候排在第一个的是下面这个。
[Maximum Margin Clustering Made Practical](http://www.machinelearning.org/proceedings/icml2007/papers/532.pdf)
这篇文章的目标函数形式看样子和上面的nonparametric的差别好大，难道是我找错了？以后再核实吧。这篇文章的插图很不错，有美女，有斑马，原来是一篇ICML07，

好了这篇文章指出了maximum margin clustering的提出论文,一篇nips05：[Maximum Margin Clustering](https://papers.nips.cc/paper/2602-maximum-margin-clustering.pdf)

## 其它Deep Clustering的资料
这篇博客总结了好多[Deep Learning for Clustering](https://amundtveit.com/2016/12/02/deep-learning-for-clustering/)。没事可以看一下。
该博主还推荐了一个视频[Foundations of Unsupervised Deep Learning (Ruslan Salakhutdinov, CMU)](https://www.youtube.com/watch?v=rK6bchqeaN8)，我看到此页面是一个视频列表，不错。