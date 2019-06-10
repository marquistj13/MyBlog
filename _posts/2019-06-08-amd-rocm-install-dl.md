---
layout: post
title: 通过 rocm 的方式安装 dl 环境
categories:  [系统环境]
tag: [配置文件]
---

* content
{:toc}

## 前言
用来吃鸡的 RX588 闲着也是闲着，看能不能用起来，装个dl环境玩玩儿吧。
系统环境：
1. ubuntu 18.04, 16G RAM
1. 我的Python环境是 anaconda 3.7 base，并没有新建虚拟环境。注意安装anaconda的时候可能提示你要初始化，如果你初始化了，那么每次打开terminal都会有个base，如果不想这样的话，只需要在你的 `.bashrc` 的conda init部分的配置后面加入 `conda deactivate`即可。
1. cpu: ryzen 1600
1. gpu: rx580 8g  (也就是 gfx803)
1. 这时候是  ROCm2.4 

## Pytorch
### 前言
两大类方法吧
1. 不使用docker
1. 使用docker 

第一、二种方法安装失败了，第三种成功了。

不管哪一种方法，都要先安装 rocm。

#### 第一类方法：不使用docker，直接安装到系统中（失败啦）
这一类又分成倆：
第一个是不太官方的安装指南：
在 [PyTorch+HIP AMD GPU?! #10670](https://github.com/pytorch/pytorch/issues/10670)中有人提到可以这样：
1. 先根据[rocm官网](https://rocm.github.io/install.html)的指示安装rocm
1. `python tools/amd_build/build_pytorch_amd.py`
1. `USE_ROCM=1 python setup.py install`

说的比较笼统，其实自己装的时候比这个稍微复杂一点。

第二个是：[官方安装指南：Building PyTorch for ROCm](https://github.com/ROCmSoftwarePlatform/pytorch/wiki/Building-PyTorch-for-ROCm) 中的 `Option 4: Install directly on host`
这个不确定是否成功，存疑。


#### 第二类方法（成功了）
这一类也分成倆：
第一个是pull 官方的docker
[官方安装指南：Building PyTorch for ROCm](https://github.com/ROCmSoftwarePlatform/pytorch/wiki/Building-PyTorch-for-ROCm** 提供的推荐用法， 推荐用的是 docker
我下载了  rocm2.3 ubuntu16.04 和 rocm2.4 ubuntu16.04， 貌似 rocm2.3 ubuntu16.04没法编译，rocm2.4 ubuntu16.04编译好之后 test nn不通过，但只是cuda相关的不通过，其实是可以用的。

第二个是自己建docker：
[官方安装指南：Building PyTorch for ROCm](https://github.com/ROCmSoftwarePlatform/pytorch/wiki/Building-PyTorch-for-ROCm) 提供的option 2 ，Install using PyTorch upstream docker file


### 如何优雅地使用docker中的jupyter notebook
这一步放到这里是因为装好之后要经常运行这一部分，哈哈。

根据[在 docker 中运行 Jupyter notebook](https://blog.windrunner.me/programming/jupyter-docker.html)的说明，
为了固定端口映射，加入 `-p 18888:8888` 参数，就可以将系统的 0.0.0.0:32768 映射到 container 中的 8888 端口：
```sh
docker run -it -v $HOME:/data --privileged --rm --device=/dev/kfd --device=/dev/dri --group-add video -p 18888:8888 install_pytorch
```
当然，上面`install_pytorch`是我自己建的docker的名字。
我要是用官方的话，就是这个啦：
```sh
docker run -it -v $HOME:/data --privileged --rm --device=/dev/kfd --device=/dev/dri --group-add video -p 18888:8888 rocm/pytorch:rocm2.4_ubuntu16.04
```


根据[在 docker 中运行 jupyter，并在本机上打开网页](https://blog.csdn.net/cy_tec/article/details/84400721),在docker中运行：
`jupyter notebook --ip 0.0.0.0 --no-browser --allow-root`
就会提示：`http://(4760b8da6769 or 127.0.0.1):8888/?token=a8f4c65a6c97db87fc38d199fe6399562741aa44a05e3829`

由于我们已经将host的18888端口映射到docker镜像的8888端口，因此，只需在host上打开：`http://127.0.0.1:18888/?token=a8f4c65a6c97db87fc38d199fe6399562741aa44a05e3829` 就行了。

### 如何删除多余的docker
这次探索之后运行 `docker images` 会出现好多image，可以使用 `docker rmi <iamgeid>` 来删除，只保留有用的一个。
当然，很可能我们在commit的时候忘了加tag， 那么repo:tag 都是空的，这时候就会很难删除了，这时可以先用 `docker tag` 打上repo 和 tag,然后再删掉就行了。


### 根据[rocm官网](https://rocm.github.io/install.html)的指示安装rocm
这里和[rocm官网](https://rocm.github.io/install.html)官网基本一样，我抄到这里是为了方便：
1. 安装rocm-dkms meta-package:
```sh
sudo apt update
sudo apt install rocm-dkms
```
1. 将user加到video 这个group： `sudo usermod -a -G video $LOGNAME`
1. 将 `rocminfo` 和 `clinfor` 加到环境变量，就可以随便调用啦
`echo 'export PATH=$PATH:/opt/rocm/bin:/opt/rocm/profiler/bin:/opt/rocm/opencl/bin/x86_64' | sudo tee -a /etc/profile.d/rocm.sh`

注意要确保 `rocminfo`能够成功运行，要是不能运行的话就重启系统，或者重装，总之下面几步都要确保这个能运行。

### 第一类方法（失败的安装）
#### 第一个
安装rocm的各种东西
这一步其实是编译pytorch的时候老是提示错误，所以要装的。
1. `rocRAND`
根据[官网](https://github.com/ROCmSoftwarePlatform/rocRAND) 进行安装即可
```sh
git clone https://github.com/ROCmSoftwarePlatform/rocRAND.git
cd rocRAND; mkdir build; cd build
CXX=hcccmake -DBUILD_BENCHMARK=ON ../. 
make -j4
sudo make install
```
1. `rocsparse`: `sudo apt install rocsparse`
1. `hipSPARSE`: `sudo apt update && sudo apt install hipsparse`
1. `rocBLAS`: `sudo apt-get install rocblas`
1. `rocFFT`: `sudo apt update && sudo apt install rocfft`
1. `MIOpen`: 可以安装opencl版，也可以安装hip后端版，这里我安装hip版 `sudo apt-get install miopen-hip`
1. `hip-thrust`: `sudo apt install hip-thrust`

下载pytorch源码并编译(失败啦)


安装依赖:
`conda install numpy ninja pyyaml mkl mkl-include setuptools cmake cffi typing`

下载源码：`git clone --recursive https://github.com/pytorch/pytorch`

编译准备：
`python tools/amd_build/build_pytorch_amd.py`

默认需要占很大的内存，我的物理内存16g被撑没了。我的系统自带的swap空间是2g，我又按照[ubuntu 18.04 设置swap 交换分区文件](https://blog.csdn.net/lhs960124/article/details/80446433)临时加了20G：
```sh 
sudo dd if=/dev/zero of=swap bs=1024 count=20000000
sudo mkswap -f swap
sudo swapon swap
```
这个重启电脑之后就会自动没的，所以不要急着删除。

然后就是编译了：
`USE_ROCM=1 python setup.py install`
会提示各种错误，放弃吧，少年！

#### 第二个（这个不确定是否成功，存疑）
按照 [官方安装指南：Building PyTorch for ROCm](https://github.com/ROCmSoftwarePlatform/pytorch/wiki/Building-PyTorch-for-ROCm)  `Option 4: Install directly on host` 进行安装。
注意：虽然人家说了只对 python2.7 和 python3.6 有保障，但我还是试一下python3.7，头铁哈哈。
我也试了 python2.7 ，不管2.7还是3.7都失败了

安装rocm依赖：
`sudo apt install rock-dkms rocm-dev rocm-libs miopen-hip hipsparse hip-thrust rccl`
根据后面的探索，其实还需要安装 `hip_hcc` 要不然会提示编译错误的。
`sudo apt-get install hip_hcc`

安装PyTorch package requirements：
```sh 
sudo apt install libgoogle-glog-dev libhiredis-dev libiomp-dev libleveldb-dev liblmdb-dev libopencv-dev libpthread-stubs0-dev libsnappy-dev sudo vim libprotobuf-dev protobuf-compiler
```

安装PyTorch pip requirements：
`pip install enum34 numpy pyyaml setuptools typing cffi future hypothesis`

调整  ROCm internal dependency declarations:
```sh 
sudo sed -i 's/find_dependency(hip)/find_dependency(HIP)/g' /opt/rocm/rocsparse/lib/cmake/rocsparse/rocsparse-config.cmake
sudo sed -i 's/find_dependency(hip)/find_dependency(HIP)/g' /opt/rocm/rocfft/lib/cmake/rocfft/rocfft-config.cmake
sudo sed -i 's/find_dependency(hip)/find_dependency(HIP)/g' /opt/rocm/miopen/lib/cmake/miopen/miopen-config.cmake
sudo sed -i 's/find_dependency(hip)/find_dependency(HIP)/g' /opt/rocm/rocblas/lib/cmake/rocblas/rocblas-config.cmake
```

准备编译：`python tools/amd_build/build_amd.py`

开始编译：
由于我的rx580属于gfx803，而pytorch默认同时编译gfx803, gfx900, and gfx906，所以可以指定只编译一个（运行`rocm_agent_enumerator`就可以看到你的设备名字啦）。
首先：`export PYTORCH_ROCM_ARCH=gfx803`
然后`USE_ROCM=1 USE_LMDB=1 USE_OPENCV=1 MAX_JOBS=4 python setup.py install --user`。
编译的时候我发现只用了两三G的内存。用了大概两个小时吧，感觉应该把 `MAX_JOBS` 设的大一点。

3.7可以安装成功，但test不成功，运行test：`PYTORCH_TEST_WITH_ROCM=1 python test/run_test.py --verbose`，
2.7连安装都不成功。

### 第二类方法（成功啦）
#### 第一个（官方docker）
预处理：
1. 由于前两步将pytorch目录搞的很乱，因此需要重新下载pytorch，我先删掉吧。
1. 我还把装的各种依赖删掉了。

重新安装rocm：
由于前面已经装了rocm，这里只是确保一下：`sudo apt install rocm-dkms`

在宿主机上安装rock-dkms：`sudo apt-get install rock-dkms`

安装docker-ce，这个略去。

拉取docker镜像（有可能提示权限错误，按照[Solving Docker permission denied while trying to connect to the Docker daemon socket](https://techoverflow.net/2017/03/01/solving-docker-permission-denied-while-trying-to-connect-to-the-docker-daemon-socket/)这时候貌似加个用户组就行了？ `sudo usermod -a -G docker $USER`，貌似还得重启电脑）。
[官方安装指南：Building PyTorch for ROCm](https://github.com/ROCmSoftwarePlatform/pytorch/wiki/Building-PyTorch-for-ROCm) 没更新，还是让pull rocm2.3_ubuntu16.04，其实现在[rocm/pytorch](https://hub.docker.com/r/rocm/pytorch/tags)已经有 `rocm2.4_ubuntu16.04` 了，而且我试了 在 `rocm2.3_ubuntu16.04` 中没有安装成功，在 `rocm2.4_ubuntu16.04` 里成功了（但是test nn不通过）。
`docker pull rocm/pytorch:rocm2.4_ubuntu16.04`

重新下载pytorch：
```sh 
git clone https://github.com/pytorch/pytorch.git
cd pytorch
git submodule update --init --recursive
```

运行 `docker container`,并把你的 home 目录挂载到docker的 data 目录：
```sh
sudo docker run -it -v $HOME:/data --privileged --rm --device=/dev/kfd --device=/dev/dri --group-add video rocm/pytorch:rocm2.4_ubuntu16.04
```

切换到 pytorch 目录：`cd /data/pytorch`

设为我的显卡：`export PYTORCH_ROCM_ARCH=gfx803`
编译吧: `.jenkins/pytorch/build.sh`， 大概两个多小时就好了。

其他的都能通过，只要和`test_cuda`相关的都不通过。

使用 `docker ps` 查看 container id,然后：
`docker commit -a 'author name' -m 'pytorch installed' <container_id> rocm/pytorch:rocm2.4_ubuntu16.04`

如何查看是否安装成功？
```py
import torch
torch.cuda.is_available()
torch.cuda.current_device()
torch.cuda.device(0)
torch.cuda.get_device_name(0)
```

#### 第二个是自己建docker（其实pull 的也是upstream）
自建docker镜像：
```sh
cd pytorch/docker/caffe2/jenkins
./build.sh py2-clang7-rocmdeb-ubuntu16.04
```
完了之后有个提示`"Successfully built <image_id>"`

打开image:
```sh
sudo docker run -it -v $HOME:/data --privileged --rm --device=/dev/kfd --device=/dev/dri --group-add video <image_id>
```

设为我的显卡：`export PYTORCH_ROCM_ARCH=gfx803`
编译吧: `.jenkins/pytorch/build.sh`， 大概两个多小时就好了。

官方说是要运行所有所有test，即，`.jenkins/pytorch/test.sh`其实只需要test一个就行了，即测试一下nn：
`PYTORCH_TEST_WITH_ROCM=1 python test/test_nn.py --verbose`
其他的都能通过，只要和`test_cuda`相关的都不通过。

使用 `docker ps` 查看 container id,然后：
`docker commit -a 'author name' -m 'pytorch installed' <container_id> repo:tag`
然后， 由于自己建的docker image没有tage，还需要改一下tag： ` docker tag <image_id> 'install_torch'`

如何查看是否安装成功？
```py
import torch
torch.cuda.is_available()
torch.cuda.current_device()
torch.cuda.device(0)
torch.cuda.get_device_name(0)
```

## Tensorflow
[官网 ROCmSoftwarePlatform/tensorflow-upstream](https://github.com/ROCmSoftwarePlatform/tensorflow-upstream) 有两种方式，都是 `TensorFlow 1.13.1`版本：
1. 采用docker [rocm/tensorflow:latest](https://hub.docker.com/r/rocm/tensorflow/) 
```sh
alias drun='sudo docker run -it --network=host --device=/dev/kfd --device=/dev/dri --group-add video --cap-add=SYS_PTRACE --security-opt seccomp=unconfined -v $HOME/dockerx:/dockerx'
drun rocm/tensorflow
```
1. 采用pypi, 由于我的ananconda装的是python3.7，因此没必要显式指定pip3
```sh
\# Install some ROCm dependencies
sudo apt install rocm-libs miopen-hip cxlactivitylogger
\# Pip3 install the whl package from PyPI
pip install --user tensorflow-rocm --upgrade
```

我采用的是第二种方法，即pip方式,为了加速，临时使用了tuna源：
```sh
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --user tensorflow-rocm --upgrade
```
