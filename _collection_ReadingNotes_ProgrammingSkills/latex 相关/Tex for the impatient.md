---
title:  Tex for the impatient
date:   2018-2-4
---


* content
{:toc}

## 基本概念
### box
来源：`p51 `
box就是要排版的一个矩形
小到一个字符，大到一个page都是一个个box，。
整个page就是一个个互相嵌套的box

Tex在构建paragraphs and pages的时候会隐式地进行box-building。
当然我们也可以用命令来显示地创建。
如`\hbox`在box列表里边从左到右加box，`\vbox`和`\vtop`从上到下加。

每一个box都有几个指标:
![](teximpatient\box_illustration.png)

注意，字符`g`的一部分在baseline下面，字符`h`全在上面。
另外
>Roughly speaking, then, `\vbox` puts the reference point near the bottom
of the vbox and `\vtop` puts it near the top

将box放到一个box寄存器就行了，使用box寄存器之前当然要用`\newbox`来reserve并命名一个box。



### font相关
来源：`p64 p221`

一个font就是有同样typeface design的256个字符的集合
原则是`定义、加载、然后使用`
例如，`\font\twelvebf=cmbx12`,这里`\twelvebf`是我们用来name字体的，`cmbx12`就是我们电脑里边存着的font metric文件的名字。

注意我们要用grouping来限制这个`\twelvebf`的作用域。
例如：
{\twelvebf white rabbits like carrots}

另外，字体文件一般有俩，一个指定字体的metric（.tfm），另一个指定该字体的shape（.pk或.gf），Tex只关心metric，具体这个字咋写的人家并不关心，
谁用呢？
device driver负责将`.dvi`转化为设备能识别的东西，也就是device driver才会关心这个shape文件。

`\font`的具体用法：
```
\font
\font hcontrol sequencei = hfontnamei
\font hcontrol sequencei = hfontnamei scaled hnumberi
\font hcontrol sequencei = hfontnamei at hdimeni
```
`\font`单独用的时候并不是一个command，用来取出font的值，这样就可以作为参数传给其他命令了。

后面三种就是上面例子所指出的了。
需要指出的是，字体文件名一般自带默认的design size,如`cmr10`就是10 points大小的。
最后俩用来在design size的基础上进行放缩的:
`scaled <number>`  的时候 `<number>/1000`
`at <dimen>` 的时候 `<dimen>/ds, where ds is the design size of <fontname>`

书上 `p23` 有个例子：
```
% The next two lines define fonts for the title
\font\xmplbx = cmbx10 scaled \magstephalf
\font\xmplbxti = cmbxti10 scaled \magstephalf

% Now here's the title.
\leftline{\xmplbx Example 1:\quad\xmplbxti Entering simple text}
```

这个例子中出现了`\magstephalf`,这就牵涉到magnification了

###  magnification
tex排版的时候，所有的dimension都会乘以一个因子 `f/1000`,其中`f`是`\mag`参数的值。`\mag`的默认值是1000，tex定义了几个常用的放大倍数对应的值，如1.2倍的`\magstep1`，1.4倍的`\magstep2`。介于前俩之间的`\sqrt{1.2}`倍的`\magstephalf`，总共定义到`\magstep5`

除了这种相对放大，还有一种直接指定的，即加上`true`如 `\kern 8 true pt`,不管放大倍数多少，我都产生8 points的kern

### kern
来源：`p157`
horizontal mode的时候，一个正的kern会将tex右移，负值左移
vertical mode的时候，正值下移，负值上移

kern和glue很像，只是kern不能stretch和shrink，并且一般kern的地方不能break a line or a page,除非kern后边跟了个glue

注意两点
1. kern在行末或page末尾的时候是没效果的，这时候可以用`\hglue or \vglue`
1. 另外，kern在math mode的时候不能使用mu（mathematical unit），要想用的话，请使用`\mkern`

