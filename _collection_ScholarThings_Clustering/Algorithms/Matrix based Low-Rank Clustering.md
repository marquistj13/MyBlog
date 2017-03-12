--- 
title: Matrix based Low-Rank Clustering
date:   2017-03-12
---



* content
{:toc}


先说这一篇： _Low-Rank Doubly Stochastic Matrix Decomposition for Cluster Analysis_

现有的算法受限于 nonnegative matrix factorization (NMF)，并且无法产生。 balanced partitions。
本文的算法：能够hold住large-scale manifold data sets（十万级）

但话又说回来了，这种算分关键是得 _自己定制优化算法_（即解一个目标函数，）这个一般人是hold不住的。

原理没那么难，就是先定义一个 _cluster indicator matrix_  $\bar{F}\in\{0,1\}^{N\times r}$ ,然后构造 _cluster incidence matrix_ $\bar{M}=\bar{F}\bar{F}^T$
如果我们有一个样本间的相似度矩阵 $S$,那么只要最小化一个divergence $D(S\|\bar{M})$ 就行了。

这篇文章基于另一篇icml
2012： _Clustering by Low-Rank Doubly Stochastic Matrix Decomposition_
单我很难看出来icml 2012和这篇文章的关系。

这两篇文章的实验部分性能指标都是纯度（purity），没有图，只有表。





