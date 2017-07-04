---
layout: post
title:  安装keras和tf
categories: 深度学习
tag: [Python]
---

* content
{:toc}


在win10上，用预编译版本安装mxnet老是不成功啊。
安装TensorFlow倒是很容易（按照绿绿的教程 https://github.com/VectorSL/tensorflow ）：，不过我原来一直用python2，在win上安装TensorFlow只能用3.5（https://www.tensorflow.org/install/install_windows ）
我想用keras作为前端。
虽说keras支持Python 2.7-3.5，但我用python3装keras一直不成功，只能用python2装了，但我的TensorFlow只能在py3里调用，所以很尴尬，看来keras只能用自带的theano后端了。
ps.我搜到的解决方法要么是只有一个py3环境干活的，要么是非win平台的。（虚拟py环境貌似也只用一个py版本吧）。

好了，安心学TensorFlow吧。