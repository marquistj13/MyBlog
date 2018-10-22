---
title:  437. Path Sum III (二叉树遍历)
date:   2018-10-22
---


* content
{:toc}


##  问题描述
You are given a binary tree in which each node contains an integer value.

Find the number of paths that sum to a given value.

The path does not need to start or end at the root or a leaf, but it must go downwards (traveling only from parent nodes to child nodes).

The tree has no more than 1,000 nodes and the values are in the range -1,000,000 to 1,000,000.

Example:
```
root = [10,5,-3,3,2,null,11,3,-2,null,1], sum = 8

      10
     /  \
    5   -3
   / \    \
  3   2   11
 / \   \
3  -2   1

Return 3. The paths that sum to 8 are:

1.  5 -> 3
2.  5 -> 2 -> 1
3. -3 -> 11
```

## 递归遍历 Tree 的大原则
一般都是直接思考叶子节点，左右子树同时开工，然后再往上。

## 第一种，直接递归， 32 ms

一边递归，一边构造。

```py
class Solution(object):
    def pathSum(self, root, sum):
        """
        :type root: TreeNode
        :type sum: int
        :rtype: int
        """
        if root == None:
            return 0
        self.cnt=0
        accumulate_sum_list=[]
        # 好好利用递归传参吧
        def dfs(root, accumulate_sum_list):
            accumulate_sum_list=[val+root.val for val in accumulate_sum_list]
            accumulate_sum_list.append(root.val)            
            for val in accumulate_sum_list:
                if val == sum:                    
                    self.cnt+=1
                    pass
                pass
            # accumulate_sum_list = [val for val in accumulate_sum_list if val != sum ]
            if root.left != None:                
                dfs(root.left, accumulate_sum_list)
                pass
            if root.right!=None:                
                dfs(root.right, accumulate_sum_list)
                pass
            return        
        dfs(root,accumulate_sum_list)
        return self.cnt
        
```
此解法利用递归时的参数传递，不断将 `accumulate_sum_list` 进行累加。

## 第二种，和第一种一样，只是不递归了而已
```py
class Solution(object):
    def pathSum(self, root, sum):
        """
        :type root: TreeNode
        :type sum: int
        :rtype: int
        """
        cnt = 0
        tmp_list = [(root,[])]
        while tmp_list:
            node,accumulate_sum_list=tmp_list.pop()
            if node:
                accumulate_sum_list=[val+node.val for val in accumulate_sum_list]+[node.val]
                for val in accumulate_sum_list:
                    if val == sum:                    
                        cnt+=1
                        pass
                    pass
                tmp_list.extend([(node.left,accumulate_sum_list),(node.right,accumulate_sum_list)])
                pass
            pass
        return cnt
```

总结一下，其实这种从前往后传递“信息”类型的题目，基本上都有递归或非递归的方法，非递归的时候，必须得找到一个容器来存放需要处理的节点。        