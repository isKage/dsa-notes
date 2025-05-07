def inplace_quick_sort(S: list, a: int, b: int) -> None:
    """就地快速排序: 序列 S 从 S[a] 到 S[b]"""
    if a >= b:
        return

    # 排序找出中位数 S[mid]
    mid = (a + b) // 2
    if S[a] > S[mid]:
        S[a], S[mid] = S[mid], S[a]
    if S[a] > S[b]:
        S[a], S[b] = S[b], S[a]
    if S[mid] > S[b]:
        S[mid], S[b] = S[b], S[mid]

    # 选择 S[a], S[mid], S[b] 的中位数作为 pivot
    pivot = S[mid]
    S[mid], S[b - 1] = S[b - 1], S[mid]  # 移到倒数第二
    # 下面就与普通的就地排序相同
    left = a  # 从左向右
    right = b - 2  # 从右向左

    while left <= right:  # 直到相交
        while left <= right and S[left] < pivot:
            left += 1

        while left <= right and pivot < S[right]:
            right -= 1

        if left <= right:  # 逆序, 则交换
            S[left], S[right] = S[right], S[left]  # 交换
            left, right = left + 1, right - 1  # 继续移动

    S[left], S[b - 1] = S[b - 1], S[left]  # 将基准值放到中间

    # 递归调用
    inplace_quick_sort(S, a, left - 1)
    inplace_quick_sort(S, left + 1, b)


if __name__ == '__main__':
    S = [85, 24, 63, 45, 17, 31, 96, 50]
    print("=" * 15, "Original List", "=" * 15)
    print(S)

    print("=" * 15, "After Sorted", "=" * 15)
    inplace_quick_sort(S, 0, len(S) - 1)
    print(S)
