---
layout: post
title:  如何使用本模板实现note-taking的purpose
categories: 编辑器等文档工具
tag: Jekyll
---


* content
{:toc}



本博客对应的github repository：https://github.com/marquistj13/MyBlog


模板来源
====================================
改编自：[LessOrMore](https://github.com/luoyan35714/LessOrMore)

此模板特性
====================================
简单来说是用来记笔记的。
因为post类型的文章使用markdown的时候，不能插入 `_post` 目录的图片，这一点我感觉不太好，幸好Jekyll还有一种Collection类型的“文章库”，Collection中的md文件可以插入对应Collection目录的图片，再基于Jekyll的一个特性：设置`frontmatter`的文件就用`Liquid`模板渲染一下，没有设置`frontmatter`的文件就原样copy到`_site`目录，因此我打算将其改造成利用Collection进行note-taking的blog。


使用
====================================
**本模板主要是自己捣鼓着用的，没有时间和精力进行打磨，所以有很多瑕疵，不过够自己用了**。
以下为对此捣鼓过程的总结。

下载
------------------------------------

使用git从 [MyBlog}(https://github.com/marquistj13/MyBlog) 主页下载项目

``` bash
git clone https://github.com/marquistj13/MyBlog.git
```

配置
------------------------------------
**本模板的所有配置文件均在位于根目录的文件夹 `_config_with_python`中。**

由于本模板改编自 [LessOrMore](https://github.com/luoyan35714/LessOrMore) ，因此基本配置和[LessOrMore](https://github.com/luoyan35714/LessOrMore)相同，即配置根目录的文件`_config.yml`。**本模板配置不同之处在于：**用户需要配置的文件不是根目录的`_config.yml`，而是位于根目录的文件夹 `_config_with_python` 中，即`template_config.yml`文件用于设置blog的meta data，详情请参考 [LessOrMore](https://github.com/luoyan35714/LessOrMore)。在此对于本配置文件的修改注意事项进行重申：`template_config.yml`中的baseurl修改为你的github的项目名，如果项目是'***.github.io'，则设置为空''

**本模板比[LessOrMore](https://github.com/luoyan35714/LessOrMore)增加的特性：**collection的配置，即使用使用 `menu_config.yml` 配置blog header的菜单项，举个例子：


```ruby
menus:
- menu_name_cn: 阅读笔记
  menu_name_en: ReadingNotes
  menu_list:
  - Book_NeuralNetworksAndDeepLearning
  - test
- menu_name_cn: 学术积累
  menu_name_en: ScholarThings
  menu_list: [test_scholar]
```

很容易看懂，我就是新建两个下拉菜单项，阅读笔记以及学术积累，阅读笔记的英文名ReadingNotes用于建立文件夹的时候使用，阅读笔记下面一共有两个collection项（分别对应两个文件夹，即Book_NeuralNetworksAndDeepLearnin和test，这俩文件夹下面可以存放对应的笔记，同理，学术积累菜单项下面只有一个collection即test_scholar

**小提示：**在每一个collection下面可以放入子文件夹，本模板亦可以根据子文件夹创建此collection下对于子文件夹中的文件的索引目录，这个功能是根据文章的url实现的，主要参考的是 [这篇文章](https://thinkshout.com/blog/2014/12/creating-dynamic-menus-in-jekyll/).但由于文件夹名字转换为url之后变成了ASCII码，因此从url中提取的子文件夹名字得用`Liquid`模板语言的一个filter：`url_decode`，这个filter只有新版本的Liquid的支持，如果遇到老版本的Liquid那就不行，所以，如果你对子文件夹含有中文，列出来的索引目录就是对应的ASCII码，我暂时就这么凑合着用吧，哈哈。

**在每次对`template_config.yml`或者`menu_config.yml`进行修改以后必须运行一次`buildMenu.py`**。`buildMenu.py`依赖于两个Python library：`PyYAML`和`jinja2`。