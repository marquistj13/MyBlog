---
layout: post
title:  emacs 搭配 sumatrapdf 时 latex 的inverse search
categories: [编辑器等文档工具]
tag: [emacs,latex]
---

* content
{:toc}

以下来自 [Inverse search with Emacs/AucTeX and SumatraPDF](https://tex.stackexchange.com/questions/286028/inverse-search-with-emacs-auctex-and-sumatrapdf-on-windows-10)

用emacs写latex，然后设置用SumatraPDF打开生成的pdf
如何才能双击PDF某一个地方，跳转到emacs的对应位置呢？

在emacs的启动设置中写入：`(server-start)`

然后在SumatraPDF的设置、选项中的文本框中输入：`"C:\tools\emacs-25.3_1-x86_64\bin\emacsclientw.exe" -n +%l "%f"`
注意填入你自己的emacs路径。