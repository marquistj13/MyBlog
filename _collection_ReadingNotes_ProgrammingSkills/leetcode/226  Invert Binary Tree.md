---
title:  226. Invert Binary Tree (二叉树遍历)
date:   2018-10-21
---


* content
{:toc}


##  问题描述
Invert a binary tree.
Example:
```
Input:

     4
   /   \
  2     7
 / \   / \
1   3 6   9
Output:

     4
   /   \
  7     2
 / \   / \
9   6 3   1
```
Trivia:
This problem was inspired by this original tweet by Max Howell:
>Google: 90% of our engineers use the software you wrote (Homebrew), but you can’t invert a binary tree on a whiteboard so f*** off.

## 递归遍历 Tree 的大原则
一般都是直接思考叶子节点，左右子树同时开工，然后再往上。

## 第一种，直接递归， 24 ms

一边递归，一边翻转，从叶子节点开始翻转。

```py
class Solution(object):
    def invertTree(self, root):
        """
        :type root: TreeNode
        :rtype: TreeNode
        """
        if root == None:
            return root
        if root.left == None and root.right == None:
            return root
        left = self.invertTree(root.left)
        right = self.invertTree(root.right) 
        root.left = right
        root.right = left
        return root        
```
这个很容易看懂哈。

## 迭代法
迭代法的关键是想到使用一个容器去存放待交换的子节点，python 的list 就很好使。

```py
class Solution(object):
    def invertTree(self, root):
        """
        :type root: TreeNode
        :rtype: TreeNode
        """
        if root == None:
            return []
        tmp_nodes = [root]
        while len(tmp_nodes)>0:            
            node = tmp_nodes.pop()            
            tmp=node.left
            node.left=node.right
            node.right=tmp
            if node.left != None:
                tmp_nodes.append(node.left) 
            if node.right != None:
                tmp_nodes.append(node.right)
        return root
```
一开始交换根节点的左右子节点，
然后将左右子节点分别存进去，再逐个弹出来进行交换。        
