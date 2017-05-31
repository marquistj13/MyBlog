--- 
title:  两篇子空间聚类综述
date:   2017-5-31
---



* content
{:toc}

## Meta
子空间聚类的应用场景很固定：你已经知道了这个高维数据集的本征维度比较小
那么就得显示地利用这个低本征维度的特点。然而，问题来了：这些个低纬度的子空间，你们的维度到底是多少？一切恩恩怨怨由此而来……

以下是几篇文章的小结。
其中
* A Tutorial on Subspace Clustering从ml和cv圈儿的角度来综述（ including algebraic methods [7, 8, 9, 10],
iterative methods [11, 12, 13, 14, 15], statistical methods [16,
17, 18, 19, 20], and spectral clustering-based methods [7, 21,
22, 23, 24, 25, 26, 27].）
* Subspace Clustering for High Dimensional Data: A Review 
从data mining community的角度来综述。

## A Tutorial on Subspace Clustering
首先是Algebraic Algorithms，有基于Matrix factorization的，即搞一个 low-rank factorization of the data matrix $X$, 但效果不怎么好，有俩问题：不知道改选哪些column，改选多少column。

先说代数法。
Generalized PCA (GPCA)呢，是一个代数几何法，用多项式来搞，main idea是：可以用n阶多项式来拟合n个子空间的union，在一个点的微分得到的矢量正交于包含这个点的子空间。
很显然啊，你用这么strick的intuition（或者说是法则？）很明显对于实际数据不太好啊，即带了noise就要gg。

至于迭代法，就是先搞一个initial segmentation，用经典PCA给每一个group来fit一个子空间。然后再迭代这两步就行了。这种算法有：K-planes and K-subspaces。
但初始化很重要，要不然收敛不好啊，对于K-subspaces来说，还对outlier敏感，还有n以及其他参数 $d_i$ 等也需要提前知道，因此还需要模型选择。 

其他几个Statistical Methods，如Mixtures of Probabilistic PCA (MPPCA)、Agglomerative Lossy Compression (ALC)、Random Sample Consensus (RANSAC)我就不抄了，这些东西限制很强啊。

最后就是基于Spectral Clustering的算法。形式都很复杂啊，当然affinity matrix的选择还是逃不掉的，还有各种优化问题……

## Subspace Clustering for High Dimensional Data: A Review
这篇文章也只是简介了几个算法而已。分为两大类：Bottom Up Subspace Search Methods以及Iterative Top Down Subspace Search Methods

至于为啥这俩都是搜索方法，就得从头说起了。
我们先回忆一下普通的特征选择，即选好特征之后，然后在这些特征上聚类啊等等，但如果不同的cluster处于不同的子空间呢？普通的特征选择就没法搞了，这就是子空间聚类的motivation啦。

和普通的特征选择一样的地方在于，子空间聚类需要a search method and an evaluation criteria，当然它的evaluation criteria更特殊一些。

对于Bottom Up Subspace Search Methods来说，利用的是 downward closure property of density to reduce the search space,即，如果在 $k$ 个维度中有dens units，那么在所有 ( $k-1$ )维的投影也有dense units。

对于Iterative Top Down Subspace Search Methods，首先在整个特征空间搞一个initial approximation of the clusters，然后每一个cluster对于每一个维度都有一个weight。

至于为啥这篇paper是从data mining的角度来综述的，是因为，在文末的application里边都是一些web text mining啊，dna microarray analysis啦这些东西。