--- 
title:  Driver Drowsiness Estimation from EEG Signals Using Online Weighted Adaptation Regularization for Regression (OwARR)
date:   2017-03-01
---



* content
{:toc}

## 总览
### Meta
看到了Chin-Teng Lin挂名的文章，忍不住看一下人家的行文，多多参考嘛
作者中还有U.S. Army Research Laboratory，阵容不小。

本文是一篇 Transfer learning and domain adaptation的应用文章，当然也有新算法，都是套路啊，稍微了解一些就行了。

### 结构
一个偏向application（EEG Signals信号处理）的文章，提出新算法就会有很强的说服力

实验部分从第五页就开始了，貌似看着很良心啊，Evaluation，Preprocessing and Feature Extraction等都有描述，而且Regression Performance Comparison，Computational Cost，Robustness to Noises， Parameter Sensitivity Analysis等都有一个小节进行探讨，

###  abstract写的很好。
首先是需求：_high-performance and robust learning algorithms that can effectively handle individual differences, i.e., algorithms that can be applied to a new subject with zero or very little subject-specific calibration data_
由此引入Transfer learning and domain adaptation的必要性。

然后，本文考虑的是regression问题：_online driver drowsiness estimation from EEG signals_

方法：integrating fuzzy sets with domain adaptation

数据集： simulated driving dataset with 15 subjects 
卖点：本文的方法在calibration data数量、computational cost方面都有提升。

## intro





