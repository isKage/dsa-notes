class _DoublyLinkedBase:
    """双向链表的基础类/父类"""

    # -------------- 嵌套的节点类 _Node --------------
    class _Node:
        """双向链表的节点类，包含元素值、prev 指针和 next 指针"""
        __slots__ = '_element', '_prev', '_next'

        def __init__(self, element, prev, next):
            self._element = element
            self._prev = prev
            self._next = next

    # -------------- 正式实现链表 --------------
    def __init__(self):
        """初始化一个空链表"""
        # 创建头哨兵、尾哨兵
        self._header = self._Node(None, None, None)
        self._trailer = self._Node(None, None, None)

        self._header._next = self._trailer  # 头哨兵 next 指向尾哨兵
        self._trailer._prev = self._header  # 尾哨兵 prev 指向头哨兵

        self._size = 0  # 链表长度，不包括头尾哨兵

    def __len__(self):
        """链表长度 len() 重载"""
        return self._size

    def is_empty(self):
        """判断是否为空"""
        return self._size == 0

    def _insert_between(self, e, predecessor, successor):
        """在节点 predecessor, successor 插入插入新节点，并返回这个新节点"""
        # 创建新节点，并将其 prev 指向 predecessor | 其 next 指向 successor
        newest = self._Node(e, predecessor, successor)

        predecessor._next = newest  # predecessor 的 next 指向新节点
        successor._prev = newest  # successor 的 prev 指向新节点

        self._size += 1
        return newest

    def _delete_node(self, node):
        """传入节点并删除，返回被删除的值"""
        # 记录将被删除的节点的前后信息
        predecessor = node._prev
        successor = node._next
        # 连接 predecessor 和 successor
        predecessor._next = successor
        successor._prev = predecessor

        element = node._element
        # 孤立节点 node : 设为空，用于标识这是即将被删除的节点
        node._prev, node._next, node._element = None, None, None

        self._size -= 1
        return element
