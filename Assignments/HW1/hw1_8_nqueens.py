"""
N 皇后问题：在 NxN 格的国际象棋上摆放 N 个皇后，使其不能互相攻击，即任意两个皇后都不能处于同一行、同一列或同一斜线上，问有多少种摆法？
"""


class Empty(Exception):
    """栈为空的异常类"""
    pass


class ArrayStack:
    """基于数组的栈数据类型 LIFO"""

    def __init__(self):
        """初始化空栈"""
        self._data = []  # 适配器模式，隐藏 list 实例化对象

    def __len__(self):
        """栈的元素个数"""
        return len(self._data)

    def is_empty(self):
        """判断是否为空"""
        return len(self._data) == 0

    def push(self, e):
        """向栈顶插入元素"""
        self._data.append(e)

    def top(self):
        """返回栈顶元素"""
        if self.is_empty():
            raise Empty("Stack is empty")
        return self._data[-1]

    def pop(self):
        """从栈顶删除元素"""
        if self.is_empty():
            raise Empty("Stack is empty")
        return self._data.pop()


def n_queens_stack(N):
    """
    N 皇后问题
    :param N: 棋盘大小 N x N
    :return: 结果列表 res = []
    """
    res = []  # 存储所有有效解
    stack = ArrayStack()  # 存储每一行的信息

    # 初始状态：queen 的位置，第 0 行，第一个 set 表示列，第二个表示主对角线，第三个表示副对角线
    # set() 存储了之前放入皇后的位置，表示已被占有，后面的行皇后不可填入这些列
    stack.push(([], 0, set(), set(), set()))

    while not stack.is_empty():
        # Step 1: 出栈当前状态
        queen, row, cols, diag1, diag2 = stack.pop()

        # 如果所有行都处理完毕，说明 queen 是一个有效解
        if row == N:
            # 转换为棋盘表示
            res.append([' · ' * i + ' Q ' + ' · ' * (N - i - 1) for i in queen])
            continue

        # Step 2: 在当前行选择列的位置，即 queen 位置
        for col in range(N):
            # 检查 主对角线、副对角线 是否有其他皇后
            curr_diag1 = row - col  # 正对角线：行 - 列
            curr_diag2 = row + col  # 反对角线：行 + 列

            # 列、主对角线、副对角线 是否被占用，占有则跳过，继续寻找
            if col in cols or curr_diag1 in diag1 or curr_diag2 in diag2:
                continue

            # 创建新集合（创建副本，以免相互干扰，否则会直接改变栈中其他元素的值）
            new_cols = set(cols)  # 创建新的列集
            new_diag1 = set(diag1)  # 创建新的主对角线集
            new_diag2 = set(diag2)  # 创建新的副对角线集

            # 更新
            new_cols.add(col)  # 将当前列加入列 new_cols 集，表示占有
            new_diag1.add(curr_diag1)  # 将当前正对角线加入冲突集，表示占有
            new_diag2.add(curr_diag2)  # 将当前反对角线加入冲突集，表示占有
            new_queen = queen + [col]  # 将当前列加入路径，表示占有

            # 压入新状态：更新皇后位置、下一行、列、对角线
            stack.push((new_queen, row + 1, new_cols, new_diag1, new_diag2))

    return res, len(res)


if __name__ == '__main__':
    res, res_num = n_queens_stack(8)  # 8 皇后问题
    for row in res:
        print("Answer:")
        for i in row:
            print(i)
    print("Total {} answers!".format(res_num))
