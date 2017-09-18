--- 
title: 目标函数设置的一些小技巧
date:   2017-9-18
---



* content
{:toc}


## 直接相乘
在论文Bahrampour S, Moshiri B, Salahshoor K. Weighted and constrained possibilistic C-means clustering for online fault detection and isolation[J]. Applied Intelligence, 2011, 35(2): 269-284.
的第四页提到，由于要对时间序列进行聚类，因此聚类时需要考虑时间信息，即聚类时不仅要考虑相似度，还要加入一个constraint，即同一个cluster中的点还要求必须来自successive time points.
作者是这么搞的：
![](toconstraintheobjectfunction\formula8.png)

很显然，要想让总的目标函数小起来，在 $d_{ij}$ 大的时候，隶属度 $\mu_{ij}$ 必须小，同时 和时间限制有关的 $A_i(t_j)$ 就得大， $(t_j-\alpha_i)^2$ 就得小，也就是逼迫时间很近，即该点与聚类中心的时间上的距离很近。