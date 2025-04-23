import ctypes


class DynamicArray:
    """
    自定义实现动态数组，_ 开头表示非公有方法，不建议外部误调用
    """

    def __init__(self):
        """初始化空数组"""
        self._n = 0  # 数组实际元素个数
        self._capacity = 1  # 默认数组空间大小
        self._A = self._make_array(self._capacity)  # 创建大小为 _capacity 的数组

    def _make_array(self, c):
        """创建大小为 c 的数组"""
        return (c * ctypes.py_object)()

    def __len__(self):
        """返回数组元素个数"""
        return self._n

    def __getitem__(self, k):
        """索引数组第 k 个元素"""
        if not 0 <= k < self._n:
            raise IndexError('Invalid index')
        return self._A[k]

    def append(self, obj):
        """数组末尾添加元素"""
        if self._n == self._capacity:  # 判断数组空间
            self._resize(2 * self._capacity)  # 翻倍增量策略

        self._A[self._n] = obj  # 更新数组尾部元素
        self._n += 1  # 更新实际元素个数

    def _resize(self, c):
        """扩展数组大小"""
        B = self._make_array(c)  # 创建大小为 c 的新数组
        for k in range(self._n):
            # 拷贝原来数组元素
            B[k] = self._A[k]

        self._A = B  # 更新数组对象
        self._capacity = c  # 更新存储空间大小

    def __str__(self):
        """字符串重载，以字符串得到方式展示数组内容"""
        return "[" + ", ".join(str(self._A[i]) for i in range(self._n)) + "]"

    def get_memory_size(self):
        """返回数组的内存分配大小（字节）"""
        return self._capacity * ctypes.sizeof(ctypes.py_object)

    def insert(self, obj, position):
        """在第 position 位置插入 obj"""
        # 解决索引问题
        while position < 0:
            position += self._n
        position = position % self._n

        if self._n == self._capacity:
            # 空间不足
            self._resize(2 * self._capacity)  # 扩展

        for j in range(self._n, position, -1):
            # 后 n - position 向后移动一位
            self._A[j] = self._A[j - 1]

        self._A[position] = obj  # 更新第 position 位的元素
        self._n += 1  # 更新元素个数

    def remove(self, obj):
        """删除值 obj (不考虑重复)"""
        for k in range(self._n):
            if self._A[k] == obj:
                for j in range(k, self._n - 1):
                    # 前移
                    self._A[j] = self._A[j + 1]

            self._A[self._n - 1] = None  # help garbage collection
            self._n -= 1  # 更新个数
            return True
        raise ValueError('Value not found')  # 无匹配


# %%
array = DynamicArray()
for k in range(20):
    length = len(array)
    size = array.get_memory_size()
    print("数组大小: {}, 数组内存分配: {} Byte (字节)".format(length, size))
    array.append(k)

print(array)

# %%
array.insert(-1, 0)
array.insert(-1, -1)
print(array)

# %%
array.remove(-1)
print(array)
