---
layout: post
title:  这个博客是如何搭建的
date:   2017-01-22 16:44
categories: 编辑器等文档工具
tag: Jekyll
---


* content
{:toc}


本博客对应的github repository：https://github.com/marquistj13/MyBlog

## 搭建缘由
* 一个顺手工具的逝去
自从韩桑向我推荐为知笔记之后，我逐渐依赖上了它。对Markdown的完美支持以及截图功能的整合使得它堪称完美（以我有限的经验来说算是吧）。于是我就用为知笔记来记一些可以归档的东西，日记还是用Emacs的org-mode。（ps，为知笔记可以导出纯文本，但它的源文件是二进制的，这个可能是为了解决md文件中插入图片的问题吧）
不过从1月份开始它强行给非会员“断网”了，我一直依赖的云同步就这么没了。对于这件事我们也不太好评价，我觉得人不应该被某一个工具给奴役吧，它要离你而去，你又不用钱去挽留，好聚好散吧。

* 寻找替代品
感伤之余我决定探索新的笔记解决方案。先是Evernote，发现md的图片插入问题实在难以解决，好多人都在用七牛的图片链接（暂且这么叫吧），我对这个有点不太放心，总感觉这些图片存在自己够得着的目录才比较踏实。因此又转向github，但转过来之后才发现github对于md的渲染是有自己的癖好的，我在为知笔记以及一些md客户端如现在用的haroopad（棒子出品），它们都是将换行给literally处理了，在github上则给忽略了，因此我喜欢用无序列表作为小标题的癖好就无法被照料了，好伤心；而且github的多个文件夹管理起来实在不好搞，这时候我想到了为知笔记等文件夹管理的好处了，好怀念……
不过天无绝人之路，我发现每一个github的project都可以创建一个GitHub Pages（就是一个网站啦），而且可以自定义theme，瞬间打开了新世界的大门，这样就可以方面地在md中插入图片，又可以用html方面地定制我的文件夹功能了。
我决定尝试一下。

* 搜寻替代品过程的感悟
写markdown的时候一定要养成好习惯，该换行的时候一定要换行啊。


