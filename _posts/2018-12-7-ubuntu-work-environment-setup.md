---
layout: post
title:  ubuntu18.04 以及 16.04 我的常用软件环境安装
categories:  [系统环境]
tag: [日常琐事]
---

* content
{:toc}

##  安装 显卡驱动
笔记本自带了 1050 的显卡。
打开搜索框，搜索 Additional Drivers，根据这个窗口，选择 使用  Nvidia binary
(注意，先`sudo apt-get update`,要不然会找不到驱动)

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
但实际经验告诉我，放在`/opt/zotero` 目录会遇到更新时的目录权限问题，因此，我将其放在我的home目录，并将该命令命名为Zotero
因此上述解压命令为：`tar jxvf 文件名 -C ~/Zotero`。

此时直接运行 zotero，就行了，然后邮件图标，固定到launcher就行了

如果没法正确显式到launcher，就按照如下步骤：
>
1. zotero官方提供了 `set_launcher_icon` 脚本，用来生成 `zotero.desktop` 文件，它负责在侧边栏放置一个启动项。
生成之后，生成该文件在 `~/.local/share/applications/` 的一个软链接，如 `ln -s ~/Zotero/zotero.desktop ~/.local/share/applications/zotero.desktop`，此时仍然没有出现在侧边栏。
2. 此时运行 zotero 命令即可打开Zotero的窗口，在 16.04 里，zotero打开之后，在侧边栏里可以点击右键固定在launcher上，只是可能没法显示正确的图标，此时只需要将执行固定操作后生成的`.desktop`文件修改，将其`Icon`值设为我么生成的`zotero.desktop`中的`Icon`值即可。
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
### 基本安装(这个就是使用自带的输入法啦，如果使用搜狗，就不需要这一步)
搜索language support,点击 `Install /Remove Languages`，找到 chinese (simplified)，安装就行了。

此时，我的18.04 的右上角并没有出现输入法的切换选项。
怎么办呢？
打开Settings，Region & Language，在 Input Sources中点击加号，选择Chinese,然后在里边找到一个输入法就行了，我选的是智能拼音，然后电脑右上角就有输入法显示的图标啦。

此时就可以用汉语输入法啦。

### 将ibus替换为fcitx（搜狗需要这一步）
有人说自带的ibus框架比较难用，所以要换一下。
`sudo apt-get install fcitx`
重启电脑（貌似不重启也行），在language support的keyboard input method system那里选择fcitx即可。

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

### 方法1，使用图形界面（不推荐）
首先搜索安装 `Gnome tweaks`,安装好之后，可以搜索到，它的名变成了 Tweaks，差不多吧。
现在的版本和上面链接给出的不太一样了，不过功能一样。
找到 `Keyboard & Mouse`,然后 点击 `Additional Layout Options`，找到 `Ctrl position`，选择 `Swap Ctrl and Cas Lock`，搞定。
>注：在18.04上没问题，但在我的16.04上就有问题，第一个就是安装问题，得用命令行安装，好像是`sudo apt install genome-tweak-tool`，第二个问题是重启以后可能失效。

### 方法2，使用配置文件（推荐）
建立 `~/.xmodmap` 文件，写入：
```
!
! Swap Caps_Lock and Control_L
!
remove Lock = Caps_Lock
remove Control = Control_L
keysym Control_L = Caps_Lock
keysym Caps_Lock = Control_L
add Lock = Caps_Lock
add Control = Control_L
```
然后 `xmodmap ~/.xmodmap`。

重启以后也会失效，因此我们需要登陆之后手动运行这个命令。

能不能开机启动这个命令呢？
但我尝试了很多方法都不行，例如
1. 搜索`startup applications`，然后加入上述命令 `xmodmap ~/.xmodmap` 。
2. 使用`crontab`，建立一个文件，例如 `~/.marquis_cron`，写入：
`@reboot /usr/bin/xmodmap ~/.xmodmap`
3. 我也试了各种启动脚本，如`.profile`，都不行，尝试加入`sleep 4`也不行。

