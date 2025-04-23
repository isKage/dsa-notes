from collections.abc import Sequence


class NewRange(Sequence):
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
        for i in NewRange(self._start, self._length):
            result += str(self._start + i * self._step) + ", "
        result = "[" + result[:-2] + "]"
        return result


if __name__ == "__main__":
    r = NewRange(0, 10)
    print(r)

    print(4 in r)  # 判断 4 是否在序列中 __contains__ 方法
    print(r.index(0))  # 返回下标 index 方法
    print(r.count(1))  # 查看多少值等于 1
