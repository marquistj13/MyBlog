---
title:  第六章
---


* content
{:toc}

CHAPTER 6 Deep learning

## 引言
上一章我们知道了DNN比SNN难训练多了。
在本章，我们要develop techniques以训练DNN，并展望NN以及AI的未来。
本章的focus：理解DNN背后的一些core principles，并将其应用于mnist数据集上。
理解了本章解释的这些fundamental，就很容易理解很多work了。
## 引入卷积网络
我们在前几章用的都是全连接的layer来分类图像，但这么做有点strange。因为这种网络结构并没有考虑到图像的spatial structure。
解释一下就是：我们不是将图像展开成784个点了嘛，这样距离不一样的input pixel地位都一样，因此spatial structure必须得从训练数据中进行infer才能得到。
而convolutional neural networks作为一种新的网络结构，则直接钦定了网络必须显式地考虑这种spatial structure。 这个结构的好处就是，卷积网络能够很快地训练（作者后边提到大概是普通DNN的3倍吧），训练快的好处就是能够训练多层网络啦。
## 卷积网络的three basic ideas: local receptive fields, shared weights, and pooling
* local receptive fields
在全连接的layer中，我们认为输入就是一个长条状的东西，而在卷积网络中，我们应该将其认为是$28\times28$的一个方框的neuron，这个方框的每一个格点代表一个像素值。
在本例中，卷积层hidden layer的每一个neuron对应于输入层方框的一个 $$5 \times 5$$ 的一个区域，即25个像素点，这个区域就叫做**local receptive fields**
（强调一下，这个local receptive fields对应的是input image的一小块像素值，其实就是一个窗体。
这个窗体可以往右移动，也可以往下移动，每移动一次就对应hidden layer的一个neuron。当然，移动的步长也是随意指定的，以下的分析中，我们默认步长为1）
对于$28\times28$的输入来说，$5\times5$的窗体可以往右移动23次，因此横向总共有24个窗体，纵向也是，故hidden layer总共有$24\times24$个neuron。


* shared weights and biases
在卷积网络中，local receptive fields对应的权值是一样的，在上例中，对于hidden layer的第$j,k$个neuron,其输出为：$\begin{eqnarray} 
  \sigma\left(b + \sum_{l=0}^4 \sum_{m=0}^4  w_{l,m} a_{j+l, k+m} \right).
\tag{125}\end{eqnarray}$
注意，$a_{x,  y}$是$x,y$处的input activation。
这就意味着，这个hidden layer检测的是同一种feature，如这个$5\times5$的区域中是否存在竖线等。如果我们定义 input layer to the hidden layer 的映射为**feature map**，那么，显然一个feature map一般是不够的，我们如果定义三个feature map的话，那么这个hidden layer的neuron数目就是$3\times24\times24$，顺便提一下，由于feature map是在input image的各个区域都要来一遍的，因此它具有平移不变性。
如果用feature map的权值值作为灰度值，那么我们就能可视化学习到的feature map了，作者通过一个20个feature map的例子说明了，这些学习到的feature map很明显不是随机的值，而是有明显的结构，但是我们很难猜出来这些权值的意义。关于这类work，作者提到一篇文章：Visualizing and Understanding Convolutional Networks by Matthew Zeiler and Rob Fergus (2013).
共享eights and biases的好处很明显：减少了卷积网络的参数，如果我们用20个feature map，总共需要$20\times (5\times 5+1)=520$个参数，而如果采用普通的网络结构，隐含层有30个neuron的话，得需要大概$784\times 30+30=23550$的参数，相差40倍啊！当然这个是不能直接比的，但很明显**卷积层利用平移不变性大大减少了参数**，使得训练速度加快。


* Pooling layers
这个层一般紧接着卷积层，用来简化卷积层的information，搞出一个condensed feature map，例如我们可以将卷积层的一个$2\times2$的neuron给summarize一下，可以用**max-pooling**，即取$2\times2$输入区域中的最大值。易得，$24\times24$个neuron就会变成$12\times12$的neuron。
可以这么理解Pooling layers：你这个卷积层不是用来检测输入图像有啥特征么，就是看一下这个区域有没有一个给定的特征，而且不要位置信息啦。
也可以使用**L2 pooling**，即这个$2\times2$的平方和。


