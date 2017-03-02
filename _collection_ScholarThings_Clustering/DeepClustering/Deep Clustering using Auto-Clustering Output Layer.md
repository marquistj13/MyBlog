--- 
title: 17.3.2 Deep Clustering using Auto-Clustering Output Layer
---



* content
{:toc}

这是一篇ICML17在审的文章。
## 摘要
光看摘要没啥有意思的嘛。

1. 有一句，增加正则化项以encourage the neural network to reveal its own explicit clustering objective。没有人工钦点它的目标函数？一股清流啊……
2. 由于寻找subclasses是无监督的，因此可以轻易变成半监督。
3. 这个network能够naturally create sub-clusters under the provided main class labels.

我居心不良地揣测一下，作者非得扯上半监督，很明显是对无监督效果的不自信吧，待会儿看完文章再核实一下
粗略扫了一下实验部分，的确，无监督部分的实验的确需要更多的调教，效果还可以，当然没有半监督的好。

##  Auto-Clustering Output Layer
初看这一章的序言，感觉很牛逼啊。
一个ANN，在优化classification objective的时候，通过ACOL这个输出层，能够find subclasses within these classes.
作者称之为
>perform a secondary task - unsupervised clustering - while the primary task -
supervised classification - is being carried out.

这么搞为啥还能成为无监督？因为我们的data并没有subclass的信息，即subclass exploration这一步是无监督的。
这样整个learning procedure