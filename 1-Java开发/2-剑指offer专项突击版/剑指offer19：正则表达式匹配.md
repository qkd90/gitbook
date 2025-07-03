![在这里插入图片描述](https://img-blog.csdnimg.cn/20190725154508238.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2phY2tpZV9vMm8y,size_16,color_FFFFFF,t_70)

## 1.递归的思想依次匹配
1.![在这里插入图片描述](https://img-blog.csdnimg.cn/20190725155036730.png)
2.如果第二位是*：第一位如果匹配，则三种情况
	

 -  pattern直接后移两位
 -  s后移一位，pattern后移两位
 - 	s后移一位，pattern不动
	



有一种为true，则结果为true
3.其余情况一位一位比较

```python
class Solution:
    # s, pattern都是字符串
    def match(self, s, pattern):
        # write code here
        if (len(s) == 0 and len(pattern) == 0):
            return True
        if (len(s) > 0 and len(pattern) == 0):
            return False
        if (len(pattern) > 1 and pattern[1] == '*'):
            if (len(s) > 0 and (s[0] == pattern[0] or pattern[0] == '.')):
                return (self.match(s, pattern[2:]) or self.match(s[1:], pattern[2:]) or self.match(s[1:], pattern))
            else:
                return self.match(s, pattern[2:])
        if (len(s) > 0 and (pattern[0] == '.' or pattern[0] == s[0])):
            return self.match(s[1:], pattern[1:])
        return False
```

	


