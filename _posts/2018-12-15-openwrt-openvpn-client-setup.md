---
layout: post
title:  将 openwrt 路由器作为 openvpn client
categories:  [系统环境]
tag: [配置文件,OpenWrt]
---

* content
{:toc}

## 简单配置 openwrt 相关
### 安装 openwrt （现在是 `18.06.1`的版本啦）
路由器型号： linksys WRT1200AC
在 [Linksys WRT AC Series](https://openwrt.org/toh/linksys/wrt_ac_series#stable) 找到 [Repository](https://downloads.openwrt.org/releases/18.06.1/targets/mvebu/cortexa9/)，然后找到路由器型号对应的文件，即 `linksys-wrt1200ac-squashfs-factory.img`，进行下载即可。

在路由器上将固件文件写入（建议插网线）。

### 网页端访问 openwrt
安装好 openwrt 之后，自带 luci 界面，默认wifi是关闭的。
用网线连接路由器的lan口，浏览器输入`192.168.1.1`，默认不带 root 密码，登陆进去，设置密码，ok。

### ssh访问
直接 `ssh root@192.168.1.1` 即可。

### 执行软件源更新
运行 `opkg update` 即可在后面安装各种软件啦。

出错的解决：
如果此命令显示无法 download 对应的文件，而连接路由器的电脑可以访问网络，且出错信息中的文件可以在电脑端浏览器上下载，那就是很大的问题了。
出了问题我试了如下两种方法。
1. 错误的尝试
我遇到这种情况是因为路由器是二级路由，即 openwrt 路由器是接在另一个路由器上的，一级路由的ip是`192.168.1.1`，二级路由的ip也是`192.168.1.1`，
此时，虽然连接 openwrt 路由器的设备可以正常上网，但 极有可能 openwrt 路由器自己没法 `ping baidu.com`，有人说
我按照别人的方法设置openwrt 路由器的wan的dns为`8.8.8.8`此时openwrt 路由器可以`ping baidu.com`了，但仍然无法成功执行`opkg update`。
1. 我的解决方案
不要将openwrt 路由器作为二级路由啦，作为一级路由就行啦。

### 安装中文
执行 `opkg install luci-i18n-base-zh-cn`
只需要等一会儿，luci 界面 就会变成中文啦。

## 下面将介绍两种配置方法，我的经验是：第一种不work，第二种work
本文的client的配置适用以下方法设置的openvpn server：
1. [SoftEtherVPN](https://github.com/SoftEtherVPN/SoftEtherVPN_Stable/releases)
2. [StreisandEffect/streisand](https://github.com/StreisandEffect/streisand)
3. [angristan/openvpn-install](https://github.com/angristan/openvpn-install)


## 第一种 openvpn 设置（失败的尝试，不要参照这个做，直接按照下面的`第二种 openvpn 设置`操作就行了)
以下参考自：
1. 主要部分来自：[opwnwrt官方教程OpenVPN Client](https://openwrt.org/docs/guide-user/services/vpn/openvpn/client)
2. dns的设置部分来自：[Setting an OpenWrt Based Router as OpenVPN Client](https://github.com/StreisandEffect/streisand/wiki/Setting-an-OpenWrt-Based-Router-as-OpenVPN-Client)

### 故障描述
根据这种方法设置好之后，可以发现路由器自己可以上google，但连接路由器的设备没法上。很奇怪，目前不知道结解决方法。
我不想把这一部分删掉，有兴趣的同学可以将这个失败的方法和成功的方法对照，看看啥地方的原因，我猜测是这种方法把各种东西，如接口啊，防火墙的zone啊都起名为`vpnclient`，很有可能吧。

### 安装 openvpn
`opkg install openvpn-openssl luci-app-openvpn openssl-util`
### 创建网络接口（这个是tun的接口，应该是隧道吧）
```
uci set network.vpnclient="interface"
uci set network.vpnclient.ifname="tun0"
uci set network.vpnclient.proto="none"
 
uci commit network && service network restart
```

此时在luci的`网络->接口`界面就能看到多了一个叫做`vpnclient`的接口，其实我猜测只要上面代码中`network.vpnclient` 换成 `network.name`就能创建一个名为 `name`的接口。
此时其协议显示为：`协议: 不配置协议`
### 配置防火墙的Default Rules & Forwarding
```
uci add firewall zone
uci set firewall.@zone[-1].name="vpnclient"
uci add_list firewall.@zone[-1].network="vpnclient"
uci set firewall.@zone[-1].input="REJECT"
uci set firewall.@zone[-1].output="ACCEPT"
uci set firewall.@zone[-1].forward="REJECT"
uci set firewall.@zone[-1].masq="​1"​
uci set firewall.@zone[-1].mtu_fix="1"
 
uci add firewall forwarding
uci set firewall.@forwarding[-1].src="lan"
uci set firewall.@forwarding[-1].dest="vpnclient"
 
uci commit firewall && service firewall restart
```
此时在`网络->防火墙`界面就能看到多了一个名为`vpnclient`的zone，并且看到了`lan`到`vpnclient`都是accept的。
## 配置openvpn client
这里就是重头戏了。
### 先设置基本的 openvpn client
指定配置文件的地址：
```
uci set openvpn.vpnclient="openvpn"
uci set openvpn.vpnclient.enabled="1"
uci set openvpn.vpnclient.config="/etc/openvpn/vpnclient.ovpn"
 
uci commit openvpn && service openvpn restart
```

### 将配置文件传递到路由器
`scp ./vpnclient.ovpn root@192.168.1.1:/etc/openvpn/`

### 然后设置`vpnclient.ovpn`的内容
如果你的openvpn只需要配置文件，不需要密码验证，只需要把配置文件传过去就行了，不需要添加用户验证文件。
下面考虑需要输入用户名和密码的情况：
1. 首先运行：
```
sed -r -i "
s:^(auth-user-pass).*:\1 /etc/openvpn/vpnclient.auth\nauth-nocache:
s:^(redirect-gateway).*:\1 def1:
" /etc/openvpn/vpnclient.ovpn
```
这个命令就会帮助我们将配置文件中的`auth-user-pass` 替换为：
```
auth-user-pass /etc/openvpn/vpnclient.auth
auth-nocache
```
1. 然后运行：
```
cat << "EOF" > /etc/openvpn/vpnclient.auth && chmod 600 /etc/openvpn/vpnclient.auth
YOUR_VPN_USER_NAME
YOUR_VPN_PASSWORD
EOF
```
注意将用户名和密码替换进去哈。
这条命令就会创建`/etc/openvpn/vpnclient.auth`文件，并写入EOF。
1. 最后重启openvpn：
`service openvpn restart`

### dns 的设置
刚才我们执行了`service openvpn restart`，很大概率此时终端无法通过路由器上网了，即 `ping baidu.com` 都不行，因此`ping google.com`更不行。
只有将`服务->OpenVPN`界面的`vpnclient`给`stop`了才能正常访问网络，当然，此时openvpn也就下线了。
也就无法达到我们的目的了，怎么办？

我们可以通过设置，让服务器端给我们解析地址。
具体而言，就是在ovpn配置文件中，告诉openvpn：“兄弟，你给我执行两个脚本，让服务器端给我们解析地址吧！”

好了，打开`/etc/openvpn/vpnclient.ovpn`，在其开头（其实应该啥地方都行）加入：
```bash
script-security 2 # needed to be able to use 'up' and 'down' scripts
up "/etc/openvpn/updns" # FIX DNS, we will create it later
down "/etc/openvpn/downdns" # FIX DNS, we will create it later
```

下面建立处理dns的两个脚本。
首先运行即可：
```bash
cat<<'EOF' > /etc/openvpn/updns
#!/bin/sh
mv /tmp/resolv.conf.auto /tmp/resolv.conf.auto.hold
echo $foreign_option_1 | sed -e 's/dhcp-option DOMAIN/domain/g' -e 's/dhcp-option DNS/nameserver/g' >/tmp/resolv.conf.auto
echo $foreign_option_2 | sed -e 's/dhcp-option DOMAIN/domain/g' -e 's/dhcp-option DNS/nameserver/g' >> /tmp/resolv.conf.auto
echo $foreign_option_3 | sed -e 's/dhcp-option DOMAIN/domain/g' -e 's/dhcp-option DNS/nameserver/g' >> /tmp/resolv.conf.auto
EOF


cat<<'EOF' > /etc/openvpn/downdns
#!/bin/sh
mv /tmp/resolv.conf.auto.hold /tmp/resolv.conf.auto
EOF
```

然后增加可执行权限
```bash
chmod 755 /etc/openvpn/updns
chmod 755 /etc/openvpn/downdns
```

检查一下：`ls -l /etc/openvpn/*dns` 可以看到这俩文件啦。

最后重启openvpn服务：`service openvpn restart`

运行：`ps | grep [o]penvpn; echo && logread -e openvpn` 若无输出，说明没有运行
此时可以再次运行`service openvpn restart`。

如果运行：`ps | grep [o]penvpn; echo && logread -e openvpn` 看到 `Initialization Sequence Completed`，恭喜你，成功啦。
然后可以`CTRL+C`退出命令啦。
现在可以`ping baidu.com` 以及`ping google.com`啦

## debug
路由器自己可以上google，但设备没法上。很奇怪，目前不知道结解决方法。


 
## 第二种 openvpn 设置
以下参考自：
1. 每个子配置部分（如接口配置）之后的生效部分参考自：[opwnwrt官方教程OpenVPN Client](https://openwrt.org/docs/guide-user/services/vpn/openvpn/client)
2. 主要部分来自 [Setting an OpenWrt Based Router as OpenVPN Client](https://github.com/StreisandEffect/streisand/wiki/Setting-an-OpenWrt-Based-Router-as-OpenVPN-Client)

## 基本步骤

### 保证路由器空间大于 1M
`df -h`

### 安装中文
执行 `opkg install luci-i18n-base-zh-cn`
只需要等一会儿，luci 界面 就会变成中文啦。

### 连接路由器并在路由器上安装openvpn
`opkg install openvpn-openssl luci-app-openvpn openssl-util`
如果你的路由器空间很小，那只运行下面这个就行了，不过这样的话，就没法在luci界面进行显示很多东西了。，只能在命令行看到啦。
```bash
opkg update
opkg install openvpn-openssl # brings openvpn kmod-tun liblzo zlib libopenssl (~1M)
```
### 让openvpn开机运行（略过吧，这一步不需要运行，我的openwrt 18.01安装的，它会自启动的）
`/etc/init.d/openvpn enable`

## openvpn 的设置
### 创建网络接口（这个是tun的接口，应该是隧道吧）
```
# a new network interface for tun:
uci set network.streisandvpn=interface
uci set network.streisandvpn.proto='none' #dhcp #none
uci set network.streisandvpn.ifname='tun0'

uci commit network && service network restart
```

此时在luci的`网络->接口`界面就能看到多了一个叫做`streisandvpn`的接口，其实我猜测只要上面代码中`network.streisandvpn` 换成 `network.name`就能创建一个名为 `name`的接口。
此时其协议显示为：`协议: 不配置协议`
### 配置防火墙的Default Rules & Forwarding
```
# a new firewall zone (for VPN):
uci add firewall zone
uci set firewall.@zone[-1].name='vpn'
uci set firewall.@zone[-1].input='REJECT'
uci set firewall.@zone[-1].output='ACCEPT'
uci set firewall.@zone[-1].forward='REJECT'
uci set firewall.@zone[-1].masq='1'
uci set firewall.@zone[-1].mtu_fix='1'
uci add_list firewall.@zone[-1].network='streisandvpn'

# enable forwarding from LAN to VPN:
uci add firewall forwarding
uci set firewall.@forwarding[-1].src='lan'
uci set firewall.@forwarding[-1].dest='vpn'
 
uci commit firewall && service firewall restart
```
此时在`网络->防火墙`界面就能看到多了一个名为`vpn`的zone，并且看到了`lan`到`vpn`都是accept的。

### 指定 openvpn 的配置文件
指定配置文件的地址：
```bash
# a new OpenVPN instance:
uci set openvpn.streisand=openvpn
uci set openvpn.streisand.enabled='1'
uci set openvpn.streisand.config='/etc/openvpn/streisand.conf'
 
uci commit openvpn && service openvpn restart
```
注释：
> 此处的配置文件指定为 `/etc/openvpn/streisand.conf`，其实你可以任意起名字，扩展名也无所谓，我一般叫它 `vpnclient.ovpn`，如果你也这么配置的话，下面对应的部分也改成 `vpnclient.ovpn`即可。


### dns 的设置
原作者建议不要在路由器上自己设置，而是使用服务器端的：
>Set up two script that use the DNS provided through the VPN Tunnel on the Streisand host (recommended).

即，设置两个脚本，这俩脚本使用的是我们的Streisand端托管VPN隧道提供的DNS
我也准备采用这种方式哈。

下面我们将建立文件并在里面设置dns，然后建立这两个脚本。

### 获取ovpn配置文件
1. [SoftEtherVPN](https://github.com/SoftEtherVPN/SoftEtherVPN_Stable/releases)搭建的话直接可以用server端的gui界面导出`.ovpn`的配置文件
1. 如果你是按照[Streisand](https://github.com/StreisandEffect/streisand)的介绍搭建的服务器
这搭建好Streisand之后，会生成一个`streisand.html`文件，从这个文件可以下载。
里边有很多下载选项，我就点的第一个`alarm-laugh`，就下载了一个`[ip]-direct.ovpn`这种名字的配置文件。
__注意__：>`streisand`的配置文件默认应该是没有密码的，所以无需我们自己建密码文件了。
1. [angristan/openvpn-install](https://github.com/angristan/openvpn-install)也是直接生成配置文件的。

### 根据ovpn配置文件生成我们自己的配置文件 `/etc/openvpn/streisand.conf` 
当然配置文件的名称只要和上面一致就行，即和 `uci set openvpn.streisand.config='/etc/openvpn/streisand.conf'` 一致就行了。


下面以[Streisand](https://github.com/StreisandEffect/streisand)的配置文件为例，介绍如何进行dns的配置。
>1. [angristan/openvpn-install](https://github.com/angristan/openvpn-install)的配置文件的修改和这个一样
1. 貌似[SoftEtherVPN](https://github.com/SoftEtherVPN/SoftEtherVPN_Stable/releases)需要建立用户名和密码，因此除了这里的介绍之外，还需要参照上面`第一种 openvpn 设置`的介绍建立一个`vpnclient.auth`的文件用于存放用户名和密码。

我们将利用 `cat` 和`EOF' `从终端生成文件（不用`scp`的时候就可以用这种方法）
首先，用纯文本编辑器打开`[ip]-direct.ovpn`
找到这一行 `router [ip] 255.255.255.255 net_gateway`，在此行开头加 `#` 将其注释。因为这一行我们从服务器端可以得到，所以要注释掉。
在文件开头加入：
```bash
script-security 2 # needed to be able to use 'up' and 'down' scripts
up "/etc/openvpn/updns" # FIX DNS, we will create it later
down "/etc/openvpn/downdns" # FIX DNS, we will create it later
```
注意：
>原文中的openvpn选项为：`script-security 2 system` 但加了system选项以后就没法运行了，所以我把它去掉了。

然后在任意位置加入OpenVPN log and status file（这一步可以省略，我没加）
```bash
log-append /var/log/openvpn.log # To append to log file
status /var/log/openvpn-status.log # To mantain a status file
```

在文件开头加入：`cat<<'EOF' > /etc/openvpn/streisand.conf` （要保证这一行在文件最开头）
在文件末尾加入：`EOF` （要保证这一行在文件最末尾）

然后拷贝整个文件的内容到终端，就会生成`/etc/openvpn/streisand.conf`文件了。
即`ls -l /etc/openvpn/streisand.conf`就能看到了。
### 建立处理dns的两个脚本
首先运行即可：
```bash
cat<<'EOF' > /etc/openvpn/updns
#!/bin/sh
mv /tmp/resolv.conf.auto /tmp/resolv.conf.auto.hold
echo $foreign_option_1 | sed -e 's/dhcp-option DOMAIN/domain/g' -e 's/dhcp-option DNS/nameserver/g' >/tmp/resolv.conf.auto
echo $foreign_option_2 | sed -e 's/dhcp-option DOMAIN/domain/g' -e 's/dhcp-option DNS/nameserver/g' >> /tmp/resolv.conf.auto
echo $foreign_option_3 | sed -e 's/dhcp-option DOMAIN/domain/g' -e 's/dhcp-option DNS/nameserver/g' >> /tmp/resolv.conf.auto
EOF


cat<<'EOF' > /etc/openvpn/downdns
#!/bin/sh
mv /tmp/resolv.conf.auto.hold /tmp/resolv.conf.auto
EOF
```

然后增加可执行权限
```bash
chmod 755 /etc/openvpn/updns
chmod 755 /etc/openvpn/downdns
```

检查一下：`ls -l /etc/openvpn/*dns` 可以看到这俩文件啦。

### 运行openvpn
第一种方法：在终端执行 `service openvpn restart`
第二种方法：在luci界面的`服务->Openvpn`那里，点一下，将我们的`streisand`给`start`。

## debug 相关的命令
### 查看运行情况
如果上一步中，我们在配置文件中加入了log，那么可以查看log文件：
```
/etc/init.d/openvpn stop      # stop daemon in case that is currently running
rm /var/log/openvpn.log       # delete previous OpenVPN log
/etc/init.d/openvpn start     # start OpenVPN
sleep 1                       # wait a second.
tail -f /var/log/openvpn.log  # monitor log.
```

如果我们没有让它log：可以运行`ps | grep [o]penvpn; echo && logread -e openvpn`

不管怎么样，如果看到`Initialization Sequence Completed`，恭喜你，成功啦。
然后可以`CTRL+C`退出命令啦。

### 保证你的vpn是成功的
运行 `traceroute 8.8.8.8`，如果看到经过了我们的服务器的ip，那就成功啦。
这里去trace其他的ip也是可以的。

或者访问[这个网页](https://duckduckgo.com/?q=ip+address&ia=answer)看到我们的ip在服务器那边就行啦。

### 使用 crontab 定时重启

#### 基本知识
每次快到晚上的时候貌似都会断开连接，因此我决定每隔几分钟就要重启一次服务。
根据[linux下crontab每隔5分钟执行一次任务的写法](http://outofmemory.cn/code-snippet/434/linux-crontab-meige-5-fenzhong-execution-yici-task-xiefa)的说明，
>有两种写法
第一种写法是*/5，这种写法有的系统会不支持
`*/5 * * * * /xxx/task.sh`
第二种写法比较繁琐，但所有系统都支持：
`0,5,10,15,20,25,30,35,40,45,50,55 * * * * /xx/task.sh`


[OpenWrt Cron and crontab 官网介绍](https://openwrt.org/docs/guide-user/base-system/cron)有教程，且两种指定方式都支持
据我的测试，这种 `0,5,10,15,20,25,30,35,40,45,50,55 * * * * /xx/task.sh` 更好使一点。


我发现吗，每次restart大概耗时3秒左右。
我目前打算每隔三十分钟执行一次,可以用：
`*/30 * * * * service openvpn restart`
或者：
`0,30 * * * * service openvpn restart`

创建一个文件如`vim marquis_cron`，写入上述命令
然后执行 `crontab marquis_cron` 就行了。

执行完可以用`crontab -l`查看所有的配置，用`crontab -r`删除配置。

#### 使能cron
[官方教程](https://oldwiki.archive.openwrt.org/doc/howto/cron)说没有默认启用cron，因此要Activating cron，只需要运行一次就行啦：
```
/etc/init.d/cron start
/etc/init.d/cron enable
```

#### 寻找能运行的命令
以下测试的时候我用的5分钟。

上面 `0,5,10,15,20,25,30,35,40,45,50,55 * * * * service openvpn restart` 运行之后，，使用 
`ps | grep [o]penvpn; echo && logread -e openvpn` 看到了我们的cron脚本的运行结果：
>Wed Dec 19 11:25:00 2018 cron.info crond[3327]: USER root pid 3970 cmd service openvpn restart

但是我在luci界面看到的正在运行的openvpn的pid不是这个数字。
同时手动运行`service openvpn restart`发现luci界面的openvpn的 pid就是手动运行之后使用`ps | grep [o]penvpn; echo && logread -e openvpn`看到的pid，同时这个命令的输出给出了完整的运行命令，即：
`/usr/sbin/openvpn --syslog openvpn(streisand) --status /var/run/openvpn.streisand.status --cd /etc/openvpn --config /etc/openvpn/streisand.conf`

但我试了还是不行。
在[openwrt下的openvpn client实现](https://segmentfault.com/a/1190000004172000)中找到了一个命令`/etc/init.d/openvpn restart`，因此将crontab文件修改为：
`0,5,10,15,20,25,30,35,40,45,50,55 * * * * /etc/init.d/openvpn restart`

每半小时的：
`0,30 * * * * /etc/init.d/openvpn restart`

完美。