## 前期准备工作
* 主题的选择
浏览一圈之后，发现一个极简洁的 theme：[LessOrMore](https://github.com/luoyan35714/LessOrMore)。这个主题虽然很简洁，但要想进行定制，对于HTML一窍不通的我来说也是不简单的。
因此要学习新事物了，要读文档啦。

* 读文档前的 meta knowledge
当然不能一股脑地读文档了，首先你得选择哪些文档是需要读的，这时候进行search，有个粗略的了解就行了。
我先是找到http://www.jianshu.com/p/88c9e72978b4 这个中文的，后来发现下面这个英文的：
按照http://svmiller.com/blog/2015/08/create-your-website-in-jekyll/#startjekyll 的指导，最好在本地使用jekyll来建站，哈哈在本地操作就行了，没有必要非得把它搞到云端哈。因为在本地进行调试更方便嘛，这样就不用频繁地push到github上进行测试了。
总结一下：**我按照上面两个教程的指点知道了，需要在本地安装Jekyll，于是按照Jekyll的官方教程安装了Jekyll**。

* 读文档的过程
首先是[Jekyll官方文档](https://jekyllrb.com/docs/home/)，这个看完之后就能知道Jekyll的粗略原理了，然后是HTML的学习，我Google搜索HTML排在前面的就是[这个](http://w3school.com.cn/html/index.asp),快速将其浏览完。当然前面两个文档几乎是同时看的，看的目的就是：看懂[LessOrMore](https://github.com/luoyan35714/LessOrMore)的源码，当然看文档只是一方面了，只有自己去定制的时候才能理解的更深刻。
之后在读文档的时候我又发现需要读一个Jekyll用到的template语言[Liquid](https://shopify.github.io/liquid/)，这个也是很快就能读懂了。

## 定制需要的特性
### Jekyll哪些部分可以用来定制
我看了一天的[Jekyll官方文档](https://jekyllrb.com/docs/home/),我在看别人的教程以及官方文档的时候发现Jekyll要是只有blog功能的话肯定不够灵活嘛，毕竟我不一定每一篇文档都得放到_post中，而且还得以日期开头。果然在官方文档中看到了[Collection](http://jekyllrb.com/docs/collections/)这个东西。我还看了[Explain like I’m five: Jekyll collections](http://ben.balter.com/2015/02/20/jekyll-collections/)这个很好地讲collection的文章，还有这个[Getting Started with Jekyll Collections](https://www.sitepoint.com/getting-started-jekyll-collections/)
在[Explain like I’m five: Jekyll collections](http://ben.balter.com/2015/02/20/jekyll-collections/)中，作者提到post类型是用来写博客的，必须按照日期来命名，一旦写了就不怎么变了；而pages类型是用来写一些彼此之间没有什么关联的文档，如about页面以及tags等用来list的页面。由于pages没有日期的概念，因此需要经常更新。
但我们记笔记这件事就和上面这两种类型都对不上了，笔记嘛，不需要日期的概念，还得经常更新，还好**Jekyll有collection这个可以定制的类型**（我后来发现，一个博客站点所有的post同属于一个叫做post的collection）

### Jekyll的工作机理可以用来解决图片插入的问题
Jekyll的工作机理：你告诉它这个文件需要进行转换（即在frontmatter中进行指定），那么很好，我会将这个文件转换之后拷贝到_site目录，如果没有告诉Jekyll需要对这个文件进行转换，它也会原样拷贝到_site中的对应目录进行发布。利用这个特性，可以为一堆笔记建立一个collection，里边可以放入子文件夹用来存图片。（但一定要注意的是文件夹名称不可以有空格，要不然Jekyll就会自己产生一个有空格的将生成的文件放进去，而原样不动的文件则会在另一个文件夹中，这个文件夹的名称用`%20`代表空格，这样就很不好了，即md文件和它的image文件分开了）

### jekyll中公式的支持
我查了一下GFM统一用两个dollar符号`$$`来标识公式，而且inline 和 displayed math都是用俩`$`,GFM会自动推断出这俩东西的区别。
使用jekyll的时候，需要手动启用mathjax的支持，可以根据[Jekyll使用MathJax来显示数学式](http://cyukang.com/2013/03/03/try-mathjax.html)这个页面，或者[Mathjax官方主页](http://docs.mathjax.org/en/latest/start.html)的例子进行，即可以在每一个HTML中加入这俩页面介绍的几行代码，也可以在jekyll的default.html加上去。我推荐使用[How to use MathJax in Jekyll generated Github pages](http://haixing-hu.github.io/programming/2013/09/20/how-to-use-mathjax-in-jekyll-generated-github-pages/)介绍的Mathjax配置部分，当然这个页面的markdown部分我是不用的。
我的最终解决方案就是：用个例子来说吧，对于LessOrMore这个theme来说，由于没有Jekyll官网中collection部分提及的page.html，于是我就将此theme的post.html 复制过来进行改造哈哈，具体改造如下，在includes目录新建一个mathjax_support.html,里边加入[Mathjax官方主页](http://docs.mathjax.org/en/latest/start.html)提供的代码：


``` html
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}});
</script>
<script type="text/javascript" async
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_CHTML">
</script>
```
然后在`/_layout/page.html` 上部加入`{\% include mathjax_support.html \%}
`即可。(注意要把斜杠`\`去掉，我加到这里是为了防止Liquid模板把这行代码给替换掉)
我后来又在`_layout`目录的`default.html,post.html`也加上了这行代码。

### jekyll中GFM配置的额外惊喜
如果将kramdown配置成:


```ruby
kramdown:
  input: GFM
  hard_wrap: true
  gfm_quirks: paragraph_end
```
 那么就可以literally地解析换行符，这是为知笔记以及很多markdown编辑器如haroopad都支持的。以上配置的详情可阅读[GFM Parser](https://kramdown.gettalong.org/parser/gfm.html)。
注意，详细的参考配置见[Jekyll Configuration](https://jekyllrb.com/docs/configuration/),如配置toc_levels，smart_quotes等。这个configuration可以参考很多设置的trick。

## 对于LessOrMore的更改
### 文件夹更改以及冗余的去除
[LessOrMore](https://github.com/luoyan35714/LessOrMore)有一些需要调整的地方，我将那些page类型的网页，如catories，tags，feed等都移到了`_pages`文件夹，并将此目录加入配置文件`_config.yml`:`include: [_pages]`.
我还将`_include\header.html`中乱七八糟的各种东西给删掉了，用来放置我的“文件夹”，哈哈。

### collection的加入
我在`_include\header.html`中放入几个下拉菜单，每个下拉菜单用于存放不同的大类，即下拉菜单相当于一级文件夹，菜单中每一项对应一个collection，相当于二级文件夹，这些collection在配置文件中需要进行声明：


``````ruby
collections:
  ReadingNotes_Book_NeuralNetworksAndDeepLearning:
      output: true
      permalink: /ReadingNotes/Book_NeuralNetworksAndDeepLearning/:path
  ReadingNotes_test:
      output: true
      permalink: /ReadingNotes/test/:path
defaults:
  - scope:
      path: ""
      type: ReadingNotes_test
    values:
      layout: page
  - scope:
      path: ""
      type: ReadingNotes_Book_NeuralNetworksAndDeepLearning
    values:
      layout: page
``````

### 对应于此的博客header的修改
即下拉菜单的设定：


```html
<ul class="nav navbar-nav navbar-right">
        <li class="dropdown">
          <a href="#" class="dropdown-toggle" data-toggle="dropdown">阅读笔记<b class="caret"></b></a>
          <ul class="dropdown-menu"> 
            <li>
              <a href="{{ '/ReadingNotes/Book_NeuralNetworksAndDeepLearning/' | prepend: site.baseurl}}">Book_NeuralNetworksAndDeepLearning</a>
            </li>          
            <li>
              <a href="{{ '/ReadingNotes/test/' | prepend: site.baseurl}}">Test</a>
            </li>
          </ul>
        </li>
        <li class="dropdown">
          <a href="#" class="dropdown-toggle" data-toggle="dropdown">学术积累<b class="caret"></b></a>
          <ul class="dropdown-menu"> 
            <li>暂时没有</li>
          </ul>
        </li>
      </ul>
```

### 对应于以上的collection文件夹中的修改
对应的文件夹需要放置一个index.html的文件，此文件修改自`_layouts\tag.html`,如文件夹`C:\Users\Bacon\Documents\GitHub\MyBlog\_ReadingNotes_Book_NeuralNetworksAndDeepLearning`中的index为以下两处：


```html
<div id="navigation">
        	<h1>目录</h1>
      		<ul class="nav sidenav">
            {\% assign num_pages = site.ReadingNotes_Book_NeuralNetworksAndDeepLearning.size \%}         
            <li>
              {\{ "Book_NeuralNetworksAndDeepLearning" \| truncate: 25}\}
              <span style="color: #999999;" >({{ num_pages | minus:1 }})</span>            
            </li>
          </ul>
        </div>
```
以及：


```html
    <div class="col-md-9" role="main">
      <div class="panel docs-content">
        <div class="wrapper">
          <div class="home">
			  <h2 >{{ NeuralNetworksAndDeepLearning | join: "/" }}</h2>
			  <ul> 
			    {\% assign pages_list = site.ReadingNotes_Book_NeuralNetworksAndDeepLearning \%}  
			    {\% include LessOrMore/pages_list \%}
			  </ul>				
          </div>
        </div>
      </div>
    </div>
```
注意以上的`\`需要去掉。

## 插曲
19号回到家，20号看到垃圾箱里躺着一封垃圾邮件，一看竟然是拒稿信，10月份投的那篇paper被拒了。一开始很愤怒，关键是评审意见特别蛋疼，都是一些很没有水平的意见，审稿人根本都没有搞明白论文里的东西就一通乱喷，哎。
不过仔细一想，四个refree的意见基本都很可笑，其中一个refree问我，“你如何处理方法A的某个缺陷”，我很无语真的，因为我并没有在paper中用这个方法A；还有一个refree这么问我，针对我paper中背景知识介绍部分的一句话进行挑刺，我说"Typicality是fuzzy set的一种很common的解释“，然后refree就挑刺了，”你最起码要将typicality是啥给解释一下啊！“，我的天啊，我都说了这是一个很common的东西勒，你要是fuzzy圈儿的能不知道这个，不知道这个您最起码查一下啊，Google一下”typicality fuzzy set“会死啊？
没想到会遇到这么不靠谱的评审，哎
不过我一开始没有想明白，21号一直很郁闷，心想着郁闷也没啥用，就一直在玩儿Jekyll，果然玩儿着玩儿着就忘了痛苦，哈哈，反正今天也想开了，知道了学术界有这种人的存在，哈哈，很有意思。
又get到了一种消愁的方法：专注于玩儿一个没有明显回报的东西，如写博客，折腾各种小技术。

## 总结和启发
从19号到家，这几天几乎都在玩Jekyll，我发现这些新东西学起来挺好玩儿的，破除了对于html建站的神秘感，也极大增强了以后记笔记的灵活性。

* 新事物学习的重要性
学习搭建博客，又get了一个新技能哈哈，打开了新世界的大门，受到工具的限制变少了。

* 启发
以后要经常看paper啊，不要总是停留在已有知识体系中，这样子就很难进步，很难发现更大的世界，无法站在高层次去看待各种algorithm以及idea等。




