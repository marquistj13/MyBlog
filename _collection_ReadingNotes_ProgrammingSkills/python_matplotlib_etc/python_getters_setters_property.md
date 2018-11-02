---
title:  property
---


* content
{:toc}


以下来自 [What's the pythonic way to use getters and setters?](https://stackoverflow.com/questions/2627002/whats-the-pythonic-way-to-use-getters-and-setters)

### 简要用法
```py
class C(object):
    def __init__(self):
        self._x = None

    @property
    def x(self):
        """I'm the 'x' property."""
        print("getter of x called")
        return self._x

    @x.setter
    def x(self, value):
        print("setter of x called")
        self._x = value

    @x.deleter
    def x(self):
        print("deleter of x called")
        del self._x


c = C()
c.x = 'foo'  # setter called
foo = c.x    # getter called
del c.x      # deleter called
```

### 其他解释
在 Python 中，不要使用"getters" and "setters"，而是要用属性，即attributes

这个东西的背后需求是什么？

假设用户已经这么用了：
```py
value = 'something'

obj.attribute = value  
value = obj.attribute
del obj.attribute
```
上面的用法就是很普通的啦，就是public 的属性啦。

假设我们现在突然需要改变 setting and getting，同时不需要改变用户代码，那么这个时候就可以使用 `property` decorator来实现啦：
```py
class Obj:
    """property demo"""
    #
    @property
    def attribute(self): # implements the get - this name is *the* name
        return self._attribute
    #
    @attribute.setter
    def attribute(self, value): # name must be the same
        self._attribute = value
    #
    @attribute.deleter
    def attribute(self): # again, name must be the same
        del self._attribute
```

此时，如下的老代码依然可用：

```py
obj = Obj()
obj.attribute = value  
the_value = obj.attribute
del obj.attribute
```
很显然，这么搞之后，我们就可以对class的普通属性施加更多的限制，例如进行 range check，因此具有更大的自由度。
例如：
```py
class Protective(object):
    def __init__(self, start_protected_value=0):
        self.protected_value = start_protected_value
    @property
    def protected_value(self):
        return self._protected_value
    @protected_value.setter
    def protected_value(self, value):
        if value != int(value):
            raise TypeError("protected_value must be an integer")
        if 0 <= value <= 100:
            self._protected_value = int(value)
        else:
            raise ValueError("protected_value must be " +
                             "between 0 and 100 inclusive")
    @protected_value.deleter
    def protected_value(self):
        raise AttributeError("do not delete, protected_value can be set to 0")
```

### 结论
一开始用简单的属性就行了，假如以后对该属性的setting, getting, and deleting有更多限制的话，再用property decorator
>Start with simple attributes.
If you later need functionality around the setting, getting, and deleting, you can add it with the property decorator.
Avoid functions named set_... and get_... - that's what properties are for.