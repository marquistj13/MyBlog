--- 
title: Grassmannian Manifold Optimization Assisted Sparse Spectral Clustering
date:   2017-11-1
---



* content
{:toc}

## 前言
谱聚类需要谱分解到一个low-dimensional embedding of data。
稀疏之后就加了一个sparsity-induced penalty,然后一般需要用解非凸问题的ADMM。
本文provides a direct solution as solving a new Grassmann optimization problem.

## Intro
谱聚类的两步走：
(1) forming/learning a similarity/affinity matrix for the given data sample set; 
(2) performing general clustering methods to categorize data samples such as Normalized Cuts (NCut)。
本文关注与第二部， aiming at learning latent representation for original data.

不想看了。