def inplace_quick_sort(S: list, a: int, b: int) -> None:
    """就地快速排序: 序列 S 从 S[a] 到 S[b]"""
    if a >= b:
        return

    pivot = S[b]  # 取 S[b] 为基准
    left = a  # 从左向右
    right = b - 1  # 从右向左

    while left <= right:  # 直到相交
        # scan until reaching value equal or larger than pivot (or right marker)
        while left <= right and S[left] < pivot:
            left += 1

        # scan until reaching value equal or smaller than pivot (or left marker)
        while left <= right and pivot < S[right]:
            right -= 1

        if left <= right:  # 逆序, 则交换
            S[left], S[right] = S[right], S[left]  # swap values
            left, right = left + 1, right - 1  # 继续移动

    # put pivot into its final place (currently marked by left index)
    S[left], S[b] = S[b], S[left]  # 将基准值放到中间

    # make recursive calls 递归调用
    inplace_quick_sort(S, a, left - 1)
    inplace_quick_sort(S, left + 1, b)


if __name__ == '__main__':
    S = [85, 24, 63, 45, 17, 31, 96, 50]

    print("=" * 15, "Original List", "=" * 15)
    print(S)

    print("=" * 15, "After Sorted", "=" * 15)
    inplace_quick_sort(S, 0, len(S) - 1)
    print(S)
