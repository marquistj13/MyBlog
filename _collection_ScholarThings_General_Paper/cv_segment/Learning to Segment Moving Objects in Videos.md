--- 
title:  Learning to Segment Moving Objects in Videos
date:   2017-6-22
---



* content
{:toc}

一篇cvpr2015
就不仔细看了。
大概思路就是intro和论文图1所示：
先用 optical flow +  boundary detector 检测物体的boundary。
接下来就是 object detection了，作者提出的 每一个帧的 Moving Object Proposals (MOPs) 提高了物体检测的准确率。
最后，由于我们要分割移动物体，因此，要将per frame MOPs and static
proposals 搞成space-time tubes，这我就不关心了。

对于Proposal of regions的处理，作者训练了一个CNN来识别“Moving Objectness” （网络结构为图3）。


总结一下，本文主要依赖传统的处理流程，因为video的移动物体分割很难搞成end2end的么？这个我不清楚啦。
对我比较新鲜的就是，在中间环节插了一个CNN，也就是说，人家只是像利用traditional ml algorithm那样做了一个regression。