* 总结一下
乍一看，这个卷积网络的结构和以前的有很大区别嘛，但是哈，the overall picture is similar: 网络都是由一些基本单元组成，这些基本单元的behavior取决于它们的权值和bias；并且，the overall goal is still the same: 训练这些权值和bias是的网络能够好好分类。


## 实现卷积网络
作者使用Theano来实现，因为 Theano很方便实现卷积网络的BP，因为它能够自动计算所有的映射。 Theano也很快，还支持GPU。
作者在设定baseline的时候提到，regularization对于性能的提升很有限，因此一般先不管它。
baseline的效果是97.80，用一个卷积层是98.78，用两个是99.06。
作者提到，用两个卷积层也是有意义的，因为第一个卷积层得到的东西有可能还保留很多spatial structure，因此还能用第二个卷积层进一步处理。


* 使用ReLU
我们上面实现的卷积网络其实就是"Gradient-based learning applied to document recognition", by Yann LeCun, Léon Bottou, Yoshua Bengio, and Patrick Haffner (1998). 即LeNet-5的一个变种。
本节使用rectified linear units以及 l2 regularization来进一步提升性能。得到了99.23 percent的好成绩。
作者很感慨啊，实际中，使用ReLU基本上都能提升性能，那么这个ReLU为啥这么神奇呢？目前对于这个问题的理解还是很poor的，当然有一个经验解释，ReLU的不饱和特性使得它能够持续学习。


* 扩展训练数据
通过左移右移上移下移某个像素，可以扩展训练集，有效防止过拟合，得到了99.37 percent 的效果。
当然还有一些扩展方法，如Best Practices for Convolutional Neural Networks Applied to Visual Document Analysis, by Patrice Simard, Dave Steinkraus, and John Platt (2003).通过平移旋转skew等各种变小，哈哈，而且还搞出一种"elastic distortion"来模仿人类写字时的抖动。作者说，这篇论文性能提升的关键就是扩展训练集啊。


* 再加一个全连接层
效果是99.43，提升不是很明显么，作者就怀疑是不是过拟合得好好管一下啦。因此使用 dropout technique搞一下，结果是99.6


* 使用网络ensemble
我们可以训练5个不同的NN，它们的区别仅仅是初始值不一样。尽管这些NN有相似的精度，但由于它们犯得错误可能不一样（归根到底都是初始化不一样啦），因此可以让这5个NN进行表决得到结果。
作者提到，这种ensembling是一种common trick （在NN和其他ML领域都有哈），这时候准确率到了99.67，即一万个测试图像中只有33个分错了。注意这33个图像中的很多个即使是人类都很容易分错。


* 为啥只在全连接层使用Dropout
原则上卷积层也可以用，但是卷积层已经有considerable inbuilt resistance to overfitting了，因为贡献权值意味着convolutional filters（即feature map）已经强迫学习整个image了，这就使得它们不太可能学习到一些训练数据的局部特写，因此没有必要在卷积层使用regularizer，如dropout。


* 性能永无止境
一个哥们儿维持了一个网友http://rodrigob.github.io/are_we_there_yet/build/classification_datasets_results.html 用来统计mnist等数据集上的效果的paper。
只要在这些paper中深挖，你会发现很多interesting technique的，而且实现起来也很爽。 **这么做的时候，记着要先实现一个简单的能够很快训练的NN，这样能够帮助你快速理解what is going on**.
作者提到一个好玩的，在Deep, Big, Simple Neural Nets Excel on Handwritten Digit Recognition, by Dan Claudiu Cireșan, Ueli Meier, Luca Maria Gambardella, and Jürgen Schmidhuber (2010).这篇paper中，没有使用卷积层，也就是说，这个网络在80年代也是可以实现的（只是当时的计算能力有限）。It's a fun exercise to try to match these results using an architecture like theirs.


