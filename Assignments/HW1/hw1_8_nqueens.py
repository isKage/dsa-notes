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
    :return: 结果列表 res = [] 存储了转换格式后的解
    """
    res = []  # 存储所有有效解
    stack = ArrayStack()  # 栈存储皇后的位置（一个列表，元素为位置坐标）
    stack.push([])  # 初始化
    # 以列表 [] 形式存储是为了简便检索之前已经确定的皇后位置，否则需要遍历栈元素：以空间换时间

    while not stack.is_empty():  # 空栈则无解
        # Step 1: 出栈当前状态
        queens = stack.pop()
        row = len(queens)  # 列表长度代表已经放置的皇后数

        # Step 2: 如果所有行都处理完毕，说明 queens 是一个有效解列表
        if row == N:
            # 转换为棋盘表示
            res.append([' · ' * i + ' Q ' + ' · ' * (N - i - 1) for i in [q[1] for q in queens]])
            continue

        # Step 3: 在当前行选择确切位置，即向 queens 列表加入下一行新的位置
        for col in range(N):
            flag = True  # 判断是否可填入
            for r, c in queens:  # 检查之前的所有皇后位置
                if c == col or abs(r - row) == abs(c - col):
                    flag = False  # 同列、同对角线 -> False

            if flag:
                # 如果可填入则加入 queens 位置解列表
                new_queens = queens + [(row, col)]  # 需要复制一份，以免改变栈里其他元素
                # 压入新状态：更新皇后位置
                stack.push(new_queens)

    return res, len(res)  # 返回解和解个数


if __name__ == '__main__':
    res, res_num = n_queens_stack(8)  # 8 皇后问题
    for row in res:
        print("Answer:")
        for i in row:
            print(i)
    print("Total {} answers!".format(res_num))
