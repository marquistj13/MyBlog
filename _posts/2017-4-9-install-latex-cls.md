---
layout: post
title:  Texlive 添加新的cls文件
categories: 编辑器等文档工具
tag: [latex]
---




* content
{:toc}

下载好cls文件以后，我们要将其加入latex的搜索路径，放哪儿呢？
找了一圈儿，发现很简单啊

对于我的win10,texlive2016来说，先用 `kpsewhich -var-value=TEXMFHOME`看一下home是啥，我的是 `C:/Users/Marquis/texmf`，好了就放在这个文件夹就行了么

什么？ `C:/Users/Marquis` 没有 `texmf` 目录？自己建啊亲，对了还得再建一个 `tex` 目录，假设你的cls名字为xx.cls,那么最好再建一个xx的文件夹，这样
最终就是:`C:/Users/Marquis/texmf/tex/xx/xx.cls`

这时候用命令 `kpsewhich xx.cls` 如果它能找到这个xx.cls的路径，那就成功啦。
对了，不用重启电脑。