---
title:  chap3
---


* content
{:toc}

## 序言
* technique的地位
就像打高尔夫球需要不断练习挥杆动作basic swing，然后再练习其他技巧那样
BP就是我们的basic swing，即Learning的foundation，然后我们就得学习a suite of techniques用来improve我们的implemention
* 学习各种technique的方法：如何入门
available techniques 是非常多的，最好的入门方法就是，先对最重要的那些technique来一个in-depth study
理由：Mastering those important techniques一方面是因为这些technique很重要，另一方面是因为这些important technique能够加深我们对于NN中的问题的理解，因为这些technique就是为这些问题准备的嘛。
然后其他technique就可以在需要的时候去pick up啦

## The cross-entropy cost function
*  学习的理想情况：犯了错误更容易学习
就像学钢琴一样，你弹错了，有人指出来了，你改正了，很完美的一个学习流程哈
因此我们也期望NN能够learn fast from their errors，但对于输出层sigmoid+quadratic cost的组合来说，有一个很明显的缺陷，就是error大（作者给的例子就是，一个很简单的一个neuron的例子，学习一个w和b使得输出为0，此处error大指的是，初始化的w和b特别大，因此输出严重偏离0）的时候还没有error小（在此例子中，初始w和b都较小，因此error较小）的时候学的快，这是因为：
$$\begin{eqnarray}
  \frac{\partial C}{\partial w} & = & (a-y)\sigma'(z) x = a \sigma'(z) \tag{55} \\  
  \frac{\partial C}{\partial b} & = & (a-y)\sigma'(z) = a \sigma'(z),
\tag{56}\end{eqnarray}$$
（注：上式中y为0，这个是作者给的例子即目标输出为0的情况，作者通过一个单neuron的例子来说明问题，实际上很多探索都是靠特殊情况或者说是简化后的问题来进行的，这是个通用的研究方法，一定要好好感受）
因此，当$z$过大或过小的时候$ \sigma'(z)$就会接近0，因此每次$w$和$b$更新就很小了，造成学习速率很慢（ the problem of learning slowdown） 。
（注， $z$过大或过小就是， neuron saturation）
* 引入cross-entropy cost function
对于以上问题，一种解决方法就是精心设计一个新的cost function，将 $ \sigma'(z)$干掉,例如对于 $b$的更新：$ \frac{\partial C}{\partial b}  =  (a-y)\sigma'(z)$,我们期望将其变成 $ \frac{\partial C}{\partial b}  =  (a-y)$
现在开始探索，由于 $ \frac{\partial C}{\partial b}  =   \frac{\partial C}{\partial a}  \sigma'(z) $，因此新的 cost function应该满足： $ \frac{\partial C}{\partial a}   =   (a-y) \frac{1}{ \sigma'(z) } =  \frac{ a-y }{a(1-a) }= \frac{1}{1-a}-y[ \frac{1 }{a }+ \frac{1 }{1-a }] = \frac{1 }{1-a }= \frac{1-y }{1-a }- \frac{y }{a } $
对$a$积分得：$ \begin{eqnarray}
  C = -[y \ln a + (1-y) \ln (1-a)]+ {\rm constant},
\tag{76}\end{eqnarray}$
因此我们就得到了 cross-entropy cost function
$ \begin{eqnarray}
  C = -\frac{1}{n} \sum_x \left[y \ln a + (1-y ) \ln (1-a) \right],
\tag{57}\end{eqnarray}$
多个neuron的时候$ \begin{eqnarray}  C = -\frac{1}{n} \sum_x
  \sum_j \left[y_j \ln a^L_j + (1-y_j) \ln (1-a^L_j) \right].
\tag{63}\end{eqnarray}$
* 这是个reasonable的 cost function么
首先$C$非负，其次，当$a$和$y$接近的时候 $C$比较小，因为， $y=0$时，若我们的$ a \approx 0$那么上式的$ y \ln a$就是0，$ (1-y ) \ln (1-a)$也基本为0; $y=1$时,第二项为0，第一项也基本为0
cross-entropy的标准interpretation是information theory领域的。
可以认为，cross-entropy is a measure of surprise。我们的目标是学习到$x \rightarrow y = y(x)$，但实际上学习到的是$x \rightarrow a = a(x)$，其实 cross-entropy就是衡量我们学习到的平均意义上的surprise。

