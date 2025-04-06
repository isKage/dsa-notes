try:
    from .positional_list import PositionalList
except ImportError:
    from positional_list import PositionalList


class Empty(Exception):
    """自定义异常类 Empty"""
    pass


class PriorityQueueBase:
    """
    优先级队列的抽象数据类型基础类 ADT
    """

    # ---------- 嵌套的 _Item 类 ----------
    class _Item:
        """每一个元素的存储方式：(k, v)"""
        __slots__ = '_key', '_value'

        def __init__(self, k, v):
            """初始化键值对 (k, v)"""
            self._key = k
            self._value = v

        def __lt__(self, other):
            """重载运算符 <"""
            return self._key < other._key  # 根据 key 键值比较大小

    # ---------- 优先级队列 ADT ----------
    def is_empty(self):
        """__len__ 方法暂时未定义，由子类定义"""
        return len(self) == 0


class UnsortedPriorityQueue(PriorityQueueBase):
    """未排序的列表实现优先级队列"""

    def __init__(self):
        """初始化，利用队列类 PositionalList"""
        self._data = PositionalList()

    def __len__(self):
        """返回长度"""
        return len(self._data)

    def add(self, key, value):
        """增加元素 (key, value)"""
        # 向 PositionalList 队列类新增 _Item 类实例
        self._data.add_last(self._Item(key, value))

    def _find_min(self) -> PositionalList.Position:
        """最小键值元素 _Item"""
        if self.is_empty():
            raise Empty('Priority queue is empty')

        # 遍历
        small = self._data.first()
        walk = self._data.after(small)
        while walk is not None:
            # 这里的 element 返回的是一个 _Item 类
            if walk.element() < small.element():
                small = walk  # 记录最小值
            walk = self._data.after(walk)  # 向后更新一步
        return small  # 遍历完后得到最小值 (返回的是 PositionalList.Position 类)

    def min(self) -> tuple:
        """返回最小 (key, value)"""
        p = self._find_min()
        item = p.element()  # PositionalList.Position._node._element -> _Item 类
        return (item._key, item._value)

    def remove_min(self) -> tuple:
        """返回最小 (key, value) 并删除"""
        p = self._find_min()
        item = self._data.delete(p)
        return (item._key, item._value)


class SortedPriorityQueue(PriorityQueueBase):
    """排序的列表实现优先级队列"""

    def __init__(self):
        """初始化，利用队列类 PositionalList"""
        self._data = PositionalList()

    def __len__(self):
        """返回长度"""
        return len(self._data)

    def add(self, key, value):
        """增加元素 (key, value)"""
        newest = self._Item(key, value)  # 创建新的 _Item 类实例
        walk = self._data.last()  # 从最后开始检查

        # 找到第一个比 newest 大的元素
        while walk is not None and newest < walk.element():
            walk = self._data.before(walk)  # go ahead

        # 向 PositionalList 队列类新增 _Item 类实例
        if walk is None:
            self._data.add_first(newest)  # 第一个位置插入
        else:
            self._data.add_after(walk, newest)  # 在 walk 后插入

    def min(self) -> tuple:
        """返回最小 (key, value)"""
        if self.is_empty():
            raise Empty('Priority queue is empty')
        # 有序队列：第一个元素即为最小
        p = self._data.first()
        item = p.element()
        return (item._key, item._value)

    def remove_min(self) -> tuple:
        """返回最小 (key, value) 并删除"""
        if self.is_empty():
            raise Empty('Priority queue is empty')
        # 同理，第一个元素即为最小
        item = self._data.delete(self._data.first())
        return (item._key, item._value)


if __name__ == '__main__':
    upq = UnsortedPriorityQueue()
    print("=" * 15, "Unsorted Priority Queue", "=" * 15)
    upq.add(1, 'small')
    upq.add(3, 'median')
    upq.add(5, 'large')
    print("The min is:", upq.min())
    print("Delete the min:", upq.remove_min())
    print("Now, the min is:", upq.min())

    spq = SortedPriorityQueue()
    print("=" * 15, "Sorted Priority Queue", "=" * 15)
    spq.add(1, 'small')
    spq.add(3, 'median')
    spq.add(5, 'large')
    print("The min is:", spq.min())
    print("Delete the min:", spq.remove_min())
    print("Now, the min is:", spq.min())
