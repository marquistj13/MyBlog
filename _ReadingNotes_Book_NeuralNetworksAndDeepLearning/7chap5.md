---
title:  第五章
---


* content
{:toc}

CHAPTER 5 Why are deep neural networks hard to train?

## 引言
作者开头举了个设计逻辑电路的例子，客户要求只用两层门电路来设计，两层是可以做到的，但太难了（But just because something is possible doesn't make it a good idea. ）
我们在实际设计电路的时候一般先分解成子问题，然后逐渐玩上层的（类似搭积木）。例如，要实现一个乘法器，第一层就是按位加，第二层就是普通加法，第三层就是乘法啦


以上这段话的point：**So deep circuits make the process of design easier.**
这么搞其实不仅仅有利于design，而且还更有效。在论文 On the correlation of parity and small-depth circuits 中提到，shallow circuit要的基本器件是deep circuit的指数级。因此**Deep circuits 本质上比shallow circuits更加powerful**.


本章以前，作者的套路一直都是拿shallow network来说事，这就和上面那个例子一样了。这些shallow network虽然很有用，但我们在直觉上intuitively还是期望网络能够由很多层，变成deep network，从而更加powerful。 
实际上，正如上面电路的例子那样，也有论文 On the number of response regions of deep feed forward networks with piece-wise linear activations证明了**deep networks are intrinsically more powerful than shallow networks**。


坏消息是，DNN的训练经常会出现问题，以至于DNN的性能甚至比不上SNN（shallow NN）。
我们不打算因为这点困难就抛弃DNN，而是要深挖、理解为啥DNN难训练，由此知道了DNN的梯度消失、爆炸问题。研究哲学问题就可以对DNN的训练增加insight。

## The vanishing gradient problem
* 引出DNN训练时出现的问题
使用前几章的程序，我们增加NN的深度，性能并没有明显提升。
* 发现问题
如果我们可视化以上程序每一层误差向量的长度即摸值（定义为学习速率）（当然，为了公平，这些隐含层的neuron的数目一样），即$\| \delta^1 \|$,$\| \delta^2 \|$,$\| \delta^3 \|$,我们就会发现它们相差很大，越靠近输入层越小。实验表明，第一层的速率比第四个隐含层的速率低了100倍！
结论：在某些DNN中，会出现**vanishing gradient problem**：the gradient tends to get smaller as we move backward through the hidden layers。实际上，还有可能出现**exploding gradient problem**：sometimes the gradient gets much larger in earlier layers!
* 要理解vanishing gradient problem的确是一个问题啊
有人说了，梯度小不是好事么？不就相当于我们的目标函数（这里就是cost function）的微分很小了？即我们已经到极值啦？
当然，实际情况不是这样的。我们再理一遍：我们的权值是随机初始化的，由于“前面层的梯度很小”这个现象从一开始训练的前面的epoch开始就有这个问题了，因此前面层的权值基本上还是初始化时候的样子，你说这有啥好的？都这样子了，我们也就没法指望靠近输入层的layer能够学习到很底层的特征啦。
## What's causing the vanishing gradient problem? Unstable gradients in deep neural nets
本节的分析还是老套路：将问题极简化，从而便于分析。
我们考虑一个有三个hidden layer的NN，而且每一个layer（包含输入输出layer）都只有一个layer，那么第一个hidden layer的梯度就是：$$\begin{eqnarray}
\frac{\partial C}{\partial b_1} = \sigma'(z_1) \, w_2 \sigma'(z_2) \,
 w_3 \sigma'(z_3) \, w_4 \sigma'(z_4) \, \frac{\partial C}{\partial a_4}.
\tag{122}\end{eqnarray}$$
注：$a_4$就是最后一层即输出层的输出
我们画出$\sigma'$的图像以后，很明显看出来，在0的地方达到最大值0.25
* vanishing gradient problem的成因
对于初始权值来说，有$|w_j| < 1$,因此上式中$|w_j \sigma'(z_j)| < 1/4$，这些东西乱成一通只会更小。
* The exploding gradient problem
有人说了，$w_j$在训练的时候可能会增大的嘛，这样$|w_j \sigma'(z_j)| < 1/4$就可以不成立了嘛。好的，我们现在构造出一个这种情况来。
现在$w_1 = w_2 = w_3 = w_4 = 100$,而且bias取得也好，这样$\sigma'(z_j)$就不会太小啦，很好，我们可以干脆让$z_j = 0$（注意$z_1 = w_1a_0 $），这样$\sigma'(z_j) = 1/4$，此时$w_j \sigma'(z_j)=100 * \frac{1}{4} = 25$。
With these choices we get an exploding gradient.
* The prevalence of the vanishing gradient problem
用sigmoid neurons的时候，the gradient will usually vanish. 
为了避免这个问题，我们得满足$|w\sigma'(z)| \geq 1$,有人说了这不是很容易实现么？其实不然，这时候b取得不好的话，你的$z$就会很大，导致$\sigma'(z)$很小，哈哈，最后$|w\sigma'(z)|$还是很小啊。
* Unstable gradients in more complex networks
对于每一层不止一个neuron的情况，其实也是差不多的，因为还是有这么一个式子的：$\begin{eqnarray}
  \delta^l = \Sigma'(z^l) (w^{l+1})^T \Sigma'(z^{l+1}) (w^{l+2})^T \ldots
  \Sigma'(z^L) \nabla_a C
\tag{124}\end{eqnarray}$

## Other obstacles to deep learning
上面我们遇到了一个obstacle to deep learning，即unstable gradients，实际上这只是其中一个obstacle，有很多研究在试图理解the challenges that can occur when training deep networks. 
如
1. Understanding the difficulty of training deep feedforward neural networks, by Xavier Glorot and Yoshua Bengio (2010). 这一篇主要讲 sigmoid activation function的问题。
1. On the importance of initialization and momentum in deep learning, by Ilya Sutskever, James Martens, George Dahl and Geoffrey Hinton (2013). 这一篇讲到了初始化以及梯度算法的实现问题


这俩paper都表明DNN的训练时很复杂的。理解这些难以训练的原因是很多人正在研究的东西。


好消息就是，下一章我们就要搞一些DL的approach来overcome或route around all these challenges.



