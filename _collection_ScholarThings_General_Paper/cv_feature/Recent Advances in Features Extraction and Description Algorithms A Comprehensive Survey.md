--- 
title: Recent Advances in Features Extraction and Description Algorithms A Comprehensive Survey
date:   2017-03-21
---



* content
{:toc}

## Intro
The concept of feature detection and description 
>the process of identifying points in an image (interest points) that can be used to describe the image’s contents such as Edges, corners, ridges and blobs.

主要用于：
>object detection, analysis and tracking from a video stream to describe the semantics of the its actions and behavior.

## Definitions and principles
### Local features
>Local image features (also known as interest points, key points, and salient features) can be defined as a specific pattern which unique from its immediately close pixels, which is generally associated with one or more of image properties [5] [6]. Such properties include edges, corners, regions, etc

Local image feature之所以成为一个feature，就是因为它和临近它的点相比非常unique，即有代表性，而且经常和一些image properties相关联（如edges, corners, regions）

这些feature最终都是要转化成数值的。

![](RecentAdvancesinFeatures\feature_illu.png)

### Ideal Local Features
根据intensity pattern计算出来的，要满足很多特性
![](RecentAdvancesinFeatures\feature_quality.png)
facts, etc.), it is often sufficient to make detection algorithms
less sensitive to such deformations (i.e. no drastic decrease in
the accuracy)

其中Repeatability是最重要的，只要改善了其它任何一个就会改善Repeatability。
但不同的应用可能依赖的特性不一样。
distinctiveness and locality are competing properties
Efficiency and quantity are another example of such competing qualities.

### Feature Detectors
有很多review了。但no ideal detector exists until today.
the most important local features include：edge，corner，region。并且，这些local features是强相关的。

最重要的俩：MSER and the SIFT algorithms
![](RecentAdvancesinFeatures\feature_summary.png)

![](RecentAdvancesinFeatures\feature_performance.png)
