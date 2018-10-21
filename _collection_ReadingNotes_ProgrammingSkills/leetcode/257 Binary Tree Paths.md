---
title:  257  Binary Tree Paths (二叉树遍历)
date:   2018-10-21
---


* content
{:toc}


##  问题描述
Given a binary tree, return all root-to-leaf paths.
Note: A leaf is a node with no children.
Explanation: All root-to-leaf paths are: 1->2->5, 1->3
Example:
```
Input:

   1
 /   \
2     3
 \
  5

Output: ["1->2->5", "1->3"]
```

## 递归遍历 Tree 的大原则
一般都是直接思考叶子节点，左右子树同时开工，然后再往上。

## 第一种，直接递归， 32 ms

一边递归，一边构造。

```py
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def binaryTreePaths(self, root):
        """
        :type root: TreeNode
        :rtype: List[str]
        """
        if root == None:
            return []
        # leaf node 叶子节点
        if root.left == None and root.right == None:
            return [str(root.val)]
        # execute the following code from the leaf nodes up
        string_path = [str(root.val)+'->'+path for path in self.binaryTreePaths(root.left)]
        string_path += [str(root.val)+'->'+path for path in self.binaryTreePaths(root.right)]
        return string_path
        
```
很明显，对于示例来说，root 节点为 2 时的左子节点为 None，返回空 list， 而右子节点 5 则返回 `['5']`，
因此这两行
```py
string_path = [str(root.val)+'->'+path for path in self.binaryTreePaths(root.left)]
string_path += [str(root.val)+'->'+path for path in self.binaryTreePaths(root.right)]
```
得到的 string_path 为 `['2->5']`

对于 root 为 1 的节点，此时, `string_path = [str(root.val)+'->'+path for path in self.binaryTreePaths(root.left)]` 使得  `['2->5']` 变成了 `['1->2->5']`

右 子节点返回了 `['3']`,此时 `string_path += [str(root.val)+'->'+path for path in self.binaryTreePaths(root.right)]` 中右边的东西为 `['1->3']`
因此上面两行代码过后 return 的结果是 `["1->2->5", "1->3"]`



## DFS method    24  ms
这个也是纯粹利用递归的思想找到叶子节点，然后再去找字符串。

即，先递归，再构造。
```py
class Solution(object):
    def binaryTreePaths(self, root):
        """
        :type root: TreeNode
        :rtype: List[str]
        """
        leaf_nodes=[]
        parent_nodes={}
        # 构建叶子节点的list，以及各个节点的父节点的字典
        def dfs(root):
            if root == None:
                return None
            if root.left == None and root.right == None:
                leaf_nodes.append(root)
            if dfs(root.left):
                parent_nodes[root.left]=root            
            if dfs(root.right):
                parent_nodes[root.right]=root
            return 1
        dfs(root)
        tmp_results=[]
        for leaf_node in leaf_nodes:
            tmp_list=[str(leaf_node.val)]
            tmp_node = leaf_node
            while tmp_node != root:
                tmp_node = parent_nodes[tmp_node]
                tmp_list.append(str(tmp_node.val))
            tmp_results.append(tmp_list)
            pass
        results=[]
        for tmp in tmp_results:
            tmp.reverse()
            results.append("->".join(tmp))
        return results
```

思路就是，先通过 dfs 找出所有叶子节点，同时构建一个字典用于保存叶子节点的父节点，以及父节点的父节点信息。
再根据这个字典以及叶子节点，重建所有的path。

## 一边递归，一边构造，在叶子节点确认加入结果的list，这个方法更多的是一种从前往后的思想  24  ms
```py
class Solution(object):
    def binaryTreePaths(self, root):
        """
        :type root: TreeNode
        :rtype: List[str]
        """
        all_paths=[]
        def findPath(root,tmp_result):
            #  先初始化根节点
            if len(tmp_result)==0:
                tmp_result=str(root.val)
            else: # 一路添加子节点
                tmp_result+='->'+str(root.val)
                pass
            # 终于到叶子节点了，从这里开始返回
            if root.left == None and root.right == None:
                #终于找到了子节点，添加一条path进去吧！
                all_paths.append(tmp_result) 
                pass
            if root.left != None:
                findPath(root.left, tmp_result)
            if root.right != None:
                findPath(root.right, tmp_result)
                
            return
        tmp_result=''
        if root != None:
            findPath(root,tmp_result)
        return all_paths
```
这个解法让我认识到，在递归的时候，传参是多么的重要！ 参数也可以累加的哦！        


