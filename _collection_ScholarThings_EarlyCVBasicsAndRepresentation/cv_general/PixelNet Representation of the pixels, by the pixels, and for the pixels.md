--- 
title: PixelNet Representation of the pixels, by the pixels, and for the pixels.
date:   2017-03-1
---



* content
{:toc}


## update
Xiaodi Hou 组也有人搞了一篇 [Understanding Convolution for Semantic Segmentation](https://arxiv.org/pdf/1702.08502.pdf), 也用到了本文的PASCAL VOC-2012 dataset。
都是像素级的……，而且设计DNN的好多细节，我就不下载来看了。

## 啦啦
CMU的一群人搞的。还有[项目主页](http://www.cs.cmu.edu/~aayushb/pixelNet/)

第一句话的信息量就够大的：
> We explore design principles for general pixel-level prediction problems, from low-level edge detection to midlevel surface normal estimation to high-level semantic segmentation. 

本文搞的是一些像素级的预测问题:edge detection,surface normal estimation,semantic segmentation

具体问题我不想关心了，以后可以慢慢看吧，先搞些useful的东西再说。

## useful的东西
一直觊觎CV圈儿丰富的数据，在纯聚类圈儿里数据集都很naive，我现在算是开了眼界啦。
在本文的三大应用中，Segmentation部分才算和聚类沾点儿关系吧，看图：
![](PixelNetRepresentation\图6分割结果.png)

数据集描述在第九页，_Appendices：A. Semantic Segmentation_，即： PASCAL-Context dataset，PASCAL VOC 2010 segmentation annotations，PASCAL VOC-2012 dataset

这些数据集 __带有ground truth__