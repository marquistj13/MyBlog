---
layout: post
title:  TensorFlow 基本函数
categories: 深度学习
tag: [Tensorflow]
---

* content
{:toc}


###  tf.slice
```py
slice(
    input_,
    begin,
    size,
    name=None
)
```

举例：
```python
# 'input' is [[[1, 1, 1], [2, 2, 2]],
#             [[3, 3, 3], [4, 4, 4]],
#             [[5, 5, 5], [6, 6, 6]]]
tf.slice(input, [1, 0, 0], [1, 1, 3]) ==> [[[3, 3, 3]]]
tf.slice(input, [1, 0, 0], [1, 2, 3]) ==> [[[3, 3, 3],
                                            [4, 4, 4]]]
tf.slice(input, [1, 0, 0], [2, 1, 3]) ==> [[[3, 3, 3]],
                                           [[5, 5, 5]]]
```

第一个输出是`[[[3, 3, 3]]]`
我们分析一下,`begin=[1, 0, 0]`，第一个维度从第一个开始（0-based），第二三个维度从第0个开始。`size=[1, 1, 3]`,即：
第一个维度从第一个开始取出来1个，也就是说取出来
`[[[3, 3, 3], [4, 4, 4]]]`
第二个维度从0开始取出了一个也就是`[[[3, 3, 3]]]`
第三个维度全取出来，即`[[[3, 3, 3]]]`


如果是`tf.slice(input, [1, 0, 1], [1, 2, 2])`呢？
根据同样的分析：
第一个维度取出一个就是`[[[3, 3, 3], [4, 4, 4]]]`
第二个维度从0开始取出来两个就是`[[[3, 3, 3], [4, 4, 4]]]`
第三个维度从1开始取出两个`[[ 3, 3], [ 4, 4]]]`

可以通过以下脚本验证：
```python
import tensorflow as tf
pts=tf.constant([[[1, 1, 1], [2, 2, 2]],
            [[3, 3, 3], [4, 4, 4]],
             [[5, 5, 5], [6, 6, 6]]])
sess = tf.Session()
sess.run(tf.slice(pts,[1, 0, 1], [1, 2, 2]))             
```
输出就是`array([[[3, 3],
        [4, 4]]])`

当然为了，更明显，我们将原pts换一下数据：
```python
pts=tf.constant([[[1, 2, 3], [4, 5, 6]],
            [[7, 8, 9], [21, 22, 23]],
             [[24, 25, 26], [27, 28, 29]]])
sess.run(tf.slice(pts,[1, 0, 1], [1, 2, 2]))
```
此时输出就是，`array([[[ 8,  9],
        [22, 23]]])`


### tf.expand_dims
在tensor's shape中插入一个1
```py
# 't' is a tensor of shape [2]
shape(expand_dims(t, 0)) ==> [1, 2]
shape(expand_dims(t, 1)) ==> [2, 1]
shape(expand_dims(t, -1)) ==> [2, 1]

# 't2' is a tensor of shape [2, 3, 5]
shape(expand_dims(t2, 0)) ==> [1, 2, 3, 5]
shape(expand_dims(t2, 2)) ==> [2, 3, 1, 5]
shape(expand_dims(t2, 3)) ==> [2, 3, 5, 1]
```

### tf.reduce_sum
Computes the sum of elements across dimensions of a tensor.
和np的sum一样啊，只不过参数多了一点，多了个keep_dim的参数，不过一般用不着。

```py
# 'x' is [[1, 1, 1]
#         [1, 1, 1]]
tf.reduce_sum(x) ==> 6
tf.reduce_sum(x, 0) ==> [2, 2, 2]
tf.reduce_sum(x, 1) ==> [3, 3]
tf.reduce_sum(x, 1, keep_dims=True) ==> [[3], [3]]
tf.reduce_sum(x, [0, 1]) ==> 6
```