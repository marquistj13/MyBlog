---
layout: post
title:  Texlive 添加新的cls文件和bst
categories: 编辑器等文档工具
tag: [latex]
---




* content
{:toc}

## cls
下载好cls文件以后，我们要将其加入latex的搜索路径，放哪儿呢？
找了一圈儿，发现很简单啊

对于我的win10,texlive2016来说，先用 `kpsewhich -var-value=TEXMFHOME`看一下home是啥，我的是 `C:/Users/Marquis/texmf`，好了就放在这个文件夹就行了么

什么？ `C:/Users/Marquis` 没有 `texmf` 目录？自己建啊亲，对了还得再建一个 `tex` 目录，假设你的cls名字为xx.cls,那么最好再建一个xx的文件夹，这样
最终就是:`C:/Users/Marquis/texmf/tex/xx/xx.cls`

这时候用命令 `kpsewhich xx.cls` 如果它能找到这个xx.cls的路径，那就成功啦。
对了，不用重启电脑。
## bst
同理，我们在根目录`C:/Users/Marquis`新建`C:\Users\Marquis\texmf\bibtex\bst`就可以将bst直接放到这里了，
注意
+ 我探索的时候使用了 `kpsewhich your-bibtex-file.bst`，这个很有用的命令，如果你的bst的位置放好了，它就会找到这个位置，如我要放spbasic.bst,就可以`kpsewhich spbasic.bst`，这样就可以反复测试这个目录是否需要建了
+ 我建立`\bibtex\bst`的原因是效仿texlive系统自身的目录，如我先找到一个常用的bst，使用`kpsewhich IEEEtran.bst`得到了`c:/tools/texlive/2016/texmf-dist/bibtex/bst/ieeetran/IEEEtran.bst`