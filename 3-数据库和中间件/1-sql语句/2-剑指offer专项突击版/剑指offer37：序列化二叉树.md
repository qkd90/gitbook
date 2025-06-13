![在这里插入图片描述](https://img-blog.csdnimg.cn/20190715165538510.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2phY2tpZV9vMm8y,size_16,color_FFFFFF,t_70)
1.把树序列为字符串可以看成递归，先序遍历
2.碰到空指针变为特殊字符$
3.反序列化时，直接按照‘，’号分隔开
```python
# -*- coding:utf-8 -*-
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
class Solution:
    flag = -1
    def Serialize(self, root):
        s = ""
        s = self.recursionSerialize(root, s)
        return s
    def recursionSerialize(self, root, s):
        if root is None:
            s = '$,'
            return s
        s = str(root.val) + ','
        left = self.recursionSerialize(root.left, s)
        right = self.recursionSerialize(root.right, s)
        s += left + right
        return s
    def Deserialize(self, s):
        self.flag += 1
        l = s.split(',')
        if self.flag >= len(s):
            return None
        root = None
        if l[self.flag] != '$':
            root = TreeNode(int(l[self.flag]))
            root.left = self.Deserialize(s)
            root.right = self.Deserialize(s)
        return root
```

