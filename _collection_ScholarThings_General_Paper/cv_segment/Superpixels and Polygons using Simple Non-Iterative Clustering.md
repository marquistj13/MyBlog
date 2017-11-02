--- 
title:  Superpixels and Polygons using Simple Non-Iterative Clustering
date:   2017-11-2
---



* content
{:toc}

## 摘要
本文要对Simple Linear Iterative Clustering (SLIC) superpixel segmentation进行改进，
本文改进的特点：non-iterative, enforces connectivity from the start, requires lesser memory, and is faster

## intro
图像分割比较难，一个较容易的解决方法就是先simplifying an image into small clusters of connected pixels called superpixels

superpixels are commonly
expected to have the following properties [7, 18]:
• Tight region boundary adherence.
• Containing a small cluster of similar pixels.
• Uniformity; roughly equally sized clusters.
• Compactness; limiting the degree of adjacency.
• Computational efficiency.


本文先提出Simple Non-Iterative Clustering (SNIC). 
然后提出a polygonal segmentation algorithm called SNICPOLY, which uses SNIC superpixel segmenta- tion as the basis.
适合于geometric or man-made structures

## 算法
主要改变就是距离了，即公式1.

不仔细看了。