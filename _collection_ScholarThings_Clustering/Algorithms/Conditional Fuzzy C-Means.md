--- 
title:  Conditional Fuzzy C-Means
date:   2017-6-11
---



* content
{:toc}

## 内容
一篇96年的Pattern Recognition Letters，很简单。
就是将FCM的隶属度限制由：
$$
\sum_{i=1}^cu_{ik}=1 ,\forall k
$$

变成：
$$
\sum_{i=1}^cu_{ik}=f_k ,\forall k
$$

即每一个点 $k$, 都有一个隶属度的限制。
注：它的迭代公式基本上没啥变化。

这个 $f_k$ 就起到了conditional variable的作用。

这么搞之后，主要是对各个点的隶属度的变化


那么实际用的时候有啥意义呢？
作者指出，conditional variable作为context-sensitive的一种需求，在data mining中可以有：
给定 $x_i$ is _small_ ; 我们要揭示 $x_1,x_2,\ldots,x_{i-1},x_i,\ldots,x_n$ 之间的关系, 这里 _small_ 是一个模糊集

这时候我们可以将 $x_i$ 作为 conditional variable。

## 总评
这篇文章属于解决实际需求型，要写出来，那就是可遇不可求了