这个答案[Permanent xmodmap in Ubuntu 13.04](https://askubuntu.com/questions/325272/permanent-xmodmap-in-ubuntu-13-04/514277#514277) 搞了一个Python脚本来实现这个功能，我心想应该不需要这么麻烦吧，先不试啦。

__最终的解决方案：__
将 `~/.xmodmap` 更名为 `~/.Xmodmap`
它就会自动配置啦。

借鉴自：[Activating the .Xmodmap at startup](https://cweiske.de/howto/xmodmap/ar01s06.html)
```
Some distributions automatically load the ~/.Xmodmap when a user logs on in X - if yours does, consider yourself happy. One of the distris which doesn't do it is Gentoo, while SuSE does.

Here is how you get it loaded automatically: You've got to open

$KDEDIR/share/config/kdm/Xsession
and insert the following code at the beginning of the file (but after the shebang #!/bin/sh):

if [ -f $HOME/.Xmodmap ]; then
    /usr/bin/xmodmap $HOME/.Xmodmap
fi
Now save, logout and log in again. Your modmap should have been loaded now.

Using a global Xmodmap file
Xorg (at least in version 7.0) has an xinit script at /etc/X11/xinit/xinitrc that loads a global Xmodmap file for all users. The default location is /etc/X11/Xmodmap. Since KDE doesn't automatically do this, you should add it: Open the Xsession file (as described above) and add the following line:

[ -f /etc/X11/Xmodmap ] && xmodmap /etc/X11/Xmodmap
```

### 方法3，没搞成功
`sxhkd` 配合 `xte` 命令也能实现更换键位（或定义快捷键）的效果，但我折腾了半天实现不了键位的更换。

## gitkraken
git 的一个gui
直接下载安装即可。

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
>注，这一步可能会出现关于Nokogiri的错误，
按照[这里](https://stackoverflow.com/questions/47038472/nokogiri-v-1-8-1-issue-when-running-bundle-install)的步骤就行了：
`sudo apt install libxml2-dev zlib1g-dev`

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
目测还是自己去官网下载安装更快。

### 安装icon插件，让icon更漂亮
然后在vscode 中安装一个插件`vscode-icons`
### markdown 预览
vscode自带了markdown的预览，使用快捷键：`Ctrl+K V` 即可调出预览窗口，并且可以滚动同步，很良心！
### markdown 主题和快捷键
按照 [官方介绍Markdown and Visual Studio Code](https://code.visualstudio.com/docs/languages/markdown)，我又安装了：
`Markdown Shortcuts`  `Markdown TOC` `Markdown Theme Kit`

其中，`Markdown Shortcuts` 定义了很多快捷键，不过我熟悉的设置heading的并没有绑定，可用的方法是，使用 `ctrl +m ctrl m`调出快捷键窗口，然后点击就行了

### Emacs 快捷键插件
`Emacs Friendly Keymap`

### tex 语法高亮插件
`LaTeX language support`

## TeXLive
主要参考自：[在 Ubuntu 中安装 TeX Live 2018](https://stone-zeng.github.io/fduthesis/2018-05-13-install-texlive-ubuntu/)

### 安装 perl
如果想用图形界面安装的话，就需要按照perl啦
`sudo apt-get install perl-tk perl-doc`

这样，以后的texlive命令后面只需要加上`-gui`就出来界面啦。

### 安装texlive
我是直接从[TUNA](https://mirrors.tuna.tsinghua.edu.cn/CTAN/systems/texlive/Images/)下载的光盘镜像 `texlive2018.iso`

然后挂载到一个目录：`sudo mount /home/hdd/texlive2018.iso /media/marquis/`

进入光盘目录：`/media/marquis/`

开始安装：`sudo ./install-tl` （当然，`sudo ./install-tl -gui` 就是带图形界面的安装啦）。

### 设置texlive 的环境变量
此时 TeX Live 虽已安装，但其路径对于 Linux 来说仍是不可识别的。所以需要更改环境变量。

打开 ~/.bashrc，在最后添加
```bash
export PATH=/usr/local/texlive/2018/bin/x86_64-linux:$PATH
export MANPATH=/usr/local/texlive/2018/texmf-dist/doc/man:$MANPATH
export INFOPATH=/usr/local/texlive/2018/texmf-dist/doc/info:$INFOPATH
```

还需保证开启 sudo 模式后路径仍然可用。命令行中执行
`sudo visudo`
找到如下一段代码
```bash
Defaults        env_reset
Defaults        mail_badpass
Defaults secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"
```
将第三行更改为
```bash
Defaults        secure_path="/usr/local/texlive/2018/bin/x86_64-linux:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"
```
也就是加入 TeX Live 的执行路径。如果在安装时作了修改，这里的路径也都要与安装时的保持一致。

### 更新参考文献宏包
由于我自己的模板使用了`biblatex-gb7714-2015`的最新版，因此需要将其更新。

先更新宏包管理器
`sudo tlmgr update --self`

然后使用命令：
`sudo tlmgr update biblatex-gb7714-2015`
更新参考文献的宏包。

当然，也可以 `sudo tlmgr -gui`使用图形界面的形式进行更新。