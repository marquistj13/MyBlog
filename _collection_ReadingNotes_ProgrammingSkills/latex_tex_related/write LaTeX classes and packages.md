---
title:  写 classes and packages
date:   2017-11-6
---


* content
{:toc}

在 [开发一个 LaTeX 宏包需要多少知识？](https://www.zhihu.com/question/27017364) 中，刘老师提到了 [Learning to write LaTeX classes and packages](http://www.tex.ac.uk/FAQ-writecls.html) 这个网站，
写模板其实就是写一些 `\(re)newcommand` and `\(re)newenvironment` commands
虽然写模板涉及很多东西，终究还是有一个学习顺序的，如以上提到的clsguide.pdf我就看过了。

Good things come in little packages An introduction to writing ins and dtx files

Rolling your own Document Class Using LATEX to keep away from the Dark Side



thuthesis的使用
一开始编译的时候可能会遇到各种错误，很大原因就是自己电脑的各种latex包需要更新了，我用的texlive2016，直接用自带的包管理器更新所有已安装的package就行了，记得更新的时候选择近一点的源，中科大或清华的都行吧。

Windows平台 `make` 命令的使用
Linux系统一般自带了 `make` 工具，Windows下需要自己安装，估计cygwin和mingw都能用吧。 我安装了mingw，具体安装步骤：
用mingw-get-setup.exe安装mingw的MinGW Installation Manager, 然后只安装最核心的版本就行了，即 `msys-base`,然后将其bin目录加到path中，如我的bin目录是 `C:\tools\mingw\msys\1.0\bin`，这样就能在 `cmd` 中使用 `make` 了。