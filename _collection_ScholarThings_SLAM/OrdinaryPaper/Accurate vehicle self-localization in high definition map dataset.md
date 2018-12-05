--- 
title: Accurate vehicle self-localization in high definition map dataset
date:   2018-12-4
---



* content
{:toc}


以下来自：
Zang, Andi, Zichen Li, David Doria, and Goce Trajcevski. “Accurate Vehicle Self-Localization in High Definition Map Dataset.” In Proceedings of the 1st ACM SIGSPATIAL Workshop on High-Precision Maps and Intelligent Applications for Autonomous Vehicles  - AutonomousGIS ’17, 1–8. Redondo Beach, California: ACM Press, 2017. https://doi.org/10.1145/3149092.3149094.


## 摘要
自动驾驶需要对vehicle进行实时定位，称为self-localization or ego-localization
为了在各种条件下维持可靠性
1. harsh conditions and environmental uncertainties (e.g. GPS denial or imprecision),
2. sensor malfunction,
3. road occlusions,
4. poor lighting,
5. inclement weather.

系统需要包含
1. GPS receiver,
2. in-vehicle sensors (e.g. cameras and LiDAR devices)
3. 3D High-Definition (3D HD) Maps

本文综述了自定位技术，并提出一个数据集 `10km of the Warren Freeway in the San Francisco Area`
设备为：
1. 消费级单目相机
2. 消费级GPS
3. 产品级（production-grade）3D HD Maps

## Intro
两种常用的基于点云的定位：
1. LiDAR 可直接获取 3D 信息，缺点是cost and weather dependency
2. 从 2D stereo camera （双目或多目相机）亦可以重建 3D 信息，

亦可以通过检测以下object进行定位
1. lane markings ， 
2. pole-like objects , 
3. curbs , 
4. even occupancy grids

有了 HD map，可以通过triangulation使用特征进行定位。

###  DATASET DESCRIPTION
#### Vehicle and Sensor Configuration
包含一个校准过的 HERE True platform，__用来提供真值__
> Velodyne 32 LiDAR unit, 高分辨率相机，高分辨率定位单元

能得到：
1. well-registered point clouds
2. street view imagery

还有
1. 消费级的 dash camera
2. 消费级的 GPS

camera和gps的位置关系未给定。

已经将真值，dash camera，GPS的数据进行时间戳同步（对齐）。

#### High Precision Map Modeling
将road 分为 12米长的段。

并提供了包含三部分的road model：
1. Lane Boundary。 lane marking 以及 路肩都有。
2. Occupancy Grid:light poles, road signs, and overpass bridges,等的occupancy grid
3. Road Sign：限速标记，路段确认等。