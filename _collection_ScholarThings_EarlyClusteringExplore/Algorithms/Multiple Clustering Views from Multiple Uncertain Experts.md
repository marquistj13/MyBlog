--- 
title:  Multiple Clustering Views from Multiple Uncertain Experts
date:   2017-11-1
---



* content
{:toc}

## 前言
本文目标：在给定多个不确定性专家输入的情况下，自动discover 多种聚类方法。
The benefits of learning the experts’ views include 1) enabling the discovery of multiple diverse clustering structures, and 2) improving the quality of clustering solution in each view by assigning higher weights to experts with higher confidence

## intro
正是由于不同用户对similarity的定义不一样，因此同一个dataset才会有不同的聚类方式，即不同的views。
当然，要想将不同的expert supervision to guide the clustering towards the right solution，那就是半监督了。


在exploratory data analysis setting, where ground truths are not known, different experts might provide supervision (pairwise contraints) with varying views in mind.

因此，本文的问题就是：
how to discover multiple clustering structures in the data given potentially diverse constraints from multiple uncertain experts.

本文的贡献：
1， Multiple experts are automatically assigned to different latent views and constraints provided by each expert is assumed to be noisy perturbations of the clustering associated with that expert’s view. Thus, multiple clustering structures can be discovered.
1. by explicitly modeling the uncertainty of each expert, experts with higher accuracies are assigned higher weights

## 方法
用狄利克雷分布来搞expert views

判别聚类：Instead of assuming the generative process of data X, discriminative clustering directly models the conditional distribution of cluster label given data.

后边一坨全是各种分布。然后用变分法来最大化marginal 分布。

但是啊，数据预处理还是少不了啊，例如对于face数据集，还得pca