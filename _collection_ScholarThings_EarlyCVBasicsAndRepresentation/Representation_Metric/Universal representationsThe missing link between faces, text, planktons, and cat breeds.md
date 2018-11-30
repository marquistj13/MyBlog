--- 
title: 17.2.22-28 Universal representationsThe missing link between faces, text, planktons, and cat breeds Tracking
date:   2017-02-28
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


## 摘要
历史进程：现在有大量labelled datasets以及high capacity models
自我奋斗：machine vision systems 的性能也在逐渐improve

局限性：不同的 vision 问题依然得由不同的 model 去做。
与强大的人类视觉对比： 人类视觉只是在幼年时期学习到一个universal representation 就可以解决很多 vision 问题，并且 **在顶多只需要微调的情况下，仅需要little  training data就可以解决很多vision 问题**。
结论：**universal representation 很重要**。

本文做了啥：我们想知道 **一个NN能否work as universal representations**，咋着才能知道呢？**就看它的 capacity 和 它能解决多少vision 问题 之间的关系**！

详细一点：单个NN能够解决好多visual domain的问题（from sketches to planktons and MNIST digits），并且只需要normalize the information in the network, by using domainspecific scaling factors or, more generically, by using an
instance normalization layer

## Intro
### 要干啥
只要有了general-purpose representations ，很多vision 问题只需要学习一次就行了。

但 the nature and scope of such universal representations remains unclear，本文就是通过研究 不同应用的DNN的共享程度来 shed some light on this question


要学习到 a single network that works well for _all the problems simultaneously_

### 这么干的合理性
虽然有很多 multi-task scenarios 的情况了
> Our goal, instead, is to check whether extreme visual diversity still allows a sharing of information.

在这种设定下，作者试图investigate _NN的 capacity 和 它能解决多少vision 问题 之间的关系_。
如果problems完全无关，那么size是按比例增加，而 capacity是unbounded increase （也就是需要很大capacity的model）。
如果problem有重叠，那么 _complexity growth gradually slows down, allowing model complexity to catch up_。在极限情况下：
>universal representations become possible

### 两个微小的贡献
1. 通过实验证明，NN的capacity可以很大
2. 参数共享需要 normalize information carefully, in order to compensate for the different dataset statistic

## Method and Experiments
此部分有很多细节性的东西，如Batch and instance normalization，好多术语如Batch purity

在 _3.3. Training regime_ 中，作者提到，对于每一个 domain，其 batch  都会被SGD用到，因此每个domain 实际用到的 traning example的数目是一致的。
这就对应于 _weighing the domain-specific loss functions equally_ 。

>Finally, note that architectures may only partially share features, up to some depth. Obviously, domain-specific parameters are updated only from the pure batches corresponding to that domain.

在 Experiments 中，所有图片都要  resize 成 64 × 64的。而且dataset需要白化：减去均值除以标准差。

网络架构：_Residual Networks_

实验结果部分一直在强调 _normalization_。

## Conclusions
universal models 的一个组成部分就是  universal representations， 本文探讨的就是这个东西 i.e. feature extractors that work well for all visual domains, despite the significant diversity of the latter。

作者认为， NN 的前几层可以认为是 feature extractor。

本文表明，只要加了 _normalization parameters以及domain-specific scaling factors, in order to compensate for inter-domain statistical shifts_ ,就可以实现 information sharing 即NN结构和参数的共享。

## 总结与感悟
这篇文章应该是作者使用DNN时很自然的想法，作者结论成立的一个重要前提是DNN的capicity很大，经得起各种结构性改变的 _折腾_ 
实际上这个结论也是可以预料到的，domain不同，当然需要对参数进行特别的调教，这种调教恰好可以由normalization来实现。

没有啥神秘的。
