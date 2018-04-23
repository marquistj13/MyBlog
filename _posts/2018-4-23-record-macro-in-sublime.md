---
layout: post
title:  sublime的markdown环境设置 录制宏 并绑定快捷键
categories: [编辑器等文档工具]
tag: [sublime]
---

* content
{:toc}

## color scheme
`Preferernces -> color scheme` 然后选择 Monokai, 这个就是非常赏心悦目的屎黄色。

## 设置MarkdownEditing的宽度和主题色
*主题色*
主题色貌似还可以单独设定，这里不管了。
*风格*
默认的MarkdownEditing风格是GitHub flavored Markdown， 可以通过`View > Syntax > Open all with current extension as`来设定其他分割。
*宽度*
默认的markdown的界面特别窄，可以通过，`Preferernces -> Package setting > Markdown Editing > markdown gfm settings user`,写入
```
{
    "color_scheme": "Packages/MarkdownEditing/MarkdownEditor-Yellow.tmTheme",
    "wrap_width": 160
}
```
请忽略这里的color scheme.

## 录制宏 并绑定快捷键
在用markdown记笔记的时候，经常需要插入代码环境，
每次都要输入三个符号，然后指定cpp，有点麻烦，所以要录制宏啊，在`tools > record macro`， 或使用快捷键 `ctrl x )`，录制完以后，可以直接用 `ctrl x e`执行刚刚录制的宏。

也可以`tools > save macro`,将其保存下来，假设指定其文件名为cpp(.后面的不用管啦),就可以为其绑定快捷键。
按照[How do I assign a keyboard shortcut to recorded macro in Sublime Text](https://superuser.com/questions/609057/how-do-i-assign-a-keyboard-shortcut-to-recorded-macro-in-sublime-text)的指示，打开 `Preferences → Key Bindings - User`,写入：
```
[
    { "keys": ["ctrl+t"], "command": "run_macro_file", "args": {"file": "Packages/User/cpp.sublime-macro"} }
]
```
即可使用快捷键"ctrl+t"打开刚才录制的宏啦。