import os


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def draw_line(tick_length, tick_label=''):
    """绘制刻度

    Args:
        tick_length (int): 刻度长度，即 '-' 字符个数
        tick_label (str, optional): 刻度数，不重要. Defaults to ''.
    """
    line = '-' * tick_length
    if tick_label:
        line += ' ' + tick_label
    print(line)


def draw_interval(center_length):
    """记录分型个数的辅助函数

    Args:
        center_length (int): 负责传入刻度长度给 draw_line 函数，即 '-' 字符个数
    """
    if center_length > 0:
        draw_interval(center_length - 1)
        draw_line(center_length)
        draw_interval(center_length - 1)


def draw_ruler(len_of_ruler, num_scale):
    """绘制刻度尺

    Args:
        len_of_ruler (int): 刻度尺长度，即最大刻度
        num_scale (int): 最大刻度的长度，即最大刻度的 '-' 字符个数，决定了分形次数
    """
    draw_line(num_scale, '0')
    for j in range(1, 1 + len_of_ruler):
        draw_interval(num_scale - 1)
        draw_line(num_scale, str(j))


def binary_search(data, target, left, right):
    if left > right:
        # 全遍历后仍然没找到
        return False

    mid = (left + right) // 2
    if target == data[mid]:
        return True
    elif target < data[mid]:
        return binary_search(data, target, left, mid - 1)
    else:
        return binary_search(data, target, mid + 1, right)


def disk_usage(path):
    total = os.path.getsize(path)  # 当前目录自身的大小
    if os.path.isdir(path):
        for filename in os.listdir(path):
            # 遍历其下子目录的名称
            child_path = os.path.join(path, filename)
            total += disk_usage(child_path)  # 递归调用 计算子目录的大小

    print("{}  {}".format(total, path))
    return total


def linear_sum(seq: list, n: int):
    if n == 1:
        return seq[0]
    else:
        return linear_sum(seq, n - 1) + seq[n - 1]


def reverse(seq, i, j):
    if i < j:
        seq[i], seq[j] = seq[j], seq[i]
        reverse(seq, i + 1, j - 1)


def binary_sum(seq, i, n):
    if n == 1:
        return seq[i]
    else:
        half = n // 2
        return binary_sum(seq, i, half) + binary_sum(seq, i + half, n - half)


def binary_fib(k):
    """ 【不推荐】 """
    if k == 0 or k == 1:
        return k
    else:
        return binary_fib(k - 1) + binary_fib(k - 2)


def linear_fib(k):
    if k == 1:
        return 0, 1
    else:
        i, j = linear_fib(k - 1)
        return j, i + j


def is_solution(S):
    res = False
    if S[0] + S[1] == S[2]:
        res = True
    return res


def puzzle_solve(k, S, U):
    for e in list(U):  # 遍历集合 U 中的每一个元素
        S.append(e)  # 将 e 添加到序列 S 的末尾
        U.remove(e)  # 将 e 从集合 U 中移除

        if k == 1:
            if is_solution(S):
                # 检查当前序列 S 是否是谜题的解
                print("Solution found: {} + {} = {}".format(S[0], S[1], S[2]))
        else:
            # 递归调用，继续扩展序列
            puzzle_solve(k - 1, S, U)

        # 回溯
        S.pop()  # 将 e 从序列 S 的末尾移除
        U.add(e)  # 将 e 添加回集合 U


if __name__ == "__main__":
    # 阶乘
    print("=" * 15 + " 阶乘 " + "=" * 15)
    print(factorial(4))  # 24

    # 标尺刻度
    print("=" * 15 + " 标尺刻度 " + "=" * 15)
    draw_ruler(len_of_ruler=1, num_scale=3)

    # 二分查找
    print("=" * 15 + " 二分查找 " + "=" * 15)
    seq = [2, 4, 5, 7, 8, 9, 12, 14, 17, 19, 22, 25, 27, 28, 33, 37]
    print(binary_search(seq, target=22, left=0, right=len(seq) - 1))

    # 磁盘大小
    print("=" * 15 + " 磁盘大小 " + "=" * 15)
    print(os.path.getsize(os.getcwd()))
    total = disk_usage(os.getcwd())
    print(total)

    # 递归求前 n 项和
    print("=" * 15 + " 递归求前 n 项和 " + "=" * 15)
    seq = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(linear_sum(seq, 3))

    # 逆置序列
    print("=" * 15 + " 逆置序列 " + "=" * 15)
    seq = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    reverse(seq, i=0, j=len(seq) - 1)
    print(seq)
    reverse(seq, i=3, j=len(seq) - 1)
    print(seq)

    # 二路递归求和
    print("=" * 15 + " 二路递归求和 " + "=" * 15)
    seq = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(binary_sum(seq, i=0, n=len(seq)))
    print(binary_sum(seq, i=1, n=len(seq) - 1))

    # 二路递归产生斐波那契数列 【不推荐】
    # print("=" * 15 + " 二路递归产生斐波那契数列 " + "=" * 15)
    # for i in range(10):
    #     print(binary_fib(i), end=' ')

    # 线性递归产生斐波那契数列
    print("=" * 15 + " 线性递归产生斐波那契数列 " + "=" * 15)
    for i in range(1, 10):
        front, back = linear_fib(i)
        print(back, end=' ')
    print()

    # 求和谜题
    print("=" * 15 + " 求和谜题 " + "=" * 15)
    U = {1, 2, 3, 4}
    k = 3
    S = []
    puzzle_solve(k, S, U)
