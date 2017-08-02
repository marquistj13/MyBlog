---
layout: post
title:  安装keras和tf
categories: 深度学习
tag: [Python]
---

* content
{:toc}

## 第一次装TensorFlow
现有环境：canopy 2.7版本，然后手动安装py3.5
在win10上，用预编译版本安装mxnet老是不成功啊。
安装TensorFlow倒是很容易（按照绿绿的教程 https://github.com/VectorSL/tensorflow ）：，不过我原来一直用python2，在win上安装TensorFlow只能用3.5（https://www.tensorflow.org/install/install_windows ）
我想用keras作为前端。
虽说keras支持Python 2.7-3.5，但我用python3装keras一直不成功，只能用python2装了，但我的TensorFlow只能在py3里调用，所以很尴尬，看来keras只能用自带的theano后端了。
ps.我搜到的解决方法要么是只有一个py3环境干活的，要么是非win平台的。（虚拟py环境貌似也只用一个py版本吧）。
好了，安心学TensorFlow吧。


## 问题的爆发
在 https://www.tensorflow.org/api_docs/python/ 看到了tf.contrib.learn.KMeansClustering，因此就像运行一下这个tensorflow/tensorflow/contrib/learn/python/learn/estimators/kmeans.py目录下的kmeans_test.py，但是运行的时候老是提示scipy有问题
```
File "scipy\linalg\setup.py", line 20, in configuration
        raise NotFoundError('no lapack/blas resources found')
    numpy.distutils.system_info.NotFoundError: no lapack/blas resources found
```

在用 `python 3 -m pip install scipy` 重装scipy不成功，很无奈啊


这时候我发现canopy有3.5版本的，遂安装了一下，人家没有把python加入path，所以没法直接在cmd中调用Python，然后想到以后可能跟各种Python版本打交道，我就因为这个把用了将近三年的canopy卸载了，今天下午一直重装了好几次canopy，哦哦。
马后炮：canopy的virtual env功能并不友好，详见[Canopy Command Line Interface (CLI)](http://docs.enthought.com/canopy/configure/canopy-cli.html)。

## 启用anaconda 安装TensorFlow和keras （此为y3.5的情形，已过时，现在tf1.2.1已经支持py3.6了）
* TensorFlow
据说anaconda创建新的py环境特别简单方便，试一下吧。

下载anaconda3时装的是py3.6，而TensorFlow要求Windows上需要安装py3.5，因此，按照 [conda官方:Managing Python](https://conda.io/docs/py2or3.html) 的指示
打开 anaconda prompt,
先创建py3.5的环境:`conda create -n py35 python=3.5 anaconda`,这样就装了py3.5最新版即py3.5.3, 同时也安装了anaconda
，在 `Anaconda3\envs` 下就有了 py35这个文件夹，然后 `activate py35` 就行了。

然后根据 [tensorflow 官网](https://www.tensorflow.org/install/install_windows) 的建议
>In Anaconda, you may use conda to create a virtual environment. However, within Anaconda, we recommend installing TensorFlow with the pip install command, not with the conda install command.

即，先创建一个py3.5的环境，然后用pip安装，而不用conda安装（conda也是一种包管理器）。
    ```
    pip install --upgrade tensorflow-gpu
    ```
注意，由于我的py35环境的pip就是pip3了，因此，此处直接用pip就行了。

有可能会出现如下错误：
 >   FileNotFoundError: [WinError 2] 系统找不到指定的文件。 一堆路径然后 setuptools-27.2.0-py3.5.egg
    
此时只需要`conda install setuptools`就行了。
如果还不行就再运行一次`pip install setuptools`
    

然后继续`pip install --upgrade tensorflow-gpu`,就安装成功了。

注：用conda创建新的环境的时候可以指定需要安装哪些版本的各种库。详见：[Managing packages](https://conda.io/docs/using/pkgs.html)

* keras
安装Keras `pip install keras`,直接就可以用TensorFlow的后端了。

## 在jupyter notebook中使用tf
由于我用conda创建py35环境的时候同时安装了anaconda，即用的是 `conda create -n py35 python=3.5 anaconda` 因此它已经在py35给我安装了ipython 和 jupyter，但不知是和原因，无法成功在jupyter中使用tf，根据 [这篇博客:Windows环境下安装TensorFlow并在Jupyter notebook上使用](http://blog.csdn.net/index20001/article/details/73555182) 
的介绍(其实[这一篇博客](http://blog.csdn.net/shengyingpo/article/details/70237754)更简洁，看这个就行了)，进入py35环境后，运行下面三个命令：
```
conda install ipython
conda install jupyter
ipython kernelspec install-self --user
```
即可，但上面那篇博客的细节可以不理了，解释的不一定对。实际上第一个命令给我更新了ipython，第二个啥都没做，第三个的输出为：
>[TerminalIPythonApp] WARNING | Subcommand `ipython kernelspec` is deprecated and will be removed in future versions.
[TerminalIPythonApp] WARNING | You likely want to use `jupyter kernelspec` in the future
[InstallNativeKernelSpec] WARNING | `jupyter kernelspec install-self` is DEPRECATED as of 4.0. You probably want `ipython kernel install` to install the IPython kernelspec.
[InstallNativeKernelSpec] Removing existing kernelspec in C:\Users\Marquis\AppData\Roaming\jupyter\kernels\python3
[InstallNativeKernelSpec] Installed kernelspec python3 in C:\Users\Marquis\AppData\Roaming\jupyter\kernels\python3

我也看不出来原因哈，反正能用了。

## update：直接在最新版的anaconda3.6安装tf就行了。
在 https://github.com/tensorflow/tensorflow/blob/r1.2/RELEASE.md 1.2版本的更新中，我们看到从Release 1.2.0开始已经支持 *Python 3.6 support on Windows.*了，只是官方的[安装文档](https://www.tensorflow.org/install/install_windows)没有更新，导致我又用anaconda装了3.5版本的Python和tf。

和py35的情况差不多
先 `conda install setuptools`
然后`pip install --upgrade tensorflow-gpu`(如果还不行就再运行一次`pip install setuptools`)