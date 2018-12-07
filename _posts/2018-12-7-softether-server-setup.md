---
layout: post
title:  softether 服务器设置  及 ubuntu18.04 自启动设置
categories:  [系统环境]
tag: [配置文件]
---

* content
{:toc}

## 前言
距离第一次整理 softether 的安装，即 [SoftEther VPN Server 配置 （含本机作为server 以及 vps 作为server）]({{ site.baseurl }}{% link _posts/2017-12-23-SoftEther-server.md %})，已经快一年了。
发现以前有些步骤有些多余，并且有很多东西需要更新了，所以今天再整理一下。

## server 安装
>注意：(本节的明确视情况，请自行添加 `sudo`)

###  首先装好ubuntu（16.04 或 18.04）。

### 安装编译器（主要是make吧）
`apt-get update`
`apt-get install build-essential`

### 下载源码
由于不可描述的原因，官方的下载网站可能访问不了，因此需要在github的托管上下载 server，位置是 [SoftEtherVPN/SoftEtherVPN_Stable](https://github.com/SoftEtherVPN/SoftEtherVPN_Stable/releases)。

搞到下载链接后，直接：`wget 下载链接`，就能下载到当前目录了。

### 解压并编译源码
`tar zxvf 文件名` 就会默认解压为一个叫做 `vpnserver` 的文件夹。
`cd` 进去，执行 `./.install.sh` 就能安装好啦。

### 运行server
安装好之后，直接 `sudo ./vpnserver start` 启动服务

注意：貌似此处无需运行 `./vpncmd `
### 配置server端
在windows安装并允许server 管理工具（注意安装的时候选择，仅安装管理工具就行了，不需要在windows上安装server）。
直接连接我么你的server的ip就行了，不需要密码！
连接之后，会弹出一个窗口让你设置服务器的密码的！
进去之后有个 step by step 的引导，照着做就行了，这样就能确保你的虚拟hub能够初始化，这一步十分关键，记住哈，一定要初始化 virtual hub，我一般把这个virtual hub的名字命名为 VPN。
当然如果直接跳过step by step 的引导也是可以的，前提是你有配置文件，直接导入以前的配置文件就行了。
什么，不知道配置文件在哪里？点击首页的齿轮图标那里就行了！

### server端的配置细节
我一般都会在hub属性那里，把系统的log都关掉，只保留登录信息的log。
我一般还enable 了secure nat，并在里面设置一个dns server，取 [这个页面的任意一个就行了](https://github.com/lennylxx/ipv6-hosts)，这样客户端就不用自己解析dns了（我只见过ubuntu的客户端还需要自己设置dns server的，我的手机不需要，windows 的client也不需要）。

## ubuntu 18.04 的开机启动
18.04 把我以前习惯用的 `rc.local` 默认关掉了。
一搜索18.04 的开机启动，基本全是如何重新启用`rc.local`。

不能这么搞啊，要与时俱进啊！
在：
>https://ubuntuforums.org/showthread.php?t=2391911
https://askubuntu.com/questions/1041455/what-is-the-correct-way-to-run-a-command-after-boot-on-ubuntu-18-04
https://askubuntu.com/questions/814/how-to-run-scripts-on-start-up/816#816

提到可以使用`crontab`！
我以前只知道用`crontab`执行定时任务，它竟然还能设置开机启动项！

好了废话不多说了。
根据 [19. crontab 定时任务](http://linuxtools-rst.readthedocs.io/zh_CN/latest/tool/crontab.html)的参考，可以在 `$HOME` 建一个crontab文件，`$HOME` 目录是啥，你 `echo $HOME`就知道了,我的就是 root目录。
好了，我们新建一个 `marquis_cron` 的文件，文件名随意哈。
然后里面填写：
```
@reboot sudo /home/ubuntu/vpnserver/vpnserver start
```
注意 `vpnserver` 的路径要填写绝对路径哈，根据你的实际情况来吧。
例如：
```
@reboot /root/vpnserver/vpnserver start
```

然后运行 `crontab marquis_cron`就行了。

如果不想要这个crontab文件了，可以用 `crontab -r`来删除，详情看上面的链接。
用`crontab -l`可以查看当前cron的状态。


当然，由于crontab很通用，因此不局限于18.04的系统。