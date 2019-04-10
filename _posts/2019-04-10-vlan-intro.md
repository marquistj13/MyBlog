---
layout: post
title: OpenWRT 中 vlan 的使用
categories:  [系统环境]
tag: [配置文件]
---

* content
{:toc}

声明:
本人非网络工程背景，只是用到了vlan，用的过程中查了点资料，理解可能不全面，因此只是笔记性质。


## openwrt 官网的示例
在 [Switch Documentation](https://openwrt.org/docs/guide-user/network/vlan/switch) 中有一图：
![]({{ '/blog_images/2019-04-10-vlan-intro/asus-internals-default.png' | prepend: site.baseurl}})
文章中说，只要有大于一个lan口基本都需要vlan。
对应于上图而言，在luci中:
* wan口对应的设备是 `eth0`, 对应的vlan 是 `vlan1`
* lan口对应的设备是 `eth0`, 对应的vlan 是 `vlan0`
* wifi 对应的设备是 `eth2`

## 我的设备的vlan
### 粗浅的认识
我的设备是 Linksys WRT1200AC, 固件版本是 OpenWrt 18.06.1。

![]({{ '/blog_images/2019-04-10-vlan-intro/vlan201_router_switch_final.png' | prepend: site.baseurl}})
装好openwrt之后其实只有 `vlan1` 和 `vlan2`，最后面的 `vlan201` 是我自己建的，用来传输带tag（也就是vlan id)的数据，我们暂时先不管 `vlan201`。

先搞清楚图中的 `未标记` 和 `已标记` 的意思:
在 [VLAN](https://openwrt.org/docs/guide-user/network/vlan/switch_configuration) 中说的很清楚了，不管是 `未标记` 还是 `已标记`，都是相对于将要到达某个口的network traffic而说的，而不是已经进到某个口的network traffic。
1. `已标记`：进入该口的network traffic必须是带tag的，以上图第一行（即vlan 1)为例，进入 CPU (eth0 设备) 的数据必须是带tag的
1. `未标记`：进入该口的network traffic必须是不带tag的（要是数据带tag，就会将该数据也就是 network traffic 丢弃掉），并且从该口出去的network traffic的tag会被remove掉。 **注意** 每一个口只能对一个vlan id设为  `未标记`（很容易理解嘛，如果一个口对 vlan1 设为  `未标记`，同时也对 vlan2 设为  `未标记`，那么它就不知道自己到底属于哪个vlan了，实际上 network traffic 进入该口之后是要打上对应的vlan tag的，它就不知道到底该打上哪个tag了）
1. `关`：带有该vlan id的数据无法到达这些口。

### 详细的解释
上面这些描述其实还没那么好理解，我们再详细解释一下。
1. 很明显，此处 `eth0` 就是我们的路由器的 lan 口，对应于 `vlan1`, `eth1` 就是 wan 口，对应于 `vlan2`
1. 先看第一行， 即 `vlan1`, 不带tag 的数据到达 lan1, lan2, lan3 之后就会被打上 vlan1 的tag，然后由于 CPU (eth0) 设为了`已标记`，因此这些带有 vlan1 tag 的数据能进入 CPU (eth0)。由于 lan 4 和wan都设为 `关`，因此这些带有 vlan1 tag 的数据无法到达lan4 和 wan。从这个意义上来说，lan1, lan2, lan3 和 CPU (eth0) 同属于 vlan1。 另外注意，虽然 不带标签的数据进入 lan1之后被打上了 vlan 1 tag，从而送到了 CPU(eth0),但是这些带有 vlan 1 tag 的数据从 lan1出去（就是到路由器外面）的时候会将 vlan 1 tag 去掉。
1. 再看第二行，即 `vlan2`,也就是 WAN口对应的vlan，很明显只有 wan 和 CPU (eth1) 加入了 vlan2。
1. 再看第三行， 即 `vlan201`， 很明显只有 CPU (eth0) 和 lan4加入了 vlan 201。注意 此处 lan 4 我设置成了 `已标记`，也就是说只有带有 vlan 201 tag的数据才能通过 lan4。



