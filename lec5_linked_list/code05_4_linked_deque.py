from utils import Empty
from utils import _DoublyLinkedBase


class LinkedDeque(_DoublyLinkedBase):
    """双向链表实现双端队列"""

    # -------------- 继承父类 --------------
    """不需要定义 `__init__` `__len__` `is_empty` 方法"""

    # -------------- 添加双端队列的功能 --------------
    def first(self):
        """获取第一个元素的值，注意头节点是哨兵，没有值"""
        if self.is_empty():
            raise Empty('Deque is empty')

        return self._header._next._element

    def last(self):
        """获取最后一个元素的值，注意尾节点是哨兵，没有值"""
        if self.is_empty():
            raise Empty('Deque is empty')

        return self._trailer._prev._element

    def insert_first(self, e):
        """在头部插入元素"""
        # 直接调用父类 _insert_between 方法，在头哨兵和第一个元素节点之间插入
        return self._insert_between(e, self._header, self._header._next)

    def insert_last(self, e):
        """在尾部插入元素"""
        # 直接调用父类 _insert_between 方法，在最后一个元素节点和尾哨兵之间插入
        return self._insert_between(e, self._trailer._prev, self._trailer)

    def delete_first(self):
        """删除第一个元素"""
        if self.is_empty():
            raise Empty('Deque is empty')

        # 直接调用父类 _delete_node 方法，删除头节点的下一个节点
        return self._delete_node(self._header._next)

    def delete_last(self):
        """删除最后一个元素"""
        if self.is_empty():
            raise Empty('Deque is empty')

        # 直接调用父类 _delete_node 方法，删除尾节点的上一个节点
        return self._delete_node(self._trailer._prev)


if __name__ == '__main__':
    print("=" * 15, "Initializing Deque", "=" * 15)
    ldq = LinkedDeque()
    print("Deque is empty: {}".format(ldq.is_empty()))

    print("=" * 15, "Add Element", "=" * 15)
    x1, x2, x3, x4 = 1, 2, 3, 4

    print("add: {}, {}".format(x1, x2))
    ldq.insert_first(x1)
    ldq.insert_last(x2)
    print("first: {}, last: {}".format(ldq.first(), ldq.last()))

    print("add: {}, {}".format(x3, x4))
    ldq.insert_first(x3)
    ldq.insert_last(x4)
    print("first: {}, last: {}".format(ldq.first(), ldq.last()))

    print("=" * 15, "Delete Element", "=" * 15)

    print("delete: {}, {}".format(ldq.delete_first(), ldq.delete_last()))
    print("first: {}, last: {}".format(ldq.first(), ldq.last()))

    print("delete: {}, {}".format(ldq.delete_first(), ldq.delete_last()))
    print("Deque is empty: {}".format(ldq.is_empty()))
