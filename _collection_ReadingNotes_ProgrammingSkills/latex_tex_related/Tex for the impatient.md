---
title:  Tex for the impatient
date:   2018-2-4
---


* content
{:toc}




## 基本概念
### tex的解剖学结构 anatomy of TEX
eye：从输入文件将字符读到mouth中
mouth：将字符character变成token
gullet食道：将`macros, conditionals, and similar construct`进行展开，注意，展开一个token之后可能导致其他token也需要展开，一般情况下是从左到右展开，除非遇到了改变展开顺序的command 如`\expandafter`,然后将其送到stomach胃里边。
stomach：将token按照group进行处理，其实就是将字符等组装成page，然后送到肠道。如line breaking（将段落break成行），page breaking（将行和其他vertical mode material转化成page）
intestines（肠道）：将page转化为其他形式，将输出发送到`.dvi`文件。
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
来源：`p230 p75`
`\def <control sequence> <parameter text> { <replacement text> }`

macro其实就是一个定义，给这些token一个name

最多可以使用9个参数。

参数有两种类型：
1. delimited parameters 
2.  undelimited parameters
即没有分割的参数，和有分割的参数。

## 稍微上层一点的
### noident
来源：`p112`
当tex结束一个段落的时候会进入vertical mode，此时noident命令就会执行以下命令：
1. 首先插入`\parskip`这个段间glue，
1. 将tex设为horizontal mode
1. 开始一个unindented paragraph

当然，noident还有另一个功能：
取消段落首行的indent
如下面例子
```
\parindent = 1em
Tied round the neck of the bottle was a label with the
words \smallskip \centerline{EAT ME}\smallskip
\noindent beautifully printed on it in large letters
```
### par
`\par` 用来结束一个段落
将tex设为vertical mode

注意：由于tex会将空行识别成`\par`这个token，因此这个命令不常用。

由于`\par`也会产生interparagraph space，因此可以使用`\vskip -\lastskip`来把它取消掉。

另外，`\par`不同于`\noident`,`\par`并不会让tex重新开始一个新的段落。

### 其他终止段落用的命令
`\smallskip`:用来skip 3个point,and can stretch or shrink by 1 point
`\vskip`

`\medskip` 等价于俩`\smallskip`
`\bigskip` 等价于俩`\medskips`

### llap
`\llap <argument>`:将当前位置往左移动`<argument>`的宽度，输出`<argument>`
一般用于将文本放到outside of the current margins

### hbox 
```
\hbox { <horizontal mode material> }
\hbox to <dimen> { <horizontal mode material> }
\hbox spread <dimen> { <horizontal mode material> }
```
总共有以上三种用法。
第一种，hbox具有{ <horizontal mode material> }的自然长度。
第二种，hbox的长度为<dimen>
第三种，hbox的长度为<dimen>+{ <horizontal mode material> }的自然长度

对于后两种情况，一般需要手动加入`\hfil`
如：
```
\hbox{ugly suburban sprawl}
\hbox to 2in{ugly \hfil suburban \hfil sprawl}
\hbox spread 1in {ugly \hfil suburban \hfil sprawl}
% Without \hfil in the two preceding lines,
% you'd get `underfull hbox'es.
```

另外:
`\line <argument>`会产生一个等于当前行长度的hbox，并将argument放进去。
   
### leaders
 `\leaders <box or rule> <skip command>`:重复<box or rule>，直到填满整个水平空间，这个水平空间由<skip command>指定。
如以下示例：
```
\def\dotting{\leaders\hbox to 1em{\hfil.\hfil}\hfil}
\line{The Political Process\dotting 18}
\line{Bail Bonds\dotting 26}
```
会产生类似目录的效果，即项目...页码。
其中`\hbox to 1em{\hfil.\hfil}`是要重复的东西，称为leader，而`<skip command>`就是后边的\hfil

### 改变字体
```
\font\tenrm = pplr % Palatino
% Define a macro for invoking Palatino.
\def\pal{\let\rm = \tenrm \baselineskip=12.5pt \rm}
\pal % Use Palatino from now on.
```
其中`\let <control sequence> = <token>`就是让`<control sequence>`获取`<token>`的当前meaning。
而此处`\rm`就是一种和`\bf`,`\it`等并列的一种font style。

