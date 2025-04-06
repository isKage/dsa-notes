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


class PositionalList(_DoublyLinkedBase):
    """利用双向链表实现位置列表类"""

    # -------------- 内嵌的位置类 --------------
    class Position:
        """抽象的位置类，存储节点的位置信息"""

        def __init__(self, container, node):
            """初始化位置信息"""
            # _container 存储列表类 PositionalList 表明当前位置类属于这个列表类
            self._container = container
            self._node = node

        def element(self):
            """返回当前位置的节点元素值"""
            return self._node._element

        def __eq__(self, other):
            """检查二者是否具有相同的位置信息 重载运算符 =="""
            return type(other) is type(self) and other._node is self._node

        def __ne__(self, other):
            """与上面相反 重载运算符 !="""
            return not self == other

    # -------------- 检查位置类、为节点实例化位置类 --------------
    def _validate(self, p):
        """检查是否是合法的 Position 类，返回位置类存储的节点类"""
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position')
        if p._container is not self:
            # 检查当前位置类 p 是否属于当前列表，以免误操作了别的列表
            raise ValueError('p does not belong to this container')
        if p._node._next is None:
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self, node):
        """对每个节点，实例化它的位置类"""
        if node is self._header or node is self._trailer:
            return None
        else:
            # 创建属于当前列表的位置类
            return self.Position(self, node)

    # -------------- 查看位置列表类的方法 --------------
    def first(self):
        """返回第一个节点的位置类，注意不含哨兵节点"""
        return self._make_position(self._header._next)

    def last(self):
        """返回最后一个节点的位置类，注意不含哨兵节点"""
        return self._make_position(self._trailer._prev)

    def before(self, p):
        """返回位置类 p 前面的位置类"""
        node = self._validate(p)  # 检查是否是合法的位置类
        return self._make_position(node._prev)

    def after(self, p):
        """返回位置类 p 后面的位置类"""
        node = self._validate(p)
        return self._make_position(node._next)

    def __iter__(self):
        """迭代器，逐个生成返回列表的元素值"""
        cursor = self.first()
        while cursor is not None:
            yield cursor.element()
            cursor = self.after(cursor)

    # -------------- 改变位置列表类的方法 --------------
    def _insert_between(self, e, predecessor, successor):
        """使用父类方法，但返回位置类"""
        # 覆写父类插入方法
        node = super()._insert_between(e, predecessor, successor)
        return self._make_position(node)

    def add_first(self, e):
        """在头部插入，返回位置类"""
        return self._insert_between(e, self._header, self._header._next)

    def add_last(self, e):
        return self._insert_between(e, self._trailer._prev, self._trailer)

    def add_before(self, p, e):
        """在位置类 p 前插入"""
        original = self._validate(p)
        return self._insert_between(e, original._prev, original)

    def add_after(self, p, e):
        original = self._validate(p)
        return self._insert_between(e, original, original._next)

    def delete(self, p):
        """删除位置类 p 返回 p 上的值"""
        original = self._validate(p)
        return self._delete_node(original)  # 父类方法

    def replace(self, p, e):
        """替换位置 p 的值为 e，返回 p 位置之前的值"""
        original = self._validate(p)
        old_value = original._element
        original._element = e
        return old_value


def insertion_sort(L: PositionalList):
    """
    对链表插入排序
    :param L: 位置列表类 PositionalList
    :return: no return
    """
    if len(L) > 1:
        marker = L.first()
        while marker != L.last():  # 遍历链表
            pivot = L.after(marker)
            value = pivot.element()  # 保存后一个节点的值
            if value > marker.element():  # 满足排序要求（从小到大）
                marker = pivot
            else:
                walk = marker
                # 当没到第一个元素 并且 walk 前一个元素比 value 大，walk 不断向前找
                while walk != L.first() and L.before(walk).element() > value:
                    walk = L.before(walk)

                L.delete(pivot)
                L.add_before(walk, value)  # 插入到此时 walk 前


if __name__ == '__main__':
    print("=" * 15, "Positional List based on Linked List", "=" * 15)
    pl = PositionalList()

    p1 = pl.add_first(e=1)
    p2 = pl.add_last(e=2)
    p0 = pl.add_first(e=0)
    p4 = pl.add_last(e=4)

    for p_node_element in pl:
        print(p_node_element, end=" ")
    print()

    print("p1 == p2 : {}".format(p1 == p2))
    print("p1 != p2 : {}".format(p1 != p2))

    p3 = pl.add_after(p=p2, e=3)

    for p_node_element in pl:
        print(p_node_element, end=" ")
    print()

    print("first: {}".format(pl.first().element()))

    print("=" * 15, "Insertion sort", "=" * 15)
    pl.add_before(p=p2, e=5)
    pl.add_before(p=p0, e=9)
    pl.add_after(p=p2, e=2)
    pl.replace(p=p4, e=3)
    pl.replace(p=p3, e=4)

    for p_node_element in pl:
        print(p_node_element, end=" ")
    print()

    insertion_sort(pl)

    for p_node_element in pl:
        print(p_node_element, end=" ")
    print()