* 为啥我们能够训练
我们在上一章看到，在DNN中梯度一般unstable的问题，那么问题来了，How have we avoided those results?
答案是我们并没有避免这些结果。我们只是做了一些a few things that help us proceed anyway。其中包括1.使用卷积层减少参数2.使用更powerful的正则化技巧（如dropout and convolutional layers）来减少过拟合3.使用ReLU来加速训练（3到5倍）4.使用GPU训练很长时间。
当然我们也用了其他idea：利用大量数据集，调教好的cost，好的初始化，增加训练数据


* 你用的这些网络能算深么
我们上面的例子中，只用了4个隐含层，这还能叫DNN嘛？
实际上4个隐含层比早期的那些1个隐含层的、偶尔2个隐含层的NN深多了。再说了，15年的state-of-the-art 也只是才dozens of hidden layers而已。
有人说了，你的hidden layer没我多哈，你搞的就不是真正的深度学习哈。
其实这个说法很目光短浅啊，这种定义其实就相当于依赖于当前大家都在搞的深度。The real breakthrough in deep learning was to realize that it's practical to go beyond the shallow 11- and 22-hidden layer networks that dominated work until the mid-2000s. 
这个breakthrough是很significant的，开启了对于much more expressive models的探索的大门。layer的数目并不是多么有意义，意义在于这些更深的网络能够用来实现其他目标，如更高的分类精度。


* 训练不易，且行且珍惜
在本书中，你会感觉作者训练网络是很容易的，大错特错啊，I can guarantee things won't always be so smooth. 
作者的建议是Getting a good, working network can involve a lot of trial and error, and occasional frustration. In practice, you should expect to engage in quite a bit of experimentation. 


## Recent progress in image recognition
* 引言
在98年引入了mnist数据集，当时一般得花费数周的时间达到的效果还不如现在GPU上不到一个小时训练的结果。
因此这个数据集没法pushes the limits of available technique啦。 而只能用来for teaching and learning purposes。
因此modern work involves much more challenging image recognition problems


* 本节风格提示
本书的风格就是关注于那些具有 lasting interest 的 ideas such as backpropagation, regularization, and convolutional networks，没去管那些很时髦的东西。 有人就说了，你现在将的那些image recognition 不也是时髦的东西么，你还讲它作甚？
这种说法也对哈，很多paper的finer details都会变得没啥用了，但DNN在image recognition 还是有很大的进展的，试想一下，假如一百年后有人要回顾历史，它们肯定会将2011到现在的这段时期作为由DNN推动的huge breakthroughs的时期。这意味着一个important transition 正在发生。因此以下我们要了解一些正在发生的exciting discoveries。


 * The 2012 LRMD paper
