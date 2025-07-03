![image-20220120170821199](C:\Users\Adnim\AppData\Roaming\Typora\typora-user-images\image-20220120170821199.png)

```java
class Solution {
    Map<Character, Integer> tmap = new HashMap<Character, Integer>();
    Map<Character, Integer> smap = new HashMap<Character, Integer>();

    public String minWindow(String s, String t) {
        int tLen = t.length();
        for (int i = 0; i < tLen; i++) {
            char c = t.charAt(i);
            tmap.put(c, tmap.getOrDefault(c, 0) + 1);
        }
        int l = 0, r = -1;
        int len = Integer.MAX_VALUE, ansL = -1, ansR = -1;
        int sLen = s.length();
        while (r < sLen) {
            ++r;
            if (r < sLen && tmap.containsKey(s.charAt(r))) {
                smap.put(s.charAt(r), smap.getOrDefault(s.charAt(r), 0) + 1);
            }
            while (check() && l <= r) {
                if (r - l + 1 < len) {
                    len = r - l + 1;
                    ansL = l;
                    ansR = l + len;
                }
                if (tmap.containsKey(s.charAt(l))) {
                    smap.put(s.charAt(l), smap.getOrDefault(s.charAt(l), 0) - 1);
                }
                ++l;
            }
        }
        return ansL == -1 ? "" : s.substring(ansL, ansR);
    }

    public boolean check() {
        Iterator iter = tmap.entrySet().iterator(); 
        while (iter.hasNext()) { 
            Map.Entry entry = (Map.Entry) iter.next(); 
            Character key = (Character) entry.getKey(); 
            Integer val = (Integer) entry.getValue(); 
            if (smap.getOrDefault(key, 0) < val) {
                return false;
            }
        } 
        return true;
    }
}
```

一、滑动窗口：

本题关键点：1.
