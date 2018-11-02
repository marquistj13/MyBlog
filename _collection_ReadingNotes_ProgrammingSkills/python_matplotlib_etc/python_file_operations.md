---
title:  Python 文件操作（换行符 、路径等）
---


* content
{:toc}


### 不同系统换行符的处理
Unix、MacOS、以及 Windows 使用不同的字符来标记行末。

有了[PEP 278: Universal Newline Support](https://docs.python.org/2.3/whatsnew/node7.html) ，就可以在open的时候加入 ` 'U' or 'rU' ` 选项，这样就将读取后的文件中的换行符统一变成 `\n` 了。