![image-20220121103333716](C:\Users\Adnim\AppData\Roaming\Typora\typora-user-images\image-20220121103333716.png)

一、直接反转然后对比两个字符串是否相等：

本题关键点：1.去除字符串中多于的内容：使用Character.isLetterOrDigit函数

2.回文串：new StringBuffer(sletter).reverse();，直接用函数实现

```java
class Solution {
    public static boolean isPalindrome(String s) {
        StringBuffer sletter = new StringBuffer();
        int length = s.length();
        for (int i = 0; i < length; i++) {
            char ch = s.charAt(i);
            if (Character.isLetterOrDigit(ch)) {
                sletter.append(Character.toLowerCase(ch));
            }
        }
        StringBuffer letters = new StringBuffer(sletter).reverse();
        if(letters.toString().equals(sletter.toString())){
            return true;
        }
        return false;
    }
}
```



二、双指针法

采用左右两个指针，依次移动对比指针是否相等，直到指针相遇或者相交

```java
class Solution {
    public boolean isPalindrome(String s) {
        int n = s.length();
        int left = 0, right = n - 1;
        while (left < right) {
            while (left < right && !Character.isLetterOrDigit(s.charAt(left))) {
                ++left;
            }
            while (left < right && !Character.isLetterOrDigit(s.charAt(right))) {
                --right;
            }
            if (left < right) {
                if (Character.toLowerCase(s.charAt(left)) != Character.toLowerCase(s.charAt(right))) {
                    return false;
                }
                ++left;
                --right;
            }
        }
        return true;
    }
}
```

