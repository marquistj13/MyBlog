---
title:  clsguide-LATEX2e for class and package writers
date:   2018-2-11
---


* content
{:toc}


##  LATEX2e的特性
1. 提供了许多能够将package结构化的high-level commands
2. build classes and packages on top of each other, for example writing a
local technical report class cetechr (for the Chemical Engineering department)
based on article. 也就是基于article这个class可以创建很多class。

##  class 与 package
`document class`:将logical structure (例如 `\chapter`) into formatting (例如 `18pt bold ragged right`)的一个文件

`packages`:独立于document class的一些特性(some features such as colour or included graphics)包含在`packages`中。
实际上，你只要将一堆`\(re)newcommand and \(re)newenvironment commands`放到一个` package.sty`，就行了。


##  如何区分做class还是package？
>If the commands could be used with any document class, then make
them a package; and if not, then make them a class.

## 命令名
1. 全小写的，短的，如`\section, \emph and \times`
1. 长的、大小写混合的，如`\InputIfFileExists \RequirePackage \PassOptionsToClass`，这些是class and package writer commands，而且这些命令会一直受支持。
1. 带`@`的，例如`\@tempcnta, \@ifnextchar and \@eha`. 这些命令只能在class and package 文件中使用.这些命令在latex的后续版本不一定支持。

## Loading other files
```
\LoadClass          \LoadClassWithOptions  
\RequirePackage     \RequirePackageWithOptions
```

那么为啥不直接用`\input`呢？
因为`\RequirePackage`或者`\usepackage`可以防止重复加载，即一个package被请求加载了很多次，但最后能保证只加载一次。
而`\input`并没有这个机制。

## Make it robust
大原则就是，尽量使用latex自带的macro，不要使用tex的macro
如box的操作，用`\sbox, \mbox and \parbox`,不要用tex的`\sbox, \mbox and \parbox`

另外一个相关的命令:`\DeclareRobustCommand`,用于定义和encoding-independent com-
mands，因为LATEX2e支持不同的encodings。
完整语法：
```
\DeclareRobustCommand {<cmd>} [<num>] [<default>] {<definition>}
\DeclareRobustCommand* {<cmd>} [<num>] [<default>] {<definition>}
```
其中带`*`的用于定义短的命令。

## Using classes and packages
格式：
`\RequirePackage[<options>]{<package>}[<date>]`
`\RequirePackage{ifthen}[1994/06/01]`

`\LoadClass[<options>]{<class-name>}[<date>]`
`\LoadClass[twocolumn]{article}`

这俩其实和用户使用的`\usepackage`和`\documentclass`的语法一样。

不同的是，可以将当前class的option原样传递给要load的class或package：
```
\LoadClassWithOptions{<class-name>}[<date>]
\RequirePackageWithOptions{<package>}[<date>]
```
如
```
\LoadClassWithOptions{article}
\RequirePackageWithOptions{graphics}[1995/12/01]
```

##  options
这么声明的：
`\DeclareOption{hoptioni}{hcodei}`
例如graphics包就是这么声明的：`\DeclareOption{dvips}{\input{dvips.def}}`
这样当`\usepackage[dvips]{graphics}`的时候，就会加载`dvips.def`文件。

当用户使用无效的option时候，可以这么处理：
```
\DeclareOption*{%
\PackageWarning{fred}{Unknown option `\CurrentOption'}%
}
```

也可以利用这个特性这么做：
```
\DeclareOption*{%
\input{\CurrentOption enc.def}%
}
```
即不管啥选项都去加载`<ENC>enc.def`其中`<ENC>`是选项名。

也可以将未处理的option传给其他class或package：
```
\DeclareOption*{%
\PassOptionsToClass{\CurrentOption}{article}%
}
```
当然这么用的话要确保将来你去load这个article类。


要执行option：`\ProcessOptions\relax`
也就是执行每一个option的code。


另外，`\DeclareOption*`，其实就是用来处理未显示定义的option的。而且如果你的class如果没有这个东西的话，默认情况下会将未声明的option传给所有package。
而对于你写的package文件，默认情况下未声明的option会产生error。

对于option的处理，有以下两个命令可以用：
`\CurrentOption`,当前option的名字。
`\OptionNotUsed`,将当前option加到`unused options'列表里边。

另外：
```
\PassOptionsToPackage {<options-list>} {<package-name>}
\PassOptionsToClass {<options-list>} {<class-name>}
```
注意此处`\PassOptionsToPackage`将option加入到options-list，而将来使用`\RequirePackage or \usepackage`的时候的option也在这个options-list里边，举个例子：
```
\PassOptionsToPackage{foo,bar}{fred}
\RequirePackage[baz]{fred}
```
等同于：`\RequirePackage[foo,bar,baz]{fred}`
`\PassOptionsToClass`同理。

## Delaying code
有俩主要用于`\DeclareOption or \DeclareOption*`的code部分的命令。
```
\AtEndOfClass {<code>}
\AtEndOfPackage {<code>}
```
也就是将这些code先保存在一个列表里边，直到class or package的最后再执行。
其中，在列表里边的顺序以其声明的顺序而定。


还有类似的命令：
```
\AtBeginDocument {<code>}
\AtEndDocument {<code>}
```
当然这个`\AtBeginDocument` hook里边的code不能放排版相关的命令，以免unpredictable。

## option的执行
这里深入讨论一下option执行的顺序和惯例。

### 实现一个需求，即执行默认的option
首先一个需求，如果我们要默认执行一些选项。可以使用`\ExecuteOptions {<options-list>}`，记着要将其放到`\ProcessOptions`的前面。

一个例子：
`\ExecuteOptions{11pt,twoside,twocolumn}`

### 如何不按照option声明的顺序执行，而是按照调用命令的顺序执行
使用`\ProcessOptions*`即可。
此时，对于一个package来说，就会首先处理package的global option.

那么什么是global option？

### Local options和Global options
Global options：用户通过`\documentclass[<options>]`指定的option
Local options：通过`\PassOptionsToPackage{<options>} \usepackage[<options>] \RequirePackage[<options>]` 显示指定的option。

例如，对于以下：
```
\documentclass[german,twocolumn]{article}
\usepackage{gerhardt}
```
而package gerhardt calls package fred with:
```
\PassOptionsToPackage{german,dvips,a4paper}{fred}
\RequirePackage[errorshow]{fred}
```
那么对于fred来说，其local options 为 german, dvips, a4paper and errorshow; fred's only global option is twocolumn.

latex的机制确保这些option至多执行一次。
