from utils import Empty


class LinkedCircularQueue:
    """循环链表实现循环队列"""

    # -------------- 嵌套的节点类 _Node --------------
    class _Node:
        """单向链表的节点，非公有，实现循环队列"""
        __slots__ = '_element', '_next'  # _Node 类只拥有这 2 个属性

        def __init__(self, element, next):
            self._element = element
            self._next = next

    # -------------- 正式实现队列 --------------
    def __init__(self):
        """初始化空队列"""
        self._tail = None  # 只需要一个指针
        self._size = 0

    def __len__(self):
        """返回长度"""
        return self._size

    def is_empty(self):
        """判断是否为空"""
        return self._size == 0

    def first(self):
        """展示队列第一个元素值 tail.next ，但不改变队列"""
        if self.is_empty():
            raise Empty('Queue is empty')
        # 对循环链表而言，定义尾指针指向节点的下一个节点为头节点
        head = self._tail._next
        return head._element

    def dequeue(self):
        """删除并返回队列头节点 tail.next 和元素"""
        if self.is_empty():
            raise Empty('Queue is empty')

        oldhead = self._tail._next  # 获取头节点
        if self._size == 1:
            self._tail = None  # 只有一个节点，删除后变成空队列
        else:
            self._tail._next = oldhead._next
            # 原来的 tail.next 即 oldhead 被释放，因为没有指针指向它
        self._size -= 1
        return oldhead._element

    def enqueue(self, e):
        """在尾部 tail 增加新节点"""
        newest = self._Node(e, None)
        if self.is_empty():
            # 如果为空，则新节点自己指向自己，后面再由 tail 指向 newest
            newest._next = newest
        else:
            newest._next = self._tail._next  # 新节点指向头节点
            self._tail._next = newest  # 原来的尾节点的 next 指针指向新节点
        self._tail = newest  # 尾节点更新
        self._size += 1

    def rotate(self):
        """训练轮转一次"""
        if self.is_empty():
            raise Empty('Queue is empty')
        self._tail = self._tail._next  # 指示指针 (尾指针) tail 向后移动一位


if __name__ == '__main__':
    print("=" * 15, "Initializing Circular Queue", "=" * 15)
    q = LinkedCircularQueue()

    print("=" * 15, "Add Elements", "=" * 15)
    x1, x2, x3, x4 = 1, 2, 3, 4
    print("add: {}".format(x1))
    q.enqueue(x1)
    print("first: {}".format(q.first()))

    print("add: {}".format(x2))
    q.enqueue(x2)
    print("first: {}".format(q.first()))

    print("add: {}".format(x3))
    q.enqueue(x3)
    print("first: {}".format(q.first()))

    print("add: {}".format(x4))
    q.enqueue(x4)
    print("first: {}".format(q.first()))

    print("=" * 15, "Rotation", "=" * 15)
    print("rotate")
    q.rotate()
    print("first: {}".format(q.first()))

    print("rotate")
    q.rotate()
    print("first: {}".format(q.first()))

    print("rotate")
    q.rotate()
    print("first: {}".format(q.first()))

    print("rotate")
    q.rotate()
    print("first: {}".format(q.first()))

    print("=" * 15, "Remove the Last one", "=" * 15)
    print("dequeue: {}".format(q.dequeue()))
    print("first: {}".format(q.first()))

    print("=" * 15, "Rotation", "=" * 15)
    print("rotate")
    q.rotate()
    print("first: {}".format(q.first()))
    print("rotate")
    q.rotate()
    print("first: {}".format(q.first()))
