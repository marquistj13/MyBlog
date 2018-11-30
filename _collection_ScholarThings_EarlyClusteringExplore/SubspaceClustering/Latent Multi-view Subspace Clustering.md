--- 
title: Latent Multi-view Subspace Clustering
date:   2017-11-2
---



* content
{:toc}

## 前言
题目里有个latent，其实就是，不在原始特征上做子空间聚类，而是在寻找latent representation的时候，同时基于这个representation进行data reconstruction.

至于multiview，我感觉是用来凑数的吧
## intro
Recently, the subspace clustering based on selfrepresentation has been proposed, where each data point can be expressed with a linear combination of the data points themselves.

而multiview的初衷是，每一个点都可以described with information from multiple sources of features、

## 算法
就是将self representation和multiew的对于目标函数组合一起，再搞点权值。
不细看了。