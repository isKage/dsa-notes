try:
    from .map_base import MapBase
except ImportError:
    from map_base import MapBase


class SortedTableMap(MapBase):
    """有序映射：有序数组实现"""

    # ------------- 非公有方法 -------------
    def _find_index(self, k, low, high):
        """二分查找：最左边且 >= k"""
        if high < low:
            return high + 1  # 未找到
        else:
            mid = (high + low) // 2
            if k == self._table[mid]._key:  # 找到对应的键
                return mid
            elif k < self._table[mid]._key:
                return self._find_index(k, low, mid - 1)  # 二分查找递归
            else:
                return self._find_index(k, mid + 1, high)

    # ------------- 公有方法 -------------
    def __init__(self):
        """初始化列表存储"""
        self._table = []

    def __len__(self):
        """返回长度"""
        return len(self._table)

    def __getitem__(self, k):
        """查找键为 k"""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j == len(self._table) or self._table[j]._key != k:
            raise KeyError('Key Error: ' + repr(k))  # 没有找到
        return self._table[j]._value

    def __setitem__(self, k, v):
        """插入/修改元素"""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j < len(self._table) and self._table[j]._key == k:
            self._table[j]._value = v
        else:
            self._table.insert(j, self._Item(k, v))  # 在 j 位置插入

    def __delitem__(self, k):
        """删除元素"""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j == len(self._table) or self._table[j]._key != k:
            raise KeyError('Key Error: ' + repr(k))  # 没有找到元素
        return self._table.pop(j)  # 删除并返回被删除的 _Item 实例

    def __iter__(self):
        """迭代器饿的方式返回键"""
        for item in self._table:
            yield item._key

    def __reversed__(self):
        """反向返回序列"""
        for item in reversed(self._table):
            yield item._key

    def find_min(self):
        """返回键值对 (k, v) 最小的 k"""
        if len(self._table) > 0:
            # 有序映射：第一个即为最小
            return (self._table[0]._key, self._table[0]._value)
        else:
            return None

    def find_max(self):
        """返回最大键值的 (k, v)"""
        if len(self._table) > 0:
            # 有序映射：最后一个即为最大
            return (self._table[-1]._key, self._table[-1]._value)
        else:
            return None

    def find_lt(self, k):
        """找到 k 的前一个"""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j > 0:
            return (self._table[j - 1]._key, self._table[j - 1]._value)
        else:
            return None

    def find_gt(self, k):
        """找到 k 的后一个"""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j < len(self._table) and self._table[j]._key == k:
            # 避免出界
            j += 1
        if j < len(self._table):
            return (self._table[j]._key, self._table[j]._value)
        else:
            return None

    def find_range(self, start, stop):
        """迭代器的方式返回 start <= key < stop"""
        if start is None:
            j = 0
        else:
            j = self._find_index(start, 0, len(self._table) - 1)
            while j < len(self._table) and (stop is None or self._table[j]._key < stop):
                yield (self._table[j]._key, self._table[j]._value)
                j += 1


if __name__ == '__main__':
    stm = SortedTableMap()

    n = 16
    print("=" * 15, f"Add {n} (key, value) for test", "=" * 15)
    for new in range(n):
        stm[new + 1] = "test" + str(new + 1)
    print("Key = 6, then Value =", stm[6])

    start, stop = 2, 8
    print("=" * 15, f"From {start} to {stop}", "=" * 15)
    for item in stm.find_range(1, 6):
        print(item)

    key, value = -4, "Smallest"
    print("=" * 15, f"Add a new one ({key}, {value}) and find it", "=" * 15)
    stm[key] = value
    print(stm.find_min())
