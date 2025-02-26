def find_max(data):
    """ 寻找最大数 O(n) """
    biggest = data[0]
    for val in data:
        if val > biggest:
            biggest = val
    return biggest


data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(find_max(data))


def prefix_average1(data):
    """ 计算前缀平均值 二次算法 O(n^2) """
    n = len(data)
    ave = []
    for i in range(n):
        total = 0
        for j in range(i + 1):
            total += data[j]
        ave.append(total / (i + 1))
    return ave


data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(prefix_average1(data))


def prefix_average2(data):
    """ 计算前缀平均值 线性算法 O(n) """
    n = len(data)
    total = 0
    ave = []
    for i in range(n):
        total += data[i]
        ave.append(total / (i + 1))
    return ave


data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(prefix_average2(data))


def disjoint1(A, B, C):
    """ 三集不相交 三层循环 O(n^3) """
    for a in A:
        for b in B:
            for c in C:
                if a == b == c:
                    return True
    return False


A = [1, 2, 3]
B = [3, 4, 5, 6]
C = [3, 7, 8, 9, 10]
print(disjoint1(A, B, C))


def disjoint2(A, B, C):
    """ 三集不相交 循环中加入判断 运气好则为 O(n^2) 实际为 O(n^3) """
    for a in A:
        for b in B:
            if a == b:
                for c in C:
                    if a == c:
                        return True
    return False


A = [1, 2, 3]
B = [3, 4, 5, 6]
C = [3, 7, 8, 9, 10]
print(disjoint2(A, B, C))


def unique1(data):
    """ 元素唯一性 简单迭代 O(n^2) """
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[i] == data[j]:
                return False
    return True


data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 9]
print(unique1(data))


def unique2(data):
    """元素唯一性 先排序 O(n * log n)"""
    temp = sorted(data)
    for i in range(1, len(temp)):
        if temp[i] == temp[i - 1]:
            return False
    return True


data = [1, 3, 2, 6, 5, 4, 7, 10, 9, 9]
print(unique2(data))
