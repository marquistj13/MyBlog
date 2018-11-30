--- 
title: formulate clustering as penalized regression
date:   2017-03-11
---



* content
{:toc}

无监督问题一般还是得按照有监督的套路来搞。

经典的算法如Kmeans没有明确说出来是按照有监督搞，其实看形式也差不多了嘛，都得有object function，只是聚类的来的更弱一些罢了。
我们现在看到的这个approach即clustering as penalized regression，就是 __将这个思想严格执行起来了__。

这次不去追究该approach的起源了。反正不打算入坑哈哈。

先说这篇文章 _Cluster Analysis: Unsupervised Learning via Supervised Learning with a Non-convex Penalty_ 
作者是统计学出身，所以很浓重的公式味儿。
一开始我还是很羡慕人家能够游走于各种公式推理之间，随着阅读量的增加，逐渐发现人家也很无奈啊。问题的复杂度一上来，各种式子都没辙了，你得尽量简化才能搞成漂亮的式子。运算的过程中还得各种逼近……
令人沮丧的是辛苦得到的漂亮式子，还不好用。算法运行结果不太漂亮，所以很少看到他们放聚类结果图哈哈。
仔细一想啊，人家各种逼近技巧都用了，为啥还很有可能比不上一些很简单的工程trick？
其实大家都是逼近，所谓条条大路通罗马，但是，每一种聚类方法都是错误的，因为 the truth （即真正意义上的聚类算法）是不可能由我等凡人看见或搞出来的，所以各种聚类算法不管形式多么漂亮或不漂亮，大家谁也别瞧不起谁，能work就行。

好了，言归正传。
目标函数的形式：

$$ \hat{\mu}=\text{arg}\min_{\mu}\frac{1}{2} \sum_{i=1}^{n}\|x_i-\mu_i\|_2^2+ \lambda\sum_{i<j} \|\mu_i-\mu_j\|_1 $$


思想就是，对于每一个点 $x_i$ ，我都给你一个聚类中心 $\mu_i$ ，只要 $x_i$ 和 $x_j$ 这哥俩的聚类中心就得相同，这意味着，目标函数中必须增加对不一样的聚类中心的惩罚，即上式的第二项。

但这种目标函数很不好解。而且速度很慢。
故，同一拨人又写了一篇文章： _A New Algorithm and Theory for Penalized Regression-based Clustering_，这篇新文章搞了新解法，又给了好多证明，还有finitesample mis-clustering error bound。

