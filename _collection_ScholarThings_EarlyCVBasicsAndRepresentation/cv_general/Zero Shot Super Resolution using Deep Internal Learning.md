--- 
title: Zero-Shot Super-Resolution using Deep Internal Learning
date:   2017-12-20
---



* content
{:toc}


## 主要内容
项目主页：http://www.wisdom.weizmann.ac.il/~vision/zssr/

网络功能：给定一个 lower-resolution 的 image， 输出一个 high-resolution 的 image， 即 从 LR 到 HR.

既然是"Zero-Shot"， 那么训练数据咋整？ 给定一个输入图像，先将其降采样成略小一点的图像序列，其中每一个图像作为 HR, 再将其scale-factor成 LR，这样就得到了一个 Lr-Hr 序列作为训练数据。
然后每一个LR-HR pair都可以再旋转镜像。
这样一个单一的test image就得到一堆训练数据。"Zero-Shot"大功告成。

这么搞还有一个reason。即The Power of Internal Image Statistics。
由于网络的最终任务是从 LR 到 HR.
而作者发现
>small image patches (e.g., 5x5, 7x7) were shown to repeat many times inside a single image, both within the same scale, as well as across different image scales.

因此，只需要一个图像就行了。

## 网络结构
用8个隐含层的纯CNN（因此对输入的size不做要求）。

## 总结和借鉴
总结：
本文实际上就是将CNN用在了super resolution上面。原则来说没有新东西，因此作者主要将贡献写为
>We introduce the concept of “Zero-Shot” SR, which exploits the power of Deep Learning, without relying on any external examples or prior training.

也就是应用一下。
唯一新的一点我感觉就是敢直接不用新的训练数据。


借鉴和思考：
在成熟的cnn基础上，才可以实现非常high-level的intuition，如本文中的利用small image patches 的重复特性，虽然这个性质可能是作者强加的解释，但毕竟有一点道理。

归根到底还是快速将一个问题转化为 supervised Learning。