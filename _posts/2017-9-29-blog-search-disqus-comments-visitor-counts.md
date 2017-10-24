---
layout: post
title:  jekyll博客加入谷歌站内搜索 disqus 评论 以及访问计数 谷歌站长统计
categories: 个人笔记
tag: [心情]
---

* content
{:toc}

## disqus
disqus评论系统很容易加，我五月份加的，只记得按照disqus的官方说明做就行了。
我现在搜了一下，在 [这里](https://disqus.com/admin/install/platforms/jekyll/)就有说明。 我记得如果新注册disqus的时候会有向导，按照guide就会有对应的可供粘贴的代码。
更改详见[这个commit](https://github.com/marquistj13/MyBlog/commit/efcb98a44de42a20c4436b8ce2a9de628eac6193)

## 访问计数
也是五月份加的，用的是busuanzi， [官网的教程](http://busuanzi.ibruce.info/)很简单，就两行代码。
更改详见[这个commit](https://github.com/marquistj13/MyBlog/commit/5c80d9a6b9d1ae2f18a85d352bd633b2aaaaeb49)

## 谷歌站内搜索
搜索“add google search in your website jekyll”
按照官方教程[Create a search engine](https://support.google.com/customsearch/answer/2630963)进行设置，得到一段代码（注：和上面两个一样，这个代码也是定制得来的，因此应该用自己的谷歌账号设置）， 定制完之后，还可以通过 [此页面](https://cse.google.com/cse/all)进行修改，如增加网站，搜索语言等。

官方给出了粘贴示意：
```html
<html>
<head>
<title>my site</title>
...
<head>
<body>
<div1>...</div1>
将代码粘贴在此处
<div2>...</div2>
</body>
</html>
```
即，要在body之间。
我仔细研究了我的博客模板，发现header就在body中，所以加到header中就行了，无奈技术不行，这个搜索框太大，太高，老是变成两行。只好将其放到header下面，content的上面，由于 `_layouts` 目录的page和post都是由default得到的，因此直接改default就行了。

详细更改见[这个commit](https://github.com/marquistj13/MyBlog/commit/223c7fc6dfff2aabff21bef3fa2b4eede8cf3a26)

很丑，没办法。

我看别人（如 [任平生笔记站内搜索](http://note.rpsh.net/search/)）是通过加入一个搜索页面来实现的，也就是没有嵌入到所有网页中。

好了，就这么搞吧，在header加个搜索按钮，然后跳出一个搜索页面。

另外，我发现这个搜索结果是根据google索引的结果来的，即新的博客文件可能搜索不到，因此需要建立sitemap，还好，github pages支持jekyll-sitemap这个控件，对于咱们的博客模板来说，在 `"_config_with_python\template_config.yml`中修改如下：
`plugins: [jekyll-paginate, jekyll-sitemap]`,即加入jekyll-sitemap，如果需要在本地运行Jekyll预览的话，还需要在本地安装jekyll-sitemap，即
`gem  install jekyll-sitemap`
(注，以上sitemap的安装参考自[这个博客](http://ju.outofmemory.cn/entry/124653)以及[Sitemaps for GitHub Pages](https://help.github.com/articles/sitemaps-for-github-pages/))

## 谷歌站长工具
需要在google 站长工具的Search Console中验证网站所有权，即下载一个HTML的验证文件，上传到网站根目录即可。