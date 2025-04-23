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


class HeapPriorityQueue(PriorityQueueBase):
    """
    堆的实现：完全二叉树，根节点为 min
    """

    # ---------- 非公有方法：二叉树结构 ----------
    def _parent(self, j):
        """返回父节点"""
        return (j - 1) // 2

    def _left(self, j):
        """当前位置的左子节点"""
        return 2 * j + 1

    def _right(self, j):
        """当前位置的右子节点"""
        return 2 * j + 2

    def _has_left(self, j):
        """左子节点是否存在/合法"""
        return self._left(j) < len(self._data)

    def _has_right(self, j):
        """右子节点是否存在/合法"""
        return self._right(j) < len(self._data)

    def _swap(self, i, j):
        """交换 i j 位置上的元素 <=> 冒泡"""
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _upheap(self, j):
        """向上冒泡"""
        parent = self._parent(j)  # j 的父节点
        if j > 0 and self._data[j] < self._data[parent]:  # 非根节点/不满足 Heap-Order
            self._swap(j, parent)  # 冒泡/交换
            self._upheap(parent)  # 递归实现，向上 (parent) 冒泡

    def _downheap(self, j):
        """向下冒泡"""
        # 找到最小的子节点 small_child
        if self._has_left(j):  # 左/非叶节点
            left = self._left(j)
            small_child = left

            if self._has_right(j):  # 右/非叶节点
                right = self._right(j)
                if self._data[right] < self._data[left]:
                    small_child = right

            # 不满足 Heap-Order
            if self._data[small_child] < self._data[j]:
                self._swap(small_child, j)  # 冒泡/交换
                self._downheap(small_child)  # 递归实现，向下 (small_child) 冒泡

    # ---------- 公有方法：堆结构 ----------
    def __init__(self, contents=()):
        """列表用来存储完全二叉树，可根据 contents 自底向上初始化"""
        if not contents:
            self._data = []
        elif not isinstance(contents[0], tuple):
            self._data = [self._Item(e, e) for e in contents]  # 全部写入，任意放置
        else:
            self._data = [self._Item(k, v) for k, v in contents]  # 全部写入，任意放置
        if len(self._data) > 1:  # 确实需要初始化，若为空或只有 1 个则不需要冒泡
            self._heapify()  # 自底向上，逐个冒泡，使得满足 Heap-Order

    def _heapify(self):
        """从底向上初始化堆的冒泡过程"""
        start = self._parent(len(self) - 1)  # 从最后一个节点的父节点开始向下冒泡
        for j in range(start, -1, -1):  # 从后向前，一直到根节点
            self._downheap(j)

    def __len__(self):
        """重载 len()"""
        return len(self._data)

    def add(self, key, value):
        """增加元素"""
        self._data.append(self._Item(key, value))  # 尾部新增
        self._upheap(len(self._data) - 1)  # 从最后一个向上冒泡

    def min(self):
        """查看 min 不删除"""
        if self.is_empty():
            raise Empty('Priority queue is empty')

        item = self._data[0]  # 由 Heap-Order 性质，第一个元素为 min
        return (item._key, item._value)

    def remove_min(self):
        """删除 min"""
        if self.is_empty():
            raise Empty('Priority queue is empty')

        self._swap(0, len(self._data) - 1)  # 交换最后一个元素和根节点
        item = self._data.pop()  # 删除最后一个元素，即交换来的根节点/min
        self._downheap(0)  # 从根/第一个开始向下冒泡
        return (item._key, item._value)


if __name__ == '__main__':
    hpq = HeapPriorityQueue()
    print("=" * 15, "Heap Priority Queue by Array", "=" * 15)
    hpq.add(1, 'small')
    hpq.add(3, 'median')
    hpq.add(5, 'large')
    print("The min is:", hpq.min())
    print("Delete the min:", hpq.remove_min())
    print("Now, the min is:", hpq.min())

    print("=" * 15, "Heap Priority Queue by Array", "=" * 15)
    l = [(1, 'small'), (2, 'median'), (3, 'large')]
    hpq = HeapPriorityQueue(l)
    print("The min is:", hpq.min())
    print("Delete the min:", hpq.remove_min())
    print("Now, the min is:", hpq.min())
