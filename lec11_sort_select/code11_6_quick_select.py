import random


def quick_select(S, k):
    """返回 S 中第 k 小的数"""
    if len(S) == 1:
        return S[0]

    pivot = random.choice(S)  # 随机选取基准
    # 分为 3 个子序列
    L = [x for x in S if x < pivot]
    E = [x for x in S if x == pivot]
    G = [x for x in S if pivot < x]

    if k <= len(L):
        return quick_select(L, k)  # k th smallest lies in L
    elif k <= len(L) + len(E):
        return pivot  # k th smallest equal to pivot
    else:
        j = k - len(L) - len(E)  # new selection parameter
        return quick_select(G, j)  # k th smallest is jth in G


if __name__ == '__main__':
    S = [85, 24, 63, 45, 17, 31, 96, 50]

    print("=" * 15, "Original List", "=" * 15)
    print(S)

    k = 1
    print("=" * 15, f"The {k}th smallest is", "=" * 15)
    k_th = quick_select(S, k)
    print(k_th)
