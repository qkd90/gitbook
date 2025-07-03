![image-20220119113046732](C:\Users\Adnim\AppData\Roaming\Typora\typora-user-images\image-20220119113046732.png)

```java
class Solution {
    public int lengthOfLongestSubstring(String s) {
        // 哈希集合，记录每个字符是否出现过
        Set<Character> occ = new HashSet<Character>();
        int len = s.length();
        // 右指针，初始值为 0，还没有开始移动
        int lp = 0, ans = 0;
        for (int i = 0; i < len; ++i) {
            if (i != 0) {
                // 左指针向右移动一格，移除一个字符
                occ.remove(s.charAt(i - 1));
            }
            while (lp < len && !occ.contains(s.charAt(lp))) {
                // 不断地移动右指针
                occ.add(s.charAt(lp));
                ++lp;
            }
            // 从i 到 lp 个字符是一个极长的无重复字符子串
            ans = Math.max(ans, lp - i);
        }
        return ans;
    }
}
```

一、滑动窗口：

本题关键点：1.从左至右，左指针对应一次开头的一个字母，移动右指针知道出现重复字母为止就是完成了一次搜索，依次移动左指针直到最后，就完成了全部字符串的搜索

![image-20220119143318840](C:\Users\Adnim\AppData\Roaming\Typora\typora-user-images\image-20220119143318840.png)

2.采用hashset来存储已经有的字符，这个数据结构查找更有优势，不过就是没有顺序，但是对我们的题目没有影响，不需要顺序的时候使用