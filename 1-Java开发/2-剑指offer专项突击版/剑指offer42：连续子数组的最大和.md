#### 剑指offer42：连续子数组的最大和

![image-20210113161811475](C:\Users\User\AppData\Roaming\Typora\typora-user-images\image-20210113161811475.png)

```java
class Solution {
    public int maxSubArray(int[] nums) {
        int res = nums[0];
        for(int i = 1; i < nums.length; i++) {
            nums[i] += Math.max(nums[i - 1], 0);
            res = Math.max(res, nums[i]);
        }
        return res;
    }
}
```

