---
layout: post
title:  python decorator
categories: 编程
tag: [Python]
---

* content
{:toc}


python 的 decorator 很强大，今天趁机学一下。
记录一下几个重要的资料


在 [how-to-make-a-chain-of-function-decorators](https://stackoverflow.com/questions/739654/how-to-make-a-chain-of-function-decorators) 页面，有一个三千赞的答案，我看完了，有点啰嗦，不过还算能理解。 真正对我有用的还是另外一个答案，即就是将
```python
@decorator
def func():
    ...
```

展开成
```python
def func():
    ...
func = decorator(func)
```


另一个中文博客 [Python中的装饰器decorator](http://www.cnblogs.com/Jerry-Chou/archive/2012/05/23/python-decorator-explain.html) 讲的也很详细，可做快速回忆之用。


另一个英文博客 [A guide to Python's function decorators](https://www.thecodeship.com/patterns/guide-to-python-function-decorators/)也不错。