##  Softmax
* 引入 softmax layer
应对the problem of learning slowdown，除了改变cost function之外，也可以改变output neuron，即采用softmax layers of neurons：$ \begin{eqnarray}
  a^L_j = \frac{e^{z^L_j}}{\sum_k e^{z^L_k}},
\tag{78}\end{eqnarray}$
这个layer的特点很明显：所以输出$a^L_j$之和为1，其中任意一个 $a^L_j$增大，都会引起其他 $a^L_j$减小，以维持总和为1，因此可以解释为一个概率分布
* 应对 The learning slowdown problem
首先定义一个 log-likelihood cost function：$ \begin{eqnarray}
  C \equiv -\ln a^L_y.
\tag{80}\end{eqnarray}$
对于Minist的例子来说，如果真实label是7，那么上式的cost就是$-\ln a^L_7$
下面我们推导以下$\sigma^L_j= \frac{\partial C}{\partial z^L_j} $，首先求$ \frac{\partial a^L_j}{\partial z^L_k} $,易求得，$ \frac{\partial a^L_j}{\partial z^L_k}= \begin{cases}a^L_j(1-a^L_j) & j= k\\-a^L_ja^L_k & j\neq k\end{cases}$
简化以下： $ \frac{\partial a^L_j}{\partial z^L_k}= a^L_j( \sigma_{jk} -a^L_k)$, 故，$ \frac{\partial C}{\partial z^L_j}= a^L_k-\sigma_{jk}$
上式的意思是，若$j==k$则$\frac{\partial C}{\partial z^L_j}= a^L_j-1$否则就是 $\frac{\partial C}{\partial z^L_j}= a^L_j$
再进一步：若j对应的输出就应该输出1，则对于$k\neq j$的neuron来说，他们对应的输出就应该是0（注意我们采用的是One-hot coding），因此这些index为$k$的neuron的error只能从$ z^L_j$得到，因此上式就有意义了，在以上推导的基础上，我们总结如下：$$ \begin{eqnarray}
  \frac{\partial C}{\partial b^L_j} & = & a^L_j-y_j  \tag{81} \\
  \frac{\partial C}{\partial w^L_{jk}} & = & a^{L-1}_k (a^L_j-y_j)
\tag{82}\end{eqnarray}$$   
因此softmax layer+  log-likelihood cost function也能搞定t he learning slowdown problem
当然a sigmoid output layer and cross-entropy, or a softmax output layer and log-likelihood都可以用，区别是后者可以将output解释为概率
* "softmax"名字的由来
对于$ \begin{eqnarray}
  a^L_j = \frac{e^{c z^L_j}}{\sum_k e^{c z^L_k}},
\tag{83}\end{eqnarray}$
在$ c \rightarrow  \infty $时，若$z ^L_j$最大，则 $a ^L_j$就为1，否则为0，因此 $ c =1 $的 softmax就是max的 a "softened" version of the maximum function

