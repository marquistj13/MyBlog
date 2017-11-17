--- 
title: unified聚类探索
date:   2017-11-13
---



* content
{:toc}


##  主题：图像分割
如何规避卷积层啊？
目测啊，目前的卷积层（第一层）仅仅利用了滤波的思路，即滤出来一个个特征，如果我不想这么搞呢。
感觉邻域信息的利用不止这一种approach吧。

## distance function: 邻域信息的利用
传统的单纯以点为计算单元的聚类模式很难hold住具有复杂pattern的dataset

有人说了，我把它变成kernel version不就行了么。
注意啊，加了kernel之后，我们还得choose这个kernel的参数，从而间接控制非线性变换的形式。
相较之下，卷积操作并没有太直接地涉及这个变换的形式，而仅仅用来获取特征。当然，如果动态来看，调教卷积参数的过程其实也是调节变换的过程，为了简化，姑且认为卷积只用来进行特征提取吧。

基于minimum spanning tree的representation学习算法和图论有关，即先建立一个graph，还得考虑cluster之间的连接，也就是将树划分成子树，如
```
Saglam, Ali, and Nurdan Akhan Baykan. “Sequential Image Segmentation Based on Minimum Spanning Tree Representation.” Pattern Recognition Letters, Advances in Graph-based Pattern Recognition, 87 (February 1, 2017): 155–62. https://doi.org/10.1016/j.patrec.2016.06.001.
```
的图2. 目测里边没啥变换，就是利用图论进行聚类，而且目测是逐帧搞的？
仔细一想啊，在最小化spanning tree的时候，其实隐含了邻域条件的，因为在构建graph的过程中，每一个vertex代表一个像素点，而vertex之间的连接权值是根据其邻域确定的，例如对于上面提到的论文来说，就是8邻域的信息。

## 问题具体化：组合具有明显差异的像素点，让其来看起很近，问题是根据啥去组合？
啊，看来只有考虑邻域信息，才能hold住这么一个艰难的问题：即，如何将很明显的有很大差异的像素点“组合”到一起，亦即，将其distance认为很近。
这个问题如果按照其本来的面目去搞就很难，即，learn一个distance function，达到以上“组合”的目的。
我们先复习一下卷积层的解决思路，它就不是单纯考虑像素点之间的距离了，而是考虑邻域像素点的加权和作为特征，然后再进行运算或者 learn 这些权值。
言归正传，以原问题的视角再分析一次，如果这个需要learn的distance function仅考虑像素点，不考虑邻域的话，这个function单纯的以不同像素特征作为计算distance的依据，显然不是很reasonable，咦，难道随意加一个邻域信息就行了？估计没这么简单吧。
>（ps。某种意义上，很多prototype based algorithm都涉及了邻域信息，如prototype计算过程中涉及了很多点，类似于加权求和，当然这个邻域信息的利用并非刻意为之，而是目标函数最小化的过程中的必然结果，既然这么多符合人们intuition的目标函数最后都说要利用邻域信息，那么就将其作为先验进行explicitly利用岂不更好，卷积滤波就是利用了邻域信息的结果吧）

## 无监督的关键：利用common  structure这个信息
还有一点，人家dnn搞的semantic segmentation和instance segmentation是有监督的，我们现在遇到的问题是，如何在没有监督信息的情况下来学习一些common structure。
首先，我们要明确一下，关于无监督的，不同于gan等生成模型致力于在学习如何还原输入的时候learn到好的representation，我们要远离这个input reconstruction的套路，毕竟这个reconstruction也是得下功夫训练的啊（很长时间啊）。我们追求的应该是在另一种目标函数下的学习，即，寻找多个image中的common structure。比如一个image中有一个aeroplane，这个aeroplane可能各个部分的像素值差异特别大，特别是还有复杂背景的情况下，那么对于传统的prototype的聚类算法来说就没有一个对应的学习机制来利用多个image中的重复结构，也就是说，对于多个image中的common structure，我们应该将其当做一个整体来看待（即聚到一个cluster），当然这个“整体”并非在各个image中一模一样，而是有各种视角差异、形状差异和像素差异，这里当然也不是完全没有监督，只是这个监督信息非常隐蔽，也就是，我们知道这么多image中肯定有很多common的structure。 说到这里，我想起了ng的 `Distance Metric Learning, with Application to Clustering with Side-Information`，在这篇文章中，作者假设已经知道了某些点属于同一个cluster，然后最大化地利用这个信息，即这几个点之间的距离最小，当然为了避免trivial解，还加了个限制，让已知的不在一个cluster的点的距离最大，或不在已知同一cluster点之间的距离最大，作者学习到的就是欧氏距离的协方差矩阵吧。
我的想法和这个还是有很大差别的吧。
我们这里没有已知的同一个cluster的点，也没有label，
一种思路：将prototype的概念泛化，变成prototype function，以融合prototype和distance function。每一个点不能以原尺度进行计算，也就是说，其绝对数值的意义不大了，关键是周围领域的关系，

## 总结
综上，为了达到一个目标：将不同视角和shape的同一种对象（如aeroplane）consider 为同一个cluster
我们要同时利用两个信息：
1. 邻域信息（用于distance或特征的计算）
2. common structure的信息（要想法放到目标函数中）
关于第二点，也可以说要搞出来一直学习机制以discover多个image的重复结构。

## 实现
像素值+邻域值 共同决定了 该像素的归属。
### 目标函数
在有label的时候，目标函数中几乎不需要input的直接参与，只需要网络输出和label就行了。
无label的时候，input是否也可以回避？
亦即将common structure的loss直接加进去，怎么加？

以往prototype based clustering基本上会出现每一个 data point 与各个prototype的误差，或者各种奇形怪状的distance function。
这个其实就是一种common structure类型的loss。如KMeans，每一个data point（对于图像来说就是整个图像了，而非像素点），但未免有一点点不太合理，这里每一个data point分别于各个prototype（每一个prototype可以看作一个common structure）产生一个loss，总的目标函数是让所有点的总的loss最小。

如果能够自动确定common structure的数目就好了。
占整个图像major region的像素点肯定对这个loss的贡献最大，故将其聚为一类是learn的必然结果，至于这个loss的形式如何，值得思考啊。
上面的loss，可以是单一image内的loss，也可以是image间的loss
按照这个思路，只需要在一个image上进行操作就行了，那么多个image的意义何在？很明显用于弥补单一image的初始分类时的邻域利用的缺陷，有可能我先在第一个image的segmentation比较粗糙，按照第一个image调教的参数的模型在第二个image上进行segmentation会很不好，那么第二个image也会对这个segmentation算法进行调教。
这个模式在有label的NN领域是很常见的，但在clustering领域貌似没见过？
传统clustering要么将很多aeroplane的images聚成一类，要么只在单一的image内聚类（或称分割），各个image之间互不通信。
采用这种模式之后就得研究如何先用一组参数进行分割，然后考虑这个分割参数在下一个image上的performance。但是如何定义loss呢。这个loss会不会又落入俗套，导致依然很难训练？
我就知道光有一种卷积操作是不够的，毕竟一种卷积操作只能搞定一种类型的特征，在cnn中，一般有好多个feature map（对于各种卷积操作），看来几何特征的提取还是CNN最拿手啊。
算了，还是不硬往DNN那边凑了，还是回到聚类领域吧。

每一个cluster有一个固定像素的prototype，如 $10 \product 10$ 的。 每个data point 参与运算的时候，应考虑其邻域，如 $10 \product 10$ 邻域（边界点没法处理了）。