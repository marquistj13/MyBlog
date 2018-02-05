---
title:  Latex fundamental 知识点
date:   2017-9-30
---


* content
{:toc}

## 空格
一行中的连续空格等同于一个空格
数学公式中的空格等同于没有空格

行首的空格会被忽略

一个空行标志一段的结束
多个空行等同于一个空行

Tex中的所有字符都要当做一个command，即使是一个最简单的字符如'a',也是a command to typeset an `a'.

control sequences有两类
1. `\`+一个或多个字母,这种的话遇到非字母就命令的名字就结束了
1. `\`+一个非字母的字符，如`\$`

一个control word会自动吸收后边的空格，破解方法：
`\TeX\ ` 或 `\TeX{}` 或 {\TeX}

Tex对于标点后边一般会自动加个额外的空格，如果不想要这个空格，咱们就在后边自己加`\ `,如 `Proc.\ Royal Acad.\ of Twits`
如果标点的前面有字母，tex就不加空格了，如果我们想要空格，就可以自己加： `A computer from IBM\null?`,这个`\null`就把字母M和问号分离了。 (这是因为句号前面如果是大写字母的话，tex认为这个句子还没有结束，不会加额外的空格 如果想主动结束可以这么搞 `DNA\null`)