##  Overfitting and regularization
* 引言
诺贝尔奖获得者Enrico Fermi曾经说道："I remember my friend Johnny von Neumann used to say, with four parameters I can fit an elephant, and with five I can make him wiggle his trunk."
这段话的point就是，一个模型的 free parameters越多，它能够descrip的现象就越多
因此，一个复杂的模型即可以和当前data吻合，也可以和其他data吻合，这就意味着，这个model没法对当前的phenomenon 进行 capture any genuine insights，其直接后果就是无法generalize to new situations.
* 初识：过拟合或过训练
这样我们就很为难了，Fermi and von Neumann连对具有4个参数的模型都不满意，而一般的NN可是上万（甚至十亿多个）个参数啊！
构造一个泛化性能不好的模型也是很简单的，对于本书的Minist例子来说，如果不用五万个训练数据，而只用1000个，在使用30个hidden neuron的情况下基本上就会过拟合了，实际训练中会出现这么一种现象，就是在横轴为epoch时，训练误差会一直减小（很有可能训练精度到100%），但test 精度并不会一直增加，而是到了一定的epoch之后就不动了，也就是说，在某一个epoch之后，模型就过拟合或过训练了。
* 应对过拟合
过拟合是NN的一个 major problem。因此为了train effectively，应该想法去detect啥时候过拟合
一种简单的方法就是只观测test 精度的曲线，等它不升了就停止训练；或者当accuracy on the test data and the training data同时stop improving的时候停止训练。
更通常的做法是利用validation_data：当classification accuracy on the validation_data饱和的时候就停止训练，即**early stopping**。当然实际应用中不能立马知道啥时候饱和了，一般继续训练下去才能发现。
（实际上一般使用validation_data选择超参数）
我们来解释一下为啥使用 validation_data而不是用 test_data 来防止过拟合 因为你如果用test_data来决定啥时候停止训练的话，很可能选择的超参数就会 ** 过拟合到test_data ** ，因此一般要用 validation_data选择超参数，用 test_data来评估超参数（即模型），也就是模型的泛化性能。
这个 approach也叫做 hold out方法，即从 training_data中hold out出 validation_data。
（作者提到，这种方法最终也得靠test data来衡量性能，因此有可能我们用 validation_data选择超参数，在 test data上一看性能不行啊，再用 validation_dat选一组超参数吧，这样最后也会过拟合到 test data上，不过这个问题一般不用考虑）
*  初识： Regularization
reducing overfitting的一种方法就是增加训练数据，另一种方法就是减小NN的size，但是large networks have the potential to be more powerful than small networks，因此不采用这种方法了。
当然应对过拟合还有一些techniques，这些technique在有固定数目的训练数据和固定size的NN的情况下也可以用，即regularization techniques。
本节介绍weight decay or L2 regularization,以下就是regularized cross-entropy：$ \begin{eqnarray} C = -\frac{1}{n} \sum_{xj} \left[ y_j \ln a^L_j+(1-y_j) \ln
(1-a^L_j)\right] + \frac{\lambda}{2n} \sum_w w^2.
\tag{85}\end{eqnarray}$
当然quadratic cost也可以正则化：$ \begin{eqnarray} C = \frac{1}{2n} \sum_x \|y-a^L\|^2 +
  \frac{\lambda}{2n} \sum_w w^2.
\tag{86}\end{eqnarray}$
理解方法就是将它们看作：$ \begin{eqnarray}  C = C_0 + \frac{\lambda}{2n}
\sum_w w^2,
\tag{87}\end{eqnarray}$
正则化的效果就是让NN更prefer那些small weights，如果学习到的一组weight比较大，那么它对应的const部分必须小。因此正则化是一种折衷：between finding small weights and minimizing the original cost function。
偏微分：$$ \begin{eqnarray}
  \frac{\partial C}{\partial w} & = & \frac{\partial C_0}{\partial w} +
  \frac{\lambda}{n} w \tag{88} \\
  \frac{\partial C}{\partial b} & = & \frac{\partial C_0}{\partial b}.
\tag{89}\end{eqnarray} $$
权值更新: $$\begin{eqnarray}
  w & \rightarrow & w-\eta \frac{\partial C_0}{\partial
    w}-\frac{\eta \lambda}{n} w \tag{91} \\
  & = & \left(1-\frac{\eta \lambda}{n}\right) w -\eta \frac{\partial C_0}{\partial w}.
