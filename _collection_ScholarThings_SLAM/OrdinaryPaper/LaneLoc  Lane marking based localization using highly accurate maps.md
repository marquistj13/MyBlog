--- 
title: LaneLoc Lane marking based localization using highly accurate maps
date:   2018-12-5
---



* content
{:toc}


以下来自：
Schreiber, Markus, Carsten Knoppel, and Uwe Franke. “LaneLoc: Lane Marking Based Localization Using Highly Accurate Maps.” In 2013 IEEE Intelligent Vehicles Symposium (IV), 449–54. Gold Coast City, Australia: IEEE, 2013. https://doi.org/10.1109/IVS.2013.6629509.



## 摘要
GNSS 在市区无法达到分米级的精度。
本文使用stereo camera、包含curbs（路边） and road markings的高精地图、以及IMU data实现此精度需求。
（使用GNSS做初始化）

至于 IMU 用来干啥了，文中应该没有显示地提到，在 Kalman Filter 那一节中的 yaw rate就是惯导提供的。。

本文中实验用的是自己建的地图。

## MAPPING
Mapping 和 online localization 是完全分开的。
mapping的时候用高精度GNSS，并使用360度的velodyne laser得到complete road geometry（包含交叉路口等）。

俯视的广角相机，然后进行lane detection，
相机视角较小，远处的lane以及road boundary由lasers canner的图像来获取。


由于分辨率和对比度的原因，这些marking 信息得 __手动标注__。


## ONLINE LOCALIZATION
### 基于 Kalman Filter 的定位模型
状态矢量为静止坐标系（stationary coordinate system）中的一个二维位置 $(X,Y)$，以及车辆在此坐标系中的偏航角 $\varphi$，地图上的点也是处于这个坐标系。
状态方程很简单，就是一个线性的离散更新方程。

地图坐标系旋转一下就变到车辆坐标系啦。

残差的计算需要在车辆坐标系进行。
我们用相机等算的点基本上都是相对于车辆坐标系的，因此需要将地图点转化到车辆坐标系。

测量模型描述了所有测量点的期望位置 $h(\vec{x}_{veh})$ （注意这个 $h$ 函数隐含了地图坐标系到车辆坐标系的变换）与对应的车辆坐标系的测量 $\vec{y}$ 之差：
$$\vec{r}=\vec{y}-h(\vec{x}_{veh})$$

测量模型的方差为地图方差+相机高度和朝向导致的back-projection噪声之和。

### Map Matching
地图里 markings 以及 curbs 都是用 line segment表示的。
我们的测量值是点。
这就涉及到 line segment 和点 进行匹配的问题。

文中将line segment采样成几个点，然后再进行匹配。

#### Lane Marking 的测量
使用oriented matched filter检测lane marking（对于遮挡的marking的处理：就是不处理，使用Freespace忽略掉遮挡区域）。

首先根据当前的状态向量，将地图（其实就是地图里的line segment）投射到图像上，
然后将search lines放到lane marking的期望位置（应该就是上面投射后的line segment吧）附近，
此时，oriented matched filter就能检测到图像中的lane marking了
然后根据stereo 相机的深度信息，将检测到的lane marking投射到road上，即变换到车辆坐标系，这样就得到了上一小节（即  `基于 Kalman Filter 的定位模型`)中的测量值。

#### Curb Measurement
使用以下文献的方法：
>P. Greiner, M. Enzweiler, C. Knoeppel, and U. Franke, “Towards multicue
urban curb recognition,” in IEEE Intelligent Vehicles Symposium,
Gold Coast, Australia, 2013

## EVALUATION
### Evaluation on Test Track
此数据集比较完美
>50 km，平稳路段，没有curbs and other traffic，Road markings特别明显。

对于online localization的精度，
每个图像中，可测量前方15米的范围

在此数据集上，mean residual 达到了 7.0 cm 的精度。

### Evaluation of Road Dataset
系统启动的时候用GNSS的均值进行初始化（就是初始路段的均值)。

mean residual为 11 cm,  大概是 11 个像素点。

误差大的地方主要是维度误差较大，这些地方基本上只有solid line，或者遇到dashed segment or stopline 的时候。

注：我们的高清地图是 10 cm 级的。

