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

## openvpn 端口号被封的解决办法
最近老是被封，我以为是openvpn协议被封了，因为这时候 l2tp以及softether client都能用，后来发现是端口号被封了，其实只要将默认的 `1194` 端口改掉就行了。

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
在windows安装并运行server 管理工具（注意安装的时候选择，仅安装管理工具就行了，不需要在windows上安装server）。
直接连接我么你的server的ip就行了，不需要密码！
连接之后，会弹出一个窗口让你设置服务器的密码的！
进去之后有个 step by step 的引导，照着做就行了，这样就能确保你的虚拟hub能够初始化，这一步十分关键，记住哈，一定要初始化 virtual hub，我一般把这个virtual hub的名字命名为 VPN（也就是默认值）。
当然如果直接跳过step by step 的引导也是可以的，前提是你有配置文件，直接导入以前的配置文件就行了。
什么，不知道配置文件在哪里？点击首页的齿轮图标那里就行了！

注意：如果你使用了动态域名绑定了你的vps的公网ip，那么一定要保存其 dns 钥（即配置文件的 declare DDnsClient部分），也就是说，你的配置文件的dns 钥不变，那么你的softether的动态域名就不会变，当然运行这个钥的server只能有一个，也就是不能俩server同时运行。

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

## 禁用SecureNAT，使用 local bridge
参照：
1. [基本安装（使用SecureNAT）](http://blog.lincoln.hk/blog/2013/03/19/softether-on-vps/)
2. [禁用SecureNAT，使用 local bridge](http://blog.lincoln.hk/blog/2013/05/17/softether-on-vps-using-local-bridge/) 
3. [local bridge的命令行配置版](https://www.williamjbowman.com/blog/2015/12/22/a-transparent-ad-blocking-vpn-via-softether-privoxy/)
4. [vpn-adblock有对应博客](https://github.com/nomadturk/vpn-adblock)

主要参照前两个链接。

### 前言
SecureNAT 太慢了，所以要使用 local bridge的方式，当然根据第一个链接的说明，SecureNAT 和 local bridge 只能同时enable一个，因此这里先 `禁用 SecureNAT`。
另外，我们还得配置 `DHCP server` 。

为了简化说明，这里重复了前面的一些步骤。

由于这里将vpn server的启动做成了 `/etc/init.d` 下的启动脚本，因此它自己会开机自启动，不需要我们上面的crontab了。

### 基本安装（使用启动脚本来开启和关闭vpnserver）
将编译好的文件夹复制到 `/usr/local` 目录， 
`cp vpnserver/ /usr/local/ -r`

并设置service：
`vim /etc/init.d/vpnserver`,
并粘贴以下内容：
```
#!/bin/sh
### BEGIN INIT INFO
# Provides:          vpnserver
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable Softether by daemon.
### END INIT INFO
DAEMON=/usr/local/vpnserver/vpnserver
LOCK=/var/lock/subsys/vpnserver
test -x $DAEMON || exit 0
case "$1" in
start)
$DAEMON start
touch $LOCK
;;
stop)
$DAEMON stop
rm $LOCK
;;
restart)
$DAEMON stop
sleep 3
$DAEMON start
;;
*)
echo "Usage: $0 {start|stop|restart}"
exit 1
esac
exit 0
```

然后enable这个 service：
```
chmod 755 /etc/init.d/vpnserver
mkdir /var/lock/subsys
update-rc.d vpnserver defaults
```

以后我们就能用
```
/etc/init.d/vpnserver start
/etc/init.d/vpnserver stop
```
来开启和关闭服务器了。

### Local bridge Setup
下面将网络设置成：
```
Network setup
VPN Server IP: 192.168.30.1
VPN Client IP Range: 192.168.30.2-192.168.30.222
Tap Device name: tap_soft
```

先根据[禁用SecureNAT，使用 local bridge](http://blog.lincoln.hk/blog/2013/05/17/softether-on-vps-using-local-bridge/) 设置 local bridge：
![bridge的设置](http://blog.lincoln.hk/images/softether_local_bridge/create-local-bridge.png)

为了防止图片加载不出来，我们用文字记录一下：
1. 用windows端的softether vpn  server manager连接服务器（当然先运行服务器哈），然后打开 `本地网桥设置`
2. `选择要桥接的虚拟hub`，就选默认的 `VPN` 就行了（实际上，我的服务器上只有这一个hub）
3. `要创建的类型`，选择 `新tab设备的桥接`，其中，`新tab设备的名称`填入 `soft`。
4. `创建本地桥`

此时运行 `ifconfig tap_soft` 就能看到我们的 soft 了。

### 配置 `DHCP server`
由于我们禁用了SecureNAT 和 SecureDHCP，因此需要自己安装 DHCP server， 这里使用 `dnsmasq`:
`apt-get install dnsmasq`。

然后在 `/etc/dnsmasq.conf` 的末尾加入以下内容,使得接口 `tap_soft` 上enable dhcp server，并设置dns-server：
```
# Listen to interface
interface=tap_soft
# Let's give the connecting clients an internal IP
dhcp-range=tap_soft,192.168.30.2,192.168.30.222,12h
# Default route and dns
dhcp-option=tap_soft,3,192.168.30.1
# Set IPv4 DNS server for client machines
dhcp-option=option:dns-server,192.168.30.1,8.8.8.8
# How many DNS queries should we cache? By defaults this is 150
# Can go up to 10k.
cache-size=10000
```

**注：** 这里的dns-server设置很重要，要不然客户端会很慢。

为了使得 Softether 启动的时候，dncp server 也启动，我们需要修改Softether的启动脚本，将 `/etc/init.d/vpnserver` 修改，加入 `/etc/init.d/dnsmasq` 的配置，（当然你不加在这里也行，只要讲dnsmasq设为开机启动也行）：
```
#!/bin/sh
### BEGIN INIT INFO
# Provides:          vpnserver
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable Softether by daemon.
### END INIT INFO
DAEMON=/usr/local/vpnserver/vpnserver
LOCK=/var/lock/subsys/vpnserver
TAP_ADDR=192.168.30.1

test -x $DAEMON || exit 0
case "$1" in
start)
$DAEMON start
touch $LOCK
sleep 1
/sbin/ifconfig tap_soft $TAP_ADDR
/etc/init.d/dnsmasq start
;;
stop)
$DAEMON stop
rm $LOCK
/etc/init.d/dnsmasq stop
;;
restart)
$DAEMON stop
sleep 3
$DAEMON start
sleep 1
/sbin/ifconfig tap_soft $TAP_ADDR
/etc/init.d/dnsmasq restart
;;
*)
echo "Usage: $0 {start|stop|restart}"
exit 1
esac
exit 0
```

### 打开 ipv4 forwarding
`vim /etc/sysctl.conf`
找到 `#net.ipv4.ip_forward = 1`，取消这一行的注释。

然后运行 `sysctl --system`。

### 使用 `iptables` 设置VPN的 的traffic forwarding 
将POSTROUTING规则添加到 iptables：
`iptables -t nat -A POSTROUTING -s 192.168.30.1/24 -j SNAT --to-source [YOUR VPS IP ADDRESS]`

为了保证系统重启以后这个 iptables rule 依然能够 survive，需要安装 `iptables-persistent`:
`apt-get install iptables-persistent`

注意，持久化的东西放在了：
```
/etc/iptables/rules.v4
/etc/iptables/rules.v6
```
这俩文件里边。

如果需要修改规则的话，就需要重新运行 `iptables -t nat -A POSTROUTING -s 192.168.30.1/24 -j SNAT --to-source [YOUR VPS IP ADDRESS]`，
然后运行 `iptables-save > /etc/iptables/rules.v4`。

当然，也可以删除 `/etc/iptables/rules.v4` 中的内容。

### 重启服务器
```
/etc/init.d/vpnserver restart
/etc/init.d/dnsmasq restart
```
这个时候用softether client连接服务器，可以看到给我们分配了ip。

由于我们已经在 `/etc/init.d/vpnserver` 里加入了 `dnsmasq` 的启动配置，因此重启系统的时候啥都不用管，vpnserver就会自启动了。

### 有可能出问题的地方
#### 53端口被占用
我设置了服务器之后，客户端老是获取不到ip，很明显dnsserver出问题了。运行 `/etc/init.d/dnsmasq restart` 提示53端口被占用。
我按照[启动或重启 dnsmasq 提示端口 53 被占用的解决方案 ](https://www.cnblogs.com/Yogile/p/12779744.html)搞定了。
