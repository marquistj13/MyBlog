---
title:  1. Two Sum  (使用unordered_map，哈希表)
date:   2018-4-7
---


* content
{:toc}


##  问题描述
Given an array of integers, return indices of the two numbers such that they add up to a specific target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

__Example:__
```
Given nums = [2, 7, 11, 15], target = 9,

Because nums[0] + nums[1] = 2 + 7 = 9,
return [0, 1].
```
## 最直观的的想法就是两层循环，Brute Force
复杂度为 `O(n^2)`.

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        vector<int> tmp;
        tmp.reserve(2);
        int length = nums.size();
        for (int i=0; i<length; ++i)
            for (int j=i+1; j<length; ++j)
                if (nums.at(i) + nums.at(j) == target)
                {
                    tmp.push_back(i);
                    tmp.push_back(j);
                    return tmp;
                }
                    
    }
};
```
## 使用搜索，(Two-pass Hash Table) 
由于`std::unordered_map::find`的平均复杂度为constant，最坏复杂度为linear，因此可以将其中一个循环转化为一个搜索问题，从而减低复杂度。
```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        vector<int> ret;
        unordered_map<int, int> num_map;        
        int i =0;
        for (auto it= nums.begin(); it!= nums.end(); ++it, ++i)
        {
            num_map.insert({*it, i}); 
            // 或者：num_map[*it]= i;  
            // 或者：num_map[nums.at(i)]= i;         
        }
        for (int i=0; i< nums.size(); ++i)
        {           
            int tofind = target - nums[i];
            auto got = num_map.find(tofind);
            if(got!=num_map.end() && got->second!=i)
            {
                ret.push_back(i);
                ret.push_back(got->second);
                return  ret;
            }            
        }
    }
         
};
```
