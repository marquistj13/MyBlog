--- 
title: 17.2.22 Universal representationsThe missing link between faces, text, planktons, and cat breeds Tracking
---


* content
{:toc}

## 简介
这篇文章属于DL圈儿，由两个牛津的写的。

针对研究内容，先说一个大局观吧
1. vision领域的问题有别于其他领域，首先人家的数据一般是二维图像（当然展开以后是很多维的），并且图像里边有一些shape。这两点其实将vision非常具体化了。
在很多研究中，有具体的问题很重要。
1. vision问题的另一个加持：大多数是有监督的，即使是无监督的，也能非常perfect地转化为有监督的。

以上两点使得这个领域的效果可以调教地很好，效果好了才允许更高层的work，如本文探讨universal representation的问题。
恩，仓廪实而知礼节。


### 摘要
历史进程：现在有大量labelled datasets以及high capacity models
自我奋斗：machine vision systems 的性能也在逐渐improve

局限性：不同的 vision 问题依然得由不同的 model 去做。
与强大的人类视觉对比： 人类视觉只是在幼年时期学习到一个universal representation 就可以解决很多 vision 问题，并且**在顶多只需要微调的情况下，仅需要little training data就可以解决很多vision 问题**。
结论：**universal representation 很重要**。

本文做了啥：我们想知道**一个NN能否work as universal representations**，咋着才能知道呢？**就看它的 capacity 和 它能解决多少vision 问题 之间的关系**！
详细一点：单个NN能够解决好多visual domain的问题（from sketches to planktons and MNIST digits），并且只需要normalize the information in the network, by using domainspecific scaling factors or, more generically, by using an
instance normalization layer

## 总结
