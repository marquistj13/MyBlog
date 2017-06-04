--- 
title: Data Clustering A User s Dilemma
date:   2017-6-4
---


* content
{:toc}

题目起得很不好，太大了。 难道是因为一作是A.K Jain的缘故？
其实就是稍微综述了一下05年的时候三个聚类方面的热点：clustering ensemble, feature selection, and clustering with constraints.

对于clustering ensemble来说，将几个weak的聚类算法合称一个strong的算法，但并没有那么美好，即有很多难调的东西，而且引文中也没有令人说服的例子。 个人认为此坑莫入。

对于feature selection来说，作者提到了高斯混合模型聚类，但哪有那么美好啊。

还有clustering with constraints其实就是在具体的应用场景中，如图像分割，将我们的先验知识给incorporate进去，看到了吧，很具体的应用才会有啦。