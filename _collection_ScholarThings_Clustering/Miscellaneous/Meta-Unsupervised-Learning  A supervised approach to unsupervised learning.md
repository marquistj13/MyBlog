--- 
title: Meta-Unsupervised-Learning A supervised approach to unsupervised learning Behavior
date:   2017-03-9
---


* content
{:toc}


## Meta
这篇文章不算宏大，但又不知所云。

## intro
本文搞出一个model来试图搞清楚人类是如何无监督学习的。

可惜的是，作者搞出来的是一个theoretical model，但又没有这个model的建立过程，所以你是无法猜到作者是如何搞出这个东西来的。
让人很为难嘛。

好了，回到作者的approach。我就不原样复述了。
作者的目的就是要思考一下人类是怎么无监督学习的。ml算法和人类的不同有很多，首先是人类在做一个无监督task的时候已经有了很多先验知识，如给这堂课评价一下，这课很无聊还是有趣，对于这个task来说，人类得会用语言来表达，还得知道如何评价。
但是对于ml算法来说，这些东西基本上都是没有的。
用作者的话来说就是：
>In some sense, expecting an algorithm to cluster a small set of text reviews without external data is like asking a person to cluster course reviews written in a foreign language without a dictionary – not only would one have to learn the new language from the reviews themselves but there might not even be enough reviews to adequately cover the language.

基于以上的理由，CV最近的一个潮流就是重用（reuse）预训练的网络。

作者在  _openml.org_ 这个网站的很多数据集上进行试验，发现 K-means 在很多problem都是比较好的。
我还没搞清楚这句话的意思：
>seemingly unrelated collection of problems can be leveraged to improve average performance across datasets

这个比较有趣：
>Finally, we also show how to train a neural network using data from multiple classification problems of very different natures to improve performance on a new UL problem.

## Related work
哈，作者说Kleinberg’s impossibility theorem经常被人争论(debate),   然后作者搞的这个meta-clustering能够避免这个theorem，不过貌似已经有人举出反例说这个theorem是错的了，所以，作者你有点晚了。

## 试验
算法部分实在难以捉摸，我不知道作者在说啥，都是一些definition，也不challenging啊。
哈哈，实验部分你不可能玄乎了吧。

首先是选算法，五个算法来自scikit-learn (K-Means, Spectral, Agglomerative Single Linkage, Complete Linkage, and Ward) ，还用五个是它们五个在normalized的数据集上搞的。用 Adjusted Rand Index (ARI)来选。

啊，来到了第11页。

作者搞出一个least squares linear regression，这个回归的原理很简单，y就是ARI，x就是模型，要求的是权值
最后根据权值选取五个模型中的一个……
就是这样。