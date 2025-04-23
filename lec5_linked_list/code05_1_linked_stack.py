from utils import Empty


class LinkedStack:
    """单向链表实现栈，后进先出"""

    # -------------- 嵌套的节点类 _Node --------------
    class _Node:
        """单向链表的节点，非公有，实现栈"""
        __slots__ = '_element', '_next'  # _Node 类只拥有这 2 个属性

        def __init__(self, element, next):
            self._element = element
            self._next = next

    # -------------- 正式实现栈 --------------
    def __init__(self):
        """初始化空栈"""
        self._head = None  # 头指针，指向节点，初始化为空
        self._size = 0  # 元素个数

    def __len__(self):
        """栈元素个数 len(obj) 重载"""
        return self._size

    def is_empty(self):
        """检查是否为空"""
        return self._size == 0

    def push(self, e):
        """向栈顶部增加元素"""
        # 新建节点，指向旧的 head 新的 head 指向新节点
        self._head = self._Node(e, self._head)
        self._size += 1

    def top(self):
        """返回栈顶值，但不改变链表"""
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._head._element

    def pop(self):
        """删除并返回栈顶元素"""
        if self.is_empty():
            raise Empty('Stack is empty')
        ans = self._head._element
        # 删除头部节点
        self._head = self._head._next
        self._size -= 1
        return ans


if __name__ == '__main__':
    stack = LinkedStack()
    stack.push(1)
    print("add: {}".format(stack.top()))
    stack.push(2)
    print("add: {}".format(stack.top()))

    print("remove: {}".format(stack.pop()))

    print("top: {}".format(stack.top()))
