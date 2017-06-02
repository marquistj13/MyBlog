---
layout: post
title:  何去何从
categories: 个人笔记
tag: [规划，学术]
---


* content
{:toc}

又得做决策了。从12月到今天，整整六个月的调研，是时候了结了。
去年八月份到十一月份，一直在搞聚类，初步感受到了聚类的局限性。从十二月份开始，我着重调研了DNN、深度聚类这俩问题，期间当然夹杂了很多对于经典聚类算法的研究（特别是子空间聚类、谱聚类），还有关于聚类的各种扯淡的paper，但看的越多，就越深感无奈。

有监督这一脉的approach香火很旺的一个重要原因就是 _问题很具体_ ，如果非常general的问题搞不了，那就限定问题种类，如只搞cv问题，再具体一点就是。

而与之相对的聚类基本上一直沿着（完全）无监督的路走到黑了，零星的半监督聚类文章也不太合我口味。聚类一直无法做非常complicated的task，一个重要原因就是聚类给自己的定位太低了，为啥非得是 _similar points in the same group, dissimilar in different groups_? 这么一搞就显得聚类的终极任务就只是 _将各个points聚到一块儿，只要这些cluster能够make sense, reasonable就行了_。
当然最重要的原因还是没有label啊，有监督的DNN的参数能够由误差向量来guide the Learning proce，这时候参数多少基本都无所谓了，但没有label的话，那就是 _臣妾做不到啊_。

我坚信聚类可以完成的task绝非如此简单，隐约感觉它可以像有监督那样有令人信服的Learning的概念，即能够 generalize。 怎么算令人信服呢？当然是更加complicated的application了，而非以往依赖于矢量量化oriented的应用。
当然，现在的deep clustering也有做的不错的了，如一篇arxiv的文章Deep Clustering using Auto-Clustering Output Layer（我的笔记在[这儿]( https://marquistj13.github.io/MyBlog/ScholarThings/Clustering/DeepClustering/Deep%20Clustering%20using%20Auto-Clustering%20Output%20Layer ），貌似这篇文章刚被被icml拒掉了，我在https://2017.icml.cc/Conferences/2017/AcceptedPapersInitial 没有找到它啊。

聚类老玩儿法感觉快行不通了啊，哦，icml2017收录了一篇 Towards K-means-friendly Spaces: Simultaneous Deep Learning and Clustering，这个题目很明显了嘛，类似于用DNN做特征提取，representation Learning啊。要不要往这个方向走呢？目测这么走下去还是老路子嘛。

我现在大概的想法是，不再将聚类问题用于聚类，即要有新玩儿法。
当然突破口就是先找一个具体的应用，这个应用可以不那么general，关键是能work，而且能让人一眼看出来值得继续去发展。例如，对于一个picture，我们可以根据label信息确定超参数，注意是超参数，而参数仍然按照无监督来搞，这样就能保证整个过程是无监督的，label仅仅是一般的先验信息而已，具体细节还得再研究啊。