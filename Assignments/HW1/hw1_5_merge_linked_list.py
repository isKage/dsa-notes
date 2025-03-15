"""
请编写一个 python 函数，将两个有序的单向链表合并为一个有序链表，合并后使原链表为空。
链表的节点结构参考课件中的单向链表节点，且链表带有哨兵节点作为头节点。
有序链表中元素为从小到大排列。
"""


# 单向链表合并问题

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
        self._header = self._Node(None, None)
        self._size = 0

    def header(self):
        """返回头哨兵节点的指针"""
        return self._header

    def first(self):
        """获取第一个有实际元素的指针"""
        return self._header._next

    def after(self, p):
        """指针后移"""
        return p._next

    def __iter__(self):
        """迭代器展示元素值"""
        cursor = self.first()
        while cursor is not None:
            yield cursor._element
            cursor = self.after(cursor)

    def __len__(self):
        """链表长度"""
        return self._size

    def is_empty(self):
        """是否为空"""
        return self._size == 0

    def __getitem__(self, p):
        """根据节点指针获取元素值"""
        return p._element

    def add_first(self, e):
        """在头部插入"""
        newest = self._Node(e, self._header._next)
        self._header._next = newest
        self._size += 1
        return self._header._next

    def add_after(self, p, e):
        """在 p 后插入"""
        newest = self._Node(e, p._next)
        p._next = newest
        self._size += 1
        return p._next

    def pop_after(self, p):
        """删除 p 节点后紧跟的节点"""
        if p is self._header:
            self._header._next = None
            print("You have deleted the whole Linked List!")
        elif p._next is None:
            raise IndexError("Now is the last Node!")
        else:
            tmp = p._next
            element = tmp._element
            p._next = p._next._next
            tmp._next, tmp._element = None, None  # 显示删除
        return element

    def from_list(self, l: list):
        """从列表 list 方便的创建链表"""
        for i in reversed(l):
            self.add_first(i)
        return self._header._next  # 返回第一个元素值节点

    def __str__(self):
        """以 str 形式展示"""
        show_as_list = ""
        for i in self:
            show_as_list += str(i) + ", "
        return "<Linked List: [" + show_as_list[:-2] + "] >"

    @classmethod
    def merge(cls, ll1, ll2):
        """合并两个有序链表"""
        newll = cls()

        # 获取第一个节点（不包含哨兵节点）
        p1 = ll1.first()
        p2 = ll2.first()

        # 当前位置
        cur = newll.header()

        # 遍历 ll1 ll2 比较元素大小，将较小的元素插入到新链表中
        while p1 is not None and p2 is not None:
            if ll1[p1] <= ll2[p2]:
                cur._next = p1  # 指针指向 p1
                p1 = ll1.after(p1)  # p1 后移
            else:
                cur._next = p2
                p2 = ll2.after(p2)
            # 链表指针后移
            cur = newll.after(cur)

        # 若 ll1 ll2 仍有剩余，说明肯定是排序好的更大子链表，直接接入
        if p1 is not None:
            cur._next = p1
        else:
            cur._next = p2

        # 哨兵节点指向空，相当于置空原链表
        ll1.header()._next = None
        ll2.header()._next = None

        # 更新大小
        newll._size = len(ll1) + len(ll2)

        # 长度清零
        ll1._size = 0
        ll2._size = 0

        return newll


if __name__ == '__main__':
    # 初始化链表
    ll1 = LinkedList()
    ll2 = LinkedList()

    # 从列表创建链表
    l1 = [1, 3, 5, 7, 9]
    l2 = [2, 4, 6, 6, 8, 10, 12]
    ll1.from_list(l1)
    ll2.from_list(l2)

    # 展示原始链表
    print("=" * 15, "Initial Linked List:", "=" * 15)

    print(ll1)
    print(ll2)

    # 合并
    print("=" * 15, "Merge Linked List:", "=" * 15)

    merge_ll = LinkedList.merge(ll1, ll2)
    print(merge_ll)
    print("length of the merged ll is: {}".format(len(merge_ll)))
    print("Empty of not: {}".format("No" if not merge_ll.is_empty() else "Yes"))

    # 展示原始链表
    print("=" * 15, "Have Delete the Initial Linked List?", "=" * 15)

    print(ll1)
    print("length of the merged ll is: {}".format(len(ll1)))
    print("Empty of not: {}".format("No" if not ll1.is_empty() else "Yes"))

    print(ll2)
    print("length of the merged ll is: {}".format(len(ll2)))
    print("Empty of not: {}".format("No" if not ll2.is_empty() else "Yes"))
