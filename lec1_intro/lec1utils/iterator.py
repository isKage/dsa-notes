class SequenceIterator:
    """为已经定义了__len__和__getitem__的对象实现迭代器方法"""

    def __init__(self, seq):
        """迭代器初始化"""
        self._seq = seq
        self._k = -1  # 只有迭代器调用时才从 0 开始

    def __next__(self):
        """迭代器"""
        self._k += 1
        if self._k < len(self._seq):
            return self._seq[self._k]  # 返回向前一步后的值
        else:
            raise StopIteration()

    def __iter__(self):
        """一般__iter__方法都要返回自己，一种书写规范"""
        return self


if __name__ == '__main__':
    l = [1, 2, 3, 4, 5]
    t = (9, 8, 7, 6, 5)

    l_seq = SequenceIterator(l)
    print(next(l_seq))
    print(next(l_seq))
    print(next(l_seq))

    t_seq = SequenceIterator(t)
    print(next(t_seq))
    print(next(t_seq))
    print(next(t_seq))

