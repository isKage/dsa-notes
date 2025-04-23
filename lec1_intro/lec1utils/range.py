class Range:
    """模拟Python的Range类: range(start, stop, step)"""

    def __init__(self, start, stop=None, step=1):
        """
        初始化
        :param self: 对象自身
        :param start: 起始数字
        :param stop: 终止数字
        :param step: 每步跨度
        :return: Range类
        """
        if step == 0:
            raise ValueError("step can not be zero")

        if stop is None:
            # 应对输入 Range(n), 则当作 Range(0, n) 处理
            start = 0
            stop = start

        # 计算真实长度，应对有余数的情形
        self._length = max(0, (stop - start + step - 1) // step)
        # 考虑到已经计算长度，故无需记录 stop
        self._start = start
        self._step = step

    def __len__(self):
        """长度"""
        return self._length

    def __getitem__(self, index):
        """取数值"""
        if index < 0:
            index += self._length  # 从后向前取

        if index >= self._length or index < 0:
            raise IndexError("index out of range")

        return self._start + index * self._step

    def __str__(self):
        """只是以列表的形式展示，不重要。因为Range是模仿Python的range功能"""
        result = ""
        for i in Range(self._start, self._length):
            result += str(self._start + i * self._step) + ", "
        result = "[" + result[:-2] + "]"
        return result


if __name__ == '__main__':
    print("r1")
    r1 = Range(0, 10)
    print(r1[0])
    print(r1[-1])
    print(len(r1))
    # print(r1[10])  # IndexError: index out of range

    print("r2")
    r2 = Range(0, 10, 2)
    print(r2[1])

    print("r3")
    r3 = Range(0, 10, 3)
    for i in r3:
        print(i)
    print(r3)
