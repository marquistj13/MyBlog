--- 
title: Mapping and localization using GPS, lane markings and proprioceptive sensors
date:   2018-12-6
---



* content
{:toc}


以下来自：
[1]TAO Z, BONNIFAIT P, FREMONT V等. Mapping and localization using GPS, lane markings and proprioceptive sensors[C]//2013 IEEE/RSJ International Conference on Intelligent Robots and Systems. Tokyo: IEEE, 2013: 406–412.

## 摘要
一般需要将 GPS 估计值 和 dead-reckoning sensor（航位测量法）的估计进行融合。

GPS 值一般用来系统初始化。

本文研究了几个GPS 误差模型，证明他们都是可观的（observable），并在定位器中使用shaping filters进行试验，。

本文使用的是 L1-GPS （ mono-frequency receiver with C/A pseudo-ranges）
即，民用的，所有卫星都会广播的信号。

## SYSTEM MODELING
### 坐标系
首先介绍了 GPS 坐标系 $R_O$，车辆坐标系 $R_M$，相机坐标系 $R_C$，
以及相机坐标系到车辆坐标系，以及车辆坐标系到GPS 坐标系的变换。
### 运动模型
然后介绍了，dead-reckoning，主要是惯导的数据。
### 相机测量
采用多项式拟合法得到以下物理量：
>lateral distance, the slope, the curvature and the curvature derivative of the detected lane marking.

后边用于定位的有：纬度方向的距离，以及朝向（即lateral distance, the slope）。

## MOBILE MAPPING
使用：
1. NovAtel RTK-GPS （比普通的GNSS精度高一点）
2. IMU
3. 普通相机（和定位时用的一样）

自己提取lane marking的信息。
也就是离线建图，根据上一节**相机测量**部分提取的系数，得到lane marking的位置。

然后利用Douglas-Peucker’s algorithm将提取的lane marking矢量化。
## GPS 误差模型
GPS 定位误差的特性
1. 并非白噪声
2. bias比较明显（大气层传播的延迟）
3. 多径效应（multi-path）

此处给出三个误差模型，即GPS测量误差所遵循的微分方程。

可观性：
>如果一个状态能够和输入输出以及输入输出的有限阶微分用解析方程进行表示，那么该状态可观。
当然，可观性还有基于李微分的定义。


## 考虑了 上一节的误差模型后的GPS 位置
本节给出了存在上一节的误差项时的 GPS 位置的更新方程。

然后使用EKF实现。

## 结果
### 实验设置
使用以下文献提出的 point-to-curve map-matching process,从而找到对应的 lane marking segments
>M. El Badaoui El Najjar and P. Bonnifait, “A road-matching method
for precise vehicle localization using kalman filtering and belief
theory,” Journal of Autonomous Robots, vol. Volume 19, no. Issue
2, pp. 173–191, September 2005.

## 定位结果
首先不用 GSP，只用 相机 和 DR （dead-reckoning）

然后再实验融合了 相机、DR、GPS 的情况。