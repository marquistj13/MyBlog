---
layout: post
title:  Ubuntu cv 环境搭建
categories: [编程,系统环境]
tag: [Ubuntu,OpenCV ]
---

* content
{:toc}


## ubuntu16.04系统安装和配置
### 系统下载
在清华大学开源软件镜像站找到[这个ubuntu16.04的链接](https://mirrors.tuna.tsinghua.edu.cn/ubuntu-cdimage/ubuntu-gnome/releases/16.04/release/),我能访问v6网站，因此直接用浏览器下载，10m每秒。

### VirtualBox 
同样也在清华大学开源软件镜像站，[这里](https://mirror.tuna.tsinghua.edu.cn/help/virtualbox/)

### 和宿主机共享粘贴板
打开ubuntu系统，VirtualBox-设备-安装增强功能，即可让ubuntu和宿主机共享粘贴板。

### 网络设置，使用v6
我的宿主机win10用了倆网卡，无线网卡（连接无线wifi）走v4流量，有线网卡（连接墙壁信号）走v6流量, 注意我的win10之所以可以用倆网卡，是因为有线网卡的v4被我禁用了。

因此，我将ubuntu也设倆网卡（在virtualbox那里设置），一个桥接到无线网卡，另一个桥接到有线网卡，然后在ubuntu中将这俩网络重命名，同样disable有线网卡的v4。

将 [lennylxx ipv6-hosts](https://github.com/lennylxx/ipv6-hosts)的hosts文件附加到`/etc/hosts` 中，然后更新网络（直接重启就行了）。

### 设置清华的源
[这里](https://mirror.tuna.tsinghua.edu.cn/help/ubuntu/)
然后，`apt update`,`apt install build-essential`

### ssh的使用
由于VirtualBox的桌面并不是特别灵活，因此选择口碑很好的MobaXterm，这样既能ssh，也能传文件，装在我的win10上就行了。
比较喜欢的MobaXterm的快捷键，即粘贴命令：Shift+Insert

同时应该在ubuntu安装ssh server:
`sudo apt install openssh-server`

### 设置无图形界面的启动  Booting into text mode in 16.04
为啥有这个需求？
我的ubuntu放在virtualbox中，每次打开的时候主机风扇嗡嗡响，资源占用太多，所以我就琢磨着把图形界面关掉啦。的确有点用。好了，切入正题。

根据[Booting into text mode in 16.04](https://askubuntu.com/questions/870221/booting-into-text-mode-in-16-04/870226)的介绍
可以这么办：
`sudo systemctl set-default multi-user.target`

To return to default booting into X, use
`sudo systemctl set-default graphical.target`

To see the current default target,
`sudo systemctl get-default`

答主给的解释：
现在ubuntu使用 systemd 作为 init system。
启动系统的时候，systemd会去查询default.target这个值，这个值有俩状态：
1. multi-user.target (system fully up, no graphics) 
2. graphical.target (system fully up, with graphics)

如果临时希望打开图形界面，那么不要使用`startx`, 要用：`sudo lightdm start`

## 安装开发环境
### 安装emacs
如果在命令行干活的话，可以考虑emacs，以前用过几天的vim，不太习惯，只好投入emacs的阵营了。
`sudo apt install emacs`

由于我关闭了图形界面，因此可以指定emacs以无窗口的方式启动。
[这里](https://askubuntu.com/questions/23645/how-do-i-download-the-command-line-emacs-instead-of-the-gui-one)介绍了如何启动：
`emacs -nw`

解释如下： `-nw, --no-window-system` 
>Tell Emacs not to use its special interface to X. If you use this switch when invoking Emacs from an xterm(1) window, display is done in that window.


### 安装git `sudo apt install git`

### 安装cmake
`sudo apt install cmake`

### 安装eigen
`sudo apt install libeigen3-dev`

### 安装Ceres Solver
这里[Installation](http://ceres-solver.org/installation.html)够用了。
先下载:
`git clone https://ceres-solver.googlesource.com/ceres-solver`
也就是这一坨：
```
# CMake
sudo apt-get install cmake
# google-glog + gflags
sudo apt-get install libgoogle-glog-dev
# BLAS & LAPACK
sudo apt-get install libatlas-base-dev
# Eigen3
sudo apt-get install libeigen3-dev
# SuiteSparse and CXSparse (optional)
# - If you want to build Ceres as a *static* library (the default)
#   you can use the SuiteSparse package in the main Ubuntu package
#   repository:
sudo apt-get install libsuitesparse-dev
# - However, if you want to build Ceres as a *shared* library, you must
#   add the following PPA:
sudo add-apt-repository ppa:bzindovic/suitesparse-bugfix-1319687
sudo apt-get update
sudo apt-get install libsuitesparse-dev
```

We are now ready to build, test, and install Ceres.
```
cd ceres-solver
mkdir ceres-bin
cd ceres-bin
cmake ../ceres-solver-1.13.0
make -j3
make test
# Optionally install Ceres, it can also be exported using CMake which
# allows Ceres to be used without requiring installation, see the documentation
# for the EXPORT_BUILD_DIR option for more information.
sudo make install
```

### 同时安装OpenCV 和opencv_contrib
为了方便我就下载最新版吧。现在是3.4.1。

先下载：
`git clone https://github.com/opencv/opencv.git`
`git clone https://github.com/opencv/opencv_contrib.git`

在[opencv_contrib的介绍里](https://github.com/opencv/opencv_contrib)指出，需要和OpenCV一块儿编译，即：
```
$ cd <opencv_build_directory>
$ cmake -DOPENCV_EXTRA_MODULES_PATH=<opencv_contrib>/modules <opencv_source_directory>
$ make -j5
```
注意，一般的套路是，在OpenCV文件夹中，`mkdir build`,在`build`目录进行cmake和make。

一个小坑：我一开始是先装的OpenCV，再尝试安装opencv_contrib，此时会提示无法下载`ippicv_2017u3_lnx_intel64_general_20170822.tgz`,找了一圈儿搞不定，我就把build目录删干净，重新一块儿安装它俩，即OpenCV 和opencv_contrib


比较好的安装教程是[这个:Ubuntu下opencv3.3和opencv_contrib的编译安装](http://blog.csdn.net/xiangxianghehe/article/details/78780269),我搬运一下：

先安装以下依赖包
```
sudo apt-get install build-essential  

sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev  

sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev  

sudo apt-get install pkg-config
```

进入我们在OpenCV文件夹中的build目录：
`cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules/ .. `
注意`../../opencv_contrib`就是你下载的`opencv_contrib`的文件夹的路径，按需要修改这个就行了。

继续在build文件夹：
```
make -j8        #8线程编译
sudo make install
```


链接库共享这一步貌似不是必须的？
编译安装完毕之后，为了让你的链接库被系统共享，让编译器发现，需要执行管理命令ldconfig：
`sudo ldconfig -v`  

### 查看已安装的OpenCV的版本号
`pkg-config --modversion opencv`


### cmake的时候指定c11
我make应用程序的时候，提示我要加"-std=c++11"这个选项。
由于cmake生成的Makefile我看不懂，不知道在啥地方指定gcc或g++编译器的选项。
在[传递FLAGS给C++编译器](https://elloop.github.io/tools/2016-04-10/learning-cmake-2-commands)中提到：
>如果我的main.cpp里面用到了C++11，那么我需要告诉CMake在生成的Makefile里告诉编译器启用C++11。与此类似，我可能也要传递其他FLAGS给编译器，怎么办？
答案是：设置CMAKE_CXX_FLAGS变量
加上：
```
set(CMAKE_CXX_FLAGS   "-std=c++11")             # c++11
```

也就是在CMakeLists.txt中加入`set(CMAKE_CXX_FLAGS   "-std=c++11")`即可。

## 安装vscode
打开c++文件后，会提示装对应的代码高亮插件，我把它推荐的插件全装了。

有的include它会提示一个小灯泡，此时按照它的提示将这些include加到 `.json` 的配置文件里就行了，这样就能更好滴提示补全和跳转了。

貌似有个插件用clang解析的？所以一直提示装clang，我在系统里装了clang之后。就没有提示了。

森博让我装了vs icon很爽。