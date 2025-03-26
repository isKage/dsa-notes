class LinkedListNoHeader:
    class _Node:
        __slots__ = '_element', '_next'

        def __init__(self, element, next):
            self._element = element
            self._next = next

        @property
        def get_item(self):
            return self._element

        @property
        def next(self):
            return self._next

    def __init__(self):
        self._head = None
        self._size = 0

    def __iter__(self):
        cursor = self._head
        while cursor is not None:
            yield cursor._element
            cursor = cursor._next

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def _insert_first(self, e):
        cursor = self._head
        self._head = self._Node(e, cursor)
        self._size += 1

    def add_first(self, e):
        self._insert_first(e)

    @classmethod
    def from_list(cls, l: list, reverse=False):
        if reverse:
            ll = cls()
            for item in reversed(l):
                ll._insert_first(item)
            return ll
        else:
            ll = cls()
            for item in l:
                ll._insert_first(item)
            return ll

    def __str__(self):
        cursor = self._head
        res = []
        while cursor is not None:
            res.append(cursor._element)
            cursor = cursor._next
        return str(res)

    @property
    def head(self):
        return self._head


class LinkedList(LinkedListNoHeader):
    def __init__(self):
        super().__init__()
        self._head = self._Node(None, None)  # 头哨兵节点
        self._size = 0

    def _insert_first(self, e):
        new = self._Node(e, self._head._next)
        self._head._next = new
        self._size += 1

    def __iter__(self):
        cursor = self._head._next  # 从真正的第一个元素开始
        while cursor is not None:
            yield cursor._element
            cursor = cursor._next

    def __str__(self):
        cursor = self._head._next
        res = []
        while cursor is not None:
            res.append(cursor._element)
            cursor = cursor._next
        return str(res)

    @property
    def head(self):
        return self._head._next


if __name__ == '__main__':
    ll = LinkedListNoHeader.from_list([1, 2, 3, 4, 5])
    print(ll)

    cur = ll.head
    cur = cur.next
    print(cur.get_item)

    ll = LinkedList.from_list([1, 2, 3, 4, 5])
    print(ll)

    h = ll.head
    print(h.get_item)
