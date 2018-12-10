---
layout: post
title:  Nemodrive 的方案参考
categories:  [定位]
tag: [方案借鉴]
---

* content
{:toc}

## 简介
### 自动驾驶简介
偶然间看到了 [NEMODRIVE​ Research group profile](https://drive.google.com/file/d/1yWkDq0IJqZidsn_MuNnuc3hYxtKR127t/view)，
此处提到，第一个自动驾驶是1961年的the Stanford Cart，它使用camera进行避障导航。

50年以来，学术界的研究促进了technology的进步，因此很多automotive companies开始参与自动驾驶的研发（R&D).

Autonomous vehicle 并非一个 device，而是一个system, `a collection of inventions applied in a novel way.`
>The real job is to endlessly improve the software part, powered by machine learning algorithms, to correctly interpret the data from all those sensors.

### Nemodrive 组的目标和方案
此组的目标是：
>building a level 4 self-driving car for the streets of the UPB campus.

此组目前的方案是：
1. enhancing a open autonomous driving platform (__Apollo Auto__) for __better localization__
2. testing the framework with a simulator
3. integrating it with the car 
4. and many more.

### 方案的可视化
这几个方案对应了几个图，很漂亮，来自[Research perspective](https://nemodrive.cs.pub.ro/research/):
#### Enhance localization using vision
![Enhance localization using vision](https://nemodrive.cs.pub.ro/wp-content/uploads/2018/09/new2.png)
#### Object detection and depth estimation
![Object detection and depth estimation](https://nemodrive.cs.pub.ro/wp-content/uploads/2018/09/nou.png)
![Object detection and depth estimation](https://nemodrive.cs.pub.ro/wp-content/uploads/2018/09/2-1.jpg)
#### End to end driving. Determine steering, acceleration & brake from images
![End to end driving. Determine steering, acceleration & brake from images](https://nemodrive.cs.pub.ro/wp-content/uploads/2018/09/3.jpg)
#### Enhance real data planning decisions using a simulator
![Enhance real data planning decisions using a simulator](https://nemodrive.cs.pub.ro/wp-content/uploads/2018/09/4.png)

## 定位
以下来自：[Localization for Autonomous Vehicles](https://aimas.cs.pub.ro/file/2018/10/Autonomous-Driving-Localization-for-Autonomous-Vehicles-AIMAS.pdf)

Apollo framework 中，GNSS和IMU 只能提供 __3米__ 的定位精度，而自动驾驶一般要求小于 __10 cm__ 的误差。
怎么解决呢？两个阶段
### 第一个阶段
__目前打算利用 UPB campus的矢量地图（vector map）+ GNSS和IMU提高精度。__
（还提到可以利用基于神经网络的vision algorithms，没提细节）

### 第二个阶段
__使用Camera与 3D-LIDAR, cameras, GNSS and IMU 的组合__
如文献：
>[5] Seif, Heiko G., and Xiaolong Hu. "Autonomous driving in the iCity—HD maps as a key
challenge of the automotive industry." Engineering 2.2 (2016): 159-162.


由于 CNN 还没成熟到可以在商用自动驾驶上进行部署，目前只能将 DL 用于替换经典 SLAM pipeline的某些部分。
如：
>[3] Milz, Stefan, et al. "Visual SLAM for Automated Driving: Exploring the Applications of Deep
Learning." Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition
Workshops. 2018.
[4] Heng, Lionel, et al. "Project AutoVision: Localization and 3D Scene Perception for an
Autonomous Vehicle with a Multi-Camera System." arXiv preprint arXiv:1809.05477 (2018).


目前该组打算利用[Apollo Ego Localization](https://github.com/ApolloAuto/apollo/tree/master/modules/elo)，以及这些知识：
>sensor fusion, Kalman filtering, Particle filters, robot modeling, machine learning


## 研究目标（可以借鉴啊）
在open-source自动驾驶平台上搞一个改善的 localization module that uses GNSS, IMU and 2D Camera data。
1. 实现多传感器融合的定位方法
2. 建立高清地图
3. 探索SOTA的多常感器自定位算法，并部署。

原文
>1. Deploy and evaluate on _UPB campus_ a multi-sensor fusion localization method (GNSS,LiDAR and IMU).
1.  Build the _UPB campus_ HD Map.
1.  __Explore state-of-the-art full sensor ego localization algorithms__ and deploy a practical solution for a self-driving car on _UPB campus_.

上面提到的 _UPB campus_ 在这里：
![](https://nemodrive.cs.pub.ro/wp-content/uploads/2018/09/Poza4-1.png)
![](https://nemodrive.cs.pub.ro/wp-content/uploads/2018/09/Poza2-1.png)