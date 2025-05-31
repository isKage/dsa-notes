def find_brute(P, T):
    """
    穷举法模式匹配
    :param P: 寻找的模式
    :param T: 被查找的对象
    :return: T 的索引位置, 若失败返回 -1
    """
    n, m = len(T), len(P)
    for i in range(n - m + 1):
        k = 0
        while k < m and T[i + k] == P[k]:
            k += 1  # 当前匹配成功, 继续匹配
        if k == m:
            return i  # 完整匹配, 返回位置
    return -1


def compute_kmp_fail(pattern):
    """计算模式的失败函数"""
    m = len(pattern)
    fail = [0] * m
    j = 1
    k = 0
    while j < m:
        if pattern[j] == pattern[k]:
            fail[j] = k + 1
            j += 1
            k += 1
        elif k > 0:
            k = fail[k - 1]
        else:
            j += 1
    return fail


def find_kmp(pattern, text):
    """
    从 text 中找到第一个完全匹配 pattern 的位置
    :param pattern: 寻找的模式
    :param text: 被查找的对象
    :return: text 的索引位置, 若失败返回 -1
    """
    m, n = len(pattern), len(text)
    if m == 0:
        return 0

    fail = compute_kmp_fail(pattern)
    j = 0
    k = 0
    while j < n:
        if text[j] == pattern[k]:
            if k == m - 1:
                return j - m + 1
            j += 1
            k += 1
        elif k > 0:
            k = fail[k - 1]
        else:
            j += 1
    return -1


if __name__ == '__main__':
    text = "abaababaabababaca"
    pattern = "ababac"

    find_idx = find_kmp(pattern, text)
    print(text[find_idx:find_idx + len(pattern)])
