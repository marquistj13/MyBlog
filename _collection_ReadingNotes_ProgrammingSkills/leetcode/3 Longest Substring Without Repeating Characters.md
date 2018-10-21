---
title: 3. Longest Substring Without Repeating Characters (哈希表，字符串string，双指针)
date:   2018-4-7
---


* content
{:toc}


##  问题描述
Given a string, find the length of the longest substring without repeating characters.

Examples:

Given "abcabcbb", the answer is "abc", which the length is 3.

Given "bbbbb", the answer is "b", with the length of 1.

Given "pwwkew", the answer is "wke", with the length of 3. Note that the answer must be a substring, "pwke" is a subsequence and not a substring.


## 解法1 滑窗法
```cpp
class Solution {
public:
    int lengthOfLongestSubstring(string s) { 
            //维持一个set，它包含i,j之间的字符，且保证不存在重复字符。
            unordered_set<char> window_set;
            int maxlen=0;
            int i=0,j=0;
            while( j<s.size()) 
            {
                  auto ret=window_set.insert(s[j]);
                  if(ret.second)//ret.second为true,则表示成功插入,即原先没有，否则就是出现了重复。
                  {
                      maxlen = max( maxlen, j-i+1);
                      ++j;
                  }
                  else //擦除i处的字符，同时将i指针向前移，直到将s[j]删除，此时i,j之间不再存在重复字符。
                  {
                     window_set.erase(s[i]);
                     i++;
                  }
            }
            return maxlen;

        }
};
```

## 解法2 暴力搜索，复杂度过高,   $O(n^3)$
```cpp
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        if (s.size()==1)
            return 1;
        int res = 0;
        for (int i=0; i< s.size(); i++)
            for (int j=i+1; j<=s.size(); j++)
            {
                if(!ifrepeat(s, i, j))
                    res = max(res, j-i);
            }
        return res;
    }
    bool ifrepeat(const string &s, int i, int j)
    {
        std::unordered_set<char> tmp;
        while(i<j)
        { 
            auto ret = tmp.insert(s[i++]);
            if(!ret.second)
                return true;            
        }
        return false;
    }
};
```

## python 版
```py
class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        maxlen=0
        hist = set()
        L = len(s)
        i, j = 0, 0
        while j< L:
            if s[j] in hist:
                if i<j:
                    hist.remove(s[i])
                    i+=1
                pass
            else:
                hist.add(s[j])
                j+=1
                maxlen=max(maxlen,j-i)
                pass
        return maxlen
```        
