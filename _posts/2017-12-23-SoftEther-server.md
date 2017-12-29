---
layout: post
title:  SoftEther VPN Server 配置 （含本机作为server 以及 vps 作为server）
categories: 系统环境
tag: [配置文件]
---

* content
{:toc}

## 方式1：在本地计算机搭建server
### 缘由以及可行性
工作室的台式机可以方便地通过有线网访问v6，具体就是双网卡模式：
将有线网卡的v4协议去掉，就不会弹出登录界面，同时有线网卡的v6还可以照常使用。
而v4的网通过路由器即可使用

因此可以将台式机作为 VPN Server，这样我的其他设备如笔记本，手机等都可以方便地用v6了。

### 台式机服务器端设置
好了开始折腾，自备梯子下载好SoftEther VPN Server之后，安装。
下面进行配置。

下面介绍官网介绍的方式。

打开软件之后，点击“连接”，就会弹出一个界面（当然我这个是设置过的，凑合看）：
![]({{ '/blog_images/2017-12-23-softether-server/new_connect.png' | prepend: site.baseurl}})
默认是用local host作为server，上面我提到的vps server作为host的话就要填入vps server的主机名端口号和密码，用local host作server的话只需要设置密码就行了。

然后弹出来一堆设置，大概按照 [官网介绍](https://www.softether.org/4-docs/2-howto/1.VPN_for_On-premise/2.Remote_Access_VPN_to_LAN) 的设置就行了。
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

### 客户端设置
在我的笔记本上安装SoftEther VPN Client，建立新连接，填入我们的vpnazure.net的域名，账户和密码，443端口，直接双击就能连接了。

题外话，如同server端有线网卡的设置，我们需要设置client端的虚拟网卡的v6 dns server，就用https://github.com/lennylxx/ipv6-hosts 页面给的两个server就行了。还有client本地的host也设置成以上的链接中的host。

由于在服务器端同时设置了本地网桥和secure nat，因此可以可以使用v6.



## 方式2：在vps上搭建server
### 服务器端
我发现有人采用vps的方式，即在其他地方搭一个vps server（如各种云主机），在该vps server 上安装SoftEther VPN Server，同时在工本地电脑上 安装SoftEther VPN server 端管理器就行了


我申请了digitalocean的一个主机，在上面搭建了softether server，为了省钱搞了个512的内存

>基本操作可以参考 [这个链接](https://www.digitalocean.com/community/tutorials/how-to-setup-a-multi-protocol-vpn-server-using-softether#step-6-create-a-virtual-hub)
我只是用它自己建了个hub：
`HubCreate VPN`
以及 `SecureNatEnable`
但这个连接貌似不太靠谱，还是暂时不要用了

我是按照
[跨网组建大型局域网之SoftEther VPN的搭建与连接](https://bbs.jiasuidc.com/index.php/2017/11/18/%E8%B7%A8%E7%BD%91%E7%BB%84%E5%BB%BA%E5%A4%A7%E5%9E%8B%E5%B1%80%E5%9F%9F%E7%BD%91%E4%B9%8Bsoftether-vpn%E7%9A%84%E6%90%AD%E5%BB%BA%E4%B8%8E%E8%BF%9E%E6%8E%A5/)
这个来的
其它类似开机自启啥的我都懒得设置了，反正服务器基本上一直开着的。

注意我按照[跨网组建大型局域网之SoftEther VPN的搭建与连接](https://bbs.jiasuidc.com/index.php/2017/11/18/%E8%B7%A8%E7%BD%91%E7%BB%84%E5%BB%BA%E5%A4%A7%E5%9E%8B%E5%B1%80%E5%9F%9F%E7%BD%91%E4%B9%8Bsoftether-vpn%E7%9A%84%E6%90%AD%E5%BB%BA%E4%B8%8E%E8%BF%9E%E6%8E%A5/)这个连接设置的，在协议设置窗口那里，只勾选了第一个框即`remote access  vpn server",没有勾选第二个，因此就没有必要设置本地网桥（还是别设了）

### dns server的设置
由于某种特殊的原因dns server的设置非常有必要，注意两个原则
__要么让vpn client端设置dns server，要么在vpn server那里设置dns server，两者必选其一__

先说第一种方案，在vpn client端设置dns server：
>用 softether client 连接的时候，需要在client的电脑上新建一个vpn网卡，反正 softether client会自己建的，然后将这个网卡的v4和v6的dns server设为https://github.com/lennylxx/ipv6-hosts  给的那几个。
也就是USA  USA
Hostname    ordns.he.net    tserv1.lax1.he.net
IPv6    2001:470:20::2  2001:470:0:9d::2
IPv4    74.82.42.42 66.220.18.42
注意我们要把softether client端的host文件设为电脑默认的。这样就能彻底依赖dns server了，只是速度好慢，估计是因为512内存太小了吧。

再说第二种方案（推荐）
> 在[跨网组建大型局域网之SoftEther VPN的搭建与连接](https://bbs.jiasuidc.com/index.php/2017/11/18/%E8%B7%A8%E7%BD%91%E7%BB%84%E5%BB%BA%E5%A4%A7%E5%9E%8B%E5%B1%80%E5%9F%9F%E7%BD%91%E4%B9%8Bsoftether-vpn%E7%9A%84%E6%90%AD%E5%BB%BA%E4%B8%8E%E8%BF%9E%E6%8E%A5/)教程的securenat那里，securenat启用之后还是用的默认配置（注意mac地址那里不要改），并没有根据以上连接重新设置dns，默认情况下，dns server1人家默认设为了192.168.30.1，我们可以不用管它，只需要设置dns 服务器地址2 就行了，我们设为74.82.42.42，然后为了保险起见在域名那里再设置一个dns server，设为tserv1.lax1.he.net

### 手机端连接
由于我们开启了 L2TP服务器功能，即（ L2TP over IPsec )，而移动端基本都内置了这个协议，因此在安卓手机自带的vpn界面（在设置里边找）。
新建一个vpn设置文件，名称随意设置，类型选为 L2TP/IPSec PSK
填写服务器地址
预共享密钥设为vpn
填写用户名和密码就行了。

有一个小trick，不开wifi连接vpn成功以后，再打开wifi会断开vpn，所以连上wifi再连vpn就行了，这个不是大问题。

### windows自带的vpn连接
windows端使用SoftEther VPN Client的设置很简单，其协议为使用SSL-VPN协议连接。

而如果使用windows自带的vpn，其设置需要一点技巧，其协议为L2TP （和手机端一样）。
根据 [SoftEther VPN——Linux下搭建VPN可以如此简单](https://www.1fishsauce.com/?p=463)的介绍，
>使用L2TP协议时应当注意：1）”VPN类型“需要选择”L2TP/IPsec“；2）需要到”高级设置“中输入先前设置的预共享密钥。细节就不再讲了，其他操作系统类似。

盗个图哈哈：
![]({{ '/blog_images/2017-12-23-softether-server/SoftEther-VPN-Config-9.jpg' | prepend: site.baseurl}})

## 解决手机端wifi无法连接vpn的问题
有时候会出现这种情况，用手机自带的vpn（在设置里边有）连接时，用数据流量很容易连接vpn，但连上wifi后就很难连接到vpn了

这时候只需要重启vpn server就行了。

为了不频繁手动重启，我决定搞一个crontab,定时重启哈哈。
根据 [19. crontab 定时任务](http://linuxtools-rst.readthedocs.io/zh_CN/latest/tool/crontab.html)的参考，可以在 `$HOME` 建一个crontab文件，`$HOME` 目录是啥，你 `echo $HOME`就知道了,我的就是 root目录。
好了，我们新建一个 `marquis_cron` 的文件，文件名随意哈。

根据示例文件：
```sh
# (put your own initials here)echo the date to the console every
# 15minutes between 6pm and 6am
0,15,30,45 18-06 * * * /bin/echo 'date' > /dev/console
```

我们打算在北京时间凌晨三点重启vpn server，换算一下，在utc 19点
具体换算时间在 [UTC与本地时间(GMT +08)换算表](http://www.timebie.com/cn/stduniversal.php)可以看到
因此 `marquis_cron` 的内容为：
```sh
0 19 * * * /root/vpnserver/vpnserver stop
0 19 * * * /root/vpnserver/vpnserver start
```

然后运行 `crontab marquis_cron`就行了。

如果不想要这个crontab文件了，可以用 `crontab -r`来删除，详情看上面的链接。
用`crontab -l`可以查看当前cron的状态。

也不知道能不能成功，我试了一下其他命令，好像没有执行？不管了。
## 其它细节备份
### Ubuntu vps端 softether server的安装
从do那里初始化一个Ubuntu之后，先apt-get update, apt-get install build-essential
然后下载softether的server，使用wget命令，server程序的地址是 
`http://www.softether-download.com/files/softether/v4.24-9652-beta-2017.12.21-tree/Linux/SoftEther_VPN_Server/64bit_-_Intel_x64_or_AMD64/softether-vpnserver-v4.24-9652-beta-2017.12.21-linux-x64-64bit.tar.gz`

这个地址可以从网页端（可能需要翻墙）下载，然后就得到了该地址。
在Ubuntu用
`wget http://www.softether-download.com/files/softether/v4.24-9652-beta-2017.12.21-tree/Linux/SoftEther_VPN_Server/64bit_-_Intel_x64_or_AMD64/softether-vpnserver-v4.24-9652-beta-2017.12.21-linux-x64-64bit.tar.gz`
就行了，然后解压使用 `tar -xvzf 文件名`
`./.install.sh`
执行 `./vpnserver start` 启动服务。 
运行 `./vpncmd` 进入VPN的命令行,选择1 “Management of VPN Server or VPN Bridge” 在指定Hostname of IP Address of Destination:这里写 `localhost:433`
然后Specify Virtual Hub Name: 这里直接回车，用默认的。
貌似还需要运行`VPN Server> ServerPasswordSet`设置远程管理密码
（根据 [SoftEther VPN Server 安装手记 + 福利](https://www.bennythink.com/softether-vpnserver.html)的指示，直接 `./vpncmd` 然后ServerPasswordSet设置密码，这样才能用管理器远程连接服务器，好像先不设密码也能连接？不管了。）

紧接着就可以用Windows端的SoftEther VPN Server Manager直接登录server进行管理了。

### 将vps端softether server开机自启
根据[SoftEther VPN Server 安装手记 + 福利](https://www.bennythink.com/softether-vpnserver.html)将服务器加入到开机启动项中，这样服务器重启了就不用每次都手动到 SSH 里开启了。
终端里依次输入：
`vi /etc/rc.local`
在 exit 0 之前写入
`/root/vpnserver/vpnserver start`
保存退出即可

### Windows上面的local host
如果在Windows上面安装了SoftEther VPN Server，默认好像自带了一个localhost的server，如果不小心删除了，再新建的话可能会出现需要Administrator登录的情况，而且无论如何都登录不了，这时候我们想到了重装SoftEther VPN Server，但卸载SoftEther VPN Server的时候很不干净，还需要去安装目录删除那些文件，我试了好几次都不成功，我又将SoftEther VPN Server的自启服务关掉（在任务管理器可以关掉它），卸载，删文件，然后重启，还是不行，这时候我感觉是win10的快速启动的原因，关机，关电源，开机，重装server，这时候终于可以连接local host了，只需要重设密码就行了，以后再也不搞了，呜呜

### vps上只需要设securenat就行了
记住不要设本地网桥！

### server级联
在[通过softether实现外网远程桌面连接校园网电脑](https://www.lookfor404.com/%E9%80%9A%E8%BF%87softether%E5%AE%9E%E7%8E%B0%E5%A4%96%E7%BD%91%E8%BF%9C%E7%A8%8B%E6%A1%8C%E9%9D%A2%E8%BF%9E%E6%8E%A5%E6%A0%A1%E5%9B%AD%E7%BD%91%E7%94%B5%E8%84%91/),有人为了用windows的远程桌面访问办公室的电脑，专门在办公室的电脑设了个localhost server，然后找到“管理级联连接”，连接到vps上的服务器，然后家里的电脑就可以直接用softether-client连vps，用内网地址连接办公室电脑了
我感觉不这么搞也行吧，办公室电脑用softether-client连vps，家里电脑也用softether-client连vps，两者自然处于同一个局域网，嗯这两种方式原理应该一样，不折腾了，没时间了。

### 保存server端配置
在主界面有一个大大的齿轮，名称是“编辑设置”，点开，它不能直接编辑，可以将其保存到文件，会生成一个`.config`的文件，用文本编辑器打开修改后，可以点击“导入文件并应用”，就生效了，而且还会自动重启server。


__哈哈， 下次安装server的时候，直接导入这个文件就行了，就不用点那么多了。__

还可以用这个文件关掉动态域名，将ddnsclient的 bool Disabled设为true就行了。


## 利用web.py搭建网站
### hello world
根据 [web.py 0.3 新手指南](http://webpy.org/tutorial3.zh-cn)的介绍搭建了一个hello world网站。

首选安装python，去anaconda官网找到Linux下载文件的链接，是一个`.sh`的文件，用wget下载好之后，安装即可，安装的时候选择加入path就行了。
然后就可以 `pip install web.py`就可以按照[web.py 0.3 新手指南](http://webpy.org/tutorial3.zh-cn)操作了。

这个文件
```python
import web

urls = (
    '/', 'index'
)

class index:
    def GET(self):
        return "Hello, world!"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
```
可以直接用，由于默认的网页应该是80端口，因此运行时使用 `python code.py 80`,就可以访问网站了。

###  怎么加入中文支持呢？
按照 [Web.py HelloWorld与中文乱码](http://www.codexiu.cn/python/blog/19224/)的介绍，只需要在return之前，加入`web.header('Content-Type','text/html;charset=UTF-8')`即可，即
```python
# coding=utf-8
import web
urls=(
      '/','index'
)
class index:
    def GET(self):
        web.header('Content-Type','text/html;charset=UTF-8')
        return 'Hello Word!你好!'
    
if __name__=='__main__':
    app=web.application(urls,globals())
    app.run()
```

### 如何一直运行这个文件呢？
根据[linux的nohup命令的用法](https://www.cnblogs.com/allenblogs/archive/2011/05/19/2051136.html), 在运行上述命令的时候 `nohup 命令 &`就行了，即 `nohup python code.py 80 &`
这样即使关闭了ssh会话，它还在运行。