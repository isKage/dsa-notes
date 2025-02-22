from abc import ABC, abstractmethod


class Sequence(ABC):
    """抽象基类 Sequence"""

    @abstractmethod
    def __len__(self):
        """返回序列长度，由子类实现"""
        pass

    @abstractmethod
    def __getitem__(self, j):
        """返回第 j 位置的值，由子类实现"""
        pass

    def __contains__(self, val):
        """查看 val 是否在序列中，返回 True or False"""
        for j in range(len(self)):
            if val == self[j]:
                return True
        return False

    def index(self, val):
        """返回 val 在序列中的下标"""
        for j in range(len(self)):
            if val == self[j]:
                return j
        raise ValueError("Value not found")

    def count(self, val):
        """计数多少值等于 val"""
        k = 0
        for j in range(len(self)):
            if val == self[j]:
                k += 1
        return k


class MyNewRange(Sequence):
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
        for i in MyNewRange(self._start, self._length):
            result += str(self._start + i * self._step) + ", "
        result = "[" + result[:-2] + "]"
        return result


if __name__ == "__main__":
    # seq = Sequence()   # 报错，因为这是抽象基类，不可实例化，有方法尚未被具体定义
    r = MyNewRange(0, 10)
    print(r)

    print(4 in r)  # 判断 4 是否在序列中 __contains__ 方法
    print(r.index(0))  # 返回下标 index 方法
    print(r.count(1))  # 查看多少值等于 1
