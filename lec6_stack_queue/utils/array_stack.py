class Empty(Exception):
    """栈为空的异常类"""
    pass


class ArrayStack:
    """基于数组的栈数据类型 LIFO"""

    def __init__(self):
        """初始化空栈"""
        self._data = []  # 适配器模式，隐藏 list 实例化对象

    def __len__(self):
        """栈的元素个数"""
        return len(self._data)

    def is_empty(self):
        """判断是否为空"""
        return len(self._data) == 0

    def push(self, e):
        """向栈顶插入元素"""
        self._data.append(e)

    def top(self):
        """返回栈顶元素"""
        if self.is_empty():
            raise Empty("Stack is empty")
        return self._data[-1]

    def pop(self):
        """从栈顶删除元素"""
        if self.is_empty():
            raise Empty("Stack is empty")
        return self._data.pop()


if __name__ == "__main__":
    stack = ArrayStack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    stack.push(4)
    print(stack.top())
    print(stack.pop())
    print(stack.top())
