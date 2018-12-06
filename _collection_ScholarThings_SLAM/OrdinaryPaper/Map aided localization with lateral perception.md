--- 
title: Map-aided localization with lateral perception
date:   2018-12-5
---



* content
{:toc}


以下来自：
[1]GRUYER D, BELAROUSSI R, REVILLOUD M. Map-aided localization with lateral perception[C]//2014 IEEE Intelligent Vehicles Symposium Proceedings. MI, USA: IEEE, 2014: 674–680.

## 摘要
使用两个 纬度方向（侧面）的相机（lateral cameras）估计 Road markings 和 车身的距离，
然后利用地图数据，使用 EKF improve “根据 惯导系统 和 GPS 得到的”位置，


注意：本文的算法仅能用于单车道，也就是不能变道。

## Intro
为了得到分米级的定位，本文算法融合了：
1. 定位数据
2. road marking检测
3. 左右车道线的地图（即车道线的edge）

## 车载设备
设备：
1. 左右两个俯视相机，用来拍车道线
2. 1Hz 的GPS
3. 66Hz 的惯导系统（加速度传感器、陀螺仪）
4. 20Hz 的里程计（测距用）
5. 轴编码器（测量车轮steering的角度）

地图：
没说地图怎么来的。
转弯的地方5m一段，直路20米一段。
共 __3.5 km__。

## 使用 左右两个俯视相机 检测 ROAD MARKING
改进了如下文献的算法：
>S. Nedevschi, V. Popescu, R. Danescu, T. Marita, and F. Oniga,
“Accurate ego-vehicle global localization at intersections through
alignment of visual data with digital map,” IEEE Transactions on
Intelligent Transportation Systems, vol. 14, no. 2, pp. 673–687, 2013

原算法分三步：
1. 提取road primitive：提取lane marker对应的像素点，并将其转换到车体坐标系
2. 检测lane marking：根据第一步的点的分布，确定可能的lane的中心
3. 估计lane shape：利用 __多项式拟合__ 估计车体的 __偏航角__ 以及 __与lane的距离__。

本文使用两个基于intensity 的 extractors （the Median Local Threshold MLT and the Symmetric Local Threshold）来改善第一步。

## 定位
EKF 的状态为：
$$X_k = (x_k, y_k, \theta_k)^T$$


预测方程采用 dead reckoning 方法，利用 轴编码器、里程计、以及惯导提供的偏航角速率计算。
仅利用这些东西很不准，再加上 GPS 才能准一点，但仍然无法达到 lane-level 的精度，即估计的位置很可能位于车道线之外。

## 利用 LANE MAP
需要根据 vehicle 估计位置，利用基于 point-to-segment 的Map-Matching来选择 map 的 lane segment。

前面的图像处理部分（即`使用 左右两个俯视相机 检测 ROAD MARKING`）得到的是局部测量坐标，怎么将其转化为绝对坐标呢？
这里使用cartography matching 算法：根据lane marking 方程得到了相机与marking之间的距离，并得到距离相机最近的路边点（相机坐标系， $P_1,P_2$，只研究这俩点就行了）在车辆坐标系的坐标。

然后计算雅可比矩阵和测量误差。

EKF 结束。

## 实验部分
lateral position 的估计误差，平均小于 10 cm。



