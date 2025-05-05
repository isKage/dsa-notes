def merge(S1: list, S2: list, S: list) -> None:
    """
    合并数组/序列 S1 S2 返回新的数组/序列
    :param S1: 顺序序列 S1
    :param S2: 顺序序列 S2
    :param S: 用于存储最终合并的结果，按照从小到大排序的序列
    :return: None
    """
    i = j = 0
    while i + j < len(S):
        if j == len(S2) or (i < len(S1) and S1[i] < S2[j]):
            S[i + j] = S1[i]  # copy i th element of S1 as next item of S
            i += 1
        else:
            S[i + j] = S2[j]  # copy j th element of S2 as next item of S
            j += 1


def merge_sort(S: list) -> None:
    """
    对序列 S 进行归并排序，直接修改原序列
    :param S: 等待排序的序列
    :return: None
    """
    n = len(S)
    if n < 2:
        return  # list is already sorted

    # divide
    mid = n // 2
    S1 = S[0:mid]  # copy of first half
    S2 = S[mid:n]  # copy of second half

    # conquer (with recursion)
    merge_sort(S1)  # sort copy of first half
    merge_sort(S2)  # sort copy of second half

    # merge results
    merge(S1, S2, S)  # merge sorted halves back into S


if __name__ == '__main__':
    S = [85, 24, 63, 45, 17, 31, 96, 50]
    print("=" * 15, "Original List", "=" * 15)
    print(S)

    print("=" * 15, "After Sorted", "=" * 15)
    merge_sort(S)
    print(S)
