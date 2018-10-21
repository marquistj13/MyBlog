---
title:  2. Add Two Numbers  (遍历单向链表)
date:   2018-4-7
---


* content
{:toc}


##  问题描述
You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.

__Example:__
```
Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
Output: 7 -> 0 -> 8
Explanation: 342 + 465 = 807.
```
## 解法
复杂度为 `O(n^2)`.

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        int carry = 0;
        ListNode dummyHead(0);
        ListNode *curr =  &dummyHead, *p= l1, *q=l2; 
        while(p!=NULL || q!=NULL)
        {
            int x= (p!=NULL)? p->val: 0;
            int y= (q!=NULL)? q->val: 0;
            int sum = x+y+carry;
            carry=sum/10;
            curr->next=new ListNode(sum%10);
            curr=curr->next;
            
            if(p!=NULL) p=p->next;            
            if(q!=NULL) q=q->next;   
          
        }
        if (carry>0)
        {
            curr->next=new ListNode(carry);
        }
        return dummyHead.next;
    }
};
```

## 使用Python
```py
class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        result = ListNode(0)
        p_result = result
        
        p1 = l1 
        p2 = l2
        step_val=0
        while p1!=None or p2!=None:             
            if p1!=None:
                val1=p1.val
            else:
                val1=0
            if p2!=None:
                val2=p2.val
            else:
                val2=0
            sum_val = val1+val2+step_val            
            p_result.next=ListNode(sum_val%10) 
            p_result= p_result.next
            step_val=sum_val/10 
            if p1!=None:
                p1 = p1.next
            if p2!=None:
                p2 = p2.next
        if step_val!=0:
            p_result.next=ListNode(step_val)
        
        return result.next
```        