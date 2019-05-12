---
layout: post
title:  重装系统：软件安装过程记录
categories: 系统环境
tag: [日常琐事]
---


* content
{:toc}

2.23早上实在受不了已经充满了各种病毒的系统，中午吃完饭就重装了一个cn_windows_10_multiple_editions_version_1607_updated_jul_2016_x64_dvd_9056935 ,用的老王的秘钥，装好之后发现是professional的，哈哈，折腾了一天，终于将好多基本软件配置完毕了。

##  zotero
需要安装 Zotero Better bittex 插件，然后选择 文件-导出文献库，保存好之后这个bib文件就能实时更新了。
另外关于同步文献的策略，我将索引文件放到zotero的服务器上，附件（pdf啦）放到坚果云。具体设置如图：
![]({{ '/blog_images/2017-02-24-record-my-system-software-reinstall/zotero_storage.png' | prepend: site.baseurl}})

## 截图
greenshot

## 压缩 解压缩
Bandizip

## LaTeX
__update 17.11.19:__ 
现在用texlive 2017了

__原安装：__
以前用的是CTEX_full,它的后台是miktex，我想自己装，哈哈，就单独下了个miktex最新版装了

在miktex的文档中，人家用的是 TeXworks编辑器，哈哈。
哦，原来miktex自带TeXworks编辑器
latexmk得自己下，用它的包管理器就行了。

我发现不能用latexmk，就自己装了，然后提示perl不存在，就装了一个strawberry perl。
原来的emacs配置还是无法调用latexm，一怒之下卸载miktex，装了ctex_full,但还是不能用，额，不想折腾了，就老老实实用pdflatex和xelatex吧

以后要直接写tex了，不用org了，毕竟太费时间了，emacs的auctex挺好用的。

注：不要过于折腾了，不要只顾着器而忘了道。



## AutoHotkey
用来将Caps键变成Ctrl键，而Caps只能由Win+Caps实现啦。
将以下两行写入一个.ahk文件
> \#Capslock::Capslock ; make Win+Caps-Lock the Caps Lock toggle
> Capslock::Control

然后将此文件放入 `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp` 开机启动即可。

## sublime text
搞了个sublime 3，还有这次我搜到好多license，哈哈，填了一个，能用。


## Markdown 编辑器
这次不用那个haroopad了，我看到sublime也有编辑markdown的插件：
https://github.com/SublimeText-Markdown/MarkdownEditing
按照说明装了之后很幸福啦。

这个插件很多快捷键特别好，谁用谁知道……

还装了一个markdown preview的包：omnimarkuppreviewer,按快捷键 <kbd>ctrl+alt+o</kbd> 就可以在浏览器预览了


## Python IDE
除了PyCharm，也可以用sublime的插件。
我用了 http://damnwidget.github.io/anaconda/ 的Anaconda 包，应该不错吧。
（注，我装MarkdownEditing的时候已经装了package control）。

## pdf阅读器
__update__:
六维有 Adobe Acrobat XI 的破解版，不想用福昕了
__原安装：__
福昕阅读器定制菜单以后发现右上角有一长条广告，解决方法：http://jingyan.baidu.com/article/ab0b56308e7bb3c15afa7d0b.html
以上链接可能有点老，我的新版本的阅读器是这样的，文件->偏好设置->常规，到这里就可以看按到广告条的设置了。


## GitHub 的UI
__update 17.11.19:__ 
刚装上github Windows
要是在cmd上运行git的话，估计还得安装Git for Windows
__原安装：__
它只能在线安装，而在线下载的速度太感人了，虽然有人提供自己下好的版本，不过都不是最新版
只好下了个GitKraken凑合一下吧，顺便尝试新事物。

## 猎鹰eagleget 替代迅雷
我看知乎上有人对他吹嘘，说是支持音视频的嗅探，我就用一下吧

## 视频播放器PotPlayer
是KMPlayer的原作者姜勇囍的新作品。
据说官网版的没有PotPlayer中文绿色版好，我就去http://www.potplayer.org 搞了个绿色版

算了，还是去官网下载吧……，不搞绿色版了

对了，有人说它可以播放迅雷的正在下载中的视频，哦算了，我反正不用迅雷了。

## ipv6设置
自从上学期学校网络改造以后，我就没法从容地获取v6地址了，重启是经常用的技能。
改造前，我可以不开有线网卡的v4协议，就能获取稳定的2001公网地址，改造以后，就必须同时打开有线网卡的v4和v6协议才能维持稳定可用的v6连接和地址了（目测，网络中心那边如果检测到你的v4没有勾上，就把你的v6连接断掉了）。
这么搞以后我就得必须用账号登陆才能享用v4了，就不能用无线连路由器了啊，我要是再登陆的话，可能会把其他人挤掉了。好痛苦。
不过我找到一种方法，现在还可以凑合哈哈。

