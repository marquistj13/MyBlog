--- 
title: 新奇的框架or算法汇总
---



* content
{:toc}

本页面维持一个论文列表，即我所遇到的比较有意思的框架或算法

[Deep Forest: Towards An Alternative to Deep Neural Networks](https://arxiv.org/abs/1702.08835)

Zhi-Hua Zhou大神17.2.28的arxiv，看名字也知道,就是要搞出来一个和DNN平行的架构，当然你必须得避免DNN的重大缺陷才有意义：
1. 只需要 small-scale training data
2. 作为一个 treebased approach, gcForest比DNN的理论分析更简单。

[A Roadmap for a Rigorous Science of Interpretability](https://arxiv.org/abs/1702.08608)
随着ml系统在复杂状况下的deployment，ml系统除了accuracy等可以量化的指标外，还存在安全性等很难量化的指标。
例如对于无人车的驾驶，咱们无法穷举所有路况（enumerate all unit tests）来检验其安全性。
这时候一个fallback（应急预案）就是interpretability。即，如果一个系统能够explain its reasoning，我们就可以验证它的reasoning is sound with respect to these auxiliary criteria.

本文目的：搞出interpretability的定义以及rigorous evaluation
