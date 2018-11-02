---
title:  yield
---


* content
{:toc}


以下来自 [What does the “yield” keyword do?](https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do)

### 啥时候用 yield
当你知道这个函数需要返回一大堆值，但你每次只需要读一次的时候，就可以在这个函数里使用yield。
这样就会更加memory efficient and faster。
>it's handy when you know your function will return a huge set of values that you will only need to read once.

### 解释 1
一般是写一个function，里边有 `yield`。
`yield` 关键字的用法和`return` 差不多，只不过返回的是生成器`generator`。

我们调用该函数的时候，该函数体并未执行，而是返回来一个 `generator` 对象。

那么函数体啥时候执行呢？
当我们的 `for` 使用 `generator` 对象的时候！

每次`for` 调用 `generator` 对象的时候，函数体就会执行，直到遇到`yield`，此时就会返回第一个循环值.

什么是`generator`:
```py
>>> mygenerator = (x*x for x in range(3))
>>> for i in mygenerator:
...    print(i)
0
1
4
```
这个东西用了一次就没了，因此不能再一次运行 `for i in mygenerator` 了。


### 解释 2 
如何去简单地理解使用`yield`的函数呢？
可以这么理解：
1. 在函数开始的地方插入一个list，即 `result = []`
1. 将每一个`yield`表达式替换为 `result.append(expr)`
1. 在函数底部插入：`return result`
1. 这样就没有`yield`啦，就好理解啦。


