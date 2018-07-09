---
layout: post
title:  tikz 官方文档的阅读笔记
categories: [编辑器等文档工具]
tag: [tikz,latex]
---

* content
{:toc}

## 本笔记序言
### Motivation
早听说 tikz 很强大，17 年的时候根据 [TeXample.net](http://www.texample.net/tikz/) 的例子画了一个论文插图，惊为天人，这玩意儿实在灵活！

因此，期望有一天能仔细了解一下。

以下就是我看tikz的[官方文档](https://ctan.org/pkg/pgf) 时的笔记，这个笔记主要是看的时候随意记录一下，方便自己的理解，也方便以后快速浏览。
换言之，这个笔记只对我有用，哈哈。

总共花了三天时间吧，从7.7 到 7.9中午，把主要部分看了一下，感觉还是很值得的。
tikz的灵活，令人叹为观止！

但只看不练是学不会它的，因此以后用的时候才能真正学会。

### 如何快速理解文档，快速上手？
1. 官方文档给出了很多例子，因此看的很快，这里也都摘了下来。
1. 可以安装 [TikzEdt](http://www.tikzedt.org/),这个玩意儿各平台都有。
这样就可以实时查看效果了，但是这个工具无法处理中文，我试了一上午的中文处理都不行，主要问题出在它必须依赖 precompile，问题就出在这，算了就不预览中文的图片就行了，
中文的可以用普通的tex自己编译，别实时看啦。
1. 要想将tikz代码插入普通的文档，可以这样：
```
\begin{figure}
\begin{tikzpicture}
    code
\end{tikzpicture}
\caption{Do not forget!}
\end{figure}
```



## 具有层次结构：环境 scope 和 style
### 环境
所有graphic都必须在 `tikzpicture` 环境中，这个 `tikzpicture` 是 最外层的 scope 环境，在每一个scope中我们使用 path命令来画图。

###  graphic option 之 style
这么设置：`\tikzset{<options>}` 

默认有 `help lines` style，即浅灰色的线，可以这么使用：
`\tikz \draw[help lines] (0,0) grid (3,3);`

怎么定义自己的 style呢？
`my style/.style={draw=red,fill=red!20}`

只用于一个图像时：
```
\begin{tikzpicture}[help lines/.style={blue!50,very thin}]
\draw (0,0) grid +(2,2);
\draw[help lines] (2,0) grid +(2,2);
\end{tikzpicture}
```

这样可以用于多个图像：
```
\tikzset{help lines/.style={blue!50,very thin}}
% ...
\begin{tikzpicture}
\draw (0,0) grid +(2,2);
\draw[help lines] (2,0) grid +(2,2);
\end{tikzpicture}
```

以上相当于重定义了 `help lines`，还可以用另一种方式进行重定义，即追加的形式 用 `/.append style` 代替 `/.style`：
```
\begin{tikzpicture}[help lines/.append style=blue!50]
\draw (0,0) grid +(2,2);
\draw[help lines] (2,0) grid +(2,2);
\end{tikzpicture}
```
注意，这也是一种覆盖定义。

style还可以传参：
```
\begin{tikzpicture}[outline/.style={draw=#1,thick,fill=#1!50},
outline/.default=black]
\node [outline] at (0,1) {default};
\node [outline=blue] at (0,0) {blue};
\end{tikzpicture}
```

## 坐标
### 显示或隐式的坐标
显式指定坐标不常用,语法就是： `坐标系统名字 cs:后边跟一堆坐标`
隐式的更常用，就是不带 cs 的

隐式指定坐标的时候，可以方便地指定某一个坐标的偏移，或所有坐标的偏移：
```
\begin{tikzpicture}
\draw[help lines] (0,0) grid (3,2);
\draw (0,0) -- (1,1);
\draw[red] (0,0) -- ([xshift=3pt] 1,1);
\draw (1,0) -- +(30:2cm);
\draw[red] (1,0) -- +([shift=(135:5pt)] 30:2cm);
\end{tikzpicture}
```

### 三种坐标系统
__以下，分别列出显示和隐式的指定__
其中，一共有 Canvas, XYZ, and Polar 这仨坐标系统。
首先是 canvas坐标：
```
\begin{tikzpicture}
\draw[help lines] (0,0) grid (3,2);
\fill (canvas cs:x=1cm,y=1.5cm) circle (2pt);
\fill (canvas cs:x=2cm,y=-5mm+2pt) circle (2pt);
\end{tikzpicture}



\begin{tikzpicture}
\draw[help lines] (0,0) grid (3,2);
\fill (1cm,1.5cm) circle (2pt);
\fill (2cm,-5mm+2pt) circle (2pt);
\end{tikzpicture}
```

然后说xyz坐标：
```
\begin{tikzpicture}[->]
\draw (0,0) -- (xyz cs:x=1);
\draw (0,0) -- (xyz cs:y=1);
\draw (0,0) -- (xyz cs:z=1);
\end{tikzpicture}


\begin{tikzpicture}[->]
\draw (0,0) -- (1,0);
\draw (0,0) -- (0,1,0);
\draw (0,0) -- (0,0,1);
\end{tikzpicture}
```

最后是canvas极坐标：
```
\tikz \draw (0,0) -- (canvas polar cs:angle=30,radius=1cm);

\tikz \draw (0cm,0cm) -- (30:1cm) -- (60:1cm) -- (90:1cm)
-- (120:1cm) -- (150:1cm) -- (180:1cm);
```

当然也可采用xyz polar：
```
\begin{tikzpicture}[x=1.5cm,y=1cm]
\draw[help lines] (0cm,0cm) grid (3cm,2cm);
\draw (0,0) -- (xyz polar cs:angle=0,radius=1);
\draw (0,0) -- (xyz polar cs:angle=30,radius=1);
\draw (0,0) -- (xyz polar cs:angle=60,radius=1);
\draw (0,0) -- (xyz polar cs:angle=90,radius=1);
\draw (xyz polar cs:angle=0,radius=2)
-- (xyz polar cs:angle=30,radius=2)
-- (xyz polar cs:angle=60,radius=2)
-- (xyz polar cs:angle=90,radius=2);
\end{tikzpicture}




\tikz[x={(0cm,1cm)},y={(-1cm,0cm)}]
\draw (0,0) -- (30:1) -- (60:1) -- (90:1)
-- (120:1) -- (150:1) -- (180:1);
```

### 坐标的交点
如果我想求通过一个点 x 的竖直线 和 一个提供 点 y 的水平线的交点，咋求？ （这里的竖直和水平是相对于坐标系的）
可以 `(x |- y)`，反过来，通过x的水平线和通过y的竖直线的交点：`(x -| y)`
例子：
```
\begin{tikzpicture}
\path (30:1cm) node(p1) {$p_1$} (75:1cm) node(p2) {$p_2$};
\draw (-0.2,0) -- (1.2,0) node(xline)[right] {$q_1$};
\draw (2,-0.2) -- (2,1.2) node(yline)[above] {$q_2$};
\draw[->] (p1) -- (p1 |- xline);
\draw[->] (p2) -- (p2 |- xline);
\draw[->] (p1) -- (p1 -| yline);
\draw[->] (p2) -- (p2 -| yline);
\end{tikzpicture}
```

### 任意曲线的交点
使用 `name intersections={选项}`，交点名字默认为intersection-1, intersection-2，如下例子：
```
\begin{tikzpicture}[every node/.style={opacity=1, black, above left}]
\draw [help lines] grid (3,2);
\draw [name path=ellipse] (2,0.5) ellipse (0.75cm and 1cm);
\draw [name path=rectangle, rotate=10] (0.5,0.5) rectangle +(2,1);
\fill [red, opacity=0.5, name intersections={of=ellipse and rectangle}]
(intersection-1) circle (2pt) node {1}
(intersection-2) circle (2pt) node {2};
\end{tikzpicture}
```
其他细节不再详细看了。

### 相对坐标 和 增量坐标
### 相对坐标的指定
`++` 符号表示，相对坐标，并将计算后的坐标作为新的当前坐标，如
```
\begin{tikzpicture}
\draw (0,0) -- ++(1,0) -- ++(0,1) -- ++(-1,0) -- cycle;
\draw (2,0) -- ++(1,0) -- ++(0,1) -- ++(-1,0) -- cycle;
\draw (1.5,1.5) -- ++(1,0) -- ++(0,1) -- ++(-1,0) -- cycle;
\end{tikzpicture}
```

`+` 仅指定相对坐标，不更新当前坐标，如：
```
\begin{tikzpicture}
\draw (0,0) -- +(1,0) -- +(1,1) -- +(0,1) -- cycle;
\draw (2,0) -- +(1,0) -- +(1,1) -- +(0,1) -- cycle;
\draw (1.5,1.5) -- +(1,0) -- +(1,1) -- +(0,1) -- cycle;
\end{tikzpicture}
```
### 相对坐标的例外情况
相对坐标的例外情况，在相对坐标作为贝赛尔曲线的控制点时，每一个控制点的“相对”情况不一样：
第一个控制点 相对于 曲线起点
第二个控制点 相对于 曲线终点
曲线终点     相对于 曲线起点
如：
```
\begin{tikzpicture}
\draw (1,0) .. controls +(30:1cm) and +(60:1cm) .. (3,-1);
\draw[gray,->] (1,0) -- +(30:1cm);
\draw[gray,<-] (3,-1) -- +(60:1cm);
\end{tikzpicture}
```

### 相对旋转坐标的指定
语法是：`<relative angle>:<distance>`
例如：
```
\tikz \draw (0,0) -- (1,1) -- ([turn]-45:1cm) -- ([turn]-30:1cm);
```
在 点  (1,1)的时候，下一个点就是相对于(1,1)，顺时针旋转45度，半径为1cm的点  。

### 坐标计算
首先必须加载 `\usetikzlibrary{calc}`
```
\begin{tikzpicture}
\draw [help lines] (0,0) grid (3,2);
\node (a) at (1,1) {A};
\fill [red] ($(a) + 1/3*(1cm,0)$) circle (2pt);
\end{tikzpicture}
```
`$(a) + 1/3*(1cm,0)$` 就是 a 点向右平移 1/3 cm。


### 首先是 factor，即百分比，Partway Modifiers
基本语法：`起始坐标!百分比!旋转角度:终点坐标`
当省略旋转角度时，就是`起始坐标!百分比!终点坐标`
如 `(1,2)!.75!(3,4)` 就是在 (1,2) 与 (3,4) 的连线的 0.75 处的一个点。
示例：
```
\begin{tikzpicture}
\draw [help lines] (0,0) grid (3,2);
\draw (1,0) -- (3,2);
\foreach \i in {0,0.2,0.5,0.9,1}
\node at ($(1,0)!\i!(3,2)$) {\i};
\end{tikzpicture}
```

带上角度后，相当于将终点坐标更新为旋转后的坐标，然后再取百分比：
如：
```
\begin{tikzpicture}
\draw [help lines] (0,0) grid (3,3);
\coordinate (a) at (1,0);
\coordinate (b) at (3,2);
\draw[->] (a) -- (b);
\coordinate (c) at ($ (a)!1! 10:(b) $);
\draw[->,red] (a) -- (c);
\fill ($ (a)!.5! 10:(b) $) circle (2pt);
\end{tikzpicture}
```
### 将上面的百分比，写成距离，就是 Distance Modifiers
如 
```
\begin{tikzpicture}
\draw [help lines] (0,0) grid (3,2);
\draw (1,0) -- (3,2);
\foreach \i in {0cm,1cm,15mm}
\node at ($(1,0)!\i!(3,2)$) {\i};
\end{tikzpicture}
```

### 投影modifier，就是将百分比，换成一个投影坐标
那么，这就是将投影坐标 正交投影到 起始点和终点连线的点上
```
\begin{tikzpicture}
\draw [help lines] (0,0) grid (3,2);
\coordinate (a) at (0,1);
\coordinate (b) at (3,2);
\coordinate (c) at (2.5,0);
\draw (a) -- (b) -- (c) -- cycle;
\draw[red] (a) -- ($(b)!(a)!(c)$);
\draw[orange] (b) -- ($(a)!(b)!(c)$);
\draw[blue] (c) -- ($(a)!(c)!(b)$);
\end{tikzpicture}
```

## path 选项的语法
### path 基本概念
正常用法是:
 `\path` 后边跟一段 path operations，例如一个 line to operation : `--(0,0)`，而当遇到operation的时候，我们可以通过方括号给一些 __graphic option__，如 `[rounded corners]`，注意，和传统的tex命令类似，有些option指定之后，会在接下来一直有效，直到对应的option将其终止，如： 
```
\tikz \draw (0,0) -- (1,1) 
[rounded corners] -- (2,0) -- (3,1) 
[sharp corners] -- (3,0) -- (2,1);
```
这个例子中，`[sharp corners]` 将 `[rounded corners]` 终结。


`\draw` 其实是 `\path[draw]` 的缩写形式，亦即，draw其实也是一种path 的图形选项。

当我们指定 `\path` 的时候，默认是不显示的，只有让它draw了，它才显示。
如 `\path (0,0) circle (1cm);` 仅仅指明在 `(0,0)` 处有一个直径 1cm的圆，就这样了，只有遇到 draw 命令的时候它才会画出来。

同理，
`\fill`  与`\path[fill]`，`\filldraw` 与 `\path[fill,draw]` 亦构成缩写关系。


### path 中，影响scope的 style
首先是every path：
```
\begin{tikzpicture}
[fill=yellow!80!black, % only sets the color
every path/.style={draw}] % all paths are drawn
\fill (0,0) rectangle +(1,1);
\shade (2,0) rectangle +(1,1);
\end{tikzpicture}
```

其次是 `insert path=<path>`
```
\tikz [c/.style={insert path={circle[radius=2pt]}}]
\draw (0,0) -- (1,1) [c] -- (3,2) [c];
```

__注意：以下的...代表空格__

###  move-to 操作


`\path . . . <coordinate> . . . ;` 里边就是 move-to 操作，也就是从某个点（坐标）开始一个path，也就是指定下一个线段的起始点。这样就可以制造不连续的线段了：
```
\begin{tikzpicture}
\draw (0,0) --(2,0) (0,1) --(2,1);
\end{tikzpicture}
```
就是俩线段，(0,1) 是最后一个线段的起始点，而这个起始点一直存放在一个名为 `current subpath start` 的变量中，如，可以这么玩：
```
\tikz [line width=2mm]
\draw (0,0) -- (1,0) -- (1,1)
-- (0,1) -- (current subpath start);
```
`current subpath start` 的值就是 (0,0)。 但这么玩，并不会产生smooth join，必须采用下面提到的cycle作为end才会smooth。

### line-to 操作
我们已经知道 `--(0,0)` 是 line-to 操作，
`\path . . . --hcoordinate or cyclei . . . ;` 就是line-to 操作。
连续的 line-to 操作会产生 smooth join，而 如果不连续，那么这个join就是不smooth的
所有以坐标结尾的path 操作都可以使用 `cycle` 作为end。
这样的效果就是，最后一个 moveto 的坐标 就作为 path 操作的期望坐标，然后添加一个 smooth join。
例子：
```
\begin{tikzpicture}[line width=10pt]
\draw (0,0) -- (1,1) -- (1,0) -- (0,0) (2,0) -- (3,1) -- (3,0) -- (2,0);
\draw (5,0) -- (6,1) -- (6,0) -- cycle (7,0) -- (8,1) -- (8,0) -- cycle;
\useasboundingbox (0,1.5); % make bounding box higher
\end{tikzpicture}
```

### 先横后竖 或 先竖后横的线
```
\path . . . -| <coordinate or cycle> . . . ;
\path . . . |- <coordinate or cycle> . . . ;
```

如：
```
\begin{tikzpicture}[ultra thick]
\draw (0,0) -- (1,1) -| cycle;
\end{tikzpicture}
```


### The Curve-To Operation
`\path . . . ..controls <c> and <d>..<y or cycle> . . . ;`
注意，此处 c, d, 都是可以省略的，这条命令画了一条三次贝赛尔曲线（cubic Bézier curve），从起始点 x 开始，x处的切线经过点 c，终点 y 处的切线经过 d，若不指定d，则应该默认d和c相等。

例子：
```
\begin{tikzpicture}
\draw[line width=10pt] (0,0) .. controls (1,1) .. (4,0)
.. controls (5,0) and (5,1) .. (4,1);
\draw[color=gray] (0,0) -- (1,1) -- (4,0) -- (5,0) -- (5,1) -- (4,1);
\end{tikzpicture}
```

以及：
```
\begin{tikzpicture}
\draw[line width=10pt] (0,0) -- (2,0) .. controls (1,1) .. cycle;
\end{tikzpicture}
```

### 矩形
`\path . . . rectanglehcorner or cyclei . . . ;`

### 图像选项 Rounding Corners
`rounded corners=<inset>`
这个 inset 默认是 4pt
它的效果可以用sharp corners关掉。

当然，中途是可以关掉的
```
\begin{tikzpicture}
\draw (0,0) [rounded corners=10pt] -- (1,1) -- (2,1)
[sharp corners] -- (2,0)
[rounded corners=5pt] -- cycle;
\end{tikzpicture}
```

### Circle  操作
`.. circle [选项]`
有以下选项：
x radius 水平半径
y radius 竖直半径
radius 同时设置 水平和竖直半径
at 使用at设置的坐标就会成为circle的圆心，而不是使用当前点（即move to的点）。
every circle 用来设置所有circle的style


例子：
```
\begin{tikzpicture}
\draw (1,0) circle [radius=1.5];
\fill (1,0) circle [x radius=1cm, y radius=5mm, rotate=30];
\end{tikzpicture}
```

还可以在外边的scope设置半径：
```
\begin{tikzpicture}[radius=2pt]
\draw (0,0) circle -- (1,1) circle -- ++(0,1) circle;
\end{tikzpicture}
```

还可以设置别名：
`\tikzset{r/.style={radius=#1},rx/.style={x radius=#1},ry/.style={y radius=#1}}`


### grid 操作
语法：`grid [选项] <corner or cycle>`
如：
```
\tikz[rotate=30] \draw[step=1mm] (0,0) grid (2,2);
```

总共有以下选项：
step, xstep, ystep，其数值可以是dimension or number
也可以用 help lines 选项。

### to  操作： 从一个点，到另一个点，实现用户自定义path

例如，`(a) to (b)` 等同于，`(a) -- (b),`
但to 操作还允许我们这样：`(a) to [out=135,in=45] (b)`，这个曲线在a点以135度出发，以45度进入b点。

可以在to之后添加node：
```
\begin{tikzpicture}
\draw (0,0) to node [sloped,above] {x} (3,2);
\draw (0,0) to[out=90,in=180] node [sloped,above] {x} (3,2);
\end{tikzpicture}
```

除了直接用普通的node之外，还可以用图形选项的形式指定node,
```
\begin{tikzpicture}
\draw (0,0) to [edge node={node [sloped,above] {x}}] (3,2);
\draw (0,0) to [out=90,in=180,
edge node={node [sloped,above] {x}}] (3,2);
\end{tikzpicture}
```

上面的选项形式还有一个快捷键，相当于，`{node[auto]{<text>}}`
`\tikz \draw (0,0) to [edge label=x] (3,2);`            


而 `edge label’` 相当于 `{node[auto,swap]{<text>}}.`

还可以使用every to选项：
```
\tikz[every to/.style={bend left}]
\draw (0,0) to (3,2);
```

普通的every to中draw并不会影响 to 的效果，可以使用 `append after command` 选项来操作：
```
\tikz[every to/.style={append after command={[draw,dashed]}}]
\draw (0,0) to (3,2);
```

还有一个选项
`to path=<path>`    
这个path 就会插到to的后边，在这个path中，还可以使用三个宏：
`\tikztostart,\tikztotarget,\tikztonodes`  
而 `\tikztonodes`  就会展开成 to 后边的node（如果有的话）
如：
```
\begin{tikzpicture}[to path={
.. controls +(1,0) and +(1,0) .. (\tikztotarget) \tikztonodes}]
\node (a) at (0,0) {a};
\node (b) at (2,1) {b};
\node (c) at (1,2) {c};
\draw (a) to node {x} (b)
(a) to (c);
\end{tikzpicture}
```

## path 上的action
### 总览
构建path之后，我们可以把它画出来，draw，可以fill 或shade，可以clip。

对于draw
`\path (0,0) circle (1cm);` 仅仅构建了一个path，只有遇到 draw的时候才会画出来，例如：
```
\path [draw] (0,0) circle (1cm);
\path (0,0) [draw] circle (1cm);
\path (0,0) circle (1cm) [draw];
```
当然也可以直接，`\draw (0,0) circle (1cm);` 因为 `\draw ` 就是 `\path[draw]` 的简称。

### 指定颜色
`color=颜色名字` 或直接 `颜色名字`
`\tikz \fill[color=red!20] (0,0) circle (1ex);`  或 `\tikz \fill[red!20] (0,0) circle (1ex);`

### draw 一个path
#### 颜色
可以使用 `draw = 颜色` 来指定画path的时候的颜色。
如：
```
\begin{tikzpicture}
\path[draw=red] (0,0) -- (1,1) -- (2,1) circle (10pt);
\end{tikzpicture}
```

#### 线宽
`line width=尺寸`，可以直接指定
当然，还有 ultra thin，very thin，thin，semithick，thick等一大堆选项，

#### line join
其他选项有：`line join`，可以设为：round, bevel, and miter,即圆的，平的，尖的

#### dash pattern
dash pattern选项指定pattern，如on
2pt off 3pt on 4pt off 4pt means “draw 2pt, then leave out 3pt, then draw 4pt once more, then
leave out 4pt again, repeat”.
```
\begin{tikzpicture}[dash pattern=on 2pt off 3pt on 4pt off 4pt]
\draw (0pt,0pt) -- (3.5cm,0pt);
\end{tikzpicture}
```

为了方便设置，还有一些选项设置好了，直接用就是了
如：solid，dotted，dash dot等一大堆。
`\tikz \draw[dash dot] (0pt,0pt) -- (50pt,0pt);`

#### 透明度 Opacity
draw opacity 选项
如：
```
\begin{tikzpicture}[line width=1ex]
\draw (0,0) -- (3,1);
\filldraw [fill=yellow!80!black,draw opacity=0.5] (1,0) rectangle (2,1);
\end{tikzpicture}
```

#### Double Lines and Bordered Lines
语法：`double=颜色`
如：
```
\tikz \draw[double]
plot[smooth cycle] coordinates{(0,0) (1,1) (1,0) (0,1)};
```
可以利用它实现border效果
```
\begin{tikzpicture}
\draw (0,0) -- (1,1);
\draw[draw=white,double=red,very thick] (0,1) -- (1,0);
\end{tikzpicture}
```

还有一个：`double distance=长度` 就是线宽啦
```
\begin{tikzpicture}
\draw[very thick,double] (0,0) arc (180:90:1cm);
\draw[very thick,double distance=2pt] (1,0) arc (180:90:1cm);
\draw[thin,double distance=2pt] (2,0) arc (180:90:1cm);
\end{tikzpicture}
```

### fill
`fill=颜色` 如`\fill (8,0) -- (9,1) -- (10,0) circle (.5cm);`

注意，使用 `\filldraw` 的时候，是，先fill，再draw。
如：
```
\begin{tikzpicture}[fill=yellow!80!black,line width=5pt]
\filldraw (0,0) -- (1,1) -- (2,1);
\filldraw (4,0) circle (.5cm) (4.5,0) circle (.5cm);
\filldraw[even odd rule] (6,0) circle (.5cm) (6.5,0) circle (.5cm);
\filldraw (8,0) -- (9,1) -- (10,0) circle (.5cm);
\end{tikzpicture}
```

#### fill 一个pattern
实际上是一种clip操作，即将pattern向各个方向重复，然后clip

语法：`pattern=名字`，这个名字其实就是 tiling pattern的名字。
如：
```
\begin{tikzpicture}
\draw[pattern=dots] (0,0) circle (1cm);
\draw[pattern=fivepointed stars] (0,0) rectangle (3,1);
\end{tikzpicture}
```

还可以同时指定 pattern color：
如
```
\begin{tikzpicture}
\def\mypath{(0,0) -- +(0,1) arc (180:0:1.5cm) -- +(0,-1)}
\fill [red] \mypath;
\pattern[pattern color=white,pattern=bricks] \mypath;
\end{tikzpicture}
```

#### 使用任意图片填充path
`path picture=<code>`
这个code可以是任何tikz的code，如 `\draw`,`\node`

可以是使用path picture bounding box来获取当前path的bounding box。如：
```
\begin{tikzpicture}
\draw [help lines] (0,0) grid (3,2);
\filldraw [fill=blue!10,draw=blue,thick] (1.5,1) circle (1)
[path picture={
\node at (path picture bounding box.center) {
This is a long text.
};}
];
\end{tikzpicture}
```
下面实现一个画叉的操作：
```
\begin{tikzpicture}[cross/.style={path picture={
\draw[black]
(path picture bounding box.south east) --
(path picture bounding box.north west)
(path picture bounding box.south west) --
(path picture bounding box.north east);
}}]
\draw [help lines] (0,0) grid (3,2);
\filldraw [cross,fill=blue!10,draw=blue,thick] (1,1) circle (1);
\path [cross,top color=red,draw=red,thick] (2,0) -- (3,2) -- (3,0);
\end{tikzpicture}
```

下面用一个图片填充：
```
\begin{tikzpicture}[path image/.style={
path picture={
\node at (path picture bounding box.center) {
\includegraphics[height=3cm]{#1}
};}}]
\draw [help lines] (0,0) grid (3,2);
\draw [path image=brave-gnu-world-logo,draw=blue,thick]
(0,1) circle (1);
\draw [path image=brave-gnu-world-logo,draw=red,very thick,->]
(1,0) parabola[parabola height=2cm] (3,0);
\end{tikzpicture}
```

### shade
可以直接 `\shade`:
`\tikz \shade (0,0) circle (1ex);`

也可以直接设定shade的方式：`shading=name`，有三种，axis, radial, and ball，即，平行于坐标轴的，径向的，球向的
```
\tikz \shadedraw [shading=axis] (0,0) rectangle (1,1);
\tikz \shadedraw [shading=radial] (0,0) rectangle (1,1);
\tikz \shadedraw [shading=ball] (0,0) circle (.5cm);
```

还能对shade的颜色进行指定：
```
\tikz \shadedraw [left color=red,right color=blue]
(0,0) rectangle (1,1);
```

还可以调整shade的角度：
`\tikz \shadedraw [shading=axis,shading angle=90] (0,0) rectangle (1,1);`

### 建立一个Bounding Box
命令 `\useasboundingbox`， 或 `\path[use as bounding box]`

这个命令相当于将path进行clip了：
```
Left of picture\begin{tikzpicture}
\draw[use as bounding box] (2,0) rectangle (3,1);
\draw (1,0) -- (4,.75);
\end{tikzpicture}right of picture.
```
此时，文字就会和图片重叠，因为我们改变了Bounding Box

当然还可以利用它来制造更多的border空间：
```
Left of picture
\begin{tikzpicture}
\useasboundingbox (0,0) rectangle (3,1);
\fill (.75,.25) circle (.5cm);
\end{tikzpicture}
right of picture.
```

可以通过 `current bounding box` 获取当前的Bounding Box

同理，通过 `current path bounding box` 获取当前path的Bounding Box

如：
```
\begin{tikzpicture}
\draw[red] (0,0) circle (2pt);
\draw[red] (2,1) circle (3pt);
\draw (current bounding box.south west) rectangle
(current bounding box.north east);
\draw[red] (3,-1) circle (4pt);
\draw[thick] (current bounding box.south west) rectangle
(current bounding box.north east);
\end{tikzpicture}
```

### clip
```
\begin{tikzpicture}
\draw[clip] (0,0) circle (1cm);
\fill[red] (1,0) circle (1cm);
\end{tikzpicture}
```
如果只想clip，不想画出来这个clip的形状，可以使用 `\clip` 即，`\path[clip]`

```
\begin{tikzpicture}
\clip (0,0) circle (1cm);
\fill[red] (1,0) circle (1cm);
\end{tikzpicture}
```

要想得到local 的clip：
```
\begin{tikzpicture}
\draw (0,0) -- ( 0:1cm);
\draw (0,0) -- (10:1cm);
\draw (0,0) -- (20:1cm);
\draw (0,0) -- (30:1cm);
\begin{scope}[fill=red]
\fill[clip] (0.2,0.2) rectangle (0.5,0.5);
\draw (0,0) -- (40:1cm);
\draw (0,0) -- (50:1cm);
\draw (0,0) -- (60:1cm);
\end{scope}
\draw (0,0) -- (70:1cm);
\draw (0,0) -- (80:1cm);
\draw (0,0) -- (90:1cm);
\end{tikzpicture}
```

### 同时在一个path 执行多个操作
使用 `preaction=<options>` 指定一些选项，它就会自动建一个scope，在这个scope中，先用这个option画一遍，然后用path自己的option画一遍：
```
\begin{tikzpicture}
\draw[help lines] (0,0) grid (3,2);
\draw
[preaction={draw,line width=4mm,blue}]
[line width=2mm,red] (0,0) rectangle (2,2);
\end{tikzpicture}
```

而 `postaction`     相反，先用main action,然后用指定的option

### Decorating and Morphing a Path
这样：
```
\begin{tikzpicture}
\draw (0,0) rectangle (3,2);
\draw [red, decorate, decoration=zigzag]
(0,0) rectangle (3,2);
\end{tikzpicture}
```

或者：
```
\begin{tikzpicture}
\node [circular drop shadow={shadow scale=1.05},minimum size=3.13cm,
decorate, decoration=zigzag,
fill=blue!20,draw,thick,circle] {Hello!};
\end{tikzpicture}
```



## node
### 总览
node本身并不是path的一部分，一般是path 被draw之前，或之后才会加到最终的picture上的。

当然可以指定path的前后node啦：
```
\tikz \fill [fill=yellow!80!black]
(0,0) node {first node}
-- (1,1) node[behind path] {second node}
-- (2,0) node
```

###  语法
`node <foreach 语句> [各种选项] (名字) at (坐标) {内容，即 node contents}`
除了内容不可省略，其它皆可以 没有。

当然还可以不用大括号指定node内容，而是用node contents放到选项中：
如`(2,0) node [green, node contents=C]`
类似的用法还有 `name`,`alias`（另外的名字，就是各种小名啦）

`behind path` 在path后边
`in front of path`

`shape`:rectangle, circle, coordinate等，当然可以省略 `shape=`

`foreach statement`:
`\tikz \draw (0,0) node foreach \x in {1,2,3} at (\x,0) {\x};`

关于各种style：
`every node` 如： `\begin{tikzpicture}[every node/.style={draw}]`
`every <shape> node`,如： 
```
\begin{tikzpicture}
[every rectangle node/.style={draw},
every circle node/.style={draw,double}]
\draw (0,0) node[rectangle] {A} -- (1,1) node[circle] {B};
\end{tikzpicture}
```

name的前缀和后缀 :`name prefix`     和 `name suffix`
```
\tikz {
\begin{scope}[name prefix = top-]
\node (A) at (0,1) {A};
\node (B) at (1,1) {B};
\draw (A) -- (B);
\end{scope}
\begin{scope}[name prefix = bottom-]
\node (A) at (0,0) {A};
\node (B) at (1,0) {B};
\draw (A) -- (B);
\end{scope}
\draw [red] (top-A) -- (bottom-B);
}
```
### Common Options: Separations, Margins, Padding and Border Rotation
`inner sep`:文本和背景（text and the shape’s background path） 之间的距离，还有 `inner xsep` 和 `inner ysep`

`outer sep` 就是将anchor往外移动，就是类似margin的概念。它默认等于线宽line width的一半，我们指定了新的line width，它也就跟着变了，为了避免这个效果，可以将`outer sep`设为 `auto`


`minimum height`
`minimum width`
`minimum size` 同时指定 `minimum height`和`minimum width`：
```
\begin{tikzpicture}
\draw (0,0) node[minimum size=2cm,draw] {square};
\draw (0,-2) node[minimum size=2cm,draw,circle] {circle};
\end{tikzpicture}
```

`shape aspect=` 改变shape的比例，如diamond的长宽之比

`shape border rotate` 就是保持text不变，而shape进行旋转的度数

### 将node分成好几部分
语法；`\nodepart[选项]{part名字}`
```
\begin{tikzpicture}
\node [circle split,draw,double,fill=red!20]
{
% No \nodepart has been used, yet. So, the following is put in the
% ‘‘text’’ node part by default.
$q_1$
\nodepart{lower} % Ok, end ‘‘text’’ part, start ‘‘output’’ part
$00$
}; % output part ended.
\end{tikzpicture}
```
可以设定其样式：`every <part name> node part`
如：
```
\tikz [every lower node part/.style={red}]
\node [circle split,draw] {$q_1$ \nodepart{lower} $00$};
```

### node text的属性
`text=<color>`

font 的属性：
`node font= <font commands>`   ，如 `node font=\itshape`，`\tiny` 以及`\small`都行。
注意，这个设定的是node中的所有text的属性

还有一个属性：
`font= <font commands>`，相对于 `node font` 的区别就是，这个 `font` 一般是相对于这个node没有建立时的dimension，如我设定 1em， 那么就是相对于node外部的text的尺寸，可以这么用：
```
\tikz [every text node part/.style={font=\itshape},
every lower node part/.style={font=\footnotesize}]
\node [circle split,draw] {state \nodepart{lower} output};
```

### text的多行的对齐和宽度
多行可以用 `\\` 换行符。

可以使用标准的latex环境，如：
```
\tikz \node [draw] {
\begin{tabular}{cc}
upper left & upper right\\
lower left & lower right
\end{tabular}
};
```

直接指定 `text width`

还有：`align` 可以是：left，flush left，right，flush right,center，flush center等

### 放置node
#### 使用anchor放置node
系统本身定义了一系列anchor，默认是其center，即，其center放置在当前坐标

还有：`anchor=<anchor name>` 就会将node进行平移，从而使得这个node的anchor name放置在当前坐标

如：
```
\begin{tikzpicture}[scale=3,transform shape]
% First, center alignment -> wobbles
\draw[anchor=center] (0,1) node{x} -- (0.5,1) node{y} -- (1,1) node{t};
% Second, base alignment -> no wobble, but too high
\draw[anchor=base] (0,.5) node{x} -- (0.5,.5) node{y} -- (1,.5) node{t};
% Third, mid alignment
\draw[anchor=mid] (0,0) node{x} -- (0.5,0) node{y} -- (1,0) node{t};
\end{tikzpicture}
```

#### 基本的放置选项
上面 使用anchor放置node的时候 一半都是用node的south作为anchor，但这么搞太复杂，因此本节定义了一系列选项：

`/above=<offset>`:效果和 anchor=south 一样，只是额外定义了一些偏移，如：`\tikz \fill (0,0) circle (2pt) node[above=2pt] {above};`
类似的用法还有`below,left,right, above right`等一些列组合

#### 高级放置选项
实际上用了positioning库，这个库重定义了上节的above等选项，因此效果可能不太一样。
用法：`above=<specification>`
specification 由两部分组成，shift + of 部分

__先说shift 部分__
这个specification为dimension的时候和上面的基本放置选项效果一样
当specification为number的时候（即没有单位），实际上是向上平移 `(0,<number>).`
还可以是以上两种的混合：`[above=.2 and 3mm,draw]`    

__再说of部分__
`[above=1cm of somenode.north]`

还可以直接跟node的名字
```
\node (some node) at (1,1) {some node};
\node (other node) [above=1cm of some node] {\tiny above=1cm of some node};
```
相当于 other node的南面距离 some node的北面 1cm

要想把这个距离设为center之间的距离，只需加 on grid 选项即可：
如：`\node (c2) [on grid,above=1cm of b2] {a};`


__两个部分介绍完了，再说其他的__
我们可以先用 `node distance` 统一设定shift部分，然后后边只需要设置of部分就行了。
如：
```
\begin{tikzpicture}[every node/.style=draw,node distance=5mm]
\draw[help lines] (0,0) grid (2,3);
% Not gridded
\node (a1) at (0,0) {not gridded};
\node (b1) [above=of a1] {fooy};
\node (c1) [above=of b1] {a};
% gridded
\begin{scope}[on grid]
\node (a2) at (2,0) {gridded};
\node (b2) [above=of a2] {fooy};
\node (c2) [above=of b2] {a};
\end{scope}
\end{tikzpicture}
```

### fit 选项
使得该node的大小正好能包括住fit后边设定的选项：
```
\node[draw=red,inner sep=0pt,thick,ellipse,fit=(root) (b) (d) (e)] {};
\node[draw=blue,inner sep=0pt,thick,ellipse,fit=(b) (c) (e)] {};
```

或将其放到背景：
```
\begin{scope}[on background layer]
\node[fill=red!20,inner sep=0pt,ellipse,fit=(root) (b) (d) (e)] {};
\node[fill=blue!20,inner sep=0pt,ellipse,fit=(b) (c) (e)] {};
\end{scope}
```

### node 的变换如旋转
两种方式：
1. 当我们指定，`\tikz[scale=3]` 的时候，如果同时设定 `node[transform shape] {X},` 那么这个node也会跟着放大
1. 直接设定node的旋转等，感受一下：
```
\begin{tikzpicture}[every node/.style={draw}]
\draw[help lines](0,0) grid (3,2);
\draw (1,0) node{A}
(2,0) node[rotate=90,scale=1.5] {B};
\draw[rotate=30] (1,0) node{A}
(2,0) node[rotate=90,scale=1.5] {B};
\draw[rotate=60] (1,0) node[transform shape] {A}
(2,0) node[transform shape,rotate=90,scale=1.5] {B};
\end{tikzpicture}
```

至于非线性变换的属性`transform shape nonlinear`这里就不看了。

### 将node显式 放到line 或curve上
`pos=<fraction>` 此时，node就会放到前一个点到当前点的某一个比例的地方。
```
\tikz \draw (0,0) -- (3,1)
node[pos=0]{0} node[pos=0.5]{1/2} node[pos=0.9]{9/10};
```

注意对于 `|-` 这种交点，0.5 就是 corner point:
```
\tikz \draw (0,0) |- (3,1)
node[pos=0]{0} node[pos=0.5]{1/2} node[pos=0.9]{9/10};
```

`auto=<direction>` 如 `auto=left` ，那么，对于连接两个点的线，就是选择node的anchor使得node在这条线的左边。
    不指定这个direction，就是将其设为auto，即自动放置。
例如：
```
\begin{tikzpicture}
[scale=.8,auto=left,every node/.style={circle,fill=blue!20}]
\node (a) at (-1,-2) {a};
\node (b) at ( 1,-2) {b};
\node (c) at ( 2,-1) {c};
\node (d) at ( 2, 1) {d};
\node (e) at ( 1, 2) {e};
\node (f) at (-1, 2) {f};
\node (g) at (-2, 1) {g};
\node (h) at (-2,-1) {h};
\foreach \from/\to in {a/b,b/c,c/d,d/e,e/f,f/g,g/h,h/a}
\draw [->] (\from) -- (\to)
node[midway,fill=red!20] {\from--\to};
\end{tikzpicture}
```
就是将红色的node放到内圈。
而如果设为 `auto=right`     红色的node就在外圈。

`swap` 就是将auto的值取反：
```
\begin{tikzpicture}[auto]
\draw[help lines,use as bounding box] (0,-.5) grid (4,5);
\draw (0.5,0) .. controls (9,6) and (-5,6) .. (3.5,0)
node foreach \pos in {0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1}
[pos=\pos,swap,fill=red!20] {\pos}
node foreach \pos in {0.025,0.2,0.4,0.6,0.8,0.975}
[pos=\pos,fill=blue!20] {\pos};
\end{tikzpicture}
```
注意这里的 `use as bounding box` 的用法。

`’` 是 `swap` 的缩写。

`sloped` 使得node进行旋转，从而node水平线和curve相切。

`upside down` 就是将node上下颠倒
```
\begin{tikzpicture}[->,allow upside down]
\draw (0,0) -- (2,0.5) node[midway,sloped,above] {$x$};
\draw (2,-.5) -- (0,0) node[midway,sloped,below] {$y$};
\end{tikzpicture
```

`midway` 等价于 `pos = 0.5`

还有一坨：
`near start,near end,very near start,at start,at end`
这些其实都是一些固定的pos值。

### 隐式地放置到line或curve上
就是隐式计算node的位置，不常用
```
\begin{tikzpicture}[near end]
\draw (0cm,4em) -- (3cm,4em) node{A};
\draw (0cm,3em) -- node{B} (3cm,3em);
\draw (0cm,2em) -- node[midway] {C} (3cm,2em);
\draw (0cm,1em) -- (3cm,1em) node[midway] {D} ;
\end{tikzpicture}
```

### Label and Pin 选项
#### 前言
用于将一个node放到另一个node的旁边。

不用这俩选项的时候，这个任务比较麻烦，如
```
\tikz [circle] {
\node [draw] (s) {};
\node [draw] (a) [right=of s] {} edge (s);
\node [draw] (b) [right=of a] {} edge (a);
\node [draw] (t) [right=of b] {} edge (b);
}
```

用了之后就爽多了：
```
\tikz [circle] {
\node [draw] (s) [label=$s$] {};
\node [draw] (a) [right=of s] {} edge (s);
\node [draw] (b) [right=of a] {} edge (a);
\node [draw] (t) [right=of b, label=$t$] {} edge (b);
}
```

#### Label Option
`label=[<options>]<angle>:<text>`

这个angle可以是度数，也可以是anchor，如 340，north （其实就是将anchor转化为对应的度数）


__angle指定的是shape border上的位置。__

这个位置是相对位置，即相对于main node的位置，如：
```
\tikz [rotate=-80,every label/.style={draw,red}]
\node [transform shape,rectangle,draw,label=right:label] {main node};
```
虽然main node是旋转的，不管你有没有选择，我都在你的当前位置（现在当然是旋转之后的位置啦）的右边

若我们指定了 `absolute`的选项，那么不管你这个main node的方向和位置，我都在你的绝对位置的方向上，如：
```
\tikz [rotate=-80,every label/.style={draw,red},absolute]
\node [transform shape,rectangle,draw,label=right:label] {main node};
```

__对于 label node的anchor，可以用如下例子理解：__
```
\tikz
\node [circle, draw,
label=default,
label=60:$60^\circ$,
label=below:$-90^\circ$,
label=3:$3^\circ$,
label=2:$2^\circ$,
label={[below]180:$180^\circ$},
label={[centered]135:$115^\circ$}] {my circle};
```


__一个特殊的angle：center__
这时候label node始终在main node的中心

__label distance指定 label node 和 main node间的距离__
```
\tikz[label distance=5mm]
\node [circle,draw,label=right:X,
label=above right:Y,
label=above:Z] {my circle};
```


__当然还可以用 every label。__

#### pin 选项
pin选项和label选项几乎一样，就是多了一个操作，__将label node 和 main node用线连起来__
如：`\tikz \node [circle,fill=blue!50,minimum size=1cm,pin=60:$q_0$] {};`


`pin distance` 等价于上面提到的 label distance
还有 every pin 选项， 
`pin position=<angle>` 和label position差不多

`pin edge=<options>` 用来设置edge的选项

```
\tikz[pin distance=10mm]
\node [circle,draw,pin={[pin edge={blue,thick}]right:X},
pin=above:Z] {my circle};
```
还有 `every pin edge`：
```
\tikz [pin distance=15mm,
every pin edge/.style={<-,shorten <=1pt,decorate,
decoration={snake,pre length=4pt}}]
\node [circle,draw,pin=right:X,
pin=above right:Y,
pin=above:Z] {my circle};
```

#### 使用 quotes 库简化label和pin的语法
如将 `label={[]<options>]<text>}` 简化为 `"<text>"<options>`
`\tikz \node ["my label" red, draw] {my node};` 等价于 `\tikz \node [label={[red]my label}, draw] {my node};`

其他的暂时不想了解。

### 将node作为坐标来连接
给node起了名字之后，例如 x， 就可以 `x.<anchor>` 来当坐标用，默认的anchor是center，但当我们使用line to的时候，系统会智能地选择anchor，如 `(1,1)--(x)` 就会从x的border来连接。

如：

```
\begin{tikzpicture}
\path (0,0) node (x) {Hello World!}
(3,1) node[circle,draw](y) {$\int_1^2 x \mathrm d x$};
\draw[->,blue] (x) -- (y);
\draw[->,red] (x) -| node[near start,below] {label} (y);
\draw[->,orange] (x) .. controls +(up:1cm) and +(left:1cm) .. node[above,sloped] {label} (y);
\end{tikzpicture}
```

###  使用edge 操作来连接node
构建完main path，就构建edge的path，然后 画完main path，再画 edge path
`\path . . . edge[<options>] <nodes> (<coordinate>)`
这个edge 操作等价于构建了如下path：
`\path[every edge,<options>] (\tikztostart) <path>;`   
其中path就是一个to path, 

不使用 edge 操作的代码：
```
\begin{tikzpicture}
\node (a) at (0:1) {$a$};
\node (b) at (90:1) {$b$} edge [->] (a);
\node (c) at (180:1) {$c$} edge [->] (a)
edge [<-] (b);
\node (d) at (270:1) {$d$} edge [->] (a)
edge [dotted] (b)
edge [<-] (c);
\end{tikzpicture}
```
同样的图使用edge 操作：

```
\begin{tikzpicture}
\node foreach \name/\angle in {a/0,b/90,c/180,d/270}
(\name) at (\angle:1) {$\name$};
\path[->] (b) edge (a)
edge (c)
edge [-,dotted] (d)
(c) edge (a)
edge (d)
(d) edge (a);
\end{tikzpicture}
```


注意，以上代码中，当很多个edge操作连在一起的时候，第一个edge操作的起始坐标就作为 `\tikztostart`

edge 的选项会继承自main path，但也可以覆盖掉：
```
\begin{tikzpicture}
\node foreach \name/\angle in {a/0,b/90,c/180,d/270}
(\name) at (\angle:1.5) {$\name$};
\path[->] (b) edge node[above right] {$5$} (a)
edge (c)
edge [-,dotted] node[below,sloped] {missing} (d)
(c) edge (a)
edge (d)
(d) edge [red] node[above,sloped] {very}
node[below,sloped] {bad} (a);
\end{tikzpicture}
```

__当然edge操作也可用quotes库__
`"<text>"’<options>` 等价于 `edge node=node [every edge quotes]<options>]{<text>}`

例如： `\tikz \draw (0,0) edge ["left", ->] (2,0);`

### 跨图片索引 node
#### 不同图片的node索引
为node添加`remember picture` 选项，这样这个node在当前页面的位置就保存下来了，
如果下个图片需要用到上面保存过的node，那么这个图片就得添加 overlay选项，

如果不想每个图片都添加记忆选项，可以这样：`\tikzstyle{every picture}+=[remember picture]`

用法：
我们先记住倆node：
`\tikz[remember picture] \node[circle,fill=red!50] (n1) {};`

和
`\tikz[remember picture] \node[fill=blue!50] (n2) {};`

接下来就可以索引这俩node了：
```
\begin{tikzpicture}[remember picture,overlay]
\draw[->,very thick] (n1) -- (n2);
\end{tikzpicture}
```
注意这里必须得有overlay选项。

还可以继续索引：
```
\begin{tikzpicture}[remember picture]
\node (c) [circle,draw] {Big circle};
\draw [overlay,->,very thick,red,opacity=.5]
(c) to[bend left] (n1) (n1) -| (n2);
\end{tikzpicture}
```
#### 通过索引当前页面的node来实现绝对位置的放置
系统维持了一个 `current page` 的node，它的south west anchor就是本页的左下角，north east anchor就是本页的右上角。

可以利用它在页面左下角写字：
```
\begin{tikzpicture}[remember picture,overlay]
\node [xshift=1cm,yshift=1cm] at (current page.south west)
[text width=7cm,fill=red!20,rounded corners,above right]
{
This is an absolutely positioned text in the
lower left corner. No shipout-hackery is used.
};
\end{tikzpicture}
```

在本页中间画圆：
```
\begin{tikzpicture}[remember picture,overlay]
\draw [line width=1mm,opacity=.25]
(current page.center) circle (3cm);
\end{tikzpicture}
```

### 追加的选项：Late Code and Late Options
有时候一开始不想，或来不及，给node添加选项，这时候可以在后边加一行代码，进行操作，如：
```
\begin{tikzpicture}
\node [draw,circle] (a) {Hello};
\node also [label=above:world] (a);
\end{tikzpicture}
```
注意第二个node没有text。

语法：`\path . . . node also[<late options>](<name>) . . . ;`
这里的那么必须已存在，且必须指定name。

注意这里的late option只在local scope中起作用，要想真起作用，还必须给定append after command and prefix after command选项。


node also 除了通过上面的operation使用以外，还可以通过选项来玩：
```
\begin{tikzpicture}
\node [draw,circle] (a) {Hello};
\path [late options={name=a, label=above:world}];
\end{tikzpicture}
```

