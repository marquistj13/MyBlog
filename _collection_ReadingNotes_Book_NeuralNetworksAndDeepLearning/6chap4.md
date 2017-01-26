---
title:  chap4
---



* content
{:toc}



## 引言

能够compute any function是NN的一大亮点，即NN具有某种一种universality，且在只有一个hidden layer也是成立的。
证明universality的早期论文有Approximation by superpositions of a sigmoidal function， Multilayer feedforward networks are universal approximators,等。前者用的是泛函分析的方法，后者用的是Stone-Weierstrass theorem。当然，对于搞数学的，这些东西看着很简单，但对于我们普通的大多数人来说还是挺难的。That's a pity, since the underlying reasons for universality are simple and beautiful.
Universality theorems本身是很好的，但由于在CS领域太常见了，我们都忘了它们本身是多么astonishing的啦。由于很多问题都可以表示成函数，因此，Universality means that, in principle, neural networks can do all these things and many more.
当然，能表示任意函数是不行的，我们还得搞出来一些good techniques for constructing or even recognizing such a network. That combination of learning algorithms + universality is an attractive mix. 

## 隐藏在这句话"a neural network can compute any function"中的两个点

1. 这个compute指的是能够逼近任意精度，而非精确地复现这个函数
2. 我们能够逼近的是连续函数，也就是进行连续逼近。当然即使是一个不连续的函数，我们的连续逼近一般也是很好的。


## Universality with one input and one output

这一节的思路很清晰。
首先，作者表明，对于一个neuron来说，将权值 $w$ 设到很大，如100的时候，这个sigmoid函数就很像阶跃函数了，而bias $b$的作用就是平移一下哈哈。
然后两个neuron都调教成阶跃函数之后，它们俩的输出进行加权，就可以组成一个方波（这里指的是“几”字形）了，很多个方波就可以逼近一个任意函数了。
（在思考过程中，这里边的一个trick就是，我们用两个sigmoid的neuron加权之后的东西来逼近 $\sigma^{-1} \circ f(x)$ ,那么它经过输出层的sigmoid之后就是目标函数的逼近了。）

## Many input variables

我们考虑二维输入的情况，这俩输入连接到一个neuron上，我们探讨一下这个neuron的输出，将其中一维的变量始终固定为0，另一个维度的变量调教成阶跃函数，那么在三维图像中就是一个Z字形的图像；如果让一直为0的那一维也调教成阶跃函数（当然也得给它一个neuron），那么就可以组成一个三维的“几”字形（当然这个“几”字有两个面是没有封住的），再用两个neuron构成一个“几”字形，这俩“几”字形就可以组成一个tower了（这个“几”字形四面都封口了），当然这个形状也需要调教。
而这个tower就可以作为类似上一节一个输入的时候的函数逼近单元那样的基本逼近单元。

## Extension beyond sigmoid neurons
ReLU是可以的，线性激活函数是不行的。

## Fixing up the step functions
由于阶跃函数的逼近并不完美，即0到1并不是竖直升上去的，因此这个跳跃就会有一定的缺憾，但是可以fix的，可以多一点阶跃函数，你这个阶跃函数跳跃的地方正好位于另一个阶跃函数不跳跃的地方，这样就好办了。

## Conclusion
以上的描述并不是用来practical prescription for how to compute using neural networks!以上的意义在于，我们不用操心NN能不能干这个事了，只需要关系what's a good way to compute the function.
当然一个重要的问题就是，既然单隐层就能解决问题，那就别用那么多hidden layers了吧，这玩意儿那么难训练是不是哈。
使用DNN的一个重要原因就是，DNN能够学习到层次知识，这种类型的知识对于解决实际问题是很有用的。对于图像分类的任务来说，我们建立的system需要理解底层的像素值，也得理解更为复杂的concept（如边缘，几何形状），实际经验表明DNN比shallow NN更擅长此类知识的学习。
总结一下：universality告诉我们，NN可以用来逼近任意函数，而实际经验告诉我们，DNN更适合学习那些用于解决实际问题的函数。