这篇paper，Building high-level features using large scale unsupervised learning, by Quoc Le, Marc'Aurelio Ranzato, Rajat Monga, Matthieu Devin, Kai Chen, Greg Corrado, Jeff Dean, and Andrew Ng (2012).简称LRMD。
这篇文章是用来分类 ImageNet的。达到了respectable 15.8 percent的精度，以前只能达到9.3啊。
 
 * The 2012 KSH paper
 这篇ImageNet classification with deep convolutional neural networks, by Alex Krizhevsky, Ilya Sutskever, and Geoffrey E. Hinton (2012).正好follow的上一篇LRMD paper。而且使用的是competition dataset。
 由于一个图片中可能有很多个物体，因此，只有你的分类器给出5个结果，只要正确结果在这5个里边就算你分对了。KSH的结果是84.7！而如果更严格一点，分类器只给出一个结果的话，准确率也达到了63.3.
 这篇文章inspired much subsequent work.而且用了俩GPU。用的是ReLU，使用随机cropping的strategy来扩大数据集，使用了a variant of l2 regularization, and dropout，使用 momentum-based mini-batch stochastic gradient descent.
 当然也可以看Alex Krizhevsky's cuda-convnet（Theano-based large-scale visual recognition with multiple GPUs, by Weiguang Ding, Ruoyan Wang, Fei Mao, and Graham Taylor (2014).）及其后续作品。还有Theano版本的代码https://github.com/uoguelph-mlrg/theano_alexnet 。而且Caffe也实现了KSH
 
 * The 2014 ILSVRC competition
 赢家是这篇Google的*Going deeper with convolutions, by Christian Szegedy, Wei Liu, Yangqing Jia, Pierre Sermanet, Scott Reed, Dragomir Anguelov, Dumitru Erhan, Vincent Vanhoucke, and Andrew Rabinovich (2014).用了22层！精度93.33！比13年的88.3和12年的84.7强了很多。
 14年还有这个竞赛的survey paper：ImageNet large scale visual recognition challenge, by Olga Russakovsky, Jia Deng, Hao Su, Jonathan Krause, Sanjeev Satheesh, Sean Ma, Zhiheng Huang, Andrej Karpathy, Aditya Khosla, Michael Bernstein, Alexander C. Berg, and Li Fei-Fei (2014).这篇文章提到，93.33已经和人类不相上下了。
 自此以后，有人将误差讲到了5.1%，因此就有媒体说击败了人类，实际上这些结果能够得出来战胜了人类的结论，是很误导人的。这个ILSVRC challenge 仅仅是一个很limited的问题，我们距离solving the problem of image recognition or, more broadly, computer vision还很遥远。
 
 * "adversarial" images 
  在文章Intriguing properties of neural networks, by Christian Szegedy, Wojciech Zaremba, Ilya Sutskever, Joan Bruna, Dumitru Erhan, Ian Goodfellow, and Rob Fergus (2013)中，提到，对于很牛逼的KSH，只要在一些能够正确分类的图像上稍微变一下就能欺骗分类器，使得分类错误。
  这就意味着，我们学习到的分类器是很离散的，即输入很离散。但也没有必要灰心丧气，因为这些"adversarial" images的出现概率是很小的。
  这篇文章有很多followup work如Deep Neural Networks are Easily Fooled: High Confidence Predictions for Unrecognizable Images, by Anh Nguyen, Jason Yosinski, and Jeff Clune (2014)提到，有些人类认为是白噪声的图片，分类器很可能将其认为是某些类。
  
  * 不必伤心
   虽然以上这些结果很讨厌，但the overall picture is encouraging，我们在一些很困难的benchmark上效果越来越好，这是很encouraging的、但 When such fundamental problems are still being discovered (never mind solved), it is premature to say that we're near solving the problem of image recognition. At the same time such problems are an exciting stimulus to further work.
   
## DNN的其他approach
* 引言
我们上面遇到的mnist问题是一个juicy problem，它forced us to understand many powerful ideas: stochastic gradient descent, backpropagation, convolutional nets, regularization, and more. But it's also a narrow problem.
看文献的时候会碰到recurrent neural networks, Boltzmann machines, generative models, transfer learning, reinforcement learning等东西，但没关系many important ideas are variations on ideas we've already discussed, and can be understood with a little effort.


* RNN
咱们以前碰到的都是feedford的，即一个input完全确定了所有neuron的activation
t's a very static picture: everything in the network is fixed, with a frozen, crystalline quality to it.
如果令hidden layer的behavior也取决于前一层layer的好几个时刻的activation，那么就得到了recurrent neural networks or RNNs.
RNN有很多数学形式，在维基上https://en.wikipedia.org/wiki/Recurrent_neural_network 已经列了13个啦。 RNN的broad idea就是在普通NN中加入了dynamic change over time的notion。


 * RNN的玩儿法
一种玩儿法就是用它来实现一些traditional ways of thinking about algorithms, ways of thinking based on concepts such as Turing machines and (conventional) programming languages. 14年有一个paper用RNN来识别简单的Python代码，还有一篇14年的paper develop了一个what they called a neural Turing machine (NTM)，用它来实现简单的程序如排序和幅值
还有一种玩儿法就是和conventional algorithmic approaches 进行互补。It'd be great to develop unified models that integrate the strengths of both neural networks and more traditional approaches to algorithms. RNNs and ideas inspired by RNNs may help us do that.
RNNs have been used to set new records for certain language benchmarks.


 * RNN的work机理以及LSTM
很多feedforward的NN的idea都可以直接用到RNN中。
RNN不好训练，原因就是梯度的unstable，将long short-term memory units (LSTMs)的idea 嵌入到 RNNs知乎就很容易得到好的结果（易训练了）。


