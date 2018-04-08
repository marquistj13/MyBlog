---
title:  强制类型转换
date:   2018-4-8
---


* content
{:toc}


##  msdn的解释
[强制转换运算符](https://msdn.microsoft.com/zh-cn/library/5f6c9f8h.aspx)
`dynamic_cast` 用于多态类型的转换。

`static_cast` 用于非多态类型的转换。

`const_cast` 用于删除 `const、volatile` 和 `__unaligned` 特性。

`reinterpret_cast` 用于位的简单重新解释。

### [dynamic_cast 运算符](https://msdn.microsoft.com/zh-cn/library/cby9kycs.aspx)
语法:  
`dynamic_cast < type-id > ( expression )`

dynamic_cast 只适用于指针或引用，而且运行时类型检查也是一项开销.
即 `type-id` 必须是指针或引用，或是`void*`

### [static_cast 运算符](https://msdn.microsoft.com/zh-cn/library/c36yw7x9.aspx)
运算符可用于将指向基类的指针转换为指向派生类的指针等操作。 此类转换并非始终安全。
### [const_cast 运算符](https://msdn.microsoft.com/zh-cn/library/bz6at95h.aspx)
从类中移除 `const、volatile` 和 `__unaligned` 特性.

### [reinterpret_cast 运算符](https://msdn.microsoft.com/zh-cn/library/e0w9f63b.aspx)
