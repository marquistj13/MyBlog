---
title:  The TeXbook
date:   2018-2-1
---


* content
{:toc}



## 第三章  control sequences
### 初识
escape character的作用：使得有限的键位足够versatile
又叫`control sequences`

### 空格
TeX 默认将`\<return>` `\<tab>` 看做 `\空格` 

打 `\TeX` 的时候，如果其后有空格，要在后边加上 `\` ，即打成`\TeX\` 因为 __escape的时候会忽略后边的空格__
如：`\TeX\ ignores spaces after control words.` 是正确的
而`\TeX ignores spaces after control words.` 就会变成： `TEXignores spaces after control words`

### primitive
Tex定义了差不多900个control sequences，其中300个是primitive，即`low-level atomic operations that are not decomposable into simpler functions`,其他控制序列是由着300个组成的。

### “函数”的功能
TeX中的`函数`的功能就是由higher-level control sequences实现的。如`\TeX`就是告诉我们“typeset the TEX logo”
higher-level control sequences的好处其实和function的好处是一样的，即如果我们不用function的话，要是有改动Tex logo的需求，每个Tex logo出现的地方都得手动去改，用了function，只需要改动function的定义就行了。

如何查看一个control sequence是否定义在一个higher level？
第一种方法：查表，本书后边有列表。
第二种方法：使用`\show\cs`命令，将`\cs`写成你要查的语句。如`\show\input`就会输出`> \input=\input.’`即它是primitive。
而`\show\thinspace`就输出
`> \thinspace=macro: ->\kern .16667em .`即`\thinspace`是`\kern .16667em`的缩写。

## 第四章 font type
Plain TEX的control sequences for changing fonts：  `rm`,`sl`,`it`,`tt`,`bf`

## 第五章 Grouping
### 引言
在第三章的时候我们提到，
>打 `\TeX` 的时候，如果其后有空格，要在后边加上 `\` ，即打成`\TeX\`

而如果后边没空格，就不能加 `\`了。
__但是__，在任何情况下 `{\TeX}`都是对的，这就是grouping的好处！

### 如何区分grouping的时候大括号的类型？
>\centerline{This information should be {\it centered}.}

1. `\centerline`:这个control sequence只会作用于紧跟着它的text，可以这样：`\centerline\TeX`,也可以这样`\centerline{\TeX\ has groups}`
1. `\it ` 这个control sequence的意思是 “change the current font”; it acts without looking ahead, so it affects everything that follows，这时候大括号的作用就是 confine the font change to a local region.

也就是说，这两个地方的大括号有不同的功能：
1. 前者将很多 words of the text 看做a single object
1. 后者provides local block structure

### 如何穿透当前的grouping？
有时候有make a definition that transcends its current group的需求
怎么实现？
答：用`\global`实现

举个例子
tex的游戏规则：当前page number存在一个register中， called `\count0`,一个output routine会增加page number。
而Output routines一般都保护在一个grouping中，因此对于 `\count0` 的更改就会在这个grouping中无效，咋办？
`\global\advance\count0 by 1`

## 第六章TeX运行，Debug
### tex的参数
在cmd输入tex，会立马出现两个`*`号，如果在这输入了一个`\`开头的control sequence，那就很普通了，如输入`\relax`即“do nothing.”
如果输入的不是`\`开头的control sequence（这时候你输入的必须得是一个已经存在的文件名），那么Tex就会自动给你插入一个`\input`,
之后才是一个`*`的正常模式，

这个机制的好处是，可以将一堆command放到一个文件中，然后作为输入送给tex。
### 运行方式
第一种：
`tex`,然后`\relax`，输入你的内容，然后`\end`,就会自动写入一个`texput.dvi`的文件中。
第二种：
先用自己的编辑器写入一个文件中，如story.tex
`tex`,然后输入，`story`就行了，退出用`\end`。

__第三种：__
以上两种都需要等待出现两个`*`号，
也可以直接， `tex \relax` 或 `tex story`
如果story中没有`\end`语句，我们就得在命令行手动输进去。或直接 `tex story \end`

### 一个例子
```tex
\hrule
\vskip 1in
\centerline{\bf A short Story}
\vskip 6pt
\centerline{\sl by A.Fuck}
\vskip .5cm
Once upon a time, in a distant 
galaxy called \"O\"o\c c,
there lived a computer
named R.~J. Drofnats.

