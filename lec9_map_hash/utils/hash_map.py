from random import randrange

try:
    from .map_base import MapBase
    from .unsorted_table_map import UnsortedTableMap
except ImportError:
    from map_base import MapBase
    from unsorted_table_map import UnsortedTableMap


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


class ChainHashMap(HashMapBase):
    """使用链址法实习哈希表"""

    # ---------- 不需初始化，只需要实现 HashMapBase 未实现的方法 ----------
    def _bucket_getitem(self, j, k):
        bucket = self._table[j]
        if bucket is None:
            raise KeyError('Key Error' + repr(k))  # 没有匹配到 k
        return bucket[k]

    def _bucket_setitem(self, j, k, v):
        if self._table[j] is None:
            self._table[j] = UnsortedTableMap()  # 用 UnsortedTableMap 实例作为新桶

        oldsize = len(self._table[j])  # 记录 j 位置的原始长度
        # _table[j] 是 UnsortedTableMap 实例，此处调用它的 __getitem__ 方法
        self._table[j][k] = v

        if len(self._table[j]) > oldsize:  # 添加成功
            self._n += 1  # 键值对数目加一

    def _bucket_delitem(self, j, k):
        bucket = self._table[j]
        if bucket is None:
            raise KeyError('Key Error' + repr(k))
        del bucket[k]  # 使用 UnsortedTableMap 的 __delitem__ 方法

    def __iter__(self):
        for bucket in self._table:
            if bucket is not None:
                # 使用 UnsortedTableMap 的 __iter__ 方法
                for key in bucket:
                    yield key


class ProbeHashMap(HashMapBase):
    """线性探测的开放寻址法实现的哈希表"""
    _AVAIL = object()  # 哨兵对象，用来标记区分与空位置 None

    def _is_available(self, j):
        """判断 j (对_table 而言的索引) 位置是否可以插入"""
        return self._table[j] is None or self._table[j] is ProbeHashMap._AVAIL

    def _find_slot(self, j, k):
        """在桶/索引 j 中搜寻含义键 k 的元组"""
        firstAvail = None
        while True:
            if self._is_available(j):  # 如果可以插入: _table[j] 是 None 或 _AVAIL
                if firstAvail is None:
                    firstAvail = j  # 记录可以插入的桶/索引
                if self._table[j] is None:
                    return (False, firstAvail)  # 没有找到匹配的 k -> False

            elif k == self._table[j]._key:  # 找到匹配的 k -> True
                return (True, j)  # 并且返回此处的索引

            j = (j + 1) % len(self._table)  # 向后探索

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


if __name__ == '__main__':
    chain_hash_map = ChainHashMap()
    chain_hash_map['A'] = 1
    chain_hash_map['B'] = 2
    chain_hash_map['C'] = 3
    for key in chain_hash_map:
        print("key: {}, value: {}".format(key, chain_hash_map[key]))

    probe_hash_map = ProbeHashMap()
    probe_hash_map['Avail'] = 100
    probe_hash_map['Bucket'] = 200
    probe_hash_map['Capacity'] = 300
    for key in probe_hash_map:
        print("key: {}, value: {}".format(key, probe_hash_map[key]))
