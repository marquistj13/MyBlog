--- 
title: Deep Unsupervised Similarity Learning using Partially Ordered Sets
date:   2017-6-14
---


* content
{:toc}

## conclusion 
主题：基于CNN的无监督approach to similarity learning

方法：framing it as a combination of surrogate classification tasks and poset ordering，使之成为 joint optimization problem of grouping samples into surrogate classes while learning the deep similarity encoding representation.

应用场景：learning fine-grained similarity relationships in the context of human pose estimation and object classification

## abstract
Deep learning of similarities 的常用方法就是基于pairs or triplets of samples来搞，很明显这种方法不太好（记得以前有篇文章说这种pair的方法学习到的是local structure）。

本文的思想很简单：
先搞一些local estimates of reliable (dis-)similarities to initially group samples into compact surrogate classes，然后利用sample的局部partial order将各个class联系到一起。
这样，Similarity learning就formulated as a partial ordering task     。
最后，利用 self-supervision 的策略，训练一个CNN，

## intro
用无监督的理由： supervised labeling of similarities is very costly. 并且，不仅image之间的similarities很重要，objects and their parts的关系也很重要

为了利用无监督数据的信息，我们需要利用images video的上下文信息，以期能够self-supervision。 但这些上下文信息太local了，因此，以往的approach都要利用能够order一个正样本和一个负样本的loss function。
然后用CNN to indirectly learn comparisons between samples that were processed in independent training batches, and generalize to unseen data.

注意，这些CNN在训练时都是indirectly balance and learn sample comparisons，当然，更加natural approach就是 __explicitly encode richer relationships between samples as supervision.__

详细来说，就是先用一些 _初始的弱的表示_ weak initial representation (e.g standard features such as HOG) 进行聚类，每个cluster一个label，这时候就可以 __训练CNN来对这些样本进行分类了__。
这么搞听着很完美，但是啊：
1. 由于初始的representation很弱，好多样本难以分类，即既不互相相似，也不互相不相似。导致这些样本在训练的时候没法用。
1. 由于类的discrete nature，分类问题产生的similarity非常 coarse。
1. 由于不同的分类任务不是一块儿优化的，导致产生互相矛盾的relationship。

本文：
1. 依然采用surrogate (i.e. artificially created) classification tasks模式
2. 将分类任务和partial ordering of samples联系起来，这样即使那些没法分类的样本也能用以训练了。
3. 显示地在given representation space优化similarity，而非直接使用用来分类的CNN的某一个中间层间接学习到的的representation space。
4. 联合优化surrogate classification tasks for similarity learning and the underlying grouping in a recurrent framework which is end-to-end trainable.

## Related Work
有了CNN之后，用pairs [39], or triplets [32] of images来搞supervised similarity的有很多。不管有监督与否，都得要求 supervisory information scales quadratically for pairs of images, or cubically for triplets.

对应的无监督approach就是搞一个surrogate (i.e. an artificial) classification task either by utilizing heavy data augmentation [6] or by clustering based
on initial weak estimates of similarities [3, 15].

similarity learning 也从 the perspective of metric learning来研究过，即当成一个cross-entropy based classification problem in which all pairwise neighbouring samples are pulled together while nonneighbouring samples are pushed away.
就是computational cost有点高。

## 本文方法论
### Grouping以构建surrogate class
使用经典的特征距离，HOG-LDA，搞出来compact groups of samples。

尽管这个HOG-LDA不能将所有sample都relate到一起，它还是可以找到最近和最远的neighbor的。这样，对于一个anchor sample $x_i$, 只要找出和它最近的 top $5%$ 就行啦。
好了这些class很compact，但大小不一，可能还有重叠。 作者将重叠的class给merge掉。
将分到 class $c$ 的点集记为 $C_c$, 且分到一个label， 将不属于任何class的点的label记为 $-1$.

### 构建Partially Ordered Sets
a poset $P_c$ is a set of samples which are softly assigned to class $C_c$.
这样，每一个 class $C_c$ 都有一个对应的 $P_c$。
当然，作者给 $P_c$ 里的sample定义了一个顺序，即对于 $x_j \in P_c, x_k \in P_C$.
如果 $x_j$ 到 $C_c$ 的 representative sample $\bar{x}_c$ 的距离都小于 $x_k$, 那么我们就说 $x_j < x_k$.

在此处note一下，作者指出，以往的 tuple 或 triplet相当于本文的  $C_c$ 只含有一个sample，而 $P_c$ 有 一个或两个sample的情况，这样就说rely on the CNN to indirectly learn to compare and reconcile the vast number of unrelated sampled pairs that were processed on different, independent mini-batches during training.
相比之下，本文的posets, explicitly encode an ordering between a large number of sample pairs (i.e pairs consisting of an unlabeled sample and its nearest class representative).
也就是说，poset强迫CNN去order all unlabeled samples，根据它们和 $z$ 个最近的class representatives的相似度。

Posets generalize tuple and triplet formulations by encoding similarity relationships between unlabeled samples to make a decision whether to move closer to a surrogate class.

### Objective function
目标函数需要：
1. 惩罚样本 $x_i$ 相对于 surrogate class label的误分类。
2. 将属于 poset $P_c$ 和距离 $P_c$ 最近的（前 $Z$ 个） class representatives pull 到一起，和其它 class representatives push出去。将距离所有surrogate classes都比较远的similarity从loss中vanish。

损失函数有两部分：
 surrogate classification loss 和  poset loss

### Joint Optimization
在这里，grouping and similarity learning tasks是互相依赖的。

 而我们学习到的representation $\phi^\theta$, 则captures similarity relationships, and an assignment of samples to surrogate classes $y$.

 A natural way to model such dependence in variables is to use a Recurrent Neural Network (RNN)。

 作者利用了一个a recurrent optimization technique. 联合学习 $\{y; \theta\}$,by unrolling the optimization into steps，后边的具体式子就看不懂了。