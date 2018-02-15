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
## expandafter
在[Tex for the impatient的笔记]({{ site.baseurl }}{% link _collection_ReadingNotes_ProgrammingSkills/latex_tex_related/Tex for the impatient.md %})中，我们已经了解了`\expandafter`的基本用法，下面根据另一篇文章`A Tutorial on \expandagter `（TUGboat 1988年的文章），来深入探讨一下其用法，主要是摘抄几个核心的例子。
###  简单的展开例子
```
\def\xx{\yy}
\expandafter\def\xx{This is fun}
```
那么执行到第二行的时候，Tex会将`\def`这个token先暂存起来不理它，然后展开`\xx`,得到`\yy`,因此这个例子等价于:`\def\yy{This is fun}`

###   例子
`\expandafter ab`
此时，先将字符`a`暂存，然后展开`b`,由于`b`没法展开，因此这俩字符还是按照原来的顺序打印出来。
这个例子告诉我们：`\expandafter`只能颠倒展开的顺序，不能颠倒执行的顺序。

###  多个`\expandafter`
如何将`\a\b\c`这仨宏的展开顺序颠倒一下呢？
为了叙述方便，我们以 $\ex_i$ 代表第i个`\expandafter`。
那么$\ex_1\ex_2\ex_3\a\ex_4\b\c$,就可以完成这个工作。
解析如下：
首先执行$\ex_1$，导致$\ex_2$被保存下来，然后Tex看到了$\ex_3$，发现这哥们还是一个`\expandafter`，那就继续往前看，就会将`\a`,保存下来（注意，目前为止，保存下来的有$\ex_2$，`\a`，而且执行过的$\ex_i$就没了。）
开始执行$\ex_4$，此时将`\b`保存下来，展开`\c`
ok,目前已经保存的tokens为，$\ex_2$，`\a`，`\b`，将这个列表放到展开后的`\c`前面。
现在执行$\ex_2$，我们还得保存`\a`,展开`\b`
好了，最后保存列表里只有`\a`了，将其展开即可。

### 一个实际例子
tonjithesis.cls有这么一段用来设置cover的：
```
\def\tongji@define@term#1{
  \expandafter\gdef\csname #1\endcsname##1{
    \expandafter\gdef\csname tongji@#1\endcsname{##1}}
  \csname #1\endcsname{}}
\tongji@define@term{secretlevel}
\tongji@define@term{secretyear}
\tongji@define@term{ctitle}
\tongji@define@term{cdegree}
```
看懂了上面的例子之后，很容易得出来这个`\tongji@define@term`的庐山真面目,就拿`\tongji@define@term{secretlevel}`来说：
`\gdef\secretlevel#1{\gdef\tongji@secretlevel{#1}}`

（注，用一个宏定义另一个宏的`##1`技巧，我们在[Tex for the impatient的笔记]({{ site.baseurl }}{% link _collection_ReadingNotes_ProgrammingSkills/latex_tex_related/Tex for the impatient.md %})已经介绍过了，回忆一下就是：`\def\first#1{\def\second##1{#1/##1}}`
这样，当我们调用`\first{One}`的时候,就会将`\second`定义成：`\def\second#1{One/#1}`）

好了，`\gdef\secretlevel#1{\gdef\tongji@secretlevel{#1}}`这么定义之后，我们就可以用`\secretlevel{绝密}`来定义一个`\tongji@secretlevel`宏了，接着可以用`\tongji@secretlevel`来表示密级，进而将其用于cover的排版。
而用户只需要调用`\secretlevel{绝密}`这么一个简单的命令就行了。

### 一种奇怪的用法
当我们需要奇怪的宏名的时候，可以配合`\csname`来实现这一个需求。
例如：
`\expandafter\def\csname a?a-4\endcsname{...}`
这样`\a?a-4`就是一个宏名了。
可想而知，如果没有`\expandafter`，上面也就是重新定义了`\csname`.



