---
layout: post
title:  自动创建blog的menu
categories: 编辑器等文档工具
tag: Jekyll
---


* content
{:toc}


本博客对应的github repository：https://github.com/marquistj13/MyBlog

## Motivation
在搭建此blog的过程中，我发现如果新加入一个collection，需要频繁地做一些很机械性的、具有固定pattern工作，如在 `_config.yml` 中加入一些配置，在 `header.html` 中加入对应菜单项，在对应的collection的目录中加入一个 `index.html` 。
很明显，这个东西最好用脚本去实现，这样就可以一劳永逸啦！

## 实现细节

我花了一天写了个脚本，当时写的时候由于很多轮子都是现学现用的，因此整个制作过程并非特别顺利，也就是说以下并不是我真正的按顺序发生的探索过程，而是事后整理的“应该按照这个顺序和要求来做”。

### 方案和各种协议的确定

* 配置文件的位置
我把所有配置文件放到一个新建的位于根目录的文件夹 `_config_with_python` 中，即原来根目录的`_config.yml`也放到这个目录了，原因很简单，我用Python脚本读写 `.yml` 文件之后， `.yml` 文件内容的顺序就会发生变化，里边的注释也就没了，这是其中一个原因，还有一个原因是，放到一个单独的文件夹感觉更美观哈哈。

* 配置文件的组成
`buildMenu.py` ：总配置文件，这个文件只需要在“增删collection”时运行一下就行了。
`menu_config.yml` ： blog的header菜单配置选项，每一个collection都存放在对应的菜单中，一般情况下，用户只需要根据这个文件进行“增删collection”就行了。
`template_config.yml`： 用于存放原根目录的 `_config.yml` 的配置内容，现在根目录的 `_config.yml`是由`buildMenu.py`生成的。
`template_header.html` ：一个模板文件（Jinja2)，用于生成blog的header，注意菜单项就在这个文件中。
`template_index.html` ：一个模板文件（Jinja2)，用于生成每一个collection文件夹下的`index.html`


### 使用 `menu_config.yml` 配置菜单项
一个example就是：


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

很容易看懂，我就是新建两个下拉菜单项，阅读笔记以及学术积累，阅读笔记的英文名ReadingNotes用于建立文件夹的时候使用，阅读笔记下面一共有两个collection项（分别对应两个文件夹，即Book_NeuralNetworksAndDeepLearnin和test，这俩文件夹下面可以存放对应的笔记。

上面这个菜单项这么配置的好处就是，用python读取出来正好是一个 value 为 list 的字典。如：


```python
import yaml
yamlFile=r".\menu_config.yml"
menu_config=yaml.load(file(yamlFile,'r'))
#print yaml.dump(menu_config,allow_unicode=True)
```

以上读出来的结果为：

```python
menu_config['menus']=[{'menu_list': ['Book_NeuralNetworksAndDeepLearning', 'test'],
  'menu_name_cn': u'\u9605\u8bfb\u7b14\u8bb0',
  'menu_name_en': 'ReadingNotes'},
 {'menu_list': ['test_scholar'],
  'menu_name_cn': u'\u5b66\u672f\u79ef\u7d2f',
  'menu_name_en': 'ScholarThings'}]
```

当然 `print yaml.dump` 出来的更漂亮。

在 `buildMenu.py` 程序中，我们需要从中提取出来一些可以直接用的字典：


```python
 # extract menus from menu_config.yml
    menu_config = yaml.load(file(yamlMenuFile, 'r'))
    menus = menu_config['menus']
    # menus is a list of menu dictionaries:
    # [
    # {'menu_name_en': 'ReadingNotes', 'menu_name_cn': u'\u9605\u8bfb\u7b14\u8bb0',
    # 'menu_list': ['Book_NeuralNetworksAndDeepLearning', 'test']},
    # {'menu_name_en': 'ScholarThings', 'menu_name_cn': u'\u5b66\u672f\u79ef\u7d2f', 'menu_list': []}
    # ]
    # menus is essential in the following configureation.

    # construct the menus_dict to update collections in yamlConfigFile and also for other use.
    menus_dict = {}
    for menu in menus:
        menus_dict[menu['menu_name_en']] = menu['menu_list']
```

这样 `menus_dict` 就是 `{'ReadingNotes': ['Book_NeuralNetworksAndDeepLearning', 'test'],'ScholarThings':['test_scholar']}`


### 根据 `menu_config.yml` 写入 `_config.yml` 的collection相关的部分

对于以上的菜单项配置，对应的写入部分为：

