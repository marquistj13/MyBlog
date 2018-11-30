--- 
title:  Subspace Learning in The Presence of Sparse Structured Outliers and Noise
date:   2017-3-24
---



* content
{:toc}


## 总括
本文的Subspace Learning仅限特定的问题，即不是general的

子空间学习其实就是学习一个低纬度的basis还有对应的系数

至于要解决实际问题，则需要在相应的目标函数上加入对应的先验

至于本文的例子或问题，在一个相对单调的背景上，有一些text，作者的先验是（第三页左上）：
>there are more vertical connectivity in English texts than horizontal

这样对于有很多竖直特征的前景也是适用的。

要分割背景和前景，同时也要套入子空间学习的框架。
$$x= P \alpha+s+\epsilon$$

> where  $P \in R^{N \times k}$ where $k \ll N$, and $\alpha$ denotes the representation coefficient in the subspace. $s$ and $\epsilon$ denote the outlier and noise components respectively.

即 $P \alpha$ 是子空间学习部分， $s$ 是我们的前景text

作者将前景的特性显示地描述出来将其作为正则化项，而原始目标函数项即子空间学习的部分几乎不变：

$$ 
 \underset{P, \alpha_i, s_i}{\text{min}}
 \sum_{i=1}^{N_d} \ \frac{1}{2} \| x_i-P\alpha_i-s_i  \|_2^2+ \lambda_1  \phi(P\alpha_i) + \lambda_2 \psi(s_i)  \\
 \ \text{s.t.}
\ \ \ \ \ \ \ \ P^tP= I, \ s_i \geq 0
$$

下面是先验部分，背景是 smooth，因此惩罚其微分，前景（text）具有sparsity and connectivit

Hence $\phi(P\alpha_i)= \| \nabla P \alpha_i \|_2^2$, and $\psi(s)= \|s\|_1+ \beta \sum_m \|s_{g_m}\|_2$, where $g_m$ shows the m-th group in the outlier (the pixels within each group are supposed to be connected).

## 优化算法
以上的优化可采用alternating optimization over $\alpha_i$, $s_i$ and $P$.
具体计算以后再看吧

## Applications For Image Segmentation
貌似目标函数又改了一下，形式还是不变啊。

## 实验部分
至于图3和图1的效果那么好，是因为你这个算法更specific嘛
有啥大不了的