好了先说如何获取v6地址
我现在发现可以用的设置为：无线网卡连接无线路由器，只勾选v4协议（我还没试过勾选v6协议的情况，试过了，勾上也可以），有线网卡的v4和v6协议都勾上。
如果获取不了，那就重启电脑吧！
弹出登陆窗口怎么办？就得设置两个网卡的优先级了。

下面就是设置的重点了。
如何让v4的数据包走无线网卡？这样咱就可以用路由器上v4啦嘛，同时有线网卡的v4连接也是活的，从而保证有线网卡的v6连接的稳定性？
上面提到了，只需要调整两个网卡的v4优先级就行了，方法就是，将两个网卡v4协议的自动跃点取消掉，详细设置：无线网卡的跃点数设为10，有线网卡的跃点数设为20，这样无线网卡的v4优先级就比有线网卡的优先级高，同时我们的有线网卡的v4也开着，两全其美啦。

update: 这种设置跃点数的方式也有不完美之处，过一个多小时就会断掉连接，哈哈。这时候虽然还是2001的公网地址，不过人家已经不给你传递数据包了。只有重启电脑才能解决。也就是说，一个多小时得重启一次电脑。

## Chrome
这个是重点，在家的时候chrome的google搜索就被一个ramber.ru的流氓给劫持了，这学期一开始更畅快，我重装了好多次都解决不了，后来删除所有关于google的数据，然后装上，卸载所有可疑的程序和extension，才解决，无奈2.23早上电脑上的病毒又强行装了六七个软件，又把我的浏览器劫持了。
一个教训：不要随便装各种extension了，不要随便浏览各种网站了。

我重装电脑后发现一个清爽的chrome的new tab本来就很好了，可惜我中病毒已久，好久没有看到这个界面了。

另外记一下谷歌默认的搜索引擎的设置。
> {google:baseURL}search?q=%s&{google:RLZ}{google:originalQueryForSuggestion}{google:assistedQueryStats}{google:searchFieldtrialParameter}{google:iOSSearchLanguage}{google:searchClient}{google:sourceId}{google:instantExtendedEnabledParameter}{google:contextualSearchVersion}ie={inputEncoding}

## 翻墙
设置好的xx-net还是有点慢，不过日常使用足够了，是不是google搜索会比较慢。

我装了学校里面的google证书，chrome基本满足学术搜索的需求了，所以日常是不需要使用xx-net来翻墙啦，只在Facebook和YouTube、中文维基的时候需要用。

最后，面对原生的v6，我还是知道如何选择滴。

