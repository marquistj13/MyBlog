--- 
title:  Densely Connected Convolutional Networks
date:   2017-10-31
---



* content
{:toc}

## 前言
基于一个intuition：layer之间的short connection越多，越好训练

传统的CNN，如果有 $L$ layers，那么总共就有 $L$ 个connections
本文的network有 $L(L+1)/2$ 个direct connections。

对于每一个layer，前面layer的输出都是它的输入。

## Intro
作者举例，很多CNN，如ResNets，Highway Networks，FractalNets都有共同特点：they
create short paths from early layers to later layers.


本文利用上面的insight实现了一个网络结构，以实现maximum information flow between layers in the network。
![](DenselyConnectedConvolutionalNetworks\fig1.png)

A possibly counter-intuitive effect of this dense connectivity pattern is that it requires fewer parameters than traditional convolutional networks, as there is no need to relearn redundant feature-maps.

Besides better parameter efficiency, one big advantage of DenseNets is their improved flow of information and gradients throughout the network, which makes them easy to train.