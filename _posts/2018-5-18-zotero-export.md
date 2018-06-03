---
layout: post
title:  zotero export 的设置
categories: [编辑器等文档工具]
tag: [zotero]
---

* content
{:toc}

## 前言
以下默认安装了zotero的Better Bib(La)TeX 。
且已经导出了keep updated的文献库（文件，导出文献库，格式，better bibtex，勾选keep updated）。

本文将解决以下问题：
1. cite key部分用来将citation key设为`simon_training_2002`这种形式，即作者名字+题目首个单词+年份。
1. 调教bib文件的field部分，用来定制产生的bib文件的field。

## cite key
### 拖放法获得cite key
为了方便导出文献的cite key，可以使用拖放的方法，即将某个文献直接拖到编辑器中，就会将其cite key插入这个编辑器。
如果使用普通纯文本工具，这种方法很好，当然word有zotero的插件就不需要这么搞，emacs有auctex插件也不需要这么搞。

具体设置参照 [Generating citekeys for your references](https://retorque.re/zotero-better-bibtex/citation-keys/)
中的 `Drag and drop/hotkey citations` 一节：
>Zotero preferences, tab Export, under Default Output Format, select “Better BibTeX Quick Copy”, and choose the Quick Copy format under the Citation keys preferences for BBT.

这样，当我们拖放的时候，就会按照咱们的better bibtex的cite key的设置。
怎么设置这个cite key的格式呢？
在首选项，better bibtex,citation keys中，设置citation key format，具体的设置可以参考上面那个链接。 下面会详细展开我的需求。

### zotero 5 改变citation key pattern （或者说format）之后的生效机制
在这记录一下我的设置。
先讲一下背景。 
首先是改变citation key pattern （或者说format）更改之后的生效机制。
由于我以前用的是zotero自带的cite key,而新版的Zotero 5情况发生了变化，也就是说，以前的zotero版本中，我们如果改变了这个citekey generator的pattern，也就是改变了citation key的格式，那么我们导出的文献库中的citation key默认是不变的，这个新的pattern在加入新的文献的时候才对这个新的文献生效，要想使得旧的文献生效，就得选择该文献，右键，refresh。

__重点来了：__不知为何，新版zotero的citation key变了，不是原来的形式了（准确来说，我以前用的是standard Bib(La)TeX exporters of Zotero，现在用的是zotero的better bibtex插件）。而我有很多文献的引用是老的citation key的形式，如`simon_training_2002`， 因此就得重新设置citation key的pattern。

当然你要想自己定制的话，可以参考上面的链接。而我只需要使用老格式就行了。
并且测试的时候可以采用上面介绍的拖放的方法。

### 我的需求 即更改citation key pattern
__具体步骤。__
而我们并不需要自己去定制这个pattern，伟大的better bibtex插件给我们提供了兼容老pattern（即standard Bib(La)TeX exporters of Zotero）的方法。
方法就是：
1. 将citation key format设为：`[zotero:clean]`, (注：位置在，首选项，better bibtex,citation keys中，设置citation key format)
2. 选择所有文献，右键refresh，然后在弹出的对话框中选择对所有适用（大概这个意思，记不清楚啦）。

大功告成。

## 调教Better BibTeX 插件生成的bib文件的field
针对 `gbt-7714-2015-author-year.bst` 或 `gbt-7714-2015-numerical.bst` 的需求，我们导出文献库的时候应选择 `Better bibtex`, 而非`Better biblatex`。

并且，需要加入 `lang` 域。
并将原`language` 域删除。

如果有中文参考文献的话, 需要手动加入pinyin 域，从而满足`gbt-7714-2015-author-year.bst`的排序需求。

对于zotero而言，可以定制生成的bib文件的field（域），在，首选项，better bibtex， advanced， postscript中，写入：
```javascript
if (Translator.BetterBibTeX && this.has.title) {
  this.add({name: 'lang', replace: true, value:item.title.match(/[\u4E00-\u9FA5]/) ? 'zh' : 'en'})
  delete this.has['language']
}
```
即可。
`记得刷新哈，选择所有文献（方法是点击我的文库，ctral+a)，邮件选择文献，refresh bibtexkey`
>要想看懂以上脚本，请看[这里](https://retorque.re/zotero-better-bibtex/scripting/)，需要懂一点点的javascript,我反正没学过javascript，边搜边学，哈哈。

我建议针对中文文献单独维持一个bib文件，对其手动加入pinyin 域，毕竟我引的中文文献很少。
在主文件中设置倆bib文件就行了，如： `\bibliography{总的文献库的位置,中文文献库的位置}`。