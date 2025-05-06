import math
from random import randrange

try:
    from collections.abc import MutableMapping  # Python 3.3+
except ImportError:
    from collections import MutableMapping  # Python 2.7 - 3.2 (已废弃)


class MapBase(MutableMapping):
    """映射 Map 的基础父类"""

    # ---------- 嵌套的 _Item 类，存储键值对 ----------
    class _Item:
        """存储键值对"""
        __slots__ = '_key', '_value'

        def __init__(self, k, v):
            """初始化键值对"""
            self._key = k
            self._value = v

        def __eq__(self, other):
            """a == b 等价于 a 和 b 键值相等"""
            return self._key == other._key

        def __ne__(self, other):
            """a != b 等价于 a 和 b 键值不等"""
            return not (self == other)

        def __lt__(self, other):
            """比较键值"""
            return self._key < other._key

        def value(self):
            return self._value

        def key(self):
            return self._key


class HashMapBase(MapBase):
    """哈希表基础抽象类"""

    def __init__(self, cap=11, p=109345121):
        """初始化空哈希表
        :param cap: 初始表可存储的大小，非实际大小
        :param p: 一个充分大的质数
        """
        self._table = cap * [None]  # 可存储空间大小
        self._n = 0  # 哈希表内存储的键值对个数
        self._prime = p  # MAD: ax+b mod p 的 p 一个充分大的质数
        self._scale = 1 + randrange(p - 1)  # MAD: ax+b mod p 的 a
        self._shift = randrange(p)  # MAD: ax+b mod p 的 b

    def _hash_function(self, k):
        """自定义哈希函数 MAD 方法"""
        # (ax+b mod p) mod N belong to [0, N-1]: N 为实际表的大小 len(_table)
        mad = (hash(k) * self._scale + self._shift) % self._prime
        return mad % len(self._table)

    def __len__(self):
        """存储的键值对个数 _n <= N"""
        return self._n

    def __getitem__(self, k):
        """根据键获取值 M[k]"""
        j = self._hash_function(k)  # calculate hash
        return self._bucket_getitem(j, k)

    def __setitem__(self, k, v):
        """设置/修改/新增键值对 M[k] = v"""
        j = self._hash_function(k)  # calculate hash
        self._bucket_setitem(j, k, v)

        # 检查是否达到容量的一半，进行扩容
        if self._n > len(self._table) // 2:
            self._resize(2 * len(self._table) - 1)  # 2 * len - 1 尽可能保证是质数

    def __delitem__(self, k):
        """删除元素 del M[k]"""
        j = self._hash_function(k)  # calculate hash
        self._bucket_delitem(j, k)
        self._n -= 1

    def _resize(self, c):
        """扩展空间"""
        old = list(self.items())  # 继承自 MutableMapping 类
        self._table = c * [None]  # 扩容至 c
        self._n = 0
        for (k, v) in old:
            self[k] = v  # 利用已经定义的 __setitem__

    def _bucket_getitem(self, j, k):
        """获取桶数组元素，由子类定义"""
        raise NotImplementedError('must be implemented by subclass')

    def _bucket_setitem(self, j, k, v):
        """修改桶数组元素，由子类定义"""
        raise NotImplementedError('must be implemented by subclass')

    def _bucket_delitem(self, j, k):
        """删除桶数组元素，由子类定义"""
        raise NotImplementedError('must be implemented by subclass')

    def __iter__(self):
        """迭代器的方式返回键值，由子类定义"""
        raise NotImplementedError('must be implemented by subclass')