* Deep belief nets, generative models, and Boltzmann machines
DL始于2006的一篇解释deep belief network (DBN)的paper，（ A fast learning algorithm for deep belief nets, by Geoffrey Hinton, Simon Osindero, and Yee-Whye Teh (2006), as well as the related work in Reducing the dimensionality of data with neural networks, by Geoffrey Hinton and Ruslan Salakhutdinov (2006).）
但DBN现在已经不火了，作者认为DBN有很多有趣的性质。1. 其一就是，DBN是一种生成模型，即有一种特殊的玩儿法  "run the network backward", generating values for the input activations.  即，生成模型更像人脑：可以读数字，也可以写数字。In Geoffrey Hinton's memorable phrase, **to recognize shapes, first learn to generate images**. 2. 其二就是，可以进行无监督和半监督学习
DBN可以用来学习到理解其他图像的一些有用特征。
但为啥DBN不火了呢？
一部分原因是 feedforward and recurrent nets 太强大了。因此大家都一窝蜂去搞这俩货了。作者说，这是历史规律，没办法的
>There's an unfortunate corollary, however. The marketplace of ideas often functions in a winner-take-all fashion, with nearly all attention going to the current fashion-of-the-moment in any given area.  


  作者说了，在当前unfashionable ideas上进行work是很难的，即使这些ide很明显是of real long-term interest. 作者认为，DBN这些生成模型理应得到更多关注
  
* Other ideas
除了用来做NLP，机器翻译，等之外，还有一篇paper：Playing Atari with Deep Reinforcement Learning将深度卷积网络和强化学习RL结合起来去学习玩video游戏。（这篇paper还有一篇nature的followup：http://www.nature.com/nature/journal/v518/n7540/abs/nature14236.html）
作者认为这个东西牛逼在这个this system is taking raw pixel data - it doesn't even know the game rules! 并且，能够从data中学习到高质量的决策，这些决策的规则是非常复杂的。That's pretty neat.


## NN的未来
* 用户界面的Intention-driven化
在谷歌搜索的时候，你拼错了，搜索引擎会给你自动修正再去搜索，而不是傻傻地用你提供的关键词去搜索。换句话说，谷歌搜索试图去猜测你的真实搜索的intention，即这是an intention-driven user interface.
即使在05年的时候，人们还是想当然地认为你和computer交互的时候必须得提供准确的信息，错一个标点都不行啊。当然，作者期望未来intention-driven user interfaces那个极大改变人机交互的方式。

* Machine learning, data science, and the virtuous circle of innovation
ML除了用来构建intention-driven user interfaces之外还可以用于data science，即用来发现the "known unknowns" hidden in data. 
作者断言，将来ML的the biggest breakthrough 将不会仅仅是conceptual breakthrough，而是能够用于产生利润的ML research，through applications to data science and other areas. 

* NN 和 DL的role
以上两条讨论了，ML能够为technology创造新的机遇。在这个过程中，我们的 NN 和 DL要扮演啥角色呢？
要回答这个问题,it helps to look at history。在80年代，NN如日中天，尤其是BP广为人知的时候，但在90年代，ML的旗帜传给了其他technique，如SVM。如今NN再度辉煌，独孤求败。但谁又能保证过几天又有新的approach能够横扫NN呢？也许NN一直都没人取代其位置？
因此，我们应该思考的是ML的未来，这样比直接思考NN容易多了。部分原因就是NN的很多问题，我们理解的都很poor，如为啥NN能在这么多参数的情况下还不过拟合，SGD为啥能work等，这些问题没有回答好就意味着NN在ML的将来的role是很不确定的。
作者做了一个预测：作者坚信，DL仍然会stay。因为NN这种学习层次概念、逐步抽象的的能力seems to be fundamental to making sense of the world.当然以后NN可能不是这种样子了，也许架构变了，学习算法变了，到时候我们都不认为它是NN了，但它们仍然在做DL。

