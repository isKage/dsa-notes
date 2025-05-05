import math


def merge(src, result, start, inc):
    """合并序列 src[start : start + inc] 和 src[start + inc : start + 2 * inc] 到 result 里"""
    end1 = start + inc  # 序列 1 的在原序列的结束索引
    end2 = min(start + 2 * inc, len(src))  # 序列 2 的在原序列的结束索引

    x, y = start, start + inc  # x, y 代表被合并的序列的当前索引
    z = start  # z 代表合并后的序列的当前索引

    # 从小到底复制到合并后的序列中
    while x < end1 and y < end2:
        if src[x] < src[y]:
            result[z] = src[x]
            x += 1
        else:
            result[z] = src[y]
            y += 1
        z += 1  # 继续

    # 将剩余的值放入合并后的序列
    if x < end1:
        result[z:end2] = src[x:end1]
    elif y < end2:
        result[z:end2] = src[y:end2]


def merge_sort(S):
    """对序列 S 进行原地归并排序"""
    n = len(S)
    logn = math.ceil(math.log(n, 2))  # log_2 n
    src, dest = S, [None] * n  # dest 用于存储结果

    for i in [2 ** k for k in range(logn)]:  # 2, 4, 8, 16, ..., n
        for j in range(0, n, 2 * i):
            merge(src, dest, j, i)  # 自底向上合并

        # 获取结果
        src, dest = dest, src

    if S is not src:
        S[0:n] = src[0:n]  # 传入最后排序后的结果


if __name__ == '__main__':
    S = [85, 24, 63, 45, 17, 31, 96, 50]
    print("=" * 15, "Original List", "=" * 15)
    print(S)

    print("=" * 15, "After Sorted", "=" * 15)
    merge_sort(S)
    print(S)
