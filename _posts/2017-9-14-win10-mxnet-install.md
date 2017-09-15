---
layout: post
title:  在win10安装mxnet GPU版本
categories: 深度学习
tag: [Python,Tensorflow]
---

* content
{:toc}

## 安装mxnet
mxnet官方文档的[Installing MXNet in Windows](https://mxnet.incubator.apache.org/get_started/windows_setup.html) 貌似很久没有更新了，反正按照这个文档我都没按照成功过，话说你啥时候更新啊，我要是早知道可以用pip安装就不用这么折腾了，哎。

在 gluon的 [安装和使用](https://zh.gluon.ai/install.html#gpu) 提到可以用pip安装了：`pip install --pre mxnet-cu80 # CUDA 8.0`   
也没提Windows能不能这么安装，记得以前在Windows安装预编译版本的mxnet是需要按照 https://github.com/yajiedesign/mxnet/releases 的编译过的版本进行安装的(ps这个github的版本我也没安装成功过)。

在[安装和使用](https://zh.gluon.ai/install.html#gpu)最下边看到一个链接：[安装和使用问题讨论和更新](https://discuss.gluon.ai/t/topic/249),里边证实了可以在Windows上用pip安装了，如下：
>9/5 更新 windows pip 安装
目前支持windows 64bit，mxnet和mxnet-cu80都是有的。


好兴奋。
于是根据[安装和使用](https://zh.gluon.ai/install.html#gpu)的介绍进行安装：
>(C:\Users\Marquis\Anaconda3) C:\Users\Marquis>pip install --pre mxnet-cu80
Collecting mxnet-cu80
  Downloading mxnet_cu80-0.11.1b20170911-py2.py3-none-win_amd64.whl (221.8MB)
    100% |████████████████████████████████| 221.8MB 2.3kB/s
Requirement already satisfied: numpy in c:\users\marquis\anaconda3\lib\site-packages (from mxnet-cu80)
Collecting graphviz (from mxnet-cu80)
  Downloading graphviz-0.8-py2.py3-none-any.whl
Installing collected packages: graphviz, mxnet-cu80
Successfully installed graphviz-0.8 mxnet-cu80-0.11.1b20170911

ps我没有用国内的镜像，仍然很快，基本上就是1.1M/s.

根据mxnet_cu80-0.11.1b20170911-py2.py3-none-win_amd64.whl可以猜出来同时支持py2和py3了，反正我装到py3.6了（即最新版anaconda的py版本）

按照[此处](https://mxnet.incubator.apache.org/get_started/install.html)的代码validate，试了一下：
```python
>>> from mxnet import ndarray as nd
>>> nd.zeros((3, 4))

[[ 0.  0.  0.  0.]
 [ 0.  0.  0.  0.]
 [ 0.  0.  0.  0.]]
<NDArray 3x4 @cpu(0)>
>>> import mxnet as mx
>>> a = mx.nd.ones((2, 3), mx.gpu())
>>> b = a * 2 + 1
>>> b.asnumpy()
array([[ 3.,  3.,  3.],
       [ 3.,  3.,  3.]], dtype=float32)
```
总算安装成功了。


## 安装gluon的教程包
根据[安装和使用](https://zh.gluon.ai/install.html#gpu)的指示，下载zip的教程包，并随便解压到一个位置，我把它放到了anaconda的env下边，目录名为 gluon_tutorials_zh，，cmd切换到该目录，并运行：
`conda env create -f environment.yml`
期间，装了py3.6.2还有jupyter，还有一大堆东西，当然都在一个名为gluon的目录下。
其实是创建了一个名为gluon的环境，用的时候只需要 `activate gluon`，试了一下可以运行，这时候gluon_tutorials_zh目录就可以随便放了，因为我们已经用它建好环境了，里边的ipynb都是可以用的。

