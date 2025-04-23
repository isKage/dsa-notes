def factorial(n):
    if n == 0:
        return 1

    res = n
    for i in range(1, n):
        res *= i
    return res


def reverse(seq, i, j):
    while i < j:
        seq[i], seq[j] = seq[j], seq[i]
        i, j = i + 1, j - 1


def binary_search(data, target, left, right):
    while left <= right:
        mid = (left + right) // 2
        if target == data[mid]:
            return True
        elif target < data[mid]:
            right = mid - 1
        else:
            left = mid + 1
    return False


if __name__ == '__main__':
    # 阶乘函数 非递归
    print("=" * 15 + " 阶乘函数 非递归 " + "=" * 15)
    print(factorial(4))

    # 逆置序列 非递归
    print("=" * 15 + " 逆置序列 非递归 " + "=" * 15)
    seq = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    reverse(seq, i=0, j=len(seq) - 1)
    print(seq)
    reverse(seq, i=3, j=len(seq) - 1)
    print(seq)

    # 二分查找 非递归
    print("=" * 15 + " 二分查找 非递归 " + "=" * 15)
    seq = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # 有序
    print(binary_search(seq, target=8, left=0, right=len(seq) - 1))

