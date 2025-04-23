"""
汉诺塔问题：
一个古老的印度神庙里有 3 根柱，其中一个自上而下放置了由小到大的 64 个金盘。
僧侣们依照以下规则把 64 个金盘移动到另一个柱子上：
- 一次只能移动一个金盘；
- 金盘只能在柱子上存放；
- 小盘必须始终放置在大盘上方；
请设计并用 Python 实现算法，接收用户输入的金盘数目 N
输出将金盘从柱子 0 移动到柱子 2 的全过程。
输出格式为：move(a, x, y)，其中 a 为盘子编号（1 ~ N），x 和 y 为柱子编号（0 ~ 2），表示将盘子 a 从柱子 x 移动到柱子 y。
"""


# 递归设计

def hanoi(N, start=0, between=1, to=2):
    """
    汉诺塔问题的逐步步骤
    :param N: 金盘数量
    :param start: 移动前金盘所在柱子
    :param between: 借助的柱子
    :param to: 最后移动到的柱子
    """

    def move(a, x, y):
        """方便的展示 move(a, x, y)"""
        # print("{} from {} to {}".format(a, x, y))
        print("move({0}, {1}, {2})".format(a, x, y))

    if N == 1:
        # 如果只有一个金盘，则直接从 start 移动到 to
        move(N, start, to)
    else:
        # 1. 先将 1 ~ N - 1 的金盘从 start 借助 to 移动到 between
        hanoi(N - 1, start, to, between)
        # 2. 然后将 N 盘移动到 to 柱
        move(N, start, to)
        # 3. 最后将 1 ~ N - 1 盘借助 start 柱移动到 to 柱 (因为此时 start 柱放着 N 比 1 ~ N - 1 都大)
        hanoi(N - 1, between, start, to)


if __name__ == '__main__':
    N = 4
    hanoi(N, start=0, between=1, to=2)
