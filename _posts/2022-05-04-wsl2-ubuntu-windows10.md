---
layout: post
title: 在windows 10 上使用wsl2安装的ubuntu
categories:  [系统环境]
tag: [配置文件]
---

* content
{:toc}

## 前言
前一阵子刚把台式机上的ubuntu双系统删掉了，只保留了win10，但win10不好搭建开发环境，因此又想折腾系统了，在不重新装系统的情况下，只剩下两种比较好的选择：
1. docker
2. wsl的ubuntu

而这两种方式对于wsl2来说，是统一的，这个可以从微软的一个很好的教程[WSL 2 上的 Docker 远程容器入门](https://docs.microsoft.com/zh-cn/windows/wsl/tutorials/wsl-containers)进行理解，我们装好docker之后，打开 Docker Desktop，确保在“设置”>“常规”中选中“使用基于 WSL 2 的引擎”，加入我们已经通过应用商店安装了ubuntu20.04,那么通过转到“设置”>“资源”>“WSL 集成”，就可Configure which WSL 2 distros you want to access Docker from.从列表中选择ubuntu20.04，然后点击应用，我们就可以在ubuntu20.04中运行docker了，很神奇！明明我装的是Docker Desktop on Windows，我却可以在wsl2安装的ubuntu中使用windows上的docker，而且二者还是同一个docker，也就是它们看到的image是一样的！

在[WSL 2 上的 Docker 远程容器入门](https://docs.microsoft.com/zh-cn/windows/wsl/tutorials/wsl-containers)中，官方的解释是：
> 1. 在 WSL 版本 1 中，由于 Windows 和 Linux 之间的根本差异，Docker 引擎无法直接在 WSL 内运行，因此 Docker 团队使用 Hyper-V VM 和 LinuxKit 开发了一个替代解决方案。 但是，由于 WSL 2 现在在具有完整系统调用容量的 Linux 内核上运行，因此 Docker 可以在 WSL 2 中完全运行。 这意味着 Linux 容器可以在没有模拟的情况下以本机方式运行，从而在 Windows 和 Linux 工具之间实现更好的性能和互操作性。
>  1. 借助 Docker Desktop for Windows 中支持的 WSL 2 后端，可以在基于 Linux 的开发环境中工作并生成基于 Linux 的容器，同时使用 Visual Studio Code 进行代码编辑和调试，并在 Windows 上的 Microsoft Edge 浏览器中运行容器。


## docker 安装
在 [Install Docker Desktop on Windows](https://docs.docker.com/desktop/windows/install/) 中，有两种backend可选，我选的是WSL 2 backend。
1. 该页面让我们确保打开了wsl，并给了我们一个新的链接：[Install Linux on Windows with WSL](https://docs.microsoft.com/en-us/windows/wsl/install)，这个新页面告诉我们只需要在管理员模式的PowerShell或cmd中运行`wsl --install` 就能安装好wsl2了。原话是：
    >This command will enable the required optional components, download the latest Linux kernel, set WSL 2 as your default, and install a Linux distribution for you (Ubuntu by default, see below to change this).

    当然，我一开始是按照别的教程走的，没有运行`wsl --install`命令，而是通过控制面板打开的wsl选项。
1.  打开新的链接：[步骤 4 - 下载 Linux 内核更新包](https://docs.microsoft.com/zh-cn/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package) 打开该链接，安装好更新包之后运行以下命令将 WSL 2 设置为默认版本：`wsl --set-default-version 2` （我当时没有执行这个，后来默认以wsl 1的方式安装好的wsl ubuntu，这样的话只需要执行`wsl --set-version Ubuntu-20.04 2`就可以把ubuntu切换到wsl 2了）
1. 下载并安装Docker Desktop on Windows
1. 装好之后，我还设置了阿里的[官方镜像加速](https://help.aliyun.com/document_detail/60750.html)，方法是：使用支付宝登录阿里云，登录 [容器镜像服务控制台](https://cr.console.aliyun.com/cn-hangzhou/instances)，在左侧导航栏选择镜像工具`->` 镜像加速器，在镜像加速器页面获取镜像加速地址。然后将改地址内容：
    ```sh
    {
        "registry-mirrors": ["<镜像加速器地址>"]
    }            
    ```
    粘贴到docker desktop的设置，docker engine中，我是直接覆盖粘贴的。


## ubuntu 安装
1. 如果执行`wsl --install`的话，默认就装好ubuntu了（当然还可以通过`wsl --install -d <Distribution Name>`更改默认的ubuntu发行版），否则就需要根据[步骤 4 - 下载 Linux 内核更新包](https://docs.microsoft.com/zh-cn/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package)走一遍，然后通过微软应用商店在线安装ubuntu，当然也可以通过该页面提供的下载链接，自己下载下来，然后在下载目录执行`Add-AppxPackage .\app_name.appx`，Appx 包下载完成后，可以通过双击 appx 文件开始运行新发行版。
1. 安装 Windows Terminal（可选），可以通过应用商店安装，也可以通过github的release界面安装。
    注：这个终端非常好用，可以打开powershell,cmd，还有ubuntu，还可以给这三种窗口分别设置主题、背景图片、透明度（以及毛玻璃特效）。
1. 换国内镜像源
    1. 备份老的 `sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak`
    1. 打开`sudo vi /etc/apt/sources.list` ，输入 `49dd`删掉内容，
    1. [阿里云的镜像在这](https://developer.aliyun.com/mirror/ubuntu)，复制，然后输入`i`进入插入模式，然后点击鼠标右键或者`Ctrl V`，就粘贴进去了。
    1. `sudo apt-get -y update`

## 使用 VS Code 在远程容器中开发
参考自：[WSL 2 上的 Docker 远程容器入门](https://docs.microsoft.com/zh-cn/windows/wsl/tutorials/wsl-containers)
若要开始使用 Docker 和 WSL 2 开发应用，建议使用 VS Code 以及 Remote-WSL 扩展和 Docker 扩展。
1. Remote-WSL 扩展：打开在 WSL 上运行的 Linux 项目（无需担心路径问题、二进制兼容性或其他跨 OS 的难题）
1. VS code Remote-Containers 扩展：打开容器内的项目文件夹或存储库，并利用 Visual Studio Code 的完整功能集在容器中执行开发工作。
1. VS Code Docker 扩：从 VS Code 内生成、管理和部署容器化应用程序的功能。 （需要 Remote-Container 扩展才能实际使用容器作为开发环境。）

官方建议：始终将代码存储在使用工具的相同文件系统中。 这将提高文件访问性能。 在本例中，我们使用的是 Linux 发行版 (Ubuntu)，并且想要将项目文件存储在 WSL 文件系统 `\\wsl\` 上。 在 WSL 中使用 Linux 工具访问项目文件时，将项目文件存储在 Windows 文件系统上会明显降低速度。

那么怎么打开wsl2的文件夹呢？在文件资源管理器输入`\\wsl$`即可，然后就能看到ubuntu-20.04文件夹了，右键该文件夹，固定到快速访问，就方便了。

## wsl2 ubuntu显示界面
主要以下参照自：
1. [搭建 WSL2 的沙雕版 GUI（VcXsrv+xfce4）](https://zhuanlan.zhihu.com/p/165660907)
1. [Windows上安装Linux桌面（WSL+Ubuntu+Kali+xfce+Deskotp）](https://zhuanlan.zhihu.com/p/473445038)

### 基本版
步骤：
1. 在win10上安装vcxsrv
1. 进入 WSL2，安装 xfce4 `sudo apt install xfce4`
1. 查看win10上的wsl2 的ip：`ipconfig`，然后找到以太网适配器 vEthernet (WSL)，我的ip是`172.22.192.1`
1. 回到 WSL2，将如下语句，添加至`~/.bashrc`或`~/.zshrc`末尾`export DISPLAY=172.22.192.1:0`,然后`source ~/.bashrc`
1. 运行 `startxfce4`
1. 在windows上打开vcxsrv，可以选择默认的One large window 和 Start no client，在 Extra settings 中勾选第三项`Disable access control`，最后，完成配置。可以将配置保存至桌面，下次就不需要点这么多次了。

另外：
1. 如果我们打开vcxsrv的时候，选择默认的One large window，`Display num=-1`，那么就是一个默认的桌面，就是普通的桌面。如果我们不选择One large window，而是`Multiple Windows`，那么我们就可以弹出独立的多个窗口，怎么弹出来呢？假如我们运行`gedit`，就会弹出来了，当然也可以同时弹出来其他窗口，这个是我比较喜欢的方式，因为我使用vscode 打开wsl的文件夹开发gui程序（或者弹出opencv窗口）的时候，直接运行`Multiple Windows`的vcxsrv是很爽的，就跟在win10上弹出来的窗口一样。
1. 我们也可以安装其他桌面，这个时候如果我们希望同时打开多个桌面环境，可参考[Windows上安装Linux桌面（WSL+Ubuntu+Kali+xfce+Deskotp）](https://zhuanlan.zhihu.com/p/473445038)，分别设置不同的display数就行了，例如在终端设置`export DISPLAY=172.22.192.1:1`，然后打开桌面`xfce4-session`，最后打开vcxsrv的时候，设置显示器为1就行了（`Display num=1`）。

### 灵活版
有时候我们的wsl的ubuntu的ip 会发生变化，其实是子网发生了变化，咋办呢？
根据[How to set up working X11 forwarding on WSL2](https://stackoverflow.com/questions/61110603/how-to-set-up-working-x11-forwarding-on-wsl2)的方案，我们只需要将以下加入`~/.bashrc`或`~/.zshrc`末尾,然后`source ~/.bashrc`：
```sh
export DISPLAY=$(ip route list default | awk '{print $3}'):0
export LIBGL_ALWAYS_INDIRECT=1
```

对于我的机器，现在是：
```sh
ip route list  default
default via 172.17.224.1 dev eth0
ip route list  default | awk '{print $3}'
172.17.224.1
```