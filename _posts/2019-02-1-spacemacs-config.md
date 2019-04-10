---
layout: post
title:  spacemacs 的配置
categories:  [编辑器等文档工具]
tag: [emacs]
---

* content
{:toc}

以下：
1. 我的emacs运行在Ubuntu上（[安装说明](https://marquistj13.github.io/MyBlog/2018/12/ubuntu-work-environment-setup/#spacemacs))
1. 不对emacs和spacemacs进行区分。
1. 配置文件特指 .spacemacs
1. 我用的emacs类型的快捷键，因此 先导`SPC` 就是 `M-m`，但是命令中间的`SPC` 还是空格的意思 。

## tex 中 bib 文件的指定
[这里](https://marquistj13.github.io/MyBlog/2018/12/ubuntu-work-environment-setup/#spacemacs)介绍了texlive 和 spacemacs 的安装.
为了能够方便地使用reftex插入参考文献，即 `C-c [`，emacs需要知道bib文件的位置。
通常我们的tex文件会有一句话指定bib文件，如`\addbibresource`,`\bibliography{references1,references2}` 等。
但是据我的经验，一般写了这个指定bib文件的命令后，必须得重启emacs才能生效，即emacs才能对`C-c [`做出反应。

由于我的系统里，bib文件一般只有一个，很多个tex的project都共享这一个就行了，所以能不能直接一次性地告诉emacs我的bib文件的地址呢？

可以，参考[RefTeX won't find my .bib file in local library tree](https://tex.stackexchange.com/questions/54739/reftex-wont-find-my-bib-file-in-local-library-tree).
只需要在配置文件的 `dotspacemacs/user-config` 部分添加： 
`(setq reftex-default-bibliography '("/home/marquis/Documents/MyLibrary.bib"))`
即可。

另外，为了让一行容纳更多字数，即不要频繁换行，我还设了`(setq-default fill-column 100)`， 不过目测没啥用……
## 配置文件的地址
输入 `M-m f e d`
## 字体大小
在配置文件的 `dotspacemacs-default-font` 设定 `:size 15` 即可。

另外我的快捷键模式是emacs类型的，即 `dotspacemacs-editing-style 'emacs`


## 启动 最大化窗口
设为true即可。
`dotspacemacs-maximized-at-startup t`

## 各种layer的配置
默认的配置文件并没有加入c++的layer。
怎么查看c++ layer的说明呢？
输入 `M-m h` 就可以看到很多选项，此时 `l` 就可以输入 `c++` 然后就能看到该layer的配置说明了,例如怎么打开该layer，该layer的选项，以及快捷键，切换头文件和cpp文件就可以`SPC m g a`。
这个`M-m h`帮助页面有很多有意思的帮助，值得参考。

我基本上是根据各种layer的配置说明进行配置的，因此`dotspacemacs-configuration-layers`变量的值为：
```lisp
 dotspacemacs-configuration-layers
   '(
     php
     yaml
     ;; ----------------------------------------------------------------
     ;; Example of useful layers you may want to use right away.
     ;; Uncomment some layer names and press <SPC f e R> (Vim style) or
     ;; <M-m f e R> (Emacs style) to install them.
     ;; ----------------------------------------------------------------
     helm
     (latex :variables latex-enable-auto-fill t)
     (c-c++ :variables
            c-c++-default-mode-for-headers 'c++-mode)
     gtags
     auto-completion
     pdf-tools
     ;; better-defaults
     emacs-lisp
     ;; git
     ;; markdown
     ;; org
     (shell :variables
             shell-default-height 30
             shell-default-position 'bottom)
     ;; spell-checking
     ;; syntax-checking
     ;; version-control
     )
```

注意，gtags用于查询源代码中各种符号的 definitions or references，用于查看源代码时进行各种跳转。
它只是一个client，因此需要安装`global`，即 `sudo apt-get install global`.
当然使用的时候，要首先产生tags，要么运行`helm-gtags-create-tags`或 (`SPC m g c`)，要么直接在你的根目录运行`gtags`，另外还可以给`gtags`不同的选项以支持不同的语言（如Python等）。
## 用户自定义设置，即变量 `dotspacemacs/user-config`
下面的配置中
1. `(setq reftex-default-bibliography '("/home/marquis/Documents/MyLibrary.bib"))` 用于配置参考文献的地址，在前面tex配置的地方讲过。
1. `(setq-default fill-column 100)` 用于配置类似换行的东西，貌似没啥用。
1. `TeX-view-program-list,TeX-view-program-selection,TeX-source-correlate-start-server` 用于指定tex生成的pdf的打开程序。注意由于在layer的配置中我们加载了`pdf-tools`因此会自动用`pdf-tools`进行打开，这里不需要设置。我把这些写下来仅仅是方便以后改用其他pdf打开程序。

```lisp
(defun dotspacemacs/user-config ()
  "Configuration function for user code.
This function is called at the very end of Spacemacs initialization after
layers configuration.
This is the place where most of your configurations should be done. Unless it is
explicitly specified that a variable should be set before a package is loaded,
you should place your code here."
  (setq reftex-default-bibliography '("/home/marquis/Documents/MyLibrary.bib"))
  ;;(require 'fill-column-indicator)
;;  (setq auto-fill-mode nil)
  (setq-default fill-column 100)
  (setq TeX-view-program-list ;; pdf view setting
        '(("SumatraPDF" "\"C:/Program Files/SumatraPDF/SumatraPDF.exe\" -reuse-instance %o") ; windows
          ("Gsview" "gsview32.exe %o") ; windows
          ("Okular" "okular --unique %o")
          ("Evince" "evince --page-index=%(outpage) %o")
          ("Firefox" "firefox %o")
          ("PDF Tools" TeX-pdf-tools-sync-view)
          ("Skim"
           (concat
            "/Applications/Skim.app/Contents/SharedSupport/displayline"
            " %n %o %b")) ; mac
          )
        TeX-view-program-selection
        '(
          (output-pdf "PDF Tools")
          )
        TeX-source-correlate-start-server t  
        )
  )
```

## projectile 的一些小技巧
`M-m p`就是projectile的各种命令了，这里我经常用`p`切换工程，`f` 查看工程的文件，`t` 显式工程目录。

## gtags 使用的一些小技巧
`M-m p g`可以查找光标所在的symbol在工程中的所有位置。
但有时候敲这么多按键挺烦的，还有我偶然试出来的快捷键，即 `M-,` 以及 `M-.` 可以更方便地进行跳转。

## 当前文件快速跳转
适用于我想找到页面单词 `fuck` 所在的位置，
`M-m j j` 输入你想找到的单词如 `fuck` 的首字母 `f`，然后根据接下来的提示输入字母，就跳转到 `fuck`了。

## 按照函数名进行浏览
参照[Moving by Defuns](https://www.gnu.org/software/emacs/manual/html_node/emacs/Moving-by-Defuns.html)
`C-M-a`
`C-M-e`
## emacs 快捷键机制探索
部分参照自 [通用代码编辑器Spacemacs](https://edward852.github.io/posts/2018/03/%E9%80%9A%E7%94%A8%E4%BB%A3%E7%A0%81%E7%BC%96%E8%BE%91%E5%99%A8spacemacs/)
### `M-m`
我感觉，这个地方其实是所有命令的总入口，分门别类了。
所有emacs 的原命令基本都总结在这个 `M-m` 里了。
### `M-x`
有时候不知道命令是啥，但就是想用，就可以 `M-x` 输入关键词，就能找到啦，例如 tex的时候需要清理临时文件，就可以输入` tex clean` 就找到了`Tex-clean`命令，很体面。

### `C-c`
主要是和buffer内容的mode相关的命令
### `C-x`
主要是和内容无关的命令。