Mr.~Drofnats---or ‘‘R. J.,’’ as
he preferred to be called---
was happiest when he was at work
typesetting beautiful documents.
\vskip 1in
\hrule
\vfill\eject
```
其中
`\hrule` 画了一条横贯文档的线
`\vfill`  用空白填充page剩下的页面
`\eject`  send it to the output file

### overfull box
运行 `tex \hsize=4in \input story \end`
即设为4inch宽，如果过窄的话，就会出现“Overfull \hbox”的提示。
例如`tex \hsize=2in \input story \end`

这是因为对于Plain Tex来说
>There simply is no good way to break the given paragraphs into
lines that are exactly two inches wide, without making the spaces between words
come out too large or too small.

什么意思呢，就是说啊，你要我（tex哈）将文档设为2英寸宽，同时又限制了我的字符间距，我是办不到的
（这个限制指的是，你指定了我的最小间距和最大间距）。
这时候就会出现一个嘿嘿的空格，很丑。

怎么解决呢？
首选我们分析一下这个问题的具体情况，在命令行有提示具体overfull了多少，当然这些信息都写到log文件中了，如`(0.98807pt too wide) `

好了，Tex给每一行都设了一个 __“badness”值__，这个值越大，允许的word之间的空隙越大。

怎么设呢？这么设`\tolerance=1600`

好了：`tex \hsize=2in \tolerance=1600 \input story \end`，这时候overfull的提示没了，但出现了一个underfull box的提示，好在没有黑黑的空格。这个提示的原因是：
>TEX reports all boxes whose badness exceeds a certain threshold called
\hbadness; plain TEX sets \hbadness=1000.)

### debug
第一种出错信息；
假如我们将story中的`vskip 1in`改为`vship 1in`
就会出现如下错误：
```tex
! Undefined control sequence.
l.2 \vship
1in
?
```
其中第一行`l.2 \vship`指出了错误的地方，下一行的`1in`是tex将要读的东西。

第二种出错信息要复杂一些。
假如我们将story中的`\centerline{\bf A short Story}`改为`\centerline{\bf A short \error Story}`，就会出现如下错误：
```tex
! Undefined control sequence.
<argument> \bf A short \error
                              Story
\centerline #1->\line {\hss #1
                              \hss }
l.3 \centerline{\bf A short \error Story}
```
这个就要复杂一点，因为现在处理的是higher-level commands。
1. 其中第一行`<argument> \bf A short \error`是错误的地方
1. 下一行的`Story`是tex将要读的东西。
1. 下面两行
```tex
\centerline #1->\line {\hss #1
                              \hss }
```
指的是`\centerline`要干的事情，这里的`#1`是`\centerline`的参数，很容易看出来上面这两行就是将`\centerline #1`替换成
`\line {\hss #1 \hss }`
1. 最后一行`l.3 \centerline{\bf A short \error Story}`是tex当前处理到的地方。

__总结__要看第一行和最后一行出错信息。

## 第七章 How TEX Reads What You Type
在plain tex中，`\ { } $ & # ^ _ % ~` 这10个字符是特殊字符，即保留字符。
要用的话必须转义才是原来的字符。

## 第八章The Characters You Type

## 第十章 Dimensions
### metric system
```
pt point (baselines in this manual are 12 pt apart)
pc pica (1 pc = 12 pt)
in inch (1 in = 72.27 pt)
bp big point (72 bp = 1 in)
cm centimeter (2.54 cm = 1 in)
mm millimeter (10mm = 1 cm)
dd didot point (1157 dd = 1238 pt)
cc cicero (1 cc = 12 dd)
sp scaled point (65536 sp = 1 pt)
```

### 两个相对单位
`em` is the width of a “quad” in the current font;
`ex` is the “x-height” of the current font

### 很稳定的单位
在Tex内部只有`sp`这个基本单位，因为可见光的波长大概是`100sp`
故对于`sp`的rounding errors基本上对人言是没有啥差别的，因此对于tex的不同实现，同样的文档肯定是produce the same line breaks and the same page breaks。

### 字体放大倍数
在文档开头`\magnification=1200`，就是将所有字体放大到1.2倍。
`\magnification=2000`是两倍。



## 第十一章Boxes