### 对应的配置文件
vlan的配置既可以在luci界面操作，也可以直接写配置文件， 即文件 `/etc/config/network`。
比较关键的部分只有三个，我摘抄如下。
1. 第一部分就是wan口和lan口的配置：
```sh
config interface 'lan'
        option type 'bridge'
        option ifname 'eth0.1'
        option proto 'static'
        option ipaddr '192.168.1.1'
        option netmask '255.255.255.0'
        option ip6assign '60'
config interface 'wan'
        option ifname 'eth1.2'
        option proto 'static'
        option ipaddr '192.168.2.3'
        option netmask '255.255.255.0'
        option gateway '192.168.2.1'
        option dns '114.114.114.114'
```
由于我的路由器是二级路由，也就是说其wan口其实接的是一级路由（一个华为路由器）的lan口，因此可以设成静态协议，将ip固定为 `192.168.2.3`。
路由器的lan口的网段是`1.1`。
1. 第二部分就是vlan的配置：
```sh
config switch_vlan
        option device 'switch0'
        option vlan '1'
        option ports '1 2 3 5t'
        option vid '1'
config switch_vlan
        option device 'switch0'
        option vlan '2'
        option ports '4 6t'
        option vid '2'
config switch_vlan
        option device 'switch0'
        option vlan '3'
        option vid '201'
        option ports '0t 5t'
```
这个配置要对照着上面的图来看，这里解释一点，如果不设置 `vid` 的话， vlan id 和 vlan number 一致，如果设了 vlan id，就按照设置的 vlan id来。
上面的配置中，`t` 代表 tagged（`已标记`)，很明显vlan 1中的 5 代表 CPU (eth0)， vlan 2中的 6 代表CPU (eth1)， vlan 201 中的 0代表 lan 4。
1. 第三部分就是 vlan interface的配置：
```sh
config interface 'vlan201'
        option proto 'static'
        option ipaddr '192.168.201.1'
        option netmast '255.255.255.0'
        option ifname 'eth0.201'
        option netmask '255.255.255.0'
```
注意哈，openwrt自带了 vlan1 和 vlan2，我们新建的vlan201要想能用，得给它建一个interface（接口）才行，
当然还得设置防火墙：
![]({{ '/blog_images/2019-04-10-vlan-intro/vlan201_firewall.png' | prepend: site.baseurl}})


## 为什么要用vlan
其实这个才是最根本的问题，我就不提啥“避免广播风暴”、“安全隔离”了，这东西我也不太懂。
我用vlan 是因为有需求。
这里先不谈我的需求，先搞清楚上面的vlan 201 可以怎么用：
由于 vlan201的lan 4已经设为了 `已标记` 因此我的电脑要是连接了lan 4就必须在电脑上新建一个vlan 2，这样电脑才能用路由器上网。 但vlan的通常用法不是这样的，而是将lan 4设为`未标记`，也就是
将配置文件改为：
```sh
config switch_vlan
        option device 'switch0'
        option vlan '3'
        option vid '201'
        option ports '0 5t'
```
这样我们的电脑连接了lan 4就行了，在电脑端只需要通常的配置，也就是dhcp就行了，这样我们的电脑就处于`192.168.201`的子网了，而连接 lan1, lan2, lan3 的电脑加入的是 vlan 1，因此位于`192.168.1`的子网，是不是很有意思？

到了这里，就可以谈我的需求啦。
我设置vlan 201的终极目的其实是将翻墙信号打上 vlan tag（因此要将lan 4设为 `已标记`），然后通过旁挂式组网的方式送给AC，最后通过AP发送出去。
原理和上面其实一样，只是多了一步，也就是建立一个openvpn的翻墙隧道：
```sh
config interface 'streisandvpn'
        option proto 'none'
        option ifname 'tun0'
```
然后将防火墙修改如下：
![]({{ '/blog_images/2019-04-10-vlan-intro/vlan201_vpn_firewall.png' | prepend: site.baseurl}})

至于如何建立vpn隧道，可参考 [将 openwrt 路由器作为 openvpn client]({{site.baseurl}}{% link _posts/2018-12-15-openwrt-openvpn-client-setup.md %})
