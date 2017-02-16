--- 
title: 17.2.16 A Graphical Social Topology Model for Multi-Object Tracking
---


* content
{:toc}

## 评价和感悟
浏览到这篇文章的时候我发现它的写作风格比较好，即图片画得很好，我就好奇人家是咋搞出来这么多图片的，而且看到文中有好多“cluster”的字眼，就花了将近半天时间来看这篇文章。
看完之后发现不过如此嘛。
严格来说，我还未进入cv圈儿，因此对于其中的细节就不去深究了，上面说了，看这个主要是猎奇，哈哈。

好了，言归正传。cv的文章向来充满了各种technical detail，这篇也不例外，夸张地说，这篇文章的各个计算公式就是明目张胆地告诉读者“我就是这么算的，这个式子要实现xxx”，当然没法说清楚的是，要实现xxx可以有很多式子，作者为啥搞成这种形式，恩，没办法，工程性质的东西就这样吧。
不知道搞多目标tracking一般是咋玩儿的，这篇貌似是off-line的吧，因为该算法的特征提取部分（在IV. TOPOLOGY PATTERN TRAINING）依赖于两个阈值，这俩阈值是根据数据集的ground truth (GT) object annotations进行暴力搜索得到的，难以直视啊，不过效果很不错。
难不成对于每一个数据集都要对阈值进行搜索？目测这就是做application的一个无奈之处吧，怪不得作者只花了很少的篇幅讲这个东西。
不过搞应用的一个好处就是related works好写一点吧。

搞清楚了，文中的这些漂亮的插图很多都是根据其物理意义来画的，估计这个圈子的图都比较好看吧……
看来选择一个圈子很重要嘛，有些圈子就是看起来高大上。

既然看了一遍了，就多学点东西再走吧，下面总结一下该文的方法，不知道会有啥可以借鉴的……

## 文章内容
在形式上，追踪算法的主体在第五章（TRACKING WITH GRAPHICAL TOPOLOGICAL MODEL），但实际上由于追踪算法是直接在提取到的feature上做的，因此本文的主体是前面的特征提取部分。

### 基本概念
>A tracklet $n_i$ is a consecutive sequence of detection responses or interpolated responses that contain the same object. The goal is to associate tracklets that correspond to the same objects, given certain spatial-temporal constraints.

一个tracklet就是，包含相同object的detection responses的一个连续序列。
追踪就是在一定的时空限制下，将tracklet和对应的object联系起来。

### 第五章：追踪
首先是Group Tracking，作者说，由于单个的tracklet不太稳定，因此先找出来一个group中持续时间很长的tracklet，称其为confident的tracklet，然后基于学习到的 social topology matrix ，将这些 confident tracklet cluster到不同的group中，再用搜索得到的阈值对graph的edge进行剔除。
然后再用一个经验式子，根据学习到的特征直接估计 virtual center states of groups。
这就是Group Tracking。

然后是Individual Tracking，这个应该是按照经典的approach来的，即搞成一个 Linear Programming problem，不去细看了。

### 第三章：特征提取和Group learning（这个Group learning和聚类有点像了）
首先是Social Topology Matrix：它*encodes the social exchanges occurring among all theobjects in a scene.
就是从图像中估计出来一堆特征，然后再组合（即线性加权）成一个特征（即Social Topology Matrix，后边的算法貌似就是根据这个matrix来做决策的。）。
这些基本特征包括，各个object之间的距离矩阵，各个object之间同时出现（即在同一个frame中出现的）的时间矩阵，速度矩阵就是两个object之间的速度相近程度的矩阵，object的朝向矩阵也是同理。

然后是Social Topology Property，即一个social topology的两个属性： compactness and consistency，这个我没咋看懂，作者定义了这俩属性应该满足的限制条件，目测应该是形成一个group的限制条件？

再往后就是Group learning，即对识别出来的group进行merge或split，因为是视频嘛，各个group一般都会动的，每个group中的人有可能分成好几拨跑向不同的方向啦。
这一步中作者说不同于 **clustering and inference methods**，本文的方法能够自动确定group的数目，并且动态变化，恩我发现这个的确和聚类算法有点像哈哈。


果然，作者在第二章的RELATED WORKS提到，这个Group learning的确有人使用hierarchical clustering of trajectories based on pairwise objects speed and distance来实现。

在Group learning的时候，作者虽然没有使用聚类算法，但这又有啥不同呢？聚类算法相对来说没法进行精确调教，而作者这种精确调教的merge-split更强大也就不奇怪了。

## 总结
一个好的application需要各种trick，后来用于解释这些trick的各种道理其实谁都能想出来，但又有谁去意识到可以用这些道理或常识呢？
天下事有难易乎？为之，则难者亦易矣。
恩，只要去做就行了，不管看起来多么fancy的东西，细究起来也就那样啦。



