![image-20220118110136988](C:\Users\Adnim\AppData\Roaming\Typora\typora-user-images\image-20220118110136988.png)

```java
class Solution {
    public List<Integer> findAnagrams(String s, String p) {
        int sLen = s.length(), pLen = p.length();
        List<Integer> ans = new ArrayList<Integer>();

        if (sLen < pLen) {
            return ans;
        }
        int[] sCount = new int[26];
        int[] pCount = new int[26];
        for (int i = 0; i < pLen; ++i) {
            ++sCount[s.charAt(i) - 'a'];
            ++pCount[p.charAt(i) - 'a'];
        }
        if (Arrays.equals(sCount, pCount)) {
            ans.add(0);
        }
        for (int i = 0; i < sLen - pLen; ++i) {
            --sCount[s.charAt(i) - 'a'];
            ++sCount[s.charAt(i + pLen) - 'a'];
            if (Arrays.equals(sCount, pCount)) {
                ans.add(i + 1);
            }
        }
        return ans;
    }
}
```

本题与14题基本一样，唯一不同是：

1.输出结果采用的是数组：ArrayList

2.最后一个循环的时候因为输出起始位置，就改为左端为i了