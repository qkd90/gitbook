
#从N个人中选K个,选中的相邻两个人的编号不超过D
import sys
N=int(sys.stdin.readline().strip())
ai_list=list(map(int,sys.stdin.readline().split()))
K, D = list(map(int,sys.stdin.readline().split())) # 这里不加list也行

#每个测试用例的第一行包含两个整数 n 和 m（1 <= n, m <= 75），表示田地的大小，接下来的 n 行，每行包含 m 个 0-9 之间的数字，表示每块位置的价值。