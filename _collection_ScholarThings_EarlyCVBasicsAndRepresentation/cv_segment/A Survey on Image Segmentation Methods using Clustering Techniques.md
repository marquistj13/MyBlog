--- 
title:  A Survey on Image Segmentation Methods using Clustering Techniques
date:   2017-11-8
---



* content
{:toc}

三哥写的一篇很水的用来凑数的综述文章，不过有些基本常识会在水文里提及的哈哈

图像分割的目的：
the objective of image segmentation is
> to simplify or change the representation of an image or convert the information of an image into a more meaningful form so that it make it easier for further analysis.

翻译一下：
1. 简化image的representation
1. 改变image的representation
1. 将image的information转化成更有意义的形式，这样便于further analysis。

作者指出，目前的图像分割技巧可以分为如下几类：
1. Thresholding based segmentation
2. Region based segmentation
 a. Region growing
 b. Region merging and splitting
3. Edge based segmentation
4. Clustering based segmentation
5. Bayesian based segmentation
6. Classification based segmentation


基于阈值化的将图像分为background and image foreground。

Region Growing就是先选择一个种子点，然后和该点连接的具有相同密度的点都被选到同一个growing region。
Region Splitting和growing相反，先将其分成unconnected regions and then merge again based on some condition.

Edge Detection。在具有rapid transition of intensity地方. So those pixels are extracted and linked together to form a closed boundary.

Bayesian:用来分类的吧，主要有Markov Random Field (MRF), Expectation Maximization (EM).

Classification:使用带label的数据来partition the image feature space