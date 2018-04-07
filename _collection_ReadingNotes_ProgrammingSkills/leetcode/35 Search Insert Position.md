---
title:  35. Search Insert Position (二分查找)
date:   2018-4-7
---


* content
{:toc}


##  问题描述
Given a sorted array and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.

You may assume no duplicates in the array.
Example 1:
```
Input: [1,3,5,6], 5
Output: 2
Example 2:

Input: [1,3,5,6], 2
Output: 1
Example 3:

Input: [1,3,5,6], 7
Output: 4
Example 1:

Input: [1,3,5,6], 0
Output: 0
```

## 首先是不用二分查找， 8ms
```cpp
class Solution {
public:
    int searchInsert(vector<int>& nums, int target) {
        
        if(target<nums.front())
            return 0;
        else if(target>nums.back())
            return  nums.size();
        int index=0;    
        for (auto it = nums.cbegin(); it != nums.cend(); ++it, ++index)
        {
            if(target<= *it)
                return index;  
        }
        
    }
};
```

## 二分查找   13ms
二分查找的终止条件比较诡异，先用`while(lo < up)`，这个好慢啊。
```cpp
class Solution {
public:
    int searchInsert(vector<int>& nums, int target) {        
      if(target < nums.front())
          return 0;
      else if(target > nums.back())
          return nums.size();
        
      int lo = 0, up = nums.size()-1, avg = (lo + up)  /2;
        while(lo < up)
        {
            if(target == nums[avg])
                return avg;
            else if(target > nums[avg])
            {
                lo = avg;
                avg =(lo + up)  /2;
                lo++;
            }
            else 
            {
                up=avg;
                avg =(lo + up)  /2;
            }
        }
        return lo;
            
        
    }
};
```

## 二分查找  8ms
这个`while(lo < avg)`更快一些。
```cpp
class Solution {
public:
    int searchInsert(vector<int>& nums, int target) {        
      if(target < nums.front())
          return 0;
      else if(target > nums.back())
          return nums.size();
        
      int lo = 0, up = nums.size()-1, avg = (lo + up)  /2;
        while(lo < avg)
        {
            if(target == nums[avg])
                return avg;
            else if(target > nums[avg])
            {
                lo = avg;
                avg =(lo + up)  /2;
            }
            else 
            {
                up=avg;
                avg =(lo + up)  /2;
            }
        }
        if(target == nums[lo])
            return lo;
        else
            return up;
            
        
    }
};
```


