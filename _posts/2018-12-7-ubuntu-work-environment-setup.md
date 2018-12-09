---
layout: post
title:  ubuntu18.04 我的常用软件环境安装
categories:  [系统环境]
tag: [日常琐事]
---

* content
{:toc}

##  安装 显卡驱动
笔记本自带了 1050 的显卡。
打开搜索框，搜索 Additional Drivers，根据这个窗口，选择 使用  Nvidia binary driver，确定就行了。

在我的 18.04刚安装好的时候，无法正常关机，只能按电源键强行关机，为啥呢？
因为没装显卡驱动。
搜索 `software & updates`，切换到 `Additional Drivers`，装上驱动，重启电脑，就行了。

## vpn
按照，[在ubuntu16.04 上的 openvpn 折腾笔记  以及 ubuntu18.04 dns 设置]({{ site.baseurl }}{% link _posts/2018-12-4-ubuntu16.04-ubuntu18.04-installopenvpn.md %})，装好openvpn就行了。

## chrome
有了vpn，就可以直接下载chrome啦。

## Zotero
### 安装并固定到侧边栏
下载好之后，根据[Installation Help](https://www.zotero.org/support/installation)进行安装，
实际上只需要解压即可，官方建议将其解压到 `/opt/zotero` 目录，可以先解压，再移动过去，或者直接解压过去：
`tar jxvf 文件名 -C /opt`。

zotero官方提供了 `set_launcher_icon` 脚本，用来生成 `zotero.desktop` 文件，它负责在侧边栏放置一个启动项。
生成之后，生成该文件在 `~/.local/share/applications/` 的一个软链接，如 `ln -s /opt/zotero/zotero.desktop ~/.local/share/applications/zotero.desktop`，此时仍然没有出现在侧边栏。

此时运行 zotero 命令即可打开Zotero的窗口，在 16.04 里，zotero打开之后，在侧边栏里可以点击右键固定在launcher上，只是可能没法显示正确的图标，此时只需要将执行固定操作后生成的`.desktop`文件修改，将其`Icon`值设为我么生成的`zotero.desktop`中的`Icon`值即可。
而在18.04里没有这个选项了，即没法直接右键，加入favourite了，怎么办？
重启电脑，打开zotero，此时就可以右键加入favourite了，而且图标也是正确的。
### 同步设置
登录zotero账号，由于zotero本身提供的存储空间太小，因此我们仅用其存储比较小的索引，即文献的名称。
而附件和全文都由支持webdav的云（如国内的坚果云）进行存储。

因此就需要取消掉 Data Syncing 的同步全文选项。
在File Syncing里也应取消掉syn attachment files..using zotero storage.

## ubuntu 自带的截图软件，并设置截图快捷键。
搜索screenshot，就打开了截图界面，但每次都对着截图界面很不爽，因此要设置快捷键。
### 找到截图命令
google以下，找到了 [ubuntu自带截图工具--方便好用](https://blog.csdn.net/qq_38880380/article/details/78233687)。

发现screenshot的命令叫做 `gnome-screenshot`，也就是可以在命令行运行。
在命令行运行 `gnome-screenshot -h`，可以看到使用说明，`-a` 代表我们要截取一个自定义的矩形区域，`-c` 代表直接存到剪切板，因此我们的最终命令是：
`gnome-screenshot -a -c`
### 如何设置快捷键
打开`system settings---->keyboard----->keyboard shortcuts`，大概就是这个位置吧，这个地方保存了很多快捷键。
我的是18.04，拉到最下面，有个加号，点击加号就能设置Custom Shortcuts了
`Name`随便设，`Command`设为`gnome-screenshot -a -c`，Shortcut，根据自己的习惯设置就行了。

### 打脸啦
我突然发现Keyboard 页面的快捷键列表里本来就有截屏的快捷键。
截取一个area到剪切板的默认快捷键为： `Ctrl+Shift+PrtScr`。
截取area并保存到图像文件的快捷键为：`Shift+PrtScr`,它会默认保存到你的 home 的 Pictures 文件夹
不要自己设置快捷键啦！

## 安装汉语支持和输入法
### 基本安装
搜索language support,点击 `Install /Remove Languages`，找到 chinese (simplified)，安装就行了。

此时，我的18.04 的右上角并没有出现输入法的切换选项。
怎么办呢？
打开Settings，Region & Language，在 Input Sources中点击加号，选择Chinese,然后在里边找到一个输入法就行了，我选的是智能拼音，然后电脑右上角就有输入法显示的图标啦。

此时就可以用汉语输入法啦。

### 将ibus替换为fcitx
有人说自带的ibus框架比较难用，所以要换一下。
`sudo apt-get install fcitx`
重启电脑，在language support的keyboard input method system那里选择fcitx即可。

### 安装搜狗输入法
自带的话，还得培养词库。
可以装一下搜狗啊。
去搜狗官网下载`.deb`，文件，然后：
`sudo apt-get install -f ./sougoupinyin后面一长串文件名哈哈`
安装成功后。
重启电脑。

就会发现电脑右上角有一个键盘图标，点击，选择 Configure Current Input Method，点击加号，然后取消勾选"Only show current language"，在下方搜索框输入pinyin，就能找到'Sougou Pinyin'啦，选择它，然后将其拖到原来的"keyboard-English(US)"之前，就搞定了。

此时，虽然可以使用搜狗输入中文，但很可能没法切换成英文，点击电脑右上角的键盘符号，选择Restart，过一会儿就行了。

## 交换 `Ctrl` 和 `Caps`
习惯了 Emacs 的快捷键以后，为了保护手指，需要将 `Ctrl` 和 不常用的 大小写转换按键`Caps`进行交换。

Emacs贴心地给出了各个系统上的交换教程：[MovingTheCtrlKey](https://www.emacswiki.org/emacs/MovingTheCtrlKey)

首先搜索安装 `Gnome tweaks`,安装好之后，可以搜索到，它的名变成了 Tweaks，差不多吧。
现在的版本和上面链接给出的不太一样了，不过功能一样。
找到 `Keyboard & Mouse`,然后 点击 `Additional Layout Options`，找到 `Ctrl position`，选择 `Swap Ctrl and Cas Lock`，搞定。

注：`sxhkd` 配合 `xte` 命令也能实现更换键位（或定义快捷键）的效果，但我折腾了半天实现不了键位的更换。
## gitkraken
git 的一个gui
这个在software center有，直接搜索安装即可。

## jekyll
按照 [Jekyll on Ubuntu](https://jekyllrb.com/docs/installation/ubuntu/) 的安装说明就能安装 Jekyll 了。

由于我的博客目录[MyBlog](https://github.com/marquistj13/MyBlog)已经有了一个`Gemfile`:
```ruby
source 'https://rubygems.org'
#gem 'github-pages', group: :jekyll_plugins
# gem 'jekyll-feed'
gem 'jekyll-paginate'
gem 'jekyll-sitemap'
gem 'jemoji'
```
因此需要去其目录安装这些"依赖"：`bundle install`
然后就可以运行`jekyll serve`了。

我的特殊配置：
在`MyBlog`目录（也就是我的博客的根目录）的同级目录，放置一个名为`run_myblog`的脚本：
```
cd MyBlog
cd _config_with_python
python buildMenu.py
cd ../
jekyll serve --port 4000 --incremental
```
不过鉴于我的博客依赖Python进行目录的生成，并使用`yaml` 和 `jinjia2`，因此可能还需要安装一下：
```
sudo apt install python-yaml
sudo apt install python-jinja2
```

## vscode
### vscode
可以利用系统的software center 搜索安装 vscode。
### 安装icon插件，让icon更漂亮
然后在vscode 中安装一个插件`vscode-icons`
### markdown 预览
vscode自带了markdown的预览，使用快捷键：`Ctrl+K V` 即可调出预览窗口，并且可以滚动同步，很良心！
### markdown 主题和快捷键
按照 [官方介绍Markdown and Visual Studio Code](https://code.visualstudio.com/docs/languages/markdown)，我又安装了：
`Markdown Shortcuts`  `Markdown TOC` `Markdown Theme Kit`

其中，`Markdown Shortcuts` 定义了很多快捷键，不过我熟悉的设置heading的并没有绑定，可用的方法是，使用 `ctrl +m ctrl m`调出快捷键窗口，然后点击就行了