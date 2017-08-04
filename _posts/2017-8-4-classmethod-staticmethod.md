---
layout: post
title:  classmethod和staticmethod的异同
categories: 编程
tag: [Python]
---

* content
{:toc}


## 角度1
根据 [difference-between-staticmethod-and-classmethod-in-python](http://pythoncentral.io/difference-between-staticmethod-and-classmethod-in-python/) 以及 [Python 中的 classmethod 和 staticmethod 有什么具体用途？
](https://www.zhihu.com/question/20021164)汇总。

### classmethod：只需要与class交互
对于类的method，我们大多数情况下只需要使用instance method，即通过self参数来干活，对于一些不需要与instance交互，只需要与class交互，如一个class的全局变量用于统计instance的数目：
```py
def get_no_of_instances(cls_obj):
    return cls_obj.no_inst
class Kls(object):
    no_inst = 0
    def __init__(self):
        Kls.no_inst = Kls.no_inst + 1
ik1 = Kls()
ik2 = Kls()
print(get_no_of_instances(Kls))
```

这么搞是可以的，但会有future维护问题，因为咱们把逻辑相关的代码分开了嘛。

怎么办呢？一个过渡的方法就是：
```py
def iget_no_of_instance(ins_obj):
    return ins_obj.__class__.no_inst
class Kls(object):
    no_inst = 0
    def __init__(self):
    Kls.no_inst = Kls.no_inst + 1
ik1 = Kls()
ik2 = Kls()
print iget_no_of_instance(ik1)
```

在Python2.2以后可以使用@classmethod装饰器来创建类方法
```py

class Kls(object):
    no_inst = 0
    def __init__(self):
        Kls.no_inst = Kls.no_inst + 1
    @classmethod
    def get_no_of_instance(cls_obj):
        return cls_obj.no_inst
ik1 = Kls()
ik2 = Kls()
print ik1.get_no_of_instance()
print Kls.get_no_of_instance()
```

**好处就是**：既可以用instance调用，也可以用class调用

### staticmethod：不需要和instance或class交互
还有一些奇葩需求，这个method既不与instance相关，也不与class相关：如设置环境变量，改变另一个class的属性等等，举例：
```py
IND = 'ON'
def checkind():
    return (IND == 'ON')
class Kls(object):
     def __init__(self,data):
        self.data = data
def do_reset(self):
    if checkind():
        print('Reset done for:', self.data)
def set_db(self):
    if checkind():
        self.db = 'new db connection'
        print('DB connection made for:',self.data)
ik1 = Kls(12)
ik1.do_reset()
ik1.set_db()
```
这么搞就将代码分开了，不好维护，如果用 `@staticmethod`,就好多了：
```py
IND = 'ON'
class Kls(object):
    def __init__(self, data):
        self.data = data
    @staticmethod
    def checkind():
        return (IND == 'ON')
    def do_reset(self):
        if self.checkind():
            print('Reset done for:', self.data)
    def set_db(self):
        if self.checkind():
            self.db = 'New db connection'
        print('DB connection made for: ', self.data)
ik1 = Kls(12)
ik1.do_reset()
ik1.set_db()
```


### 二者的不同
```py
class Kls(object):
    def __init__(self, data):
        self.data = data
    def printd(self):
        print(self.data)
    @staticmethod
    def smethod(*arg):
        print('Static:', arg)
    @classmethod
    def cmethod(*arg):
        print('Class:', arg)
 
>>> ik = Kls(23)
>>> ik.printd()
23
>>> ik.smethod()
Static: ()
>>> ik.cmethod()
Class: (<class '__main__.Kls'>,)
>>> Kls.printd()
TypeError: unbound method printd() must be called with Kls instance as first argument (got nothing instead)
>>> Kls.smethod()
Static: ()
>>> Kls.cmethod()
Class: (<class '__main__.Kls'>,)
```

## 角度2
根据 [Meaning of @classmethod and @staticmethod for beginner?](https://stackoverflow.com/questions/12179271/meaning-of-classmethod-and-staticmethod-for-beginner) 的高赞回答进行总结。

### classmethod实现和class相关的需求
假设我们有一个需求就是保存一个日期的对象，这样通过构造函数就行了
```py
class Date(object):

    def __init__(self, day=0, month=0, year=0):
        self.day = day
        self.month = month
        self.year = year
```

这个需求如果再变一下，日期不是直接给，而是需要从输入中解析，很自然地可以这么实现：
```py
day, month, year = map(int, string_date.split('-'))
date1 = Date(day, month, year)
```
但是，这么搞的话，就会使得逻辑相关的code分开，不方便维护。
__我们知道，在c++中，我们可以重载构造函数来实现这一需求，但Python没有这玩意儿啊__，因此就用`classmethod`来实现这一需求了。
```py
 @classmethod
    def from_string(cls, date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        date1 = cls(day, month, year)
        return date1

date2 = Date.from_string('11-09-2012')
```

### Static：实现一些杂碎的需求
例如用来验证date是否有效：
```py
   @staticmethod
    def is_date_valid(date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        return day <= 31 and month <= 12 and year <= 3999

    # usage:
    is_date = Date.is_date_valid('11-09-2012')
```

### static 和 calssmethod的不同
上面的例子中，我们用了`classmethod`，没有用`staticmethod`，其实都可以用，如下，只是在继承的时候有点不同。
```py
class Date:
  def __init__(self, month, day, year):
    self.month = month
    self.day   = day
    self.year  = year


  def display(self):
    return "{0}-{1}-{2}".format(self.month, self.day, self.year)


  @staticmethod
  def millenium(month, day):
    return Date(month, day, 2000)

new_year = Date(1, 1, 2013)               # Creates a new Date object
millenium_new_year = Date.millenium(1, 1) # also creates a Date object. 

# Proof:
new_year.display()           # "1-1-2013"
millenium_new_year.display() # "1-1-2000"

isinstance(new_year, Date) # True
isinstance(millenium_new_year, Date) # True
```
Thus both new_year and millenium_new_year are instances of Date class.
但如果继承一下：
```py
class DateTime(Date):
  def display(self):
      return "{0}-{1}-{2} - 00:00:00PM".format(self.month, self.day, self.year)


datetime1 = DateTime(10, 10, 1990)
datetime2 = DateTime.millenium(10, 10)

isinstance(datetime1, DateTime) # True
isinstance(datetime2, DateTime) # False

datetime1.display() # returns "10-10-1990 - 00:00:00PM"
datetime2.display() # returns "10-10-2000" because it's not a DateTime object but a Date object. Check the implementation of the millenium method on the Date class
```

datetime2 is not an instance of DateTime? WTF? 
这是因为基类用了`@staticmethod`,怎么保证子类仍然知道自己的class呢？就得使用`@classmethod`了。


```py
@classmethod
def millenium(cls, month, day):
    return cls(month, day, 2000)
```
ensures that the class is not hard-coded but rather learnt. cls can be any subclass. The resulting object will rightly be an instance of cls. Let's test that out.

```py
datetime1 = DateTime(10, 10, 1990)
datetime2 = DateTime.millenium(10, 10)

isinstance(datetime1, DateTime) # True
isinstance(datetime2, DateTime) # True


datetime1.display() # "10-10-1990 - 00:00:00PM"
datetime2.display() # "10-10-2000 - 00:00:00PM"
```