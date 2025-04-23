from utils import ArrayQueue


def YanghuiTri(n):
    """杨辉三角队列实现"""
    TriQ = ArrayQueue()

    # 第一行
    TriQ.enqueue(1)
    print('1'.center(5 * n))

    # 每一次队列中仅仅保存上一行的数据
    for m in range(2, n + 1):  # 第 2 到 n 行
        Line = '1'  # 展示这一行的结果（字符串形式）
        TriQ.enqueue(1)
        p = TriQ.dequeue()

        # 取上一行的两个元素进行加和，放在队尾
        for k in range(2, m):
            q = TriQ.dequeue()
            TriQ.enqueue(p + q)
            Line += ' ' + str(p + q)
            p = q
        TriQ.enqueue(1)
        Line += ' ' + '1'
        print(Line.center(5 * n))


if __name__ == '__main__':
    YanghuiTri(7)
