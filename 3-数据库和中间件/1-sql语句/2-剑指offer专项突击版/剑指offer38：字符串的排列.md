![在这里插入图片描述](https://img-blog.csdnimg.cn/2019071616320136.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2phY2tpZV9vMm8y,size_16,color_FFFFFF,t_70)
1.递归的思想，第一个字符和其他字符排序组合，然后依次类推
2.set函数
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190716164154836.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2phY2tpZV9vMm8y,size_16,color_FFFFFF,t_70)

```python
class Solution:
    def Permutation(self, ss):
        if len(ss) <=0:
            return []
        res = list()
        self.perm(ss,res,'')
        seq = list(set(res))
        return sorted(seq)
    def perm(self,ss,res,path):
        if ss=='':
            res.append(path)
        else:
            for i in range(len(ss)):
                self.perm(ss[:i]+ss[i+1:],res,path+ss[i])
```

