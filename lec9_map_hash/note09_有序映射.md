# 有序映射：排序检索表、跳跃表

本章补充部分有关映射的知识——有序映射，主要讲解了线性结构实现有序映射的方法，如排序检索表。介绍了一种新颖的实现方法——跳跃表。不过，更好的实现推荐使用搜索树这种非线形结构。

## 1 有序映射

### 1.1 有序映射的抽象数据类型

传统的映射 ADT 允许用户查找与给定键关联的值，这种键的查找被称为精确查找。在这一部分，我们介绍一个称为有序映射的映射 ADT 的扩展，它包括标准映射的所有行为，还增加了以下方法：

- `M.find_min()` ：用最小键返回键值对（或None，如果映射为空）
- `M.find_max()` ：用最大键返回键值对（或 None，如果映射为空）
- `M.find_It(k)` ：用严格小于 k 的最大键返回键值对（或 None，若没有这样的项存在）
- `M.find_le(k)` :用严格小于等于 k 的最大键返回键值对（或 None，若没有这样的项存在）
- `M.find_gt(k)` ：用严格大于 k 的最小的键返回键值对（或 None，若没有这样的项存在）
- `M.fnd_ge(k)` ：用严格大于或等于 k 的最小的键返回键值对（或None，若没有这样的项存在）
- `M.fnd_range(start, stop)` ：用 start <= 键 < stop 迭代遍历所有键值对。如果 start 指定
    为 None ，从最小的键开始迭代；如果 stop 指定 None，到最大键迭代结束

- `iter(M)` ：根据自然顺序从最小到最大迭代遍历映射中的所有键

- `reversed(M)` ：根据逆序迭代映射中的所有键 r ，这在 Python 中是用 reversed 来实现的

### 1.2 排序检索表

一些先进的技术可以支持排序映射 ADT，例如二叉搜索树。在本节中，我们从探索一个简单有序映射的实现开始。我们将映射的元组存储在一个基于数组的序列 A 中，以键的升序排列，我们将这个映射实现称为**排序检索表（sorted search table）**。如此可以根据二分查找来实现相关操作。

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1744803543695.png)

#### 1.2.1 Python 实现

`MapBase` 类是映射的基类，实现代码：

```python
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
```

继承 `MapBase` 类，实现有序映射，采用数字/列表的方式存储，每次插入都使用二分查找的方式，最终得到一个有序映射（有序列表，排序按照 key 从小到大）。核心在于 `_find_index` 二分查找方法的实现。

```python
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
```

测试：

```python
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

# =============== Add 16 (key, value) for test ===============
# Key = 6, then Value = test6
# =============== From 2 to 8 ===============
# (1, 'test1')
# (2, 'test2')
# (3, 'test3')
# (4, 'test4')
# (5, 'test5')
# =============== Add a new one (-4, Smallest) and find it ===============
# (-4, 'Smallest')
```

#### 1.2.2 算法分析

由于二分查找的性质，查找某个特定元素的复杂度为 **O(log n)** ，无论是查找 `k == key` 还是查看这个元素的前后。但对于 `M[k] = v` 因为存储找不到 `k == key` 的情况，即需要插入元素，此时复杂度为 **O(n)** 。

![有序映射：采用排序检索表这种线性结构实现的时间复杂度](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1744805526278.png)



## 2 跳跃表

数组实现有序映射在插入元素时复杂度为 O(n) ，而链表实现无法通过二分查找提高效率。**跳跃表**提供一个聪明的折衷方式以有效地支持查找和更新操作。

一个映射 M 的跳跃表 S 包含一列表序列 `{S0, S1, ..., Sh}` 。每一个列表 `Si` 依照键的升序存储着 M 的一个元组子集，用两个标注为 `-inf` 和 `+inf` 的哨兵键追加元组，其中 `inf` 表示无穷。此外，列表 S 还要满足下面的条件：

- 列表 `S0` 包含映射 M 中的每一项 (包含 -inf 和 +inf)
- 对于 `i = 1, 2, ..., h - 1` 列表 `S{i}` 包含一个列表 `S{i-1}`随机生成的元组的子集（还有-∞和＋8）。
- 列表 `Sh` 仅包含 -inf 和 +inf

一个跳跃表如图所示。在列表 S 中，列表 `S0` 在最底部，在 `S0` 之上有列表 `S1, S2, ..., Sh` 并且，我们称 h 为列表 S 的高度。

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1744807762142.png)

列表 `S{i+1}` 的元素从 `S{i}` 中选取，按照每一个元素 1/2 的概率，于是 `S{i+1}` 的长度大致为 `S{i}` 的一半。如此列表 S 的长度为 **h = log n** 。

我们视跳跃表为一个**水平组织成层（level）、垂直组织成塔（tower）**的二维位置集合。每个水平层是一个列表 `Si` ，每个垂直塔包含了存储着相同元组的位置，这些元组跨越连续的列表。可以使用以下操作遍历跳跃表中的每个位置：

- `next(p)` ：返回在同一水平层位置上紧接着 p 的位置。
- `prev(p)` ：返回在同一水平层位置上在 p 之前的位置。
- `below(p)` ：返回在同一垂直塔位置上在 p 下面的位置。
- `above(p)` ：返回在同一垂直塔位置上在 p 上面的位置。

我们注意到可以通过链结构简单地实现一个跳跃表，给定一个跳跃表 p 的位置，每一个单独的遍历方法需要 **O(1)** 时间，这样的链结构本质上是在垂直塔方向上对齐的双链表集合。
