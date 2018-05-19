---
layout: post
title:  win10 的 ctrl space 快捷键
categories: [编辑器等文档工具]
tag: [emacs]
---

* content
{:toc}

Emacs中频繁使用 `ctrl space` 用来mark，但这个键被傻逼windows强占为切换至中文输入法的键，不可理喻。
只得使用 `ctrl @` 代替了，但这个键又很难按。

有没有办法将 `ctrl space`改掉呢？
在[CTRL-Space always toggles Chinese IME (Windows 7)](https://superuser.com/questions/327479/ctrl-space-always-toggles-chinese-ime-windows-7)中，
找到了答案：
运行 `regedit`,找到 `HKEY_CURRENT_USER/Control Panel/Input Method/Hot Keys`,对于简体输入法，对`00000010`进行操作，而繁体输入法需要修改`00000070`。
嗯，我只需要修改`00000010`就行了。

找到右边的Key Modifiers `02c00000`,将`02` 修改为`00`
找到右边的Virtual Key `20000000`,将`20`修改为 `FF`

重启电脑，搞定。

__update__: 完了，第二天就失效了，这个方法不行啊，流氓windows！
