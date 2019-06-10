---
layout: post
title:  ubuntu18.04 以及 16.04 我的常用软件环境安装
categories:  [系统环境]
tag: [日常琐事]
---

* content
{:toc}

## 换源
在教育网环境下tuna的源很快，可以按照 [Ubuntu 镜像使用帮助](https://mirror.tuna.tsinghua.edu.cn/help/ubuntu/) 换一下。

## 台式机 无线网卡不稳定
台式机的无线网卡是usb的外接网卡，型号是 `RTL8188EUS`，不过每次开机都要好久才能用，我同时用了两种方法来处理，现在是好了，不过不知道是哪一种起了作用。
1. 把它插到后面板的2.0接口上（原先在3.0上插着）。
1. 安装 [quickreflex/rtl8188eus](https://github.com/quickreflex/rtl8188eus) 的驱动。

## 18.04 老是弹出 `System Program Problem Detected` 对话框，很烦
怎么关掉呢？
运行 `sudo gedit /etc/default/apport`
然后将 `enabled=1` 改成 `enabled=0`。

##  安装 显卡驱动
笔记本自带了 1050 的显卡。
打开搜索框，搜索 Additional Drivers，根据这个窗口，选择 使用  Nvidia binary
(注意，先`sudo apt-get update`,要不然会找不到驱动)

在我的 18.04刚安装好的时候，无法正常关机，只能按电源键强行关机，为啥呢？
因为没装显卡驱动。
搜索 `software & updates`，切换到 `Additional Drivers`，装上驱动，重启电脑，就行了。

## vpn
### 基本配置
按照，[在ubuntu16.04 上的 openvpn 折腾笔记  以及 ubuntu18.04 dns 设置]({{ site.baseurl }}{% link _posts/2018-12-4-ubuntu16.04-ubuntu18.04-installopenvpn.md %})，装好openvpn就行了。

### 特殊配置
#### 安装 OpenVPN 2.4
使用 streisand 得到的配置文件必须得用 OpenVPN 2.4 的版本，而Ubuntu 16.04的仓库中只有2.3的（你装好之后使用 `openvpn --version`就能看到版本号啦。，因此得自己编译安装。
当然2.4的无法使用network manager的归，因此装好之后得使用 `sudo openvpn 配置文件名字`运行。
下面介绍OpenVPN 2.4 的安装。
首先下载[openvpn源码](https://github.com/OpenVPN/openvpn)。
按照`INSTALL`文件的指示：
```
autoreconf -i -v -f
./configure
make
sudo make install
```
进行编译安装。make的时候若提示缺库，可按照[Unable to install openvpn-2.3.6 on Ubuntu 14.04 LTS to work work with TUN/TAP](https://stackoverflow.com/questions/27729139/unable-to-install-openvpn-2-3-6-on-ubuntu-14-04-lts-to-work-work-with-tun-tap)运行：
`sudo apt-get install libssl-dev liblzo2-dev libpam0g-dev`。

>注意：最新版貌似很难 `autoreconf -i -v -f` 成功了，怎么办呢？ 只能去[openvpn官网](https://openvpn.net/index.php/download/community-downloads.html)(当然被墙啦)下载别人conf过的版本，里边自带了 `configure` 不需要我们通过`autoreconf -i -v -f` 来生成  `configure` 了。

#### 修改配置文件,由vpn server下发dns
OpenVPN 2.4 应该是增加了新的语法，因此可以不用在Ubuntu本机修改dns，而是由vpn server下发dns。
详细说明可参照  streisand  生成的说明文件，我把核心部分贴一下。
需要在`.ovpn`配置文件的头部加入：
```
script-security 2
up /etc/openvpn/update-resolv-conf
down /etc/openvpn/update-resolv-conf
```

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

就会发现电脑右上角有一个键盘图标，点击，选择 Configure Current Input Method，点击加号，然后取消勾选"Only show current language"，在下方搜索框输入pinyin，就能找到'Sougou Pinyin'啦，选择它，然后将其拖到原来的"keyboard-English(US)"之前，就搞定了。（由于经常需要用英文输入cmd，因此最好不要把中文放在前面）。

此时，虽然可以使用搜狗输入中文，但很可能没法切换成英文，点击电脑右上角的键盘符号，选择Restart，过一会儿就行了。

### 改掉输入法切换命令 `Ctrl+Space`
系统自带的的英文输入法和我们安装的搜狗之间的切换是`Ctrl+Space`，很明显不太好，对于 18.04而言，可以邮件右上角输入法图标，选择 `configure`, 然后是 `global configure`, 在 `hotkey->Trigger input method` 那里改成其他的，如 `ctrl+,` 就行了。

## 交换 `Ctrl` 和 `Caps`
习惯了 Emacs 的快捷键以后，为了保护手指，需要将 `Ctrl` 和 不常用的 大小写转换按键`Caps`进行交换。

Emacs贴心地给出了各个系统上的交换教程：[MovingTheCtrlKey](https://www.emacswiki.org/emacs/MovingTheCtrlKey)

### 方法1，使用图形界面（在18.04上推荐使用，在16.04上不推荐）
首先搜索安装 `Gnome tweaks`,安装好之后，可以搜索到，它的名变成了 Tweaks，差不多吧。
现在的版本和上面链接给出的不太一样了，不过功能一样。
找到 `Keyboard & Mouse`,然后 点击 `Additional Layout Options`，找到 `Ctrl position`，选择 `Swap Ctrl and Cas Lock`，搞定。
>注：在18.04上没问题，但在我的16.04上就有问题，第一个就是安装问题，得用命令行安装，好像是`sudo apt install genome-tweak-tool`，第二个问题是重启以后可能失效。

### 方法2，使用配置文件（在16.04上推荐使用，在18.04上不推荐）
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
不过这种方法在 18.04上就有问题.

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
或者：
```python
pip install PyYAML
pip install jinja2
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

## Mathpix 将图片转化为 LaTex 公式
[Convert images to LaTeX](https://mathpix.com/)
这个很好使啊，从此以后做笔记再也不用手动敲公式了！
快捷键： `Ctrl+Alt+M`。

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

## qtikz 在线预览tikz图片
### 基本安装并使用中文
在[KtikZ – Editor for the TikZ language](http://www.hackenberger.at/blog/ktikz-editor-for-the-tikz-language/) 下载 `QtikZ 0.10 binary package for Ubuntu Lucid`，
安装，然后修改默认的配置文件，即
`sudo gedit /usr/share/qtikz/templates/template_example.pgs`
修改为：
```tex
\documentclass[border=0pt]{standalone}
\usepackage{amsmath}
%\usepackage{mathptmx}
\usepackage{tikz}
\usetikzlibrary{calc,positioning,shadows.blur,fit,decorations.text,arrows,arrows.meta,
backgrounds,mindmap,trees,matrix,shapes}
\usepackage{pifont}
\renewcommand{\labelitemi}{\ding{112}}
\usepackage{xeCJK}
%\setCJKmainfont{SimSun}
%\usepackage{color}
\usepackage[active,xetex,tightpage]{preview}
\PreviewEnvironment[]{tikzpicture}
\PreviewEnvironment[]{pgfpicture}
\DeclareSymbolFont{symbolsb}{OMS}{cmsy}{m}{n}
\SetSymbolFont{symbolsb}{bold}{OMS}{cmsy}{b}{n}
\DeclareSymbolFontAlphabet{\mathcal}{symbolsb}
\begin{document}
<>
\end{document}
```
即可。然后在编辑区写入 `\begin{tikzpicture} \end{tikzpicture}` 就能使用中文啦。
当然还需要将编译命令设为xelatex，在settings->Configure QTikz的 PDFLatex那里选为xelatex的路径，
即`/usr/local/texlive/2018/bin/x86_64-linux/xelatex`。

### 添加自定义的style
例如我想用一个不在ctan中的库 [moeptikz](https://github.com/moepinet/moeptikz)，就可以将其style文件下载，然后放入模板文件所在的目录，即`/usr/share/qtikz/templates/`，
并在模板文件中加入
```tex
\usepackage[shading]{moeptikz}
\newcommand*{\nodelabel}[1]{{\scriptsize\bfseries\ttfamily #1}}
```
即可编译[moeptikz](https://github.com/moepinet/moeptikz)提供的示例图片啦。

## spacemacs
### Ubuntu 库里的emacs版本貌似是24，太低了装不了spacemacs
### 首先下载 emacs，并安装
从 [tuna](https://mirrors.tuna.tsinghua.edu.cn/gnu/emacs/)下载最新版，我下的是26.1.
解压。
安装步骤参考目录里的 `INSTALL` 文件即可。
运行 `./configure`，如果提示缺少库最好安装上，如提示我缺少 `xpm`
就可：`sudo apt install libxpm-dev`，
貌似还提示我装gnutils，装上即可。

然后`make`，根据`INSTALL` 文件的指示，先测试能否运行，`./src/emacs -Q` 貌似是这个命令哈，不记得了。
如果能运行，那就安装到系统中吧，`sudo make install`，然后就可以把安装文件删掉了。
### 安装 spacemacs
`git clone https://github.com/syl20bnr/spacemacs ~/.emacs.d`
然后打开emacs，就会自动安装很多东西。
### 使用搜狗输入法
我的系统默认语言是英语。
打开emacs，此时使用我设置好的快捷键`ctrl_,`无法切换到搜狗输入法，从系统右上角的图标切换到搜狗，仍然无法输入汉字。
参考：
1. http://www.voidcn.com/article/p-fzepkvdm-um.html
1. http://heartnheart.github.io/blog/2015/01/15/SogouIME_on_English_Ubuntu_14.04/
1. https://emacs-china.org/t/topic/974

有好几种解决方法：
1. 在命令行直接运行emacs：`LC_CTYPE='zh_CN.UTF-8' emacs`
1. 在 `.bashrc`中加入 `export LC_CTYPE=zh_CN.UTF-8` 然后运行 emacs
1. 编辑/etc/environment文件。`sudo gedit /etc/environment`，在后面加上，
`LC_CTYPE="zh_CN.utf8"`

这里我用的是第三中方法。
然后打开emacs，将emacs的图标固定到launcher即可。
此时就可以用搜狗啦。

注：
>如果用第二种方法，那么固定到launcher之后还是没法用。

### 如果上面的设置还是用不了搜狗输入法的话，那么就勉强用spacemacs 自带的 chinese layer 中的`pyim`吧。
根据[Chinese layer](http://spacemacs.org/layers/+intl/chinese/README.html)的说明，我们只需要在`dotspacemacs-configuration-layers`中加入`chinese`,然后在`dotspacemacs/user-config`中加入配置：
```lisp
(setq-default dotspacemacs-configuration-layers '((chinese :variables
chinese-enable-fcitx t)))  
(require 'pyim-basedict)
(pyim-basedict-enable)
```
注意：输入法的切换命令是：`C+\`。

## tmux
### 安装tmux
按照[官方说明](https://github.com/tmux/tmux) 安装就行了。

### 安装定制插件
按照[Oh My Tmux! 的说明](https://github.com/gpakosz/.tmux) 进行安装。
安装完重启shell就能用这个插件了，如果不行就重启电脑吧。

### 根据修改修改默认的prefix
由于我有时候需要在终端运行emacs，即 `emacs -nw`，而 不管是 `C-a` 还是 `C-b` 在 emacs 中都很常用，因此 tmux 默认的 prefix `C-a` 以及 Oh My Tmux 默认的 prefix `C-b` 需要改一下。

>注意：不改也是可以的，这时候根据[If I set key bind of C-b to c-a in tmux how can I move the cursor to the beginning of the line?](https://stackoverflow.com/questions/11557076/if-i-set-key-bind-of-c-b-to-c-a-in-tmux-how-can-i-move-the-cursor-to-the-beginni) 的说明，`C-b C-b` 就会把真正的 `C-b` 发给terminal，同理 `C-a C-a` 也是。

如果要改的话，根据[Oh My Tmux! 的说明](https://github.com/gpakosz/.tmux)，只需要修改文件 `~/.tmux.conf.local` 即可。
在该文件最下面的地方有一段配置：
```bash
# replace C-b by C-a instead of using both prefixes
# set -gu prefix2
# unbind C-a
# unbind C-b
# set -g prefix C-a
# bind C-a send-prefix
```

将这一段改成：
```bash
# set C-j as the only prefix
set -gu prefix2
unbind C-a
unbind C-b
set -g prefix C-j
bind C-j send-prefix
```
然后保存，重启电脑就行啦。

### 常用快捷键汇总
本节主要参考：
1. [Tmux 快捷键 & 速查表](https://gist.github.com/ryerh/14b7c24dfd623ef8edc7)
1. [Oh My Tmux! 的说明](https://github.com/gpakosz/.tmux)

窗口相关：
>
    c  创建新窗口
    w  列出所有窗口(然后就可以切换过去啦)   
    f  查找窗口(然后就可以切换过去啦)
    ,  重命名当前窗口
    &  关闭当前窗口
    `<prefix> C-h` 和 `<prefix> C-l` 用来快速切换（左右的）窗口，上面的 `w` 和 `f` 还得按导航键或输入数字进行切换。
    `<prefix> Tab` 切换至 last active window



pane相关：
>
`<prefix> - ` 垂直分割 pane
`<prefix> _ ` 水平分割pane
`<prefix> h, <prefix> j, <prefix> k and <prefix> l` 通过 Vim 的方式对pane进行导航
`<prefix> H, <prefix> J, <prefix> K, <prefix> L`  快速 resize panes
`<prefix> < and <prefix> >` 交换 panes
`<prefix> +` 将当前 pane 最大化，并将其放到一个新的 window
`<prefix> m` 开启或关闭鼠标模式
`x`  关闭pane




