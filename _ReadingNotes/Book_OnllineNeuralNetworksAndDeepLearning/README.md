* 这是什么
这是我阅读[Neural Networks and Deep Learning](http://neuralnetworksanddeeplearning.com/index.html)的笔记。
为了方便阅读，我在每一章前面都加了个数字，方便排序。
读书时间： [2016-12-27 周二]- [2017-01-12 周四]

* 我读此书有何期望
我已有ML的基础知识，目前在研究聚类。
聚类作为无监督学习，一个非常大的不便之处在于这个圈子没有共识，我指的是在“聚类算法应该是怎么样子的”这个fundamental的问题上而言没有共识：聚类算法A要求必须指定cluster的数目（如Kmeans），聚类算法B只需要指定一堆点需要满足什么条件（如DBSCAN的密度定义）才能构成一个cluster，等等。
目前很多聚类算法对于input data的要求是很高的，即必须得有好的representation。当然，很多聚类算法的assumption就是这么严格，所以才会出现那些将已有算法进行scale到大数据的work吧。
在了解聚类领域的“无可奈何”之后，那么能不能同时learn representation+聚类呢？很明显这个问题是ill-imposed，即这些representation的学习不能太随意，正如[Unsupervised Deep Embedding for Clustering Analysis](http://icml.cc/2016/reviews/231.txt)的review1所言：
>My biggest concern is that the problem of simultaneously clustering and learning an effectively unconstrained nonlinear embedding seems ill-posed… there is no clear way to define what it means to be a “good clustering” if the underlying metric is allowed to change arbitrarily since I can always move points originally close to each other to be far apart.  If clustering in an embedding space, it seems like we should at least ask that the embedding function be topology-preserving — what this means in practice is that we need a way to make sure that the embedding function preserves local neighborhood structure (small distances should stay small even after mapping). 

 但这个东西困难并不能说明不能做是吧。 看到DL在representation Learning方面的巨大成功，我也想看看这个东西能不能排上用场，这样就会使得聚类算法的“易用性”以及应用范围大大扩展吧，最起码就能够实现End2End啦。
 因此我期望阅读此书得到“DL到底是什么”这种最基本的认知，以期将其应用于聚类算法的研究。

* 我已看过DL的哪些文献
[1]Y. LeCun, Y. Bengio, and G. Hinton, “Deep learning,” Nature, vol. 521, no. 7553, pp. 436–444, May 2015.
[2]J. Schmidhuber, “Deep learning in neural networks: An overview,” Neural Networks, vol. 61, pp. 85–117, Jan. 2015.
看完这俩就能对本书的内容有个定位啦。

* 阅读此书的感想
本书的作者实在会讲故事，我最佩服的是作者能够有信心保证本书介绍的东西是DL里边非常fundamental的idea。正如作者在第六章末尾所言，你掌握了这些idea，再理解其他东西就很容易了。作者对于这些基本idea的把握实在是特别到位，能够在纷杂的technique中抓住这些本质的东西实在难得。
好了，夸完了。我花了两周多看这本书，昨天刚看完第六章，我现在只是清晰地记得前几章中的一句话：
>Technologies come and technologies go, but insight is forever.

 其次就是模模糊糊的idea：BP是怎么回事，梯度下降是怎么回事，NN发展中各种问题的发现和解决trick。当然最清晰的还是第六章末尾啦。NN和DL现在正处于很原始的阶段，距离general AI还很遥远。对此situation清晰刻画的一个工具就是Conway’s law，而Conway’s law对这个领域的借鉴作用就是：researchers得搞出更多deep ideas才能将这个领域支撑起来，这个路途还是很exciting啊！
 
* 我没有做到的东西
很惭愧，好多书中的problem我都没做呢。现在给自己找的借口就是“我还有研究需要做，不需要折腾这些细节”，不过细细想来还是站不住脚啊，这个东西还是逃不掉的啊，少年！算了，先这么过去吧……