class ProbeHashMap(HashMapBase):
    """开放寻址法实现的哈希表"""
    _AVAIL = object()  # 哨兵对象，用来标记区分与空位置 None

    def __init__(self):
        super().__init__(cap=11, p=109345121)

        # 双重 hash 时，计算 q < N 的质数 q
        self._q = self._get_prime_less_than_N()

    def _is_available(self, j):
        """判断 j (对_table 而言的索引) 位置是否可以插入"""
        return self._table[j] is None or self._table[j] is ProbeHashMap._AVAIL

    def _bucket_getitem(self, j, k):
        found, idx = self._find_slot(j, k)
        if not found:  # 没找到匹配的 k
            raise KeyError('Key Error' + repr(k))
        return self._table[idx]._value  # 找到并返回 k 对应的值

    def _bucket_setitem(self, j, k, v):
        found, idx = self._find_slot(j, k)
        if not found:  # 没找到匹配的 k 则插入新元组
            self._table[idx] = self._Item(k, v)
            self._n += 1
        else:  # 否则改变值 _value
            self._table[idx]._value = v

    def _bucket_delitem(self, j, k):
        found, idx = self._find_slot(j, k)
        if not found:  # 没找到匹配的 k
            raise KeyError('Key Error' + repr(k))
        self._table[idx] = ProbeHashMap._AVAIL  # 删除后特殊标记

    def __iter__(self):
        for j in range(len(self._table)):  # 搜索整个存储空间 _table
            if not self._is_available(j):
                yield self._table[j]._key

    # --------------- _find_slot 方法：不同的开放寻址法 ---------------
    # ====================================================================================
    # def _find_slot(self, j, k):
    #     """线性探测：在桶/索引 j 中搜寻含义键 k 的元组"""
    #     firstAvail = None
    #     while True:
    #         if self._is_available(j):  # 如果可以插入: _table[j] 是 None 或 _AVAIL
    #             if firstAvail is None:
    #                 firstAvail = j  # 记录可以插入的桶/索引
    #             if self._table[j] is None:
    #                 return (False, firstAvail)  # 没有找到匹配的 k -> False
    #
    #         elif k == self._table[j]._key:  # 找到匹配的 k -> True
    #             return (True, j)  # 并且返回此处的索引
    #
    #         j = (j + 1) % len(self._table)  # 向后探索
    # ====================================================================================

    # ====================================================================================
    # def _find_slot(self, j, k):
    #     """二次探测：在桶/索引 j 中搜寻含义键 k 的元组"""
    #     firstAvail = None
    #     i = 1  # 步长，对于线性探测 i 恒等于 0
    #     while True:
    #         if self._is_available(j):  # 如果可以插入: _table[j] 是 None 或 _AVAIL
    #             if firstAvail is None:
    #                 firstAvail = j  # 记录可以插入的桶/索引
    #             if self._table[j] is None:
    #                 return (False, firstAvail)  # 没有找到匹配的 k -> False
    #
    #         elif k == self._table[j]._key:  # 找到匹配的 k -> True
    #             return (True, j)  # 并且返回此处的索引
    #
    #         j = (j + i * i) % len(self._table)  # 向后探索，二次探测 i^2 的步长
    #         i += 1
    # ====================================================================================

    def _resize(self, c):
        """覆写：扩展空间, 更新 self._q"""
        old = list(self.items())  # 继承自 MutableMapping 类

        self._table = c * [None]  # 扩容至 c
        self._q = self._get_prime_less_than_N()  # 更新 q
        self._n = 0
        for (k, v) in old:
            self[k] = v  # 利用已经定义的 __setitem__

    def _is_prime(self, n):
        """检查是否为质数"""
        if n <= 1:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False

        # 检查到 sqrt(n)
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True

    def _get_prime_less_than_N(self):
        """找到最大的 q < N 其中 q 为质数"""
        N = len(self._table)

        if N <= 2:
            return None

        # 从 N-1 开始反向检查
        for num in range(N - 1, 1, -1):
            if self._is_prime(num):
                return num
        return None

    # ====================================================================================
    def _double_hash(self, k):
        """计算双重哈希的步长 h'(k) = q - (hash(k) % q)"""
        return self._q - (hash(k) % self._q)

    def _find_slot(self, j, k):
        """双重哈希：在桶/索引 j 中搜寻含义键 k 的元组"""
        firstAvail = None
        i = 1  # 步长

        while True:
            if self._is_available(j):  # 如果可以插入: _table[j] 是 None 或 _AVAIL
                if firstAvail is None:
                    firstAvail = j  # 记录可以插入的桶/索引
                if self._table[j] is None:
                    return (False, firstAvail)  # 没有找到匹配的 k -> False

            elif k == self._table[j]._key:  # 找到匹配的 k -> True
                return (True, j)  # 并且返回此处的索引

            j = (j + i * self._double_hash(k)) % len(self._table)  # 向后探索，再哈希
            i += 1
    # ====================================================================================


if __name__ == '__main__':
    probe_hash_map = ProbeHashMap()
    probe_hash_map['Avail'] = 100
    probe_hash_map['Bucket'] = 200
    probe_hash_map['Capacity'] = 300
    for key in probe_hash_map:
        print("key: {}, value: {}".format(key, probe_hash_map[key]))
