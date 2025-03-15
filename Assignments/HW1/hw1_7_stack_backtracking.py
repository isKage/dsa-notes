"""
如果 3 个元素进栈顺序为 X, Y, Z，试写出所有可能的出栈顺序（可能后来者进栈时，先来者已经出栈）
"""
"""
x in; y in; z in; z out -> zyx
x in; y in; y out-> yxz yzx
x in; x out -> xzy xyz
"""


# 栈 穷举 回溯法 （使用状态栈多记录信息）

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

    def copy(self):
        """完全复制一份"""
        new = ArrayStack()
        new._data = self._data[:]
        return new


def pop_seq(l):
    """生成所有可能的出栈顺序"""
    res = []
    # 状态栈，包括空栈，已进栈的元素数量为 0，出栈元素顺序列表 (结果)
    stack = ArrayStack()
    stack.push((ArrayStack(), 0, []))  # 初始状态

    while not stack.is_empty():
        # 出栈栈顶，得到当前栈状态
        current_stack, pushed_num, popped = stack.pop()

        # Step 1: 查看是否是完整的出栈顺序列表
        if len(popped) == len(l):
            # 已出栈的数量等于 len(l) 说明是完整的出栈可能，记录进 res
            res.append(popped)
            continue

        # ------ 复制是为了 Step 2 不影响 Step 3 因为二者均依赖于之前状态栈出栈的 current_stack ------
        # Step 2: 状态栈顶出栈，补充新的可能栈状态
        # 若进栈个数未满，则复制状态，进栈后压入状态栈
        if pushed_num < len(l):  # 已进栈个数未满
            new_stack = current_stack.copy()  # 复制当前栈
            new_stack.push(l[pushed_num])  # 将下一个元素进栈
            new_popped = popped.copy()  # 复制出栈顺序列表
            new_pushed_num = pushed_num + 1  # 进栈数加一
            stack.push((new_stack, new_pushed_num, new_popped))  # 压入新状态

        # Step 3: 记录当前栈 (非状态栈) 的出栈可能
        # 栈顶元素出栈，补充出栈顺序列表
        if not current_stack.is_empty():
            new_stack = current_stack.copy()  # 复制当前栈的状态
            new_popped = popped.copy()  # 复制出栈顺序列表
            new_popped.append(new_stack.pop())  # 栈顶元素出栈，进入出栈顺序列表
            stack.push((new_stack, pushed_num, new_popped))  # 压入新状态

    return res


if __name__ == "__main__":
    l = ['X', 'Y', 'Z']
    pop_sequence = pop_seq(l)
    for seq in pop_sequence:
        print(seq)
