---
layout: post
title:  Distributed Representation
categories: 深度学习
tag: [学术]
---

* content
{:toc}


主要参考自：[Deep Learning: What is meant by a distributed representation?](https://www.quora.com/Deep-Learning-What-is-meant-by-a-distributed-representation)

## 大体来讲
来一个input，经过各种变换，用几个neuron来
* represent这个input
* 逼近output

##  和非分布式representation的区别：一维与多维
假如给你几个单词，如 word1, word2, word3等，你的任务是给每一个单词一个 unique id，非分布式的就是用一个数字表示，如1245 or 467126，这就非常compact了，但没法赋予这个数字一些semantics。
分布式的就是用一个矢量来表示，如 (0.3, 0.25, 0, 0.8) 这样就能 encode important properties/semantics到这个矢量中了。

##  信息存储与提取的角度
将information存储为一个encoded vector,这个vector的每一维都有代表一部分信息，即我可以仅仅根据其中的某几维来做决策。
### 存储
有四个东西（item）A, B, C, and D
非分布式表示：
A = 1 0 0 0
B = 0 1 0 0
C = 0 0 1 0
D = 0 0 0 1
这样四位存储已经满了，要想加一个单词E，只能擦掉上面一个东西了。

分布式：
A = 0.5 0.3 0.0 0.5
B = -0.1 -0.2 0.0 0.1
C = -0.1 0.5 0.0 -0.5
D = 0.0 0.0 0.5 0.1
这个就可以用这个representation来增加item了。
### 提取
如果想retrieve A或者B
A = -0.2 -0.2 0.0 0.1
B = -0.1 -0.2 0.0 0.1
C = -0.1 0.5 0.0 -0.5
D = 0.0 0.0 0.5 0.1
那么我们的system可能会取出来A或者B，因为它俩太像了。
我们的大脑也是类似的工作原理。
### relatedness
再来一个例子，
small apple = -0.2 -0.2 0.0 0.1
big apple = -0.1 -0.2 0.0 0.1
orange = -0.1 0.5 0.0 0.3
strawberry = -0.3 0.1 0.0 0.5
car = 0.0 0.0 0.5 0.1
truck = 0.1 -0.1 0.5 0.2
那么给你一个新的东西，[-0.2, 0.1, 0.0, 0.2]，我们可以猜出来它是一种水果。

大脑也是这么搞的。


##  distributed representation背后的idea
观测信息（即输出，如这个照出来的图片是猫还是狗）是由很多因素相互作用产生的
我们要build的这个ANN，正好有很多layer，很多feature，可以用来表示这些东西


## 更多解释
非分布式的representation，每一个concept都由一维数据表示,这样一来就有很多缺点
1. 没法提前知道有多少不同的concept
2. 没法表示相似性，如how do we represent a “big” “yellow” “volkswagen” and at the same time its relatedness to a “big” “volkswagen”, a “yellow” “volkswagen”, or even just a “volkswagen” ?
3. 好了，对于那种one hot encoding for all words，即representation的维度和词库的单词数目一样，那么我们很难用这个representation来表示相似性。
4. 即使我们可以选择哪些特征去描述concept，如yellow, big etc，但是我们仍然需要提前知道总的特征数目（很不现实啊，相比之下，分布式的就不需要知道这些东西）。并且仍然无法表征concept之间的relatedness 

而Distributed representation仅仅通过representation就可以搞定以上问题。

>实际上，不过你的模型是啥，只要满足两个条件就行了
1. each concept being represented by multiple dimensions
2. each dimension participating in the representation of multiple concepts.

翻译一下：
In a distributed representation of concepts,
1. 每一个concept都是多维的，即由一个array of values表示.
1. 每一个维度都包含了与其他concept的 _相似度信息(relatedness)_

作者举了个word2vec的例子
1. 我们可以用一个固定维度的向量来表示所有单词
2. 这些向量都是learn出来的，并且我们不需要指定feature的数目
3. 单词之间的可以用来表征similarity的信息都encode到不同的维度中了。

作者又提到，虽然有这么多好处，维度多少仍然没法随意选取。




