--- 
title: Explaining the Performance Potential of Rule-Based Fuzzy Systems as a Greater Sculpting of the State Space
date:   2018-1-5
---



* content
{:toc}

## 前言
Mendel老先生的新作。

哦，虽然看了好多fuzz的文章，还是有很多地方看不明白，先看个大概吧。

## 正题
有大量论文奖原先用 type-1 fuzzy set的模糊系统 变到 type-2 fuzzy set， 还伴随着性能的提升。
而且用了fuzzy system比crisp system就好一点了。

至于为何会这样呢？

作者在简介中先总结出以下解释
1. fuzzy system本质上是非线性的
2. fuzzy system很容易输入空间获得smooth transitions（因为mf函数有重叠嘛）。
3. type-1 fuzzy system 的design degree 比 非fuzzy system的大，type-2的又比type-1 的大。

但以上解释都没有严格的讨论。

本文的目的是提供一种解释。
目前只解释T1 and IT2 fuzzy systems，无法解释GT2 fuzzy systems。
但本文也没有提供prove，只是抛出来一个结论而已。仍需 future research。


概括来说，相比于crisp rule-based system，我们的T1 fuzzy system能够将state space雕琢地更精细。


同样，IT2 fuzzy system 比T1的有更多variability。

所谓状态空间估计就是输入空间吧。

## 具体
作者从partition的角度来展开。
介绍了Uncertainty partitions，First-and second-order rule partitions，Novelty partitions 共三种。

### Uncertainty partitions
只看公式 （4） 就行了，即对于firing level来说，T1 fuzzy system是线性组合的，IT2 fuzzy system是quadratically组合的。

至于第二页的Crisp partitions，作者提的并不多，只说了不允许考虑区间的不确定性。

### RULE PARTITIONS
不细看了，主要结论在第九页
这一小节的主要任务是数数，即rule partition的数目，这一节就是围绕数数展开的。
很显然rule的数目越多，越好吧。

### NOVELTY PARTITIONS
对于涉及到 type reduction的IT2 fuzzy systems，还可以对输入空间进行进一步的划分。


不仔细看了。



## 结论
本文的结论就是，能将输入空间划分地更精细，那就对性能提升更多。