```ruby
collections:
  collection_ReadingNotes_Book_NeuralNetworksAndDeepLearning:
    output: true
    permalink: /ReadingNotes/Book_NeuralNetworksAndDeepLearning/:path
  collection_ReadingNotes_test:
    output: true
    permalink: /ReadingNotes/test/:path
  collection_ScholarThings_test_scholar:
    output: true
    permalink: /ScholarThings/test_scholar/:path
defaults:
- scope:
    path: ''
    type: collection_ScholarThings_test_scholar
  values:
    layout: page
- scope:
    path: ''
    type: collection_ReadingNotes_Book_NeuralNetworksAndDeepLearning
  values:
    layout: page
- scope:
    path: ''
    type: collection_ReadingNotes_test
  values:
    layout: page
```

这是通过 `buildMenu.py` 程序中的如下代码实现的：


```python
# update collections related configurations in yamlConfigFile, so Jekyll knows who are collections
    h_yamlConfigFile = yaml.load(file(yamlConfigFile, 'r'))
    streamyamlConfigFile = file(yamlConfigFile, 'w')
    h_yamlConfigFile['collections'] = collections_from_dict(menus_dict)
    h_yamlConfigFile['defaults'] = defaults_from_dict(menus_dict)
    yaml.dump(h_yamlConfigFile, streamyamlConfigFile, default_flow_style=False, allow_unicode=True)
    streamyamlConfigFile.close()
```

很容易看懂，根据Jekyll的工作机理，一会儿我们需要在博客的根目录创建名为 `_collection_ReadingNotes_Book_NeuralNetworksAndDeepLearning`,`_collection_ReadingNotes_test`,`_collection_ScholarThings_test_scholar` 这三个文件夹。

然后我们就需要在以上三个文件夹中放入一个 `index.html` ，用来对当前collection（及当前菜单项中的文章进行列表），由于这个 `index.html` 最终要被Jekyll的模板语言Liquid进行渲染，因此我们其实是要生成一个模板，如何解决呢？

### 用 `template_index.html` 生成模板 `index.html`

还好我们有 Jinja2 ,也是一个模板语言，可以方便用Python调用（姑且这么理解吧，其实它就是python的一个轮子）。模板的作用就是用来生成、展开成一个大一点的东西，当然这俩模板语言的语法会有冲突，这时候就得使用 Jinja2 的的escape功能了，如 `template_index.html` 的主体部分：
![]({{ '/blog_images/2017-01-24-blog-menu-autogeneration/template_index.png' | prepend: site.baseurl }})
这里边一大坨的 ` raw  endraw ` 里边东西 `{` 就是Liquid的，外边的如 `{collection_iterm_name}` 就是 Jinja2 的。（注意，以上应该是两个`{`，可我不能在这儿写两个啊，要不然就会被Liquid替换掉，话说Liquid没有escape真烦啊。）

update: 原来Liquid也可以escape，而且和jinja2一样哈哈，测试：{% raw %}`{{` 就是Liquid的，外边的如 `{{collection_iterm_name}}` 就是 Jinja2 的。{% endraw %}


上面这一坨的替换，即 `index.html` 主要是通过 `buildMenu.py` 程序的如下代码实现的:


```python
jinja_template.render(collection_iterm_name=collection_iterm_name, collection_name=collection_name))
```

###用 `template_header.html` 生成模板 `header.html`

`template_header.html` 的主体部分如下：
![]({{ '/blog_images/2017-01-24-blog-menu-autogeneration/template_header.png' | prepend: site.baseurl}})
上面这一坨的替换，即 'header.html` 主要是通过 `buildMenu.py` 程序的如下代码实现的:


```python
# update header_file in the _includes directory, so the menus are shown in the header of our blog.
    h_template_header_file = codecs.open(template_header_file, "r", "utf-8")
    h_header_file = codecs.open(header_file, "w", "utf-8")
    jinja_template = Template(h_template_header_file.read())
    h_header_file.write(jinja_template.render(menus=menus))
    h_header_file.close()
    h_template_header_file.close()
```

## 感悟
最近这几天权当休息了，花了几天时间打造一个记笔记的blog，哈哈
我发现最近几年学会了静下心来做事情，不浮躁了，很多东西就是不能只求一个快字，慢慢来，不要错过重要的线索。要始终记得“你要到那里去”，不要陷到一个东西里边去。
就拿这次我花了几天时间去定制一个blog，猛一看觉得自己是浪费时间了，其实不然，这段时间能够沉浸下去玩儿一下，顺便知道了，自己也是可以去玩儿的。
更重要的是了却了一个重大的愿望：要有一个顺手的笔记平台。
我可以高兴地宣布：这个blog被我调教好了！
从此以后可以将各种笔记全部交由github托管了。