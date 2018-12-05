--- 
title: Mapping and localization using GPS, lane markings and proprioceptive sensors
date:   2018-12-5
---



* content
{:toc}


以下来自：
[1]TAO Z, BONNIFAIT P, FREMONT V等. Mapping and localization using GPS, lane markings and proprioceptive sensors[C]//2013 IEEE/RSJ International Conference on Intelligent Robots and Systems. Tokyo: IEEE, 2013: 406–412.

## 摘要
将 GPS 估计值 和 dead-reckoning sensor（航位测量法）的估计进行融合。

本文研究了几个GPS 误差模型，证明他们都是可观的（observable），并在定位器中使用shaping filters进行试验，。

本文使用的是 L1-GPS （ mono-frequency receiver with C/A pseudo-ranges）
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
