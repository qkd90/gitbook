# 剑指 Offer 43：1～n 整数中 1 出现的次数

## 题目描述

输入一个整数 `n`，求 `1` 到 `n` 这 `n` 个整数的十进制表示中数字 `1` 出现的次数。

示例：

```text
输入：12
输出：5
解释：1、10、11、12 中一共出现 5 次数字 1。
```

## 解题思路

如果从 `1` 遍历到 `n`，再逐位统计，时间复杂度较高。更好的方式是按位统计每一位上数字 `1` 出现的次数。

以当前位 `digit` 为分界，把数字拆成三部分：

```text
high  cur  low
高位  当前位 低位
```

例如 `n = 2304`，统计十位时：

```text
digit = 10
high = 2304 / 100 = 23
cur  = 2304 / 10 % 10 = 0
low  = 2304 % 10 = 4
```

当前位为 `1` 的数量分三种情况：

1. `cur == 0`：数量为 `high * digit`。
2. `cur == 1`：数量为 `high * digit + low + 1`。
3. `cur > 1`：数量为 `(high + 1) * digit`。

## Java 实现

```java
class Solution {
    public int countDigitOne(int n) {
        int count = 0;
        long digit = 1;

        while (digit <= n) {
            long high = n / (digit * 10);
            long cur = (n / digit) % 10;
            long low = n % digit;

            if (cur == 0) {
                count += high * digit;
            } else if (cur == 1) {
                count += high * digit + low + 1;
            } else {
                count += (high + 1) * digit;
            }

            digit *= 10;
        }

        return count;
    }
}
```

## 复杂度分析

- 时间复杂度：`O(log n)`，按十进制位数统计。
- 空间复杂度：`O(1)`。

## 易错点

- `digit * 10` 可能溢出，所以 `digit` 使用 `long`。
- `cur == 1` 时要加上 `low + 1`，表示当前高位固定时低位从 `0` 到 `low` 的所有情况。
- 统计的是十进制表示中的数字 `1`，不是包含数字 `1` 的整数个数。
