--- 
title:  Deep Forest Towards An Alternative to Deep Neural Networks
date:   2017-03-02
---



* content
{:toc}

Zhi-Hua Zhou大神17.2.28的arxiv，看名字也知道,就是要搞出来一个和DNN平行的架构，当然你必须得避免DNN的重大缺陷才有意义：
1. 只需要 small-scale training data
2. 作为一个 treebased approach, gcForest比DNN的理论分析更简单。

## Introduction
作者对于DNN的批判：
1. training data大， labeled data 当然得多了
1. 太复杂了，计算量大。
1. 超参数太多了
1. 对于不同的different options如convolutional layer structures，DNN实际上用的是不同的 learning models。

这就使得DNN的训练非常 tricky, like an art rather than science/engineering，并且理论分析也难。

作者的感受：
representation learning的能力对于DNN来说是crucial的；
要想利用大量的训练数据，学习模型的capacity必须得大。
这就解释了为啥DNN比一般的模型如SVM更复杂。
作者认为，如果换一种学习模型的形式，不用ANN，但仍然保留以上两点特性，或许可以避免DNN的缺陷。

作者的方法：gcForest(multi-Grained Cascade forest), a novel decision tree ensemble method
1. 使用cascade structure来实现representation learning
1. cascade levels可以自适应地确定，故model complexity也可以自动确定
1. 超参数比DNN少，而且performance对于超参数的设置非常robust，即对于不同domain的数据，只需要使用默认的超参数设置就行了。
1. 上面这一点使得其训练很方便，而且理论分析也更方便。
1. 可以并行化。

## 算法部分
### Cascade Forest
Representation learning in deep neural networks mostly relies on the layer-by-layer processing of raw features.
gcForest 也采用这种级联结构（cascade structure）

每一层都是由decision tree forests组成的 ensemble。
为了保证 ensemble construction的diversity，每一层都要有不同类型的forest。
本文使用two completerandom tree forests and two random forests。

进来一个输入instance，每一个forest都会产生一个class distribution的estimate。方法就是，每个tree可以count出一个distribution，然后这个forest的所有tree平均一下就行了。
层与层传递的就是class distribution vector。

原来自动确定level的数目是靠validation dataset实现的……
插一点：作者使用k-fold cross validation，即每一个输入instance使用k-1次才能传到下一层。
就是，每增加一个level，我就在validation set上估计一下performance of the whole cascade，如果没咋变，咱就停止增加。
这样，cascade levels is automatically determined。
我咋觉得DNN也可以这么玩儿？从而避免被诟病的capacity过大引起的训练难的问题？

### Multi-Grained Scanning
鉴于DNN中两大处理特征关系的结构，CNN之于raw pixels的spatial relationships，RNN之于sequence data。
本文采用multi-grained scanning来enhance cascade forest。

实际很简单，就是用sliding windows，将原维度的数据进行类似卷积层的操作，如400 dim的数据，我用100 dim的滑窗可以搞成301个100维的数据，也可以用200dim的滑窗搞成201维的数据，当然对于20x20的image panel也是类似。
这么搞以后，再将这些数据送到上一节的级联结构中就行了，实际上就是一个预处理嘛。 这一步毫无learn的概念吧。哦，看了一下2.3节，发现还是有的，得先经过 a complete-random tree forest and a random fores才能送到级联结构中。

## 实验部分
为啥都是分类的数据集。