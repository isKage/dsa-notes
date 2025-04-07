"""
基于数组实现双端队列 ADT


利用数组实现双端队列，动态存储数组，记录 front 和 size 而尾部采用循环数组的方式计算得到。
除了基础的 add_first, add_last, first, last, delete_first, delete_last 方法，
补充了 __str__, __iter__, info 分别用于展示队列、迭代器和返回 debug 调试信息，
特别地，增加类方法 init 运行从序列直接初始化队列；clear 方法清空队列。
"""


class Empty(Exception):
    """队列为空的异常类"""
    pass


class ArrayDequeue:
    """基于数组实现双端队列 ADT"""
    DEFAULT_CAPACITY = 10  # 默认数组长度

    def __init__(self, capacity=DEFAULT_CAPACITY):
        self._data = [None] * capacity
        self._size = 0
        self._front = 0

    def __len__(self):
        """返回队列实际长度"""
        return self._size

    def is_empty(self):
        """返回实际是否为空"""
        return self._size == 0

    def add_last(self, e):
        """在尾部增加元素"""
        # 如果列表已满，则增倍扩展数组
        if self._size == len(self._data):
            self._resize(2 * len(self._data))

        # 插入
        last = (self._front + self._size) % len(self._data)  # 队尾索引
        self._data[last] = e
        self._size += 1

    def add_first(self, e):
        """在头部增加元素"""
        # 如果列表已满，则增倍扩展数组
        if self._size == len(self._data):
            self._resize(2 * len(self._data))

        # 插入
        first = (self._front - 1) % len(self._data)
        self._data[first] = e
        self._front = (self._front - 1) % len(self._data)
        self._size += 1

    def delete_first(self):
        """在头部删除元素，并返回"""
        if self.is_empty():
            raise Empty("Dequeue is empty!")

        first = self._data[self._front]  # 获取出队元素值
        self._data[self._front] = None  # 出队位置置空
        self._front = (self._front + 1) % len(self._data)  # 循环利用数组
        self._size -= 1  # 长度减一
        return first

    def delete_last(self):
        """在尾部删除元素，并返回"""
        if self.is_empty():
            raise Empty("Dequeue is empty!")

        last_idx = (self._front + self._size - 1) % len(self._data)  # 尾部索引
        last = self._data[last_idx]  # 获取出队元素值
        self._data[last_idx] = None  # 出队位置置空
        self._size -= 1
        return last

    def first(self):
        """返回第一个元素"""
        if self.is_empty():
            raise Empty("Dequeue is empty!")
        return self._data[self._front]

    def last(self):
        """返回最后一个元素"""
        if self.is_empty():
            raise Empty("Dequeue is empty!")
        return self._data[(self._front + self._size - 1) % len(self._data)]

    @classmethod
    def init(cls, d: list):
        """根据序列 d 初始化一个队列"""
        dq = cls(capacity=len(d))  # 返回新对象，不使用原来的 d
        for i in range(len(d)):
            dq.add_last(d[i])
        return dq

    def clear(self):
        """清空队列"""
        self._data = [None] * len(self._data)  # 保留原来的容量
        self._front = 0
        self._size = 0

    def __str__(self):
        """字符串形式展示队列 from front to end"""
        res = []
        for e in self:
            res.append(e)
        return str(res)

    def __iter__(self):
        """增加迭代器性质"""
        walk = self._front
        for _ in range(self._size):
            yield self._data[walk]
            walk = (walk + 1) % len(self._data)

    def info(self):
        """返回非公有的属性，用于调试"""
        debug = dict()
        debug['_data'] = self._data
        debug['_front'] = self._front
        debug['_size'] = self._size
        return debug

    # ---------- non-public ----------
    def _resize(self, capacity):
        """空间为 capacity 新列表"""
        old = self._data  # 原始列表
        self._data = [None] * capacity  # 扩展后的空列表

        walk = self._front  # 队列的头部
        for k in range(self._size):
            self._data[k] = old[walk]  # 复制 old 到新的队列
            walk = (walk + 1) % len(old)  # old 是循环使用的
        self._front = 0  # 新队列的头部和列表的 0 (列表头部) 是对齐的


if __name__ == "__main__":
    """
    Test and Debug
    """

    print("=" * 10, "Init by a list", "=" * 10)
    dq = ArrayDequeue.init([1, 2, 3, 4, 5])
    print(dq)
    print("Info for Debug:", dq.info())

    print("=" * 10, "Delete first: {}".format(dq.delete_first()), "=" * 10)
    print(dq)
    print("Info for Debug:", dq.info())

    print("=" * 10, "Delete last: {}".format(dq.delete_last()), "=" * 10)
    print(dq)
    print("Info for Debug:", dq.info())

    print("=" * 10, "Add first", "=" * 10)
    dq.add_first(5)
    print(dq)
    print("Info for Debug:", dq.info())

    print("=" * 10, "Add last", "=" * 10)
    dq.add_last(1)
    print(dq)
    print("Info for Debug:", dq.info())

    print("=" * 10, "Add first, out of size", "=" * 10)
    dq.add_first('new')
    print(dq)
    print("Info for Debug:", dq.info())

    print("=" * 10, "Empty deque", "=" * 10)
    empty_dq = ArrayDequeue()
    try:
        empty_dq.delete_first()
    except Empty as e:
        print(e)

    print("=" * 10, "Clear the dq", "=" * 10)
    dq.clear()
    print(dq)
    print("Info for Debug:", dq.info())