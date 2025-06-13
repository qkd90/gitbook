![image-20220117173047599](C:\Users\Adnim\AppData\Roaming\Typora\typora-user-images\image-20220117173047599.png)

```java
class Solution {
    public boolean checkInclusion(String s1, String s2) {
        int n = s1.length(), m = s2.length();
        if (n > m) {
            return false;
        }
        int[] cnt1 = new int[26];
        int[] cnt2 = new int[26];
        for (int i = 0; i < n; ++i) {
            ++cnt1[s1.charAt(i) - 'a'];
            ++cnt2[s2.charAt(i) - 'a'];
        }
        if (Arrays.equals(cnt1, cnt2)) {
            return true;
        }
        //固定长度的滑动窗口，i是右侧，i-n是左侧，因为固定长度的窗口了
        for (int i = n; i < m; ++i) {
            ++cnt2[s2.charAt(i) - 'a'];
            --cnt2[s2.charAt(i - n) - 'a'];
            if (Arrays.equals(cnt1, cnt2)) {
                return true;
            }
        }
        return false;
    }
}
```

一、滑动窗口法：

本题关键点：

1.把字符比较转换为数字比较，且把比较字符串包含变为了比较单个字符个数是否相等，只要相等就证明存在包含关系

2.滑动窗口进一个，踢出去一个