## Jekyll
__update__：
_17.11.19更新：_ 
现在[官方](https://jekyllrb.com/docs/windows/#installation)给出了一个更简单的本地安装方法，使用[RubyInstaller](https://rubyinstaller.org/),不需要像以前先安装Chocolatey那么麻烦了。

安装好RubyInstaller之后，执行`gem install jekyll bundler`即可。
至于各种gem的安装，还是采用Gemfile的方式比较方便。

__update__：
_17.9.30更新：_ 安装好bundle之后，Jekyll相关的gem不需要一个个安装了，只需要在blog site的根目录建立一个名为Gemfile的纯文本即可，github官方出了个本地预览的介绍，即 [Setting up your GitHub Pages site locally with Jekyll
](https://help.github.com/articles/setting-up-your-github-pages-site-locally-with-jekyll/#keeping-your-site-up-to-date-with-the-github-pages-gem),按照这个页面的介绍，再加上我的插件需求，暂定Gemfile内容如下：
```
source 'https://rubygems.org'
gem 'github-pages', group: :jekyll_plugins
gem 'jekyll-feed'
gem 'jekyll-paginate'
gem 'jekyll-sitemap'
gem 'jemoji'
```
然后，直接 `bundle install` 就行了，以后更新的话，直接 `bundle update`, 当然执行这些命令的时候一定要cd到本目录，要不然会提示找不到gem文件。
另外，由于各种版本问题，上面的 `jekyll serve --port 3000 -b ""` 可能会运行不了了，根据 [这个页面](https://github.com/jekyll/jekyll/issues/3084) 的介绍，这时候就得改为 `bundle exec jekyll serve --port 3000 -b ""`

另外，本地运行脚本的配置详见：[如何使用本模板实现note-taking的purpose]({{ site.baseurl }}{% post_url 2017-01-26-how-to-use-this-blog-template-to-take-notes %}
)
__注意:__ 如果使用了'jekyll-feed'插件，那么必须在_configure中指定一个title，要不然会报错。此插件的使用详见：[Jekyll Feed plugin](https://github.com/jekyll/jekyll-feed)

__原安装方法：__
在Windows上安装比较麻烦，根据[官方](https://jekyllrb.com/docs/windows/#installation)的说明，重定向到[这个地方](https://davidburela.wordpress.com/2015/11/28/easily-install-jekyll-on-windows-with-3-command-prompt-entries-and-chocolatey/),先安装[Chocolatey](https://chocolatey.org/install),
[这个地方](https://davidburela.wordpress.com/2015/11/28/easily-install-jekyll-on-windows-with-3-command-prompt-entries-and-chocolatey/)的安装方法是：
`@powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1 && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"`

我一开始没有看见这个方法，而是按照[Chocolatey](https://chocolatey.org/install)的提示装的，步骤为：
1. 用管理员权限运行PowerShel
2. 先允许运行脚本，在[这里](https://technet.microsoft.com/zh-CN/library/hh847748.aspx)有很多允许的方式，我选用这个：
` Set-ExecutionPolicy -ExecutionPolicy RemoteSigned`
3. 然后`iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex`
4. 重设为原状态：` Set-ExecutionPolicy -ExecutionPolicy RESTRICTED`

恩走了弯路，以后长点心。

然后Install Ruby：`choco install ruby -y`
后边按照教程来就是了，不记录了。
值得注意的事，后边的东西不需要用管理员权限去运行PowerShel了。

算了，再啰嗦一下，安装`gem install bundler`的时候,会有SSL问题， 按照 http://guides.rubygems.org/ssl-certificate-update/ 来一遍就行了，然后打开PowerShel，安装：`gem install bundler ` 和 `gem install jekyll` 就行了。
（注，Jekyll不需要单独安装，本段以下的安装可先跳过，详见以下update）

亮出来我的bat脚本：
```
@echo on 
cd C:\Users\houpe\Documents\Local_GitKraken\MyBlog\_config_with_python
python buildMenu.py

cd ..\
jekyll serve -b ""
```

啊,提示需要按照paginate，用`gem install paginate`

啊，提示permission不够，无法运行server，我搜了一下，在 [这个哥们博客（他的主题很不错，以后可以参考一下](https://gaohaoyang.github.io/2016/03/12/jekyll-theme-version-2.0/),提到是被Foxit pdf reader 占用4000端口，我在任务管理器的详细信息一栏将其关掉即可。
人家给的解决方案更好：`jekyll serve --port 3000`
所以啊，就变成了：
```
@echo on 
cd C:\Users\houpe\Documents\Local_GitKraken\MyBlog\_config_with_python
python buildMenu.py

cd ..\
jekyll serve --port 3000 -b ""
```




## 电子阅读器转换软件
在 [Reading arXiv preprints on an e-reader?](https://www.reddit.com/r/MachineLearning/comments/5xtnl4/d_reading_arxiv_preprints_on_an_ereader/)提到了两个软件，一个是应用程序 [k2pdfopt](http://www.willus.com/k2pdfopt/),可以直接转换pdf，一个是Chrome扩展 [dontprint](http://dontprint.net/)

##  emacs
__update19.5.12:__
我现在用 spacemacs 了，在我的windows上的安装方法：
1. 先安装 [emacs](https://www.gnu.org/software/emacs/download.html#windows)
1. 打开 `cmd`, `cd` 进入 home目录的 `AppData\Roaming` 目录，然后运行 `git clone https://github.com/syl20bnr/spacemacs  .emacs.d` 

需要注意的是，由于spacemacs默认的字体我们没有安装，所以需要安装[adobe-fonts/source-code-pro](https://github.com/adobe-fonts/source-code-pro)字体，在我的 2k 屏上，得把size设为 20 才感觉爽。
其余的配置就参考[我在Linux下的配置吧]({{ site.baseurl }}{% link _posts/2019-02-1-spacemacs-config.md %})
__update18.5.24:__
根据[emacs的company-mode让生活更美好]({{ site.baseurl }}{% post_url 2018-5-24-emacs-company-mode-connect-to-melpa %})的说明，[这里](https://github.com/m-parashar/emax64)有一个很完美的build，而且还是emacs26.1，自带gnutls和各种dll，完美啊。
__update17.11.19:__
我发现我以前的emacs安装都来自 [这个github](https://github.com/zklhp/emacs-w64/releases)， 里边有各种图片的dll，算是作者为windows优化好的，直接用就行了。
解压后，直接运行。然后在 `C:\Users\houpe\AppData\Roaming` 加入一个名为 `.emacs` 的文件，该文件调用d盘的详细配置文件，即调用`D:\emacs\etc\.emacs`, 设置完以上两个文件以后。由于还需要安装 [cnfonts 原来叫： chinese-fonts-setup](https://github.com/tumashu/cnfonts#org8dffa7c), 因此要先执行 `M-x package-install RET cnfonts RET`,这样就会将其安装到 `C:\Users\houpe\AppData\Roaming\.emacs.d` 目录，注意我们重新安装emacs的时候只需要`C:\Users\houpe\AppData\Roaming\.emacs` 和`D:\emacs\etc\.emacs` 就行了。
备份一下这俩文件：
###  `C:\Users\houpe\AppData\Roaming\.emacs`
{% raw  %}
```
;; Added by Package.el.  This must come before configurations of
;; installed packages.  Don't delete this line.  If you don't want it,
;; just comment it out by adding a semicolon to the start of the line.
;; You may delete these explanatory comments.
(package-initialize)

(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(TeX-source-correlate-method (quote synctex))
 '(TeX-source-correlate-mode t)
 '(TeX-source-correlate-start-server t)
 '(TeX-view-program-list
   (quote
    (("Sumatra PDF" "\"C:/Program Files/SumatraPDF/SumatraPDF.exe\" -reuse-instance %o"))))
 '(ac-ispell-fuzzy-limit 2)
 '(ac-ispell-requires 4)
 '(ansi-color-faces-vector
   [default default default italic underline success warning error])
 '(ansi-color-names-vector
   ["#242424" "#e5786d" "#95e454" "#cae682" "#8ac6f2" "#333366" "#ccaa8f" "#f6f3e8"])
 '(case-fold-search t)
 '(current-language-environment "UTF-8")
 '(custom-enabled-themes (quote (tango-dark)))
 '(inhibit-startup-screen t)
 '(initial-major-mode (quote text-mode))
 '(initial-scratch-message nil)
 '(longlines-show-hard-newlines t)
 '(longlines-wrap-follows-window-size t)
 '(org-export-backends (quote (ascii beamer html latex md)))
 '(org-file-apps
   (quote
    ((auto-mode . emacs)
     ("\\.mm\\'" . default)
     ("\\.x?html?\\'" . default)
     ("\\.pdf\\'" . "\"C:/Program Files/SumatraPDF/SumatraPDF.exe\" -reuse-instance %s"))))
 '(package-selected-packages (quote (company-auctex company auctex cnfonts)))
 '(reftex-plug-into-AUCTeX t)
 '(safe-local-variable-values (quote ((TeX-master . t))))
 '(temporary-file-directory "c:/tools/emacs_tmp")
 '(transient-mark-mode (quote identity)))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )
(load-file "D:/emacs/etc/.emacs")
```
{% endraw %}
###  `D:\emacs\etc\.emacs`
{% raw  %}
```

;;(require 'linum)  
;;(global-linum-mode t)  
;;显示列号    
;;(column-number-mode t)  
;;让Emacs 可以直接打开和显示图片
(setq auto-image-file-mode t)


;;Q：在org-mode中没有自动换行，实现方法参看Emacs org mode学习笔记A：修改配置文件SUBDIRS.EL或.emacs，加上一句即可
(add-hook 'org-mode-hook (lambda () (setq truncate-lines nil)))

;;加入TODO依赖
(setq org-enforce-todo-dependencies t)
;;对于TODO项，记录完成的时刻
;;(setq org-log-done 'time)

;;启动窗口最大化
(run-with-idle-timer 0.05 nil 'w32-send-sys-command 61488)

;;设置初始目录为emacs项目目录  

;;设置latex的默认pdf阅读器
;;来自http://tex.stackexchange.com/questions/52078/sumatrapdf-with-auctex-and-foxit-reader-as-the-default-viewer
(setq TeX-view-program-list
      '(("Sumatra PDF"
         "\"C:/Program Files/SumatraPDF/SumatraPDF.exe\" -reuse-instance %o")));;这个地方是%o还是%s待定

(setq TeX-view-program-selection
      '(((output-dvi style-pstricks) "dvips and start")
        (output-dvi "Yap")
        (output-pdf "Sumatra PDF")
        (output-html "start")))

;;reftex设置 来自官方文档
(require 'reftex)
;;http://blog.modelworks.ch/?p=379 and http://www.clarkdonley.com/blog/2014-10-26-org-mode-and-writing-papers-some-tips.html
(defun org-mode-reftex-setup ()
  (load-library "reftex")
  (and (buffer-file-name) (file-exists-p (buffer-file-name))
       (progn
     ;enable auto-revert-mode to update reftex when bibtex file changes on disk
     (global-auto-revert-mode t)
     (reftex-parse-all)
     ;add a custom reftex cite format to insert links
     ;(reftex-set-cite-format "[[papers:%l][%l]]: %t \n")
     ))
  (define-key org-mode-map (kbd "C-c )") 'reftex-citation)
)  
(add-hook 'org-mode-hook 'org-mode-reftex-setup) 
(add-hook 'org-mode-hook 'turn-on-reftex)

;;设置产生pdf的过程   这个是不行的
;;(setq org-latex-to-pdf-process
;; '("pdflatex %f" "biber %b" "pdflatex %f" "pdflatex %f"))
;;设置产生pdf的过程        这个是可以的
;;(setq org-latex-pdf-process
;;  '("latexmk -pdflatex='pdflatex -interaction nonstopmode' -pdf -bibtex -f %f" "latexmk -c"))
;;这个也可以 有时是不行的，还是不要用了！
;;(setq org-latex-pdf-process (list "latexmk -f -pdf %f" "latexmk -c"))
(setq org-latex-pdf-process
  '("latexmk -pdflatex='xelatex -interaction nonstopmode' -pdf -bibtex -f %f" "latexmk -c"))


;;移动，上下，即，将某一行上下移动 
;;来自http://stackoverflow.com/questions/2423834/move-line-region-up-and-down-in-emacs
(defun move-text-internal (arg)
  (cond
   ((and mark-active transient-mark-mode)
    (if (> (point) (mark))
        (exchange-point-and-mark))
    (let ((column (current-column))
          (text (delete-and-extract-region (point) (mark))))
      (forward-line arg)
      (move-to-column column t)
      (set-mark (point))
      (insert text)
      (exchange-point-and-mark)
      (setq deactivate-mark nil)))
   (t
    (let ((column (current-column)))
      (beginning-of-line)
      (when (or (> arg 0) (not (bobp)))
        (forward-line)
        (when (or (< arg 0) (not (eobp)))
          (transpose-lines arg)
          (when (and (eval-when-compile
                       '(and (>= emacs-major-version 24)
                             (>= emacs-minor-version 3)))
                     (< arg 0))
            (forward-line -1)))
        (forward-line -1))
      (move-to-column column t)))))
(defun move-text-down (arg)
  "Move region (transient-mark-mode active) or current line
  arg lines down."
  (interactive "*p")
  (move-text-internal arg))
(defun move-text-up (arg)
  "Move region (transient-mark-mode active) or current line
  arg lines up."
  (interactive "*p")
  (move-text-internal (- arg)))
(global-set-key [M-S-up] 'move-text-up)
(global-set-key [M-S-down] 'move-text-down)


;; 设置默认编码
(setq default-buffer-file-coding-system 'utf-8)

;; c-x c-f 的时候用上下箭头来选择历史文件。
;; from  http://stackoverflow.com/questions/3527150/open-recent-in-emacs
(savehist-mode 1)
 
;;设置auctex
;; auctex setup according to https://www.emacswiki.org/emacs/AUCTeX
(setq TeX-auto-save t)
(setq TeX-parse-self t)
(setq-default TeX-master nil)
(add-hook 'LaTeX-mode-hook 'visual-line-mode)
(add-hook 'LaTeX-mode-hook 'flyspell-mode)
(add-hook 'LaTeX-mode-hook 'LaTeX-math-mode)
(add-hook 'LaTeX-mode-hook 'turn-on-reftex)
(setq reftex-plug-into-AUCTeX t)
(setq TeX-PDF-mode t)
;; my add
(add-hook 'LaTeX-mode-hook 'outline-minor-mode)

;;设置必应词典的快捷键
;; https://github.com/cute-jumper/bing-dict.el
(global-set-key (kbd "C-c d") 'bing-dict-brief)

;;Inverse search with Emacs/AucTeX and SumatraPDF
;;https://tex.stackexchange.com/questions/286028/inverse-search-with-emacs-auctex-and-sumatrapdf-on-windows-10
(server-start)

;;设置：使用 company-mode in all buffers
;;来自：http://company-mode.github.io/
(add-hook 'after-init-hook 'global-company-mode)
```
{% endraw %}
__原始方法：__
由于我以前的emacs-bin-w64-24.5-1是免安装的，因此直接将其拷过来就行了，配置文件在roaming目录，也一并拷过来，以前安装的包还在，哈哈。