###  thinspace
来源：`p153`
`\thinspace` 产生一个 $1/6$ em 的kern，也就是将tex往右移动一点点。
主要用于nested quotation的时候，例如：
```
``\thinspace`A quote.'\thinspace''\par
24,\thinspace 29--31,\thinspace 45,\thinspace 102
```

### vglue  和  hglue
来源：`p156`
这个 `\vglue` 就是一种variable-size space了。
用法：`\vglue <glue>`
其中`\vglue`用于产生一个即使page break也不会消失的glue
`\hglue`产生一个即使line break也不会消失的glue
除此之外，这俩命令就和`\hskip and \vskip`一样了。

`\vglue` 可以用于在page顶端的一个空行（即title上面），但这么用的话，明显 `\topglue`更适合一点。

### hskip 和 vskip
来源：`p155`
```
\hskip <dimen1>  plus <dimen2> minus <dimen3> i
\vskip <dimen1> plus <dimen2>  minus <dimen3> i
```
分别用于产生horizontal and vertical glue。
` <dimen2>` 是stretch ` <dimen3>`是shrink


    
###  register
来源：`p89`
 register类似编程中的variable的概念。
 总共有五种register：
```
Register  type Contents
box       a box
count     a number
dimen     a dimension
muskip    muglue
skip      glue
toks      a token list
```

每一中寄存器都有256个值，从0到255进行寻址。
具体的寻址方式是‘寄存器名+index’，例如`\muskip192`,`\count12`

怎么对寄存器赋值呢？
书中给出了两种方式的例子，box单独列出来有可能是因为它有点复杂
```
\setbox3 = \hbox{lagomorphs are not mesomorphs}
\count255 = -1
```
定义好之后，这样就可以用 `\box3`了，同理，count register 255现在的值是-1.

上面说到box比较特殊，是因为，box读出来之后，该box就会被清空。
一个解决方案就是用`\copy`来提取box 寄存器的值，同时不清空该寄存器。

很多寄存器都是留个tex自己用的，咱们不能用。如`\count0`到`\count9`用于存储page numbering的相关信息。`\box255`用于存放当前页的的内容。

tex运行的时候，可以使用 `\showthe`查看寄存器的值，如`\showthe\dimen0`

### 使用register
```
\count <register> = <number>
\dimen <register>= <dimen>
\skip <register>= <glue>
\toks <register>= <token variable> 或 {<token list>}
```
当然，以上的`=`可以省掉。

对于`\count`这种寄存器r来说，只有`\count255`不需要我们去定义就能用。
对于`\dimen`来说，`\dimen0-\dimen9`,以及`\dimen255`也是可以直接用
对于`\skip`来说，`\skip0-\skip9`,以及`\skip255`也是可以直接用


对于`\toks`,可以赋给它一个token变量（一个寄存器或参数），或者token 变量的list，此时这个list并不会直接展开，而是需要使用 `\the`.
如：
```
\toks0 = {the \oystereaters\ were at the seashore}
% This assignment doesn't expand \oystereaters.
\def\oystereaters{Walrus and Carpenter}
\toks1 = \toks0
% the same tokens are now in \toks0 and \toks1
Alice inquired as to whether \the\toks1.
```
结果就是：`Alice inquired as to whether the Walrus and Carpenter were at theseashore.`

好了，上面的 `<register>`，如何定义呢？我们需要new一下啦。

### Naming and reserving registers,

```
\newcount
\newdimen
\newskip
\newmuskip
\newtoks
\newbox
\newread
\newwrite
\newfam
\newinsert
\newlanguage
```
这么多哈哈。

其中正常的几个new，如 `\newcount, \newdimen, \newskip, \newmuskip, \newtoks, and \newbox`定义出来（或者叫reserve）的都是正常的register，
而`\newbox, \newread, \newwrite,\newfam, \newinsert, and \newlanguage`定义出来的都是对应的register的index。
如`\newbox\figbox`这么搞之后，`\figbox`只能和box相关的command一块儿用，如 `\setbox\figbox = \vbox{: : : }`

### 宏 macro
