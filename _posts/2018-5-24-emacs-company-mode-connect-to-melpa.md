---
layout: post
title:  emacs的company-mode让生活更美好 顺便找到更好的emacs安装 以解决 melpa的证书问题
categories: [编辑器等文档工具]
tag: [emacs,latex]
---

* content
{:toc}

以前用的是 `emacs-25.3_1-x86_64`。
记得在前面的博客：[使用irony将emacs打造为c++ IDE，代码补全]({{ site.baseurl }}{% post_url 2018-4-24-emacs-cpp-ide-irony %})
中，ubuntu上的emacs上用company-mode实现了c++的补全前端。

现在要写latex啦，默认的 `M+/` 补全实在不好使，咋安装company-mode呢？
`M+list-packages`,找到company安装即可。
我准备安装melpa里边的那个，但安装的时候老是提示我无法连接至melpa，找了一圈发现是因为我用的windows的build没有gnutls。
[这里](https://emacs.stackexchange.com/questions/27202/how-do-i-install-gnutls-for-emacs-25-1-on-windows)的解决方案是自己找gnutls的dll，然后放到emacs的bin目录，但这么搞好麻烦。

我采用的解决方法是重新安装emacs，[这里](https://github.com/m-parashar/emax64)有一个很完美的build，而且还是emacs26.1，自带gnutls和各种dll，完美啊。
安装好company之后，效果如下：
![]({{ '/blog_images/2018-5-24-company/company.png' | prepend: site.baseurl}})


