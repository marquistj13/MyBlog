--- 
title:  Fuzzy clustering in parallel universes
date:   2017-6-14
---



* content
{:toc}

这篇文章净扯淡啦。
本文算法基于FCM的目标函数。关注outlier的处理，即noise detection。
所谓parallel universes的实现，其实就是根据文献Dave [7], 提供的方法，将noise  cluster在目标函数中单独给一个项，即(6)式。 这些noise所在的空间就是auxiliary universe。
而原始FCM的目标函数只考虑了一个universe，因此，作者也把FCM的目标函数小修了一下。即引入一个矩阵以encoding the membership of patterns to universes，通俗的讲，就是这个点对这个universe的隶属度。

试验也很的简单
不过本文的想法倒是很好，找出noise，并显示地去除其影响。
可惜有点麻烦？