* NN和DL能够很快lead to AI么
本书中，我们用NN做的都是分类问题，我们很好奇啊，NN和DL能够解决general AI的问题么？general AI 是不是马上就实现了？
这个问题的回答依赖于 **Conway's law**
>Any organization that designs a system... will inevitably produce a design whose structure is a copy of the organization's communication structure.  

 翻译一下：你这个组织design的一个system，实际上很大程度上取决于你这个组织的通信结构，也就是谁参与了设计。
 作者强调了一下， we should understand Conway's law as referring only to those parts of an organization concerned explicitly with design and engineering.
 理解这个东西的关键在于，我们要意识到，现实中很多人没有按照这个law来办事。很多team在设计新产品的时候一般要么用老一堆人马，要么干脆就没有对应知识的人才，这样设计出来的产品很明显有很多臃肿的东西，或者有很大缺陷。很明显这是因为一种不匹配，即设计这么一个产品需要一个满足很多条件的team，但实际组建team的时候是不满足要求的。Conway's law may be obvious, but that doesn't mean people don't routinely ignore it.
 Conway's law适用于这种情况：我们这队这个东西有啥组成，到底咋build但AI显然不是这么一个问题，我们不知道AI到底该由啥组成，也就是说，当前，AI is more a problem of science than of engineering. 如果波音747设计的时候不知道喷气式引擎或者空气动力学，显然我们就不知道该聘请谁来设计飞机啦。**As Wernher von Braun put it, "basic research is what I'm doing when I don't know what I'm doing".**
 但Conway's law也是可以借鉴的。To gain insight into this question, consider the history of medicine. 一开始只有几个人懂这个东西，但But as our knowledge grew, people were forced to specialize. 等我们搞出很多deep new idea的时候，如细菌致病，抗生素机理等，一些新的领域如epidemiology, immunology,就形成了，因此我们的知识结构决定了 the social structure of medicine. 
 在很多well-established sciences有一个common pattern：这些领域一开始是一整块的，只有一些deep ideas。Early experts can master all those ideas. 但随着更多deep ideas被发现， too many for any one person to really master. 这时候这个领域的社会结构也会重组，出现很多子领域，他们的organization mirrors the connections between our deepest insights。
 >And so the structure of our knowledge shapes the social organization of science. But that social shape in turn constrains and helps determine what we can discover. This is the scientific analogue of Conway's law.
 
 在AI的早期，经常有人说
 >"Hey, it's not going to be so hard, we've got [super-special weapon] on our side", countered by "[super-special weapon] won't be enough".
 
 这些[super-special weapon] 一直在变，以前就是logic, or Prolog, or expert systems，现在就是DL。这些 super-special weapon都曾经很牛逼，现在DL也很牛逼，但DL保不准也会和这些东西一样？How can we tell if deep learning is truly different from these earlier ideas? Is there some way of measuring how powerful and promising a set of ideas is?**Conway's law 告诉我们，可以通过一个rough and heuristic proxy metric来衡量这些idea相关联的social structure 的复杂度**。
 当然只需要解决两个问题就行了。
 
 * 对于这个metric of social complexity来说，DL的这些idea有多么powerful？
   目前来看，DL还是一个非常relatively monolithic field。There are a few deep ideas, and a few main conferences, with substantial overlap between several of the conferences. 很多paper的idea都很基本，用SGD来优化一个cost function。但我们还没有很多well-developed subfields, each exploring their own sets of deep ideas, pushing deep learning in many directions. 
   因此就metric of social complexity来说，DL还是一个很shallow的field。
   It's still possible for one person to master most of the deepest ideas in the field.

 * 我们要build a general artificial intelligence需要多么powerful的theory呢？
   这个问题的答案没有人知道。可以肯定的是，还得需要很多deep ideas才能搞一个general artificial intelligence
   >And so Conway's law suggests that to get to such a point we will necessarily see the emergence of many interrelating disciplines, with a complex and surprising structure mirroring the structure in our deepest insights. We don't yet see this rich social structure in the use of neural networks and deep learning. And so, I believe that we are several decades (at least) from using deep learning to develop general AI.
   
  * 还是要exciting啊
  作者认为，DL还是有一些没有发现limit的 powerful technique以及many wide-open fundamental problems.
  That's an exciting creative opportunity.
