--- 
title: Clustering: Science or Art?
date:   2017-5-18
---


* content
{:toc}

## 摘要
本文指出，聚类算法的评估应该考虑上下文，即应用
不能将clustering当做application-independent mathematical problem

因此本文搞出一些taxonomy，用来identify能够统一对待的clustering applications。

## Intro
要想好好讨论一个问题，好好讨论就是 _clear and productive_ ， 那么最好先定义一些量化指标，如precision or objectivity or repeatability or confidence 

聚类咋定义呢？
将instance赋给一些没有预先定义的class，这些class要预期能够reflect the underlying structure"

Clustering relates data to knowledge and is a basic human activity，并且对于理解世界是非常fundamental的。


搞了很多domain independent clustering techniques，但是practitioners一直不看好啊，因为 its lack of relevance。


The loss function can be viewed as an abstraction of the ultimate end-use
problem. 但abstraction有很多种，没有一种能够够真正反映the end-user intent

到底啥是“right" clustering?
有人说了，the right answer is determinable by the data (alone, without reference to intended use):the data should vote for their preferred model type and model complexity"
但Philosophical analysis of “natural kinds" reveals substantial difficulties。

## 正文

### 两个例子
首先，作者说明了现有的评估方法不合适。
然后提出要考虑到clustering用来干啥的。

例如我们可以考虑以下两种应用场景。

* 其一，用来预处理
现在聚类只是作为整个过程的一个参数。
聚类效果好不好，和它有没有discover “meaningful groups" 无关。
只要整个过程的效果好就行了。

* 其二，用来exploratory data analysis
咋玩儿呢？一般需要可视化一下，能够让一个human use hopefully detect a pattern
如何衡量performance呢？让一个human根据聚类结果做一个hypothesis，然后在一个独立的data上来evaluate这个hypothesis的quality。
作者提到了大名鼎鼎的t-SNE


###  问题来了，咱们是否可以直接optimize the “usefulness"？
和作者想法最接近的是The information bottleneck approach。
但这个approach也是很不直接的。

### 和usefulness相关的一些meta-criteria咋样？
对于Stability，Convergence，Generalization bounds，Statistical significance这些用来handle the statistical uncertainty in the data的criteria来说，_和usefulness of a clustering有啥关系呢_？

当然取决于用法，如果作为预处理，那么只要整个system能work，这些 _statistical
considerations _ 就没啥卵用。

在“discovering structure" 这个用法上，人们没法用无限时间来穷举所有有意义的clusterring，因此statistical significance is important。
但statistical significance is a necessary (but not sufficient) criterion for
an algorithm to be useful.

## A suggestion for future research
identify 问题 有时候比 解决问题更重要。
 techniques有时候很重要，但 knowing when to use them and why to use them are more important.

作者强调，要系统性地搞出一些距离问题的catalog，但细节不表，仅仅列出这些聚类应用应该有以下几个特点（dimension），注意以下特点一般都是两方面都有的。
* Exploratory | confirmatory
* Qualitative | quantitative
* Unsupervised | supervised
 这一点很重要，现实中很多聚类问题都是有一定的additional information，如某些特征很重要，相似度的度量等。
* Bias towards particular solutions
  有时候仅仅想 join similar data points，但有时候又仅想separate different points
* Modeling the data-generating process.




