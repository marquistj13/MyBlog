---
layout: post
title:  自动化脚本用于enable/disable IPv4 on a specific network adapter
categories: 系统环境
tag: [配置文件]
---

* content
{:toc}

##  任务需求
win10的电脑，每天开机后我需要先enable有线网卡的ipv4协议，过几秒之后（有线网卡此时获取了公网v6地址）再disable有线网卡的ipv4协议（此时我继续使用无线网卡的v4）。

## 初步搜索
我找到了一个解决方法： [Script to enable/disable IPv4 on a specific network adapter Win 7](https://superuser.com/questions/759244/script-to-enable-disable-ipv4-on-a-specific-network-adapter-win-7/759246#759246):
>
you could do this in powershell like so:
Disable-NetAdapterBinding -Name MyAdapter -DisplayName "Internet Protocol Version 4 (TCP/IPv4)"
I know your question states batch file, but save this with a .ps1 extension and it should do what you need it to.

原来用powershell可以搞啊。

## 细节探索以及小问题解决
不知道网卡名字（MyAdapter）咋办？
搜索Disable-NetAdapterBinding，找到 [官网介绍](https://technet.microsoft.com/zh-cn/library/jj130872(v=wps.630).aspx) 发现仍然没有获取名字的方法，在左边发现了一个 `Get-NetAdapter` 命令，[该页面](https://technet.microsoft.com/zh-cn/library/jj130921(v=wps.630).aspx) 也没有，这时候我发现名字就是网卡名，即"以太网"。
可以用命令 `Get-NetAdapterBinding –Name * -DisplayName "Internet*"` 列出所有网卡的名字。

至于以上两个页面的命令需要注意，我们需要的另一个参数 `-DisplayName`, 微软官网列出的是英文版的命令，如果你的Windows系统是中文版的，那么就得用对应的命令的中文版，可以通过 `Get-NetAdapterBinding -Name "以太网" -AllBindings` 查看对应的 DisplayName，以及该网卡的状态。
这样-DisplayName "Internet Protocol Version 4 (TCP/IPv4)" 就得替换成：-DisplayName "Internet 协议版本 4 (TCP/IPv4)"

* 总结如下
（以下命令需要在powershell允许，而非普通的cmd）
`Enable-NetAdapterBinding -Name "以太网" -DisplayName "Internet 协议版本 4 (TCP/IPv4)"`: 用来enable 该网卡的v4 （需要管理员权限）
`Get-NetAdapterBinding -Name "以太网" -AllBindings`:查看该网卡的各种属性，包括v4是否enable了。
`Disable-NetAdapterBinding -Name "以太网" -DisplayName "Internet 协议版本 4 (TCP/IPv4)"`:就是关掉该网卡的v4 （需要管理员权限）

以上命令来自Get-NetAdapterBinding以及Disable-NetAdapterBinding的官网页面。

另外，我查到延时命令可以用  `Start-Sleep -s 10` 10 秒，或用 `Start-Sleep`的alias `sleep`.

## 写成脚本
直接将
```
Enable-NetAdapterBinding -Name "以太网" -DisplayName "Internet 协议版本 4 (TCP/IPv4)"
sleep -s 2
Disable-NetAdapterBinding -Name "以太网" -DisplayName "Internet 协议版本 4 (TCP/IPv4)"
```
保存成 `v4_enable_disnable.ps1` 找不到已管理员权限运行，因此我又写了个cmd的脚本（.bat)，根据以下资料的做法
[Provide A Batch File To Run Your PowerShell Script From; Your Users Will Love You For It](http://blog.danskingdom.com/allow-others-to-run-your-powershell-scripts-from-a-batch-file-they-will-love-you-for-it/),换成我的文件名
```
@ECHO OFF
SET ThisScriptsDirectory=%~dp0
SET PowerShellScriptPath=%ThisScriptsDirectory%v4_enable_disnable.ps1
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& {Start-Process PowerShell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File ""%PowerShellScriptPath%""' -Verb RunAs}";
```
保存为bat之后，直接双击运行即可。
（bat和ps1这俩脚本放到一个文件夹下即可。然后可以将bat发送快捷方式到桌面）

_注意_：如果用一般的编辑器保存`v4_enable_disnable.ps1`的话，可能是由于编码问题，一直无法运行成功，此时我发现需要了解以下ps1脚本的规范了，根据 [这里](https://www.howtogeek.com/141495/geek-school-writing-your-first-full-powershell-script/) 的描述，Windows上有一个Windows PowerShell ISE程序，用这个保存就行了。



