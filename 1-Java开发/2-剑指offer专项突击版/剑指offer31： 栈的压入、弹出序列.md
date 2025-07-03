![在这里插入图片描述](https://img-blog.csdnimg.cn/20190619165005455.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2phY2tpZV9vMm8y,size_16,color_FFFFFF,t_70)

```python
# -*- coding:utf-8 -*-
class Solution:
    def IsPopOrder(self, pushV, popV):
        # write code here
        if not pushV or len(pushV) != len(popV):
            return False
        stack = []
        for i in pushV:
            stack.append(i)
            while len(stack) and stack[-1] == popV[0]:
                stack.pop()
                popV.pop(0)
        if len(stack):
            return False
        return True
```
1.判断两个序列长度是否相等，压入序列是否为空

2.辅助栈： 如果不是要出栈的元素就压入，否则就弹出。

3.pop(0):从列表的头部开始弹出

4.最后如果辅助栈没有清空，说明序列不行
