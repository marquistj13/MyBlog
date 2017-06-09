--- 
title:  Clustering by Passing Messages Between Data Points
date:   2017-6-9
---



* content
{:toc}

大名鼎鼎的'AffinityPropagation'，其地位可以通过 [此页面的运行效果图](http://scikit-learn.org/stable/auto_examples/cluster/plot_cluster_comparison.html#sphx-glr-auto-examples-cluster-plot-cluster-comparison-py) 来体现。
从图中可以看出它仍然无法hold住nonlinear的shape。

原始论文介绍的有点复杂了，还是 [维基百科的介绍](https://en.wikipedia.org/wiki/Affinity_propagation) 比较好懂啊。 还有 [这位的博客](https://wenkefendou.gitbooks.io/machine-learning/content/affinity_propagation.html) 引用了知乎上的解答，很好理解, 还有 [zhang大神的博客Deciding the Number of Clusterings](http://freemind.pluskid.org/machine-learning/deciding-the-number-of-clusterings/).

论文里只能拿application （ computer vision and computational biology tasks ）来展示效果了，要不然会被人喷 nonlinear shape啊，作者这么搞就是说我能在这几个复杂应用中work。