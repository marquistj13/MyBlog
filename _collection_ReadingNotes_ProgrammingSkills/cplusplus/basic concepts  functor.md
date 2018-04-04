---
title:  c++ 基本概念之 functor
date:   2018-4-4
---


* content
{:toc}


##  重载operator() ，即函数调用运算符
在[Ceres hello-world](http://ceres-solver.org/nnls_tutorial.html#hello-world)中，遇到了一个步骤，即创建一个functor的时候：
```c++
struct CostFunctor {
   template <typename T>
   bool operator()(const T* const x, T* residual) const {
     residual[0] = T(10.0) - x[0];
     return true;
   }
};
```
那么这里 __为啥要重载()运算符呢?__

在[Why override operator()?](https://stackoverflow.com/questions/317450/why-override-operator)中解释道：
__重载()运算符的首要目的就是创建一个functor。__

__既然我们已经有了function ，为啥还需要functor的概念啊？__

_当然首选要明确一点_：定义一个函数之后，函数名就是函数指针；而functor只是一个object（对象）。

### 解释1：functor可以有状态，而普通的函数没有状态的概念。

>A functor acts just like a function, but it has the advantages that it is stateful, meaning it can keep data reflecting its state between calls.

例如：
```c++
struct Accumulator
{
    int counter = 0;
    int operator()(int i) { return counter += i; }
}
...
Accumulator acc;
cout << acc(10) << endl; //prints "10"
cout << acc(20) << endl; //prints "30"
```

这样，就实现了累加的效果。

对比一下，一个函数要实现这种效果，就需要一个全局变量来作为状态变量。

###  解释2：functor和函数指针可采用同样的方式进行调用，并且方便编译器将其inline
The main benefit is that：当你的函数可以使用templated functor的时候， the function call to operator() can be inlined. 
（注意，function pointers也是 valid functors，因为人家也有operator(), 意味着你的这个函数也可以调用函数指针）。

为了加深理解，我们看一下 `std::for_each` 的示意代码。
```c++
template <typename InputIterator, typename Functor>
void for_each(InputIterator first, InputIterator last, Functor f)
{
    while (first != last) f(*first++);
}
```
注意看啊，`for_each`的最后一个参数的类型，只要f能这么`f(bla)`使用，就行，因此，f可以是一个函数指针，也可以是一个重载了operator() 的functor。
```cpp
void print(int i) { std::cout << i << std::endl; }
...    
std::vector<int> vec;
// Fill vec

// Using a functor
Accumulator acc;
std::for_each(vec.begin(), vec.end(), acc);
// acc.counter contains the sum of all elements of the vector

// Using a function pointer
std::for_each(vec.begin(), vec.end(), print); // prints all elements
```

我们再来解释一下“ the function call to operator() can be inlined. ”这句话的意思：函数牵涉到了函数指针，而functor并不涉及指针的重定向，也就是说functor就是某个class的非虚函数，因此编译器可以确定到底调用哪个函数，然后inliine that.

### 解释3：虽然functor可以像function一样调用，但它们俩毕竟不一样
例如，我们有时候仍然需要class的 extra benefit 。
我们不想这么调用：`logger.log("Log this message");`,想这么搞：`logger("Log this message");`

再举一个例子：
我们有一个 class Reporter，它只实现了report(..),还有一个 class Writer，只实现了 write(..)。
我们现在有一个需求，将这俩class作为其他系统的模板成分（template component ）。
这么搞肯定不行：
```
T t;
t.write("Hello world");
```
但用了functors之后，可以改成这样：
```
T t;
t("Hello world");
```

## C++ Functors - and their uses
以下来自：[C++ Functors - and their uses](https://stackoverflow.com/questions/356950/c-functors-and-their-uses)
### 更容易理解的例子，关于重载的参数和状态
__functor使得 class or struct 对象能够像函数一样调用。__
当然就是通过重载，函数调用运算符`()`实现的。    
注意：其他运算符如`+ operator`可以有俩参数，但`()`可以有很多参数。
嗯，代码来了：
```c++
class myFunctor
{ 
    public:
        /* myFunctor is the constructor. parameterVar is the parameter passed to
           the constructor. : is the initializer list operator. myObject is the
           private member object of the myFunctor class. parameterVar is passed
           to the () operator which takes it and adds it to myObject in the
           overloaded () operator function. */
        myFunctor (int parameterVar) : myObject( parameterVar ) {}

        /* the "operator" word is a keyword which indicates this function is an 
           overloaded operator function. The () following this just tells the
           compiler that () is the operator being overloaded. Following that is
           the parameter for the overloaded operator. This parameter is actually
           the argument "parameterVar" passed by the constructor we just wrote.
           The last part of this statement is the overloaded operators body
           which adds the parameter passed to the member object. */
        int operator() (int myArgument) { return myObject + myArgument; }

    private: 
        int myObject; //Our private member object.
}; 
```

### 更容易理解的保存状态和inline的例子
```cpp
class MultiplyBy {
private:
    int factor;

public:
    MultiplyBy(int x) : factor(x) {
    }

    int operator () (int other) const {
        return factor * other;
    }
};
```
然后可以这么用：
```cpp
int array[5] = {1, 2, 3, 4, 5};
std::transform(array, array + 5, array, MultiplyBy(3));
// Now, array is {3, 6, 9, 12, 15}
```
functor比函数指针更容易inline。
此时，如果我们传递一个函数指针给 `std::transform`,那么除非这个调用是inline的并且编译器知道了每次传递的都是同一个函数，才会inline，否则，编译器是无法仅通过函数指针进行inline的。

###  使用boost function, to create functors from functions and methods
```cpp
class Foo
{
public:
    void operator () (int i) { printf("Foo %d", i); }
};
void Bar(int i) { printf("Bar %d", i); }
Foo foo;
boost::function<void (int)> f(foo);//wrap functor
f(1);//prints "Foo 1"
boost::function<void (int)> b(&Bar);//wrap normal function
b(1);//prints "Bar 1"
and you can use boost::bind to add state to this functor

boost::function<void ()> f1 = boost::bind(foo, 2);
f1();//no more argument, function argument stored in f1
//and this print "Foo 2" (:
//and normal function
boost::function<void ()> b1 = boost::bind(&Bar, 2);
b1();// print "Bar 2"
```

and most useful, with boost::bind and boost::function you can create functor from class method, actually this is a delegate:
```cpp
class SomeClass
{
    std::string state_;
public:
    SomeClass(const char* s) : state_(s) {}

    void method( std::string param )
    {
        std::cout << state_ << param << std::endl;
    }
};
SomeClass *inst = new SomeClass("Hi, i am ");
boost::function< void (std::string) > callback;
callback = boost::bind(&SomeClass::method, inst, _1);//create delegate
//_1 is a placeholder it holds plase for parameter
callback("useless");//prints "Hi, i am useless"
```
You can create list or vector of functors

```cpp
std::list< boost::function<void (EventArg e)> > events;
//add some events
....
//call them
std::for_each(
        events.begin(), events.end(), 
        boost::bind( boost::apply<void>(), _1, e));
 ```
