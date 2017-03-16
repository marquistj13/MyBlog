--- 
title: 两篇用Kmeans做deep Learning的很偏的文章
date:   2017-03-16
---



* content
{:toc}

## CONVOLUTIONAL CLUSTERING FOR UNSUPERVISED LEARNING
一篇Workshop track - ICLR 2016

这篇文章对于我来说实在是太偏了啊

###  从摘要里来看 
本文的工作是：
通过无监督技巧来利用层次特征 就可以减少对于带标签数据量的依赖。
而这种以无监督方式learn filter (即ConvNets filters) 的技巧本来就有， 本文只是搞出一种新的方式

也就是说本文重的是 _聚类的运用，而非聚类的design_。

怎么用呢：
> preventing the algorithm from learning redundant filters that are basically shifted version of each others

### RELATED WORK
用无监督算法来学习：ConvNets filters

作者提到，一开始用用各种高级方法如sparse coding and sparse modeling，后来用k-means的效果也不错嘛。
k-means简单，而且 只需要 __the right pre-processing and encoding scheme__。

__DNN里也有维度灾难__。

k-means在第一层不太好啊，从这个现象我猜测啊，_k-means适合的是高层次的feature，怪不得好多 deep clustering的文章在最后一层都能work_！
莫非还能推出来 _欧式距离_ 和 _高维特征_ 的 __强相关性__？

### LEARNING FILTERS
哎呀，这一节的k-means 的形式我咋看不懂啊……


## Short Text Clustering via Convolutional Neural Networks
一篇会议NAACL-HLT 2015，中科院的人写的

### 摘要
文本聚类啊，好新鲜，其实就是各种分类如 bussiness，sports

前面一大堆啊，从keyword feature到word embeddings，然后CNN，最后再将K-means用到这些learned representations上。

在算法部分我也没搞懂为啥这些learned representations就能用K-means，哈，估计DL的圈子里还没人解决这个问题？

### 实验部分
在第五页的右边底部提到一个工具的链接：http://lvdmaaten.github.io/tsne/
可以用于 __高维数据的可视化__ ，这个工具有python的代码。
