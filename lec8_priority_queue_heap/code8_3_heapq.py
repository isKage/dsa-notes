import heapq

L = [3, 2, 1, 4, 5, 6, 7, 10, 9, 8]  # 不满足 Heap-Order

# 1. 自底向上构建堆
heapq.heapify(L)
print(L)
"""
[1, 2, 3, 4, 5, 6, 7, 10, 9, 8]
1
2 3
4 5 6 7
10 9 8
满足 Heap-Order
"""

# 2. 返回最大最小的 2 个
print(heapq.nlargest(2, L))
print(heapq.nsmallest(2, L))
"""
[10, 9]
[1, 2]
"""

# 3. 去除最小
print(heapq.heappop(L))
print(L)
"""
[2, 4, 3, 8, 5, 6, 7, 10, 9]
2
4 3
8 5 6 7
10 9
满足 Heap-Order
"""
