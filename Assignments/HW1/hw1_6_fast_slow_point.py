"""
假设一个单链表类使用的节点与课件中的节点相同，但并未记录链表中节点的数目。
请为该类添加一个方法，该方法用于高效找到链表的中间节点。
若链表长度为偶数，则返回两个中间节点中靠后的那一个。
"""


# 快慢指针法

class LinkedList:
    """定义链表类"""

    class _Node:
        """节点类，非公有"""
        __slots__ = '_element', '_next'

        def __init__(self, element, next):
            self._element = element
            self._next = next

    def __init__(self):
        """初始化"""
        self._head = None
        self._size = 0

    def first(self):
        """头指针"""
        return self._head

    def after(self, p):
        """指针后移"""
        return p._next

    def __iter__(self):
        """迭代器展示元素值"""
        cursor = self.first()
        while cursor is not None:
            yield cursor._element
            cursor = self.after(cursor)

    def __getitem__(self, p):
        """根据节点指针获取元素值"""
        return p._element

    def add_first(self, e):
        """在头部插入"""
        newest = self._Node(e, self._head)
        self._head = newest
        # self._size += 1
        return newest

    def from_list(self, l: list):
        """从列表 list 方便的创建链表"""
        for i in reversed(l):
            self.add_first(i)
        return self.first()  # 返回第一个节点

    def __str__(self):
        """以 str 形式展示"""
        show_as_list = ""
        for i in self:
            show_as_list += str(i) + ", "
        return "<Linked List: [" + show_as_list[:-2] + "] >"

    # ---------- 当没有记录链表长度时 ----------
    # def __len__(self):
    #     """链表长度"""
    #     return self._size

    # def is_empty(self):
    #     """是否为空"""
    #     return self._size == 0
    # ---------------------------------------

    def mid(self):
        """返回中间节点"""
        # 快慢指针从头开始遍历
        fast = self._head
        slow = self._head

        if fast is None:
            # 避免空链表
            raise ValueError('The Linked List is Empty!')

        # 直到快指针是尾节点才停止
        while fast is not None and fast._next is not None:
            fast = fast._next._next  # 快指针每次移动 2 格
            slow = slow._next  # 慢指针每次移动 1 格

        # 当快指针到达尾节点，此时慢指针刚好在中间 len / 2
        return slow


if __name__ == '__main__':
    print("=" * 15, "Initial Linked List", "=" * 15)
    ll1 = LinkedList()
    ll2 = LinkedList()
    ll1.from_list([1, 2, 3, 4, 5])
    ll2.from_list([1, 2, 3, 4, 5, 6])
    print(ll1)
    print(ll2)

    print("=" * 15, "Middle Element", "=" * 15)
    print("Mid of ll1 is: {}".format(ll1[ll1.mid()]))
    print("Mid of ll2 is: {}".format(ll2[ll2.mid()]))
