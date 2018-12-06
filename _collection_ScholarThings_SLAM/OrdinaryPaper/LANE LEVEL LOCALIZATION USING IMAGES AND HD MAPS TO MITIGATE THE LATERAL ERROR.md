--- 
title: LANE LEVEL LOCALIZATION; USING IMAGES AND HD MAPS TO MITIGATE THE LATERAL ERROR
date:   2018-12-4
---

bundle exec jekyll serve --port 4000 --incremental

* content
{:toc}


以下来自：
Hosseinyalamdary, S., and M. Peter. “LANE LEVEL LOCALIZATION; USING IMAGES AND HD MAPS TO MITIGATE THE LATERAL ERROR.” ISPRS - International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences XLII-1/W1 (May 31, 2017): 129–34. https://doi.org/10.5194/isprs-archives-XLII-1-W1-129-2017.

## 摘要
使用 **map matching 方法**利用 GIS 数据库提高定位精度（accuracy of measured position）。

高清地图的额外信息如车道线可用来减小定位误差

本文
1. 利用相机来检测road boundary
2. 使用color mask来检测road mask
3. 利用Hough变换来拟合road 的左右 boundary。
4. 找到gis数据库中的对应road segment
5. 估计**road boundary的相机坐标**与global坐标（即，经纬度坐标系）之间的单应变换（homography transformation）
6. 估计相机位姿

本文实验中的GPS真值利用Real-Time Kinematic (RTK)得到

## Intro
我们需要估计这三个坐标系的关系
1. platform 本身有一个坐标系
2. road 坐标系以及其他platform的坐标系（local coordinate system）
3. global坐标系（global coordinate system）

GNSS 的缺点：
1. 要想达到分米级精度就很难，需要很高的成本
2. 需要视野开阔

GNSS 没法用的时候还能用 IMU ，但 IMU的会随着时间积累误差。

地图匹配技术经常用来改善GNSS的定位精度。
有了GIS，就能将GPS的测量值投射到GIS的road link上，这样垂直于道路方向（纬度方向）的 GPS 误差就能减少， 但经度方向（道路方向）的位置目前还没法改善。

文献调研
分为两部分：
1. road link的检测
2. platform的定位

## 方法
### 坐标系的关系
后边将会看到，我们需要估计出相机坐标系和global坐标系的变换，然后根据platform 坐标系和相机坐标系的变换关系，就能得到platform的坐标了。

### 寻找对应的Road Segment
离platform最近的 segment之后，我们只需要面对对应于该segment的一条line就行啦。

怎么找啊？
两步走：
1. 先缩小寻找范围，以当前位置为圆心，画个圈，如果一个road segment的vertex不在这个圈里，就排除掉
2. 然后计算当前位置与每一个road segment的距离，取最小的。

platform运动的时候怎么选？
鉴于大多数情况下，当前时刻选的road segment基本上就是下一时刻的road segment，因此只需要将当前时刻选的road segment和下一时刻选的road segment比一下就行了，从他俩中间选一个离当前gps位置最近的。

在传统的map matching中，一般是将gps的测量值project到road segment的中心，本文将起project到road boundaries of the corresponding road segment，然后测量platform 和 road segment的距离。
作者说，因此就能减少纬度误差……

### 检测 Road Boundary
Road Boundary 比 road lanes 检测的优势：
1. Road Boundary 为实线，特征较明显
2. road lanes 是有间断的线（ dashed），还可能被其他车辆遮挡
3. 在某些路段，road mark和 road lane很难区分，并且 lane 的边界很模糊

本文用的是美国的road，左边黄实线，右边白实线

不同光照下，road boundary 的黄色 和白色可能shift到其他color，因此要将RGB先转化成Hue, Saturation, and Value (HSV)空间的值。
利用以下两点，就能将图像二值化，黄色值为1，其他为0
1. 在HSV空间中，某一区间的hue成份对应黄色
2. 太亮或太暗的地方分别对应于Low saturation and high value colors

将high saturation 的地方mask掉，就能得到白实线的mask。


在二值图像的基础上，利用Hough transform来拟合直线
>The Hough transform detect the line that passes through most of pixel pairs and therefore, it detects the most prominent line.

### Lane Level Localization
image space 的摄影几何 和 road 所在空间（object space）的欧式几何之间存在一个单应变换（homography transformation），
这个单应变换可以将图像空间的点转换到road所在的空间。

单应变换的估计，理论上需要四个对应点，或对应的非平行的线，但本文中只有左右车道线，就两条，怎么办？
作者假设road width不怎么变，在此假设下，通过一点的技巧选四个点。
考虑到车体的遮挡，假设camera看到的road的第一个点距离 camera的距离为 $D$，在该点沿着维度方向画一条线，与road boundary相交于 $p1$,$p2$，并假设这两点的距离为 $d$。
假设在另一个地方也沿着维度方向画一条线，与road boundary相交于 $p3$,$p4$，并假设这两点的距离为 $d/2$。
那么这条线和camera的距离就是 $2D$.

这样就得到了image space 和 object space的四个对应点。
若已知camera的内参，且已经标定，则单应变化可分解为旋转矩阵和平移向量。


## 实验
数据集：[Lane Level Localization, University Grand Challenge, 2016](https://conference.eng.unimelb.edu.au/its-gc/)

## CONCLUSION
利用 image content 估计platform 相对于road的位置，然后根据 HD 地图将该位置转化到global坐标系
1. 性能优越于GPS position
2. 减小了位置误差的jump