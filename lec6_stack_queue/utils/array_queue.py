class Empty(Exception):
    """队列为空的异常类"""
    pass


class ArrayQueue:
    """FIFO 队列实现"""
    DEFAULT_CAPACITY = 10  # 默认数组长度

    def __init__(self):
        """初始化空队列，预留空间 DEFAULT_CAPACITY"""
        self._data = [None] * ArrayQueue.DEFAULT_CAPACITY  # 真实列表内存大小
        self._size = 0  # 队列大小
        self._front = 0  # 头指针

    def __len__(self):
        """返回长度"""
        return self._size

    def is_empty(self):
        """判断是否为空"""
        return self._size == 0

    def first(self):
        """返回第一个元素"""
        if self.is_empty():  # 是否为空
            raise Empty("Queue is empty")

        return self._data[self._front]  # 返回队列头部元素

    def dequeue(self):
        """从头部出队"""
        if self.is_empty():
            raise Empty("Queue is empty")

        answer = self._data[self._front]  # 获取出队元素值
        self._data[self._front] = None  # 出队位置置空
        self._front = (self._front + 1) % len(self._data)  # 循环利用数组
        self._size -= 1  # 长度减一
        return answer

    def enqueue(self, e):
        """队尾插入元素 e"""
        if self._size == len(self._data):
            # 如果列表已满，则增倍扩展数组
            self._resize(2 * len(self._data))

        avail = (self._front + self._size) % len(self._data)  # 队尾索引
        self._data[avail] = e
        self._size += 1

    def _resize(self, capacity):
        """空间为 capacity 新列表"""
        old = self._data  # 原始列表
        self._data = [None] * capacity  # 扩展后的空列表

        walk = self._front  # 队列的头部
        for k in range(self._size):
            self._data[k] = old[walk]  # 复制 old 到新的队列
            walk = (walk + 1) % len(old)  # old 是循环使用的
        self._front = 0  # 新队列的头部和列表的 0 (列表头部) 是对齐的

    @classmethod
    def from_list(cls, l):
        """从列表快速产生队列"""
        aq = cls()
        for e in l:
            aq.enqueue(e)
        return aq

    def __str__(self):
        """以列表形式展示"""
        tmp = []
        walk = self._front
        for _ in range(self._size):
            tmp.append(self._data[walk])
            walk = (walk + 1) % len(self._data)
        return str(tmp)

    def clear(self):
        """清空队列，保持当前容量，仅清除有效元素"""
        if not self.is_empty():  # 如果队列非空
            walk = self._front
            for _ in range(self._size):  # 遍历所有有效元素
                self._data[walk] = None  # 将元素置为 None
                walk = (walk + 1) % len(self._data)  # 循环数组
        self._size = 0  # 重置队列大小
        self._front = 0  # 重置头指针

    def __iter__(self):
        """返回一个迭代器，用于遍历队列中的元素"""
        walk = self._front  # 从队列的头部开始
        for _ in range(self._size):  # 遍历所有有效元素
            yield self._data[walk]  # 返回当前元素
            walk = (walk + 1) % len(self._data)  # 移动到下一个位置（循环数组）


if __name__ == '__main__':
    l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    q = ArrayQueue.from_list(l)
    print(q)
    print(q._data)
    q_list = [val for val in q]
    print(q_list)
    q.clear()
    print(q)
    print(q.is_empty())
    print(q._data)
