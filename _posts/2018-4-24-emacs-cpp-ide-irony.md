---
layout: post
title:  使用irony将emacs打造为c++ IDE，代码补全
categories: [编辑器等文档工具]
tag: [emacs]
---

* content
{:toc}

## 起因
vscode虽然很方便地看代码，不过时不时没法解析了，没法跳转了，没法补全了。
所以寻求emacs的解决方案。
使用irony插件很顺利地实现了 __代码补全__。
## 已有的环境
* virtual box上装了ubuntu16.04
* 已安装vscode用来看代码，这个vscode和我们介绍的emacs并无任何关系，哈哈。
* 已安装emacs 24.5， 并且emacs并无任何配置（全新的安装）。
* 已安装clang
* 已安装 cmake最新版

## 搞起来
首先按照[irony-mode官网](https://github.com/Sarcasm/irony-mode)，的步骤装上irony。

### libclang
由于irony依赖`libclang`，因此要先装它：`sudo apt install libclang-dev`

### 配置melpa,安装并配置irony
首先在home目录，即你的`~/`目录，新建一个配置文件`.emacs`,并写入：
```
(setq package-archives '(("gnu"   . "http://mirrors.tuna.tsinghua.edu.cn/elpa/gnu/")
                         ("melpa" . "http://mirrors.tuna.tsinghua.edu.cn/elpa/melpa/")))
(package-initialize)
```
注意，我用别人给的源老是找不到irony，这个清华的源很强，上面的url就是[清华大学开源镜像的页面](https://mirror.tuna.tsinghua.edu.cn/help/elpa/)给的。

然后：
`M-x package-install RET irony RET`

配置为：
```lisp
(add-hook 'c++-mode-hook 'irony-mode)
(add-hook 'c-mode-hook 'irony-mode)
(add-hook 'objc-mode-hook 'irony-mode)
(add-hook 'irony-mode-hook 'irony-cdb-autosetup-compile-options)
```

### 其他配件
irony貌似只是一个后端，代码补全的前端可以使用Company，语法检查用Flycheck，另外用来显示参数列表的eldoc也是极好的。
装吧：
```lisp
M-x package-install irony-eldoc
M-x package-install flycheck-irony
M-x package-install company-irony
```

这几个插件的配置文件可以[抄这里](https://github.com/martin-tornqvist/env/blob/master/how-to-setup-irony-mode.txt)。
详见下一节。
### 配置文件汇总
```lisp
(setq package-archives '(("gnu"   . "http://mirrors.tuna.tsinghua.edu.cn/elpa/gnu/")
                         ("melpa" . "http://mirrors.tuna.tsinghua.edu.cn/elpa/melpa/")))
(package-initialize)


;; irony-mode
(add-hook 'c++-mode-hook 'irony-mode)
(add-hook 'c-mode-hook 'irony-mode)
(add-hook 'objc-mode-hook 'irony-mode)
(add-hook 'irony-mode-hook 'irony-cdb-autosetup-compile-options)

;; company mode
(add-hook 'c++-mode-hook 'company-mode)
(add-hook 'c-mode-hook 'company-mode)

;; flycheck-mode
(add-hook 'c++-mode-hook 'flycheck-mode)
(add-hook 'c-mode-hook 'flycheck-mode)
(eval-after-load 'flycheck
'(add-hook 'flycheck-mode-hook #'flycheck-irony-setup))

;; eldoc-mode
(add-hook 'irony-mode-hook 'irony-eldoc)
```

## 想了解更多看这里啊
* rtags也是和irony平行的后端，且支持跳转，不过比较麻烦，不搞了。
* 这篇 [Emacs as a C++ IDE](http://martinsosic.com/development/emacs/2017/12/09/emacs-cpp-ide.html) 对irony和rtags介绍的很详细。

### 安装projectile
根据[Emacs as a C++ IDE](http://martinsosic.com/development/emacs/2017/12/09/emacs-cpp-ide.html)的推荐，我还装了`projectile`
,这个用来给emcas一个project的概念，从而方便在工程文件之间进行跳转，用法详见：[projectile](https://github.com/bbatsov/projectile)。

安装：
`M-x package-install [RET] projectile [RET]`

简介一下用法，只要你的文件有git等的文件，它就会将这个文件夹理解为一个project，或者你直接在文件夹里边放一个空的 `.projectile`就行了。
配置文件：
```lisp
;; projectile-mode
(add-hook 'c++-mode-hook 'projectile-mode)
(add-hook 'c-mode-hook 'projectile-mode)
```

### ctrl x ctrl f的时候用方向键选择曾经的历史文件
```lisp
;; c-x c-f 的时候用上下箭头来选择历史文件。
;; from  http://stackoverflow.com/questions/3527150/open-recent-in-emacs
(savehist-mode 1)
```