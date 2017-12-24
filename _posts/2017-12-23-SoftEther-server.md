---
layout: post
title:  SoftEther VPN Server 配置
categories: 系统环境
tag: [配置文件]
---

* content
{:toc}

## 缘由
工作室的台式机可以方便地通过有线网访问v6，具体就是双网卡模式：
将有线网卡的v4协议去掉，就不会弹出登录界面，同时有线网卡的v6还可以照常使用。
而v4的网通过路由器即可使用

因此可以将台式机作为 VPN Server，这样我的其他设备如笔记本，手机等都可以方便地用v6了。

## 服务器端设置
好了开始折腾，自备梯子下载好SoftEther VPN Server之后，安装。
下面进行配置。

我发现有人采用vps的方式，即在其他地方搭一个vps server（如各种云主机），在该vps server 上安装SoftEther VPN Server，同时在工作室的电脑上也安装SoftEther VPN Server，然后让它俩连接（好像是桥接？），不明白为啥这么搞，我没法采用这种方式，嗯。
下面介绍官网介绍的方式。

打开软件之后，点击“连接”，就会弹出一个界面（当然我这个是设置过的，凑合看）：
![]({{ '/blog_images/2017-12-23-softether-server/new_connect.png' | prepend: site.baseurl}})
默认是用local host作为server，上面我提到的vps server作为host的话就要填入vps server的主机名端口号和密码，用local host作server的话只需要设置密码就行了。

然后弹出来一堆设置，大概按照 https://www.softether.org/4-docs/2-howto/1.VPN_for_On-premise/2.Remote_Access_VPN_to_LAN 的设置就行了。
注意我们只需要一个virtual hub就行了，我将其命名为VPN，
如下图：
![]({{ '/blog_images/2017-12-23-softether-server/local_bridge.png' | prepend: site.baseurl}})

设置登录用户的随便设，反正我设了好几个，用密码验证就行。

这些东西一开始设错了没事，反正最后给我们一个主界面上面，都可以回去修改,主界面如下图：
![]({{ '/blog_images/2017-12-23-softether-server/main_screen.png' | prepend: site.baseurl}})

我们在本地网桥设置中，将hub和我的以太网适配器（即有线网卡）进行了桥接，这样有线网卡可以get到的资源，我们的vpn client都能get到了。
（不知道为啥我的台式机无线网卡没有出现在桥接列表里，不管他了，反正能用）

另外，我们需要设置虚拟nat和虚拟dhcp，在主界面点击“管理虚拟hub”，就出来了，然后在右下角就看到了。
![]({{ '/blog_images/2017-12-23-softether-server/nat.png' | prepend: site.baseurl}})
然后启用securenat，此处的虚拟dhcp的网段可以设为我的台式机server段一样的网段，即192.168.1.10段，我看其他人没动，反正咋样都行吧。

主界面的动态dns可以设一个，后缀是.sedns.cn, 注意这个动态dns不知道为啥只能在局域网使用，也就是几乎没有意义，这时候我们需要点击主界面的 VPN Azure设置，得到一个.vpnazure.net的域名，这个才可以在外网访问我们的vpn，即内网穿透。
注意：得到vpnazure.net的域名之后，一般得等待一段时间（我是好几个小时吧）才能用，啥时候能用呢，就是你ping一下这个域名，全部能reply就行了。
（注意：这个vpnazure.net的域名仍然时好时坏，不稳定，哎，凑合用，不能用就拉倒，不捯饬了）
不过据说用vpnazure.net的话，所有流量都会去azure的服务器走一遍，所以速度有点问题，要是在内网用这个server的话，就老老实实用.sedns.cn吧


要想外网能访问，我们还需要在路由器上，将443端口映射到我的台式机上，这个选项一般在路由器的nat界面，端口转发或者端口映射。

配置好之后最好备份一下，点击主界面的“编辑设置”（在齿轮旁边），然后点击“保存到文件”，我们就备份好了，这样下次安装server的时候只需要在这个地方“导入文件并应用”就行了，这样上面设置的user啊，域名啊都是老样子了。

注：一个很好的参考https://blog.feixueacg.com/softethervpn-easyvpn/
看了这个我懂了，原来server地方随意，我们打开的只是一个管理器。

## 客户端设置
在我的笔记本上安装SoftEther VPN Client，建立新连接，填入我们的vpnazure.net的域名，账户和密码，443端口，直接双击就能连接了。

题外话，如同server端有线网卡的设置，我们需要设置client端的虚拟网卡的v6 dns server，就用https://github.com/lennylxx/ipv6-hosts 页面给的两个server就行了。还有client本地的host也设置成以上的链接中的host。




## 更新
我申请了digitalocean的一个主机，在上面搭建了softether server，为了省钱搞了个512的内存
基本操作是这个链接：
https://www.digitalocean.com/community/tutorials/how-to-setup-a-multi-protocol-vpn-server-using-softether#step-6-create-a-virtual-hub

我只是用它自己建了个hub：
`HubCreate VPN`
以及 `SecureNatEnable`
其它类似开机自启啥的我都懒得设置了，反正基本上一直开着的。

好像本地网桥也要设置。

用 softether client 连接的时候，需要在client的电脑上新建一个vpn网卡，反正 softether client会自己建的，然后将这个网卡的v4和v6的dns server设为https://github.com/lennylxx/ipv6-hosts  给的那几个。
也就是USA  USA
Hostname    ordns.he.net    tserv1.lax1.he.net
IPv6    2001:470:20::2  2001:470:0:9d::2
IPv4    74.82.42.42 66.220.18.42

注意我们要把softether client端的host文件设为电脑默认的。这样就能用了，只是速度好慢，估计是因为512内存太小了吧。

