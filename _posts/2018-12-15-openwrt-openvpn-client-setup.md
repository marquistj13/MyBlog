---
layout: post
title:  将 openwrt 路由器作为 openvpn client
categories:  [定位]
tag: [方案借鉴]
---

* content
{:toc}

## 安装 openwrt （现在是 `18.06.1`的版本啦）
路由器型号： linksys WRT1200AC
在 [Linksys WRT AC Series](https://openwrt.org/toh/linksys/wrt_ac_series#stable) 找到 [Repository](https://downloads.openwrt.org/releases/18.06.1/targets/mvebu/cortexa9/)，然后找到路由器型号对应的文件，即 `linksys-wrt1200ac-squashfs-factory.img`，进行下载即可。

在路由器上将固件文件写入（建议插网线）。

## 简单配置 openwrt
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


## 第一种 openvpn 设置（路由器可以登录openvpn账户，但没法正常工作，不推荐这么做了）
以下来自：[opwnwrt官方教程OpenVPN Client](https://openwrt.org/docs/guide-user/services/vpn/openvpn/client)
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

## debug
### 保证openvpn运行
运行：`ps | grep [o]penvpn; echo && logread -e openvpn` 若无输出，说明没有运行，我重启了路由器，
然后运行了好几次`service openvpn restart`，就能在在luci的`网络->接口`界面看到在运行了，`ps | grep [o]penvpn; echo && logread -e openvpn`也有输出啦。

__马后炮：__ 实际上，只需要重启路由器，它就会自动运行openvpn，并登陆我们设置的账户。 或者每次运行`service openvpn restart`就会登录一次账户。

### 我运行 vpn 的时候无法访问网络
在`服务->OpenVPN`界面，可以看到我们的`vpnclient`在运行，在我自己的openvpn server端也看到路由器登陆vpn成功了，但此时路由器无法访问网络，
只有将`服务->OpenVPN`界面的`vpnclient`给`stop`了才能正常访问网络，当然，此时openvpn也就下线了。

有人说通过设置dns可以解决这个问题，我没搞成功……


 
## 以下是第二种 openvpn 设置
来自[Setting an OpenWrt Based Router as OpenVPN Client](https://github.com/StreisandEffect/streisand/wiki/Setting-an-OpenWrt-Based-Router-as-OpenVPN-Client)

## 基本步骤
### 首先搭建Streisand服务器
按照[Streisand](https://github.com/StreisandEffect/streisand)的介绍搭建一个服务器

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

### dns 的设置
原作者建议不要在路由器上自己设置，而是使用服务器端的：
>Set up two script that use the DNS provided through the VPN Tunnel on the Streisand host (recommended).

即，设置两个脚本，这俩脚本使用的是我们的Streisand端托管VPN隧道提供的DNS
我也准备采用这种方式哈。

下面我们将建立文件并在里面设置dns，然后建立这两个脚本。

### 获取ovpn配置文件
这搭建好Streisand之后，会生成一个`streisand.html`文件，从这个文件可以下载。
里边有很多下载选项，我就点的第一个`alarm-laugh`，就下载了一个`[ip]-direct.ovpn`这种名字的配置文件。
__注意__：
>`streisand`的配置文件默认应该是没有密码的，所以无需我们自己建密码文件了。

### 根据ovpn配置文件生成我们自己的配置文件 '/etc/openvpn/streisand.conf'
下面将利用 `cat` 和`EOF' `从终端生成文件（作者应该是懒得教我们使用`scp`了）。

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

## 运行相关的命令
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
