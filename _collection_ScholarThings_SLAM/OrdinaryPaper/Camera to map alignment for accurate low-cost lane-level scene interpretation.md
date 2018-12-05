--- 
title: Camera to map alignment for accurate low-cost lane-level scene interpretation
date:   2018-12-5
---



* content
{:toc}


以下来自：
[1]GAOYA CAO, DAMEROW F, FLADE B等. Camera to map alignment for accurate low-cost lane-level scene interpretation[C]//2016 IEEE 19th International Conference on Intelligent Transportation Systems (ITSC). Rio de Janeiro, Brazil: IEEE, 2016: 498–504.


## 摘要
其他方法基于
1. expensive detailed 3D maps
2. precise绝对位置估计传感器

本文基于state-of-the-art map data（应该就是普通的2d地图），以及便宜的position estimation 传感器，如 GNSS，来改善定位。
本文仅利用road boundary的shape作为landmark。

先从地图数据推断road geometry，然后和前置相机对齐（align）。
这个对齐就是要对比：
1. 相机的 real road view  
2. 由地图生成的 virtually generated road views 

## 算法部分

### Map Representation 
本文要根据地图数据improve GNSS 的定位，有俩不确定性来源：
1. GNSS 的定位数据
2. 低精度的map data （这些是publicly available map data，如OpenStreetMap）


要根据估计的车道和路宽，来估计road shape 的 actual geometric road shape。
### View Generation
在rough GNSS 位置的周围，允许六个自由度的variation，来生成candidates。
六个自由度：
>1. a lateral, a longitudinal and a vertical shift 
2. a rotation around all three axis.


candidate 的分布可以是随机、高斯或基于抽样的如RANSAC。
### Visual Alignment
#### HOG
使用 HOG 算法来 capture edge structures，例如 road boundaries。

在 virtual view candidate 以及相机图像上都进行以下处理
1. 预处理：Canny edge detection，并使用图像normalization算法，如gamma compression。
2. HOG （实际上，只要是基于orientation的filter都行，只是HOG简单而已）。

#### Candidate 比较
这一步实际就是比较两个向量 的局部朝向 的相似度。
就是余弦相似度啦。

## 结果

数据集 KITTI

### Single Picture Alignment
结果很好。

### Trace Evaluation
对于每一个 GNSS 位置，需要生成 155 个均匀分布的 candidates。
纬度方向：[-1.5 m, 1.5 m] 经度方向： [-0.1 m, 0.1 m]


### Statistical evaluation
为了评估维度方向的稳定性，利用KITTI 的 GPS Trace 作为真值。
结果表明：
>adaptive candidate range [-sGPS, sGPS]  is outperforming the constant candidate ranges.

## 结论
有shadow 的地方效果不好
要想 robust alignment，最好是 adaptive candidate range（就是生成candidate的那一步）。


