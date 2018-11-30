--- 
title: 谱聚类总结
date:   2017-5-30
---



* content
{:toc}

## Meta
花了一周多的时间看谱聚类，有了个大概的认识。
以下内容主要的参考文献：
Luxburg, Ulrike von. “A Tutorial on Spectral Clustering.” Statistics and Computing 17, no. 4 (December 1, 2007): 395–416. doi:10.1007/s11222-007-9033-z.

## 简要介绍
谱聚类没有那么神奇。
由于牵涉到特征值等偏数学的内容，因此它像是各种 _巧合_ 累积起来产生的。

算法的输入就是 __similarity graph__，这个graph一定要 _能够model数据之间的 local neighborhood relationships_， 构建方法有：将距离小于 $epsilon$ 的点连起来；距离为knn的点连起来；全连接图等。


首先是 unnormalized graph Laplacian matrix：
$$L=D-W$$
这个 $L$ 有个很好的性质，即对于任意矢量 $f$:
$$f^TLf=\frac{1}{2}\sum_{i,j=1}^{n}w_{ij}(f_i-f_j)^2$$
很明显，右边是有物理意义的，啥？当我们将 $f$ 理解为长度为n（数据个数）的label矢量时，意义就很明显啦。
而且从上式很容易看出来，有多少个重复的0特征根，就有多少联通的部分。 （令 $0=f^TLf=\frac{1}{2}\sum_{i,j=1}^{n}w_{ij}(f_i-f_j)^2$)

接下来就是两个 normalized graph Laplacians，一个是Shi and Malik (2000)，另一个是Ng et al. (2002)的。
至于normalized有啥好处，我是没有看出来啊，难道是当cluster之间有少许连接的时候结果也很stable？

至于从图论的角度来看，那就是各种cut问题啦。具体就不列了，反正就是各种凑啊。注意，如果只cut的话，会出现将单个点孤立出来的情形，这时候就得normalize一下，即将每一个cluster的体积等加入目标函数，这样就强行让各个cluster给balance了，但这么搞就是离散优化问题，NP hard，我们就得搞成连续优化即relax一下，但这种逼近不一定准确。

至于randomw walk的视角，以及perturbation theory视角就不需要看了。