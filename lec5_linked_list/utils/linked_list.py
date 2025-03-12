class LinkedList:
    class _Node:
        __slots__ = '_element', '_next'

        def __init__(self, element, next):
            self._element = element
            self._next = next

    def __init__(self):
        self._head = None
        self._size = 0

    def first(self):
        return self._head

    def after(self, p):
        return p._next

    def get_node(self, n):
        if n > self._size or n < 0:
            raise IndexError('Index out of range')
        cur = self._head
        for _ in range(n):
            cur = cur._next
        return cur

    def get_pos_element(self, p):
        return p._element

    def get_ind_element(self, n):
        cur = self.get_node(n)
        return cur._element

    def __iter__(self):
        cursor = self.first()
        while cursor is not None:
            yield cursor._element
            cursor = self.after(cursor)

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def add_first(self, e):
        newest = self._Node(e, self._head)
        self._head = newest
        self._size += 1
        return self._head

    def add_after(self, p, e):
        newest = self._Node(e, p._next)
        p._next = newest
        self._size += 1
        return p._next

    def insert(self, n, e):
        if n == 0:
            self.add_first(e)
        else:
            cur = self.get_node(n - 1)
            return self.add_after(cur, e)

    def delete(self, n):
        if n > self._size or n < 0:
            raise IndexError('Index out of range')
        if n == 0:
            cur = self._head
            self._head = cur._next
        else:
            cur = self.get_node(n - 1)
            pre = cur
            cur = cur._next
            pre._next = cur._next
            element = cur._element
            cur._next = cur._element = None
            self._size -= 1
            return element

    def replace_pos(self, p, e):
        old_value = p._element
        p._element = e
        return old_value

    def replace_ind(self, n, e):
        p = self.get_node(n)
        return self.replace_pos(p, e)


if __name__ == '__main__':
    l = LinkedList()

    l.add_first(1)
    l.add_first(2)
    l.add_first(3)
    l.add_first(4)

    for i in l:
        print(i)