\tag{92} \end{eqnarray} $$
注意：这一项$ 1-\frac{\eta   \lambda}{n}$使得权值不断减小，但$ -\eta \frac{\partial      C_0}{\partial w}$可能会使其增加。
*  Regularization的其它好处
除了reduce overfitting and to increase classification accuracies之外，还能使得每次训练的结果很稳定，即 the regularized runs have provided much more easily replicable results.
原因：对于未正则化的 cost function，权值矢量有可能会变得非常大，非常大的时候呢，这些权值矢量基本上都指着同一个方向（因为changes due to gradient descent only make tiny changes to the direction, when the length is long），这就使得权值矢量无法properly explore the weight space, and consequently harder to find good minima of the cost function.
(**注意：此处的length指的是 $\|\delta^l\|$** ，这个在第五章提到了）
* 为什么正则化可以减少过拟合
一般的解释就是：smaller weights are, in some sense, lower complexity, and so provide a simpler and more powerful explanation for the data, and should thus be preferred。
一种观点就是，in science，我们一般使用simpler explanation，因为simpler explanation一般不会很巧合地出现。对于NN来说，the smallness of the weights 一般意味着the behaviour of the network won't change too much if we change a few random inputs here and there. 即 a regularized network to learn the effects of local noise in the data。而对于有大weights的NN，large weights may change its behaviour quite a bit in response to small changes in the input.
也可以这么理解：正则化使得NN只能学习到一些简单的模型，这些模型只能学习到在data中经常出现的pattern。
但对于这个 "Occam's Razor"的idea，它并不是一个general scientific principle，作者也举出两个反例，证明complex explanations也会是对的。
作者给出三个警告：1 般情况下，很难确定哪个explanation更simple，2 即使能够确定，simplicity也必须谨慎使用 3 the true test of a model is not simplicity，而是其预测新的phenomenon时的效果。
* 正则化背后的boss：泛化性能，即： the question of how we generalize
正则化既不是最好的approach，也不能帮助我们理解generalization到底是怎么回事。
作者相信，在将来，我们可以develop more powerful techniques for regularization in artificial neural networks，使得我们能够generalize well even from small data sets.
实际上，本节的NN参数已经上万了，为啥还没有过拟合呢？
一种解释就是："the dynamics of gradient descent learning in multilayer nets has a `self-regularization' effect"
* 为啥不对bias进行正则化
一般来说，对 bias进行正则化不影响结果。而且不管bias大不大，基本都不会影响neuron对于input的灵敏度。
而且大bias能够给我们的NN一些灵活性，即使得neuron更容易饱和，, which is sometimes desirable

## Other techniques for regularization
* L1 regularization
即：$ \begin{eqnarray}  C = C_0 + \frac{\lambda}{n} \sum_w |w|.
\tag{95}\end{eqnarray}$
偏微分：$ \begin{eqnarray}  \frac{\partial C}{\partial
    w} = \frac{\partial C_0}{\partial w} + \frac{\lambda}{n} \, {\rm
    sgn}(w),
\tag{96}\end{eqnarray} $
权值更新: $ \begin{eqnarray}  w \rightarrow w' =
  w-\frac{\eta \lambda}{n} \mbox{sgn}(w) - \eta \frac{\partial
    C_0}{\partial w},
\tag{97}\end{eqnarray} $
对于L1 regularization，权值只是减去一个接近0的数，而L2 regularization减去的是权值的一定比例。
因此对于小的权值，L1 regularization shrinks the weight much more than L2 regularization. 总的效果就是，L1 regularization只保留一部分在high-importance connections中的权值，而将其余权值强迫变到0.
* Dropout
它不是修改cost function，而是修改网络结构本身。
我们临时性地，随机delete掉hidden neuron的一半，然后forward-propagate，backpropagate the result, also through the modified network.这样搞完a mini-batch of examples之后，再重复以上过程，即先恢复原网络结构，再随机干掉一半，再训练。
这样，学习到的权值即使干掉一半的hidden neurons也能效果好，因此实际运行NN的时候，也应该干掉一半 hidden neurons。
这个东西为啥能够有助于regularization呢？
我们先不管dropout的详细内容。如果我们用通常的方法训练出好多NN，每一个NN都会给出different results。我们一般对其结果平均一下，The reason is that the different networks may overfit in different ways, and averaging may help eliminate that kind of overfitting.
实际上dropout这个东西，就是同时训练好多个NN，因此dropout procedure就是平均了好多个不同的NN。
另外一个解释：这个technique减少了complex co-adaptations of neurons，由于一个neuron无法特别依赖于其他neuron了，它就得learn more robust features that are useful in conjunction with many different random subsets of the other neurons.
Dropout has been especially useful in training large, deep networks, where the problem of overfitting is often acute.

* Artificially expanding the training data
这么做到：making many small rotations of all the MNIST training images,
The general principle is to expand the training data by applying operations that reflect real-world variation. 

* 岔个话题：An aside on big data and what it means to compare classification accuracies
比较算法的时候，人们都是在某些数据集上比较的，但对于不同的数据量，不同的算法效果可能差别很大。
In other words, more training data can sometimes compensate for differences in the machine learning algorithm used.
这就给我们提了个醒：很多人总是 focus on finding new tricks to wring out improved performance on standard benchmark data sets.实际上这些trick在更多数据集上很有可能没法用了，因此性能的提升很可能仅仅是历史的偶然（an accident of history）。
he message to take away, especially in practical applications, is that what we want is both better algorithms and better training data. 

## Weight initialization
如果将所有的weight和bias都这么初始化：均值为0，标准差为1，那么很有可能会出现一种情况，即大家都很大，使得hidden neuron处于饱和状态，因此权值每次更新都会特别小，学习速率很慢。
对于output neuron来说，我们可以巧妙地设计cost function，但对于hidden neuron来说就没那么好办了，因此应该好好初始化啊。
分析一下初始权值比较大的原因：我们现在只考虑一个hidden neuron的情况，假如input neuron有1000个，简化一下问题，即输入x中有500个为0,500个为1，那么这个hidden neuron 就由 500 个标准差为1 的普通neuron 和 1 个标准差为1 的bias组成，即501个标准差为1的正态分布的随机变量之和组成，其z就服从一个高斯分布，均值为0，标准差为$\sqrt{501} \approx 22.4$
因此，如果将初始权值的标准差设为$1/\sqrt{n_{\rm in}}$,而bais的标准差仍然为1，那么z的均值仍然为0，标准差为：$\sqrt{500/1000+1} \approx1.22$，这样大多数权值就很小了
## Handwriting recognition revisited: the code
作者的code风格很好，单独搞了个cost function的class：
```
class CrossEntropyCost(object):
 
    @staticmethod
    def fn(a, y):
        return np.sum(np.nan_to_num(-y*np.log(a)-(1-y)*np.log(1-a)))
 
    @staticmethod
    def delta(z, a, y):
        return (a-y)
```
这个很值得学习嘛。
另外作者很感慨，实现 weight decay的也就一行代码而已，But although the modification is tiny, it has a big impact on results!
>We've spent thousands of words discussing regularization. It's conceptually quite subtle and difficult to understand. And yet it was trivial to add to our program! It occurs surprisingly often that sophisticated techniques can be implemented with small changes to code.


## 选择超参数  How to choose a neural network's hyper-parameters?
* 时运不济，命途多舛
超参数一开始很容易选的不恰当。而且 It's easy to feel lost in hyper-parameter space.
如果花了很长时间都没啥结果，那么，If the situation persists, it damages your confidence. Maybe neural networks are the wrong approach to your problem? Maybe you should quit your job and take up beekeeping?
* 本节目的
help you develop a workflow that enables you to do a pretty good job setting hyper-parameters.

* Broad strategy
首先，你的结果得比trivial算法的结果好（the first challenge is to get any non-trivial learning），即要比随机猜测好。
出了问题怎么办？人生经验：**将问题简化，即将问题规模减小，从而可以更快速地尝试各种参数**
这个简化是随问题而定的，如对于minist数据集来说，我可以只训练0和1这俩数字的image，可以先不包含隐含层，将validation images减少，从而可以更快地进行 monitoring。
你只要试出来的结果比随机猜测好，那么你就有信心继续往下调了。As with many things in life, getting started can be the hardest thing to do.
* Learning rate
我们可以用三个值试一下，画出他们仨对应的cost-epoch曲线，从而选一个合适的范围。
* Use early stopping to determine the number of training epochs
好消息就是， training epochs不依赖于其他超参数。
To implement early stopping we need to say more precisely what it means that the classification accuracy has stopped improving.
但这也不好判断嘛，更好的方法就是best classification accuracy doesn't improve for quite some time。
I suggest using the no-improvement-in-ten rule for initial experimentation, and gradually adopting more lenient rules, as you better understand the way your network trains: no-improvement-in-twenty, no-improvement-in-fifty, and so on. 

* Automated techniques
手动调参容易建立对于how neural networks behave的直觉。
当然也有自动调参的，如grid search， Bengio大神12年有一篇paper用来讲achievements and the limitations of grid search，即Random search for hyper-parameter optimization
12年还有一篇用Bayesian来调参的，Practical Bayesian optimization of machine learning algorithms 还有源码： https://github.com/jaberg/hyperopt
* 总结一下
调参的困难在于，每个人对于调参的理解都不太一样，而且不同的人的方法甚至有冲突（many papers setting out (sometimes contradictory) recommendations for how to proceed）
当然还有一些paper进行trick大汇总：Practical recommendations for gradient-based training of deep architectures, by Yoshua Bengio (2012).
Efficient BackProp, by Yann LeCun, Léon Bottou, Genevieve Orr and Klaus-Robert Müller (1998)
还有一本书：Neural Networks: Tricks of the Trade, edited by Grégoire Montavon, Geneviève Orr, and Klaus-Robert Müller.

## Other techniques
* 引言
本章介绍的那些technique啊，一部分原因是因为这些technique的确很重要，但The larger point是让我们熟悉一下NN中那些出现的问题。
*  Hessian technique
BP只用了$C(w+\Delta w)$的一阶展开，而 Hessian technique用到了一阶和二阶项。即：$ \begin{eqnarray}
  C(w+\Delta w) \approx C(w) + \nabla C \cdot \Delta w +
  \frac{1}{2} \Delta w^T H \Delta w.
\tag{105}\end{eqnarray}$
权值更新：$ \begin{eqnarray}
  \Delta w = -H^{-1} \nabla C.
\tag{106}\end{eqnarray}$
有一些theoretical and empirical results表明 Hessian technique比BP收敛快。由于采用了cost function的二阶信息，因此 Hessian technique避免了BP的很多不足。但 it's very difficult to apply in practice.其中一个原因就是计算量太大了。
*  Momentum-based gradient descent
这个东西inspire自Hessian technique，但不需要计算大矩阵。有梯度信息，也有information about how the gradient is changing.
关键就是增加了一个速度项，使得梯度直接作用于速度项，然后速度项再和权值直接挂钩，即冲量-速度-位置这么一个关系。

## Other models of artificial neuron
现在比sigmoid network效果好的model多的是啊，而且他们还learn faster, generalize better to test data, or perhaps do both.
一种就是tanh (pronounced "tanch") neuron，即$ \begin{eqnarray}
  \tanh(z) \equiv \frac{e^z-e^{-z}}{e^z+e^{-z}}.
\tag{110}\end{eqnarray}$
实际上它就是：$ \begin{eqnarray}
  \sigma(z) = \frac{1+\tanh(z/2)}{2},
\tag{111}\end{eqnarray}$
即只是将sigmoid给rescale一下，到[-1,1]
* tanh产生的原因
由于sigmoid中权值更新是$a^l_k \delta^{l+1}_j$,由于 $a^l_k$始终为正， 因此 $a^l_k \delta^{l+1}_j$只取决于$ \delta^{l+1}_j$，因此和连接到同一个neuron的权值会同时增大或减小，这样很不爽嘛。
而tanh的好处在于 $a^l_k$可正可负。
* 那种neuron更好？
现在没有证据表明谁学习更快，泛化性能更好
* ReLU：rectified linear neuron or rectified linear unit
即：$ \begin{eqnarray}
  \max(0, w \cdot x+b).
\tag{112}\end{eqnarray}$
这哥们儿的梯度就是x，因此永不饱和嘛。

## On stories in neural networks
In many parts of science ，越是简单的现象， it's possible to obtain very solid, very reliable evidence for quite general hypotheses.

但NN有大量的参数，而且参数间还有相互作用，因此很难establish reliable general statements
完全理解NN其实就是tests the limits of the human mind。因此大家都在更新各种结论。
没有人能够investigate all these heuristic explanations in depth.
Does this mean you should reject heuristic explanations as unrigorous, and not sufficiently evidence-based? No! In fact, we need such heuristics to inspire and guide our thinking. 
这就和大航海时代一样，不断发现，不断修正认知。
it's more important to explore boldly than it is to be rigorously correct in every step of your thinking.
we need good stories to help motivate and inspire us, and rigorous in-depth investigation in order to uncover the real facts of the matter.



 

































