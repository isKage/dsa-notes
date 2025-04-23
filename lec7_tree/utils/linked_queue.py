class Empty(Exception):
    """Raised when a value is an empty list."""
    pass


class LinkedQueue:
    """单向链表实现队列，先进先出"""

    # -------------- 嵌套的节点类 _Node --------------
    class _Node:
        """单向链表的节点，非公有，实现队列"""
        __slots__ = '_element', '_next'  # _Node 类只拥有这 2 个属性

        def __init__(self, element, next):
            self._element = element
            self._next = next

    # -------------- 正式实现队列 --------------
    def __init__(self):
        """初始化空队列"""
        self._head = None
        self._tail = None
        self._size = 0

    def __len__(self):
        """返回队列长度"""
        return self._size

    def is_empty(self):
        """检查是否为空队列"""
        return self._size == 0

    def first(self):
        """展示队列第一个元素值，但不改变队列"""
        if self.is_empty():
            raise Empty('Queue is empty')
        return self._head._element

    def dequeue(self):
        """删除并返回队列第一个节点和元素"""
        if self.is_empty():
            raise Empty('Queue is empty')

        ans = self._head._element  # 获取第一个元素值
        # 头指针指向下一个节点
        self._head = self._head._next
        self._size -= 1
        # 如果节点清空，则设置尾指针为空
        if self.is_empty():
            self._tail = None
        return ans

    def enqueue(self, e):
        """在尾部增加新节点"""
        newest = self._Node(e, None)
        if self.is_empty():
            self._head = newest  # 如果为空，则新节点为头节点
        else:
            self._tail._next = newest  # 否则尾节点的 next 指向新节点
        self._tail = newest  # 尾节点更新
        self._size += 1
