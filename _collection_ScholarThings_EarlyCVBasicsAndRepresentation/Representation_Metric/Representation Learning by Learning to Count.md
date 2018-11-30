--- 
title: Representation Learning by Learning to Count
date:   2017-11-29
---


* content
{:toc}

## 摘要和简介
使用人工监督信号（artificial supervision signal）进行representation learning。
这个监督信号通过等价变化得到，将图像的变换和representation的变换关联起来。
也就是学习到的是满足这个关系的representation。

本文算法属于self-supervised learning，通过定义一个提供监督信号的task来避免标注。
self-supervised learning的rational为，和最终任务（如分类或detection）最相关的pretext 任务更容易build relevant representations。

本文定义了一个新的pretext task，即counting
visual primitives。其实很简单，就是将一个imagepartition撑不重叠的区域以后，这些区域的visual primitives数目之和等于原图像中的数目。

## 相关工作
除了autoencoder可以用来在无label的情况下学习representation之外，也可以用artificial or surrogate ones来替代label。
这毕竟只是个technique。
我们知道，无监督学习可以看做是学习 $p(x)=p(x_1,x_2)$, 而这个technique其实就是将其转换为部分监督问题，即 $p(x_2|x_1)$. 这时候，我们无需知道 $p(x_1)$. 因为 $p(x_2|x_1)$ 已经足够得到 $x$ 的representation了。

举个例子，在Pathak et al. [33]中，作者将中心区域的一部分迅速作为 $x_2$， 其余的像素作为 $x_1$， 然后用gan来建模 $p(x_2|x_1)$。这个可以看做regression问题。
至于分类问题，surrogate label可以看做patch的相对位置（见Noroozi & Favaro [9, 29]）。

## 本文算法
我们的最终目的是要学习一个能够count visual primitives的特征变换 $\phi$, 这个 $\phi$ 有什么约束呢？ 我们让它去数visual primitives的数目：
$$\phi(x)=\sum_{j=1}^{4}\phi(T_j \circ x)$$
其中 $T_j$ 就是一种变换，将图片分块，其实这个已经可以了，不知道为啥，作者还要他对原信号加个变换，变成：
$$\phi(D \circ x)=\sum_{j=1}^{4}\phi(T_j \circ x)$$
$D$ 用来factor为2的降采样。以上的变换之后image的size是一样的。

## 学习的过程
如果将损失函数定义为：
$$l(x)=|\phi(D \circ x)-\sum_{j=1}^{4}\phi(T_j \circ x)|^2$$
的话，会有 $\phi(x)=0$ 这种trivial解。
因此采用contrastive loss：
$$l_{con}(x,y)=|\phi(D \circ x)-\sum_{j=1}^{4}\phi(T_j \circ x)|^2+\max\{0,10-|\phi(D \circ y)-\sum_{j=1}^{4}\phi(T_j \circ x)|^2\}$$

即，还要求，对于随机选择的不同图像 $x,y$， 它们的数出来的特征数不能一样。

## 总结
虽然可以算是self-supervised learning（自监督），但其实还是将其转换为有监督来学的。还是依赖于原来的cnn结构。

归根到底还是目标函数的设置，上面这个目标函数只是尽量保证各个区域学习到的特征的数值之和与在整个图像上得到的数值一样，但作者钦定这个数值就是特征的数目，爱说啥就是啥吧。