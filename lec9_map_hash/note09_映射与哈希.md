# 映射 (Map) 与 哈希 (Hash)

本章介绍映射、哈希表、哈希函数、哈希码、压缩函数、冲突处理。核心问题：以最快的速度实现查找、删除、插入键值对的功能。

## 1 映射

**映射 map** ：是由键值对所构成的集合，其中的键是唯一的，但值不一定唯一。映射上的主要操作为查找、插入和删除。其中映射需要解决的核心问题就是**加速查找操作**。

**字典 dict** ：是 Python 中最重要的数据结构。

- `dict` 类表示一种被称为字典的抽象概念，其中的每个键是唯一的，且被映射到对应的值上。

- `dict` 类是一种**无序映射**的实现。

为避免混淆，我们使用 “字典” 这一术语来指代 Python 的 `dict` 类，而使用 “映射” 这一术语来讨论更为一般的抽象数据类型概念。

### 1.1 映射的抽象数据类型 ADT

引入映射 M 的 ADT ，并定义其行为与 dict 类一致：

**映射 M 最重要的 5 类行为（查找、增添、删除、修改、遍历）：**

- `M[k]` ：如果存在，返回映射 M 中键 k 对应的值，否则抛出 KeyError 。Python 中该功能由特殊方法 `__getitem__` 实现。
- `M[k] = v` ：使得映射 M 中键 k 对应于值 v 。如 k 有之前对应的值，则替换掉该值。Python 中该功能由特殊方法 `__setitem__` 实现。
- `del M[k]` ：从映射 M 中删除键为 k 的键值对。如键 k 不存在则抛出 KeyError 。Python 中该功能由特殊方法 `__delitem__` 实现。
- `len(M)` ：返回映射 M 中键值对的数量。Python 中该功能由特殊方法 `__len__` 实现。
- `iter(M)` ：返回一个包含映射 M 所有键的迭代器。Python 中该功能由特殊方法 `__iter__` 实现。

**为实现其他方便的功能，映射 M 也应支持以下行为：**

- `k in M` ：如果映射 M 中包含键 k 则返回 True ，否则返回 False 。Python 中该功能由特殊方法 `__contains__` 实现。
- `M.get(k, d=None)` ：如映射 M 中存在 k 则返回 M[k] ，否则返回默认值 d 。这提供了一种避免 KeyError 风险的 M[k] 查询方法。
- `M.setdefault(k, d)` ：如映射 M 中存在键 k ，则返回 M[k] ，否则令 M[k] = d 并返回 d 。
- `M.pop(k, d=None)` ：从映射 M 中删除键为 k 的键值对，并将其值 v 返回。如 M 中不存在键 k 则返回默认值 d（如 d 为 None 则抛出 KeyError ）。
- `M.popitem()` ：从映射 M 中随机删除并返回一个键值对 (k, v) 。如 M 为空则抛出 KeyError 。
- `M.clear()` : 删除映射M中所有的键值对。
- `M.keys()` : 返回 M 的所有键。
- `M.values()` : 返回 M 的所有值。
- `M.items()` : 返回 M 的所有键值对。
- `M.update(M2)` : 将 M2 中的所有键值对信息插入 M 中。
- `M == M2` : 如果映射 M 和 M2 中包含的所有键值对完全相同则返回 True ，否则返回 False 。
- `M != M2` : 如果映射 M 和 M2 中有不同的键值对则返回 True ，否则返回 False 。

例如：

![映射 ADT 的一些操作例子](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1744194185818.png)

**应用** 考虑统计一个文档中单词出现频率的问题。使用 Python 的 dict 类实现该映射：

```python
def max_word_count(filename: str) -> tuple[str, int]:
    freq = {}
    for piece in open(filename).read().lower().split():
        # 只考虑小写字母的单词
        word = ''.join(c for c in piece if c.isalpha())
        if word:  # 单词存在
            freq[word] = 1 + freq.get(word, 0)  # 有则 +1 无则初始化为 0

    max_word = ''
    max_count = 0
    for (w, c) in freq.items():
        if c > max_count:
            max_word = w
            max_count = c

    return max_word, max_count
```

```python
if __name__ == '__main__':
    file_path = "example.txt"
    max_word, max_count = max_word_count(filename=file_path)
    print('The most frequent word is: \'{}\''.format(max_word))
    print('Its number of occurrences is: {}'.format(max_count))
    
# The most frequent word is: 'file'
# Its number of occurrences is: 3
```

### 1.2 Python 实现映射

我们可以使用 Python 自带的抽象基类帮助我们构建自己的映射类。

Python 的 `collections.abc` 模块中有以下两个抽象基类：

- `Mapping` ：包含 dict 类支持的所有**不可变方法**。
- `MutableMapping` ：包含 dict 类支持的**不可变及可变方法**。

> 【注意】在高版本的 Python 中 `MutableMapping` 已移到 `collections.abc` 中。

`MutableMapping` 类提供映射 ADT 中**除以下 5 种行为外**所有行为的具体实现：`__getitem__` ， `__setitem__` ， `__delitem__` ，`__len__` 和 `__iter__` 。所以我们只需在继承类中给出以上 5 种行为的具体实现即可得到映射 ADT 中所有行为的实现。

后续实现的类的关系图如下：

![各个类的关系图](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1744200161055.png)

#### 1.2.1 基于 MutableMapping 自定义实现的 MapBase

继承类 `MutableMapping` 并定义内嵌类 `_Item` 存储**键值对**，得到映射的基础类 `MapBase` 。

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
```

#### 1.2.2 简单的非有序映射实现 UnsortedTableMap

继承映射的基础类 `MapBase` ，使用列表简单实现可实例化的非有序映射。

```python
class UnsortedTableMap(MapBase):
    """基于未排序列表实现映射"""

    def __init__(self):
        """初始化列表"""
        self._table = []

    def __getitem__(self, k):
        """根据键取值 M[k]"""
        for item in self._table:
            if k == item._key:
                return item._value
        raise KeyError('Key Error: ' + repr(k))

    def __setitem__(self, k, v):
        """设置键为 k 的值为 v 若没有则新建 M[k] = v"""
        for item in self._table:
            if k == item._key:
                item._value = v
                return
        # 若没有找到匹配的 key 则新建
        self._table.append(self._Item(k, v))

    def __delitem__(self, k):
        """删除键为 k 的对象"""
        for j in range(len(self._table)):
            if k == self._table[j]._key:
                self._table.pop(j)  # 找到后使用列表的删除方式
                return
        raise KeyError('Key Error: ' + repr(k))

    def __len__(self):
        """对象总数目"""
        return len(self._table)

    def __iter__(self):
        """迭代器，指出 for item in M 操作"""
        for item in self._table:
            yield item._key  # 返回键 key
```

测试案例：

```python
if __name__ == '__main__':
    m = UnsortedTableMap()
    m['test1'] = 1
    m['test2'] = 2
    m['test3'] = 3
    for key in m:
        print("key: {}, value: {}".format(key, m[key]))
        
# key: test1, value: 1
# key: test2, value: 2
# key: test3, value: 3
```

**算法分析**

`UnsortedTableMap` 类的性能：

- 插入操作只需在无序列表尾增加新元素，故运行时间为 **O(1)** 。
- 查找及删除时，最坏情况下需要遍历整个列表，故运行时间为 **O(n)** 。
- 基于列表实现的无序映射，只在映射规模较小，或插入操作经常执行，但查找和删除很少执行时，较有效率。



## 2 哈希表

实践中最常用来实现映射的数据结构—— **哈希表（hash table）**

- 在哈希表中，我们直接使用键作为索引来查找键值对
- 考虑一种简单情况：映射 M 中含有 n 个元组，如使用 0 到 N-1 的整数作为键（N >= n），则可使用长为 N 的查找表来表示此映射：

![简单哈希的例子](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1744201795319.png)

因为记住了索引，此时查找、插入、删除操作均可在 **O(1)** 时间内完成。

### 2.1 哈希函数

**哈希函数（hash function）**解决了下面的问题：

- 如果 N >> n ，如何减小分配的空间？
- 映射的键不为整数的情况下，如何将其转换为索引？

哈希函数 h(k) 包括两部分：**哈希码 + 压缩函数** 。其中哈希码是将任意输入的的键值 key 转换为整数，而压缩函数则是将得到的哈希码压缩到 [0, N-1] 范围。然后再将对象存储在当下哈希函数值索引对应的位置上，即：
$$
M\ [\ h(k)\ ] = (k,\ v), \quad h(k)\in [0,\ N-1]\quad \forall\ k
$$
理想情况下，哈希函数将键均匀地映射到 [0, N-1] 这一范围内，但实践中可能有两个或更多不同键被映射到同一个索引上，这时需要进行 **冲突（collision）**处理。

### 2.2 哈希码

**哈希码**过程，相当于将任意不可变类型的键值 `k` 变为一个整数：
$$
h_1: k \to \N
$$

#### 2.2.1 将位作为整数处理

设键对应的二进制表达（不可变对象在计算机内部都对应这一个固定的 0 1 数字串）为：
$$
x = (x_0\ x_1\ x_2\ \cdots\ x_{n-1})_2
$$
**分量求和法：**将键的位（二进制表示）表示分为固定长度的几部分（如16或32位），再将各部分相加，忽略溢出。
$$
h_1(x) = \sum\limits_{i=0}^{n-1}\ x_i
$$
**分量异或法：**将键的位表示分为固定长度的几部分（如16或32位），再将各部分进行位异或运算。
$$
h_1(x) = x_0\ \oplus\ x_1\ \oplus\ x_2\ \cdots\ \oplus\ x_{n-1}
$$
**按位处理的特点：**

- 适用于键的位数大于整数位数的情况

- 可能存在的问题：忽略了各部分间的顺序，对字符串或可变长度对象不一定是个好选择

#### 2.2.2 多项式哈希码

类似地，先将键的位表示分为固定长度的几部分（如16或32位）：
$$
x = (x_0\ x_1\ x_2\ \cdots\ x_{n-1})_2
$$
选择一个非零常数 a ，计算如下多项式的值，忽略溢出：
$$
p(a) = x_0 \cdot a^{n-1} + x_1 \cdot a^{n-2} + \cdots + x_{n-2} \cdot a + x_{n-1}
$$
处理英文字符串时，33、37、39、41 特别适合选作 a 值，在超过 50000 个英文单词构成的集合上每个哈希码上的冲突小于 7 次。

为提高性能，利用 **Horner** 规则，多项式的值可以在 **O(n)** 内计算出来：
$$
p_i(a) = x_i + a\cdot p_{i-1}(a),\quad i=1,\ 2,\ \cdots\ n-1
$$

#### 2.2.3 循环移位哈希码

多项式哈希码的一个变种，将多项式哈希码中乘 a 的操作变为对部分和的循环移位。

例如，一个32位数 **00111**XX...X 的五位循环移位值取其最左边五位，并且将它们放置到数据的最右边，得到结果 XX...X**00111**。在 Python 中，二进制位循环移位可以通过使用按位运算符 `<<` 和 `>>` 完成，从而截取结果 32 位整数。

5 位循环移位在 230000 个单词构成的集合中哈希码的最大冲突次数为 3 。

#### 2.2.4 Python 中的哈希码

Python 中使用**内置函数** `hash(x)` 计算对象 x 的哈希码。只有**不可变数据类型才是可哈希的**：

- `int`、`float`、`str`、`tuple`、`frozenset` 可哈希
- `list`、`dict`、`set` 不可哈希

默认情况下，用户定义的类不可哈希。但可通过在类中实现一个使用**不可变对象计算哈希码的特殊方法** `__hash__`，有此方法的类即可哈希，如：

```python
class x:
    ...
	def __hash__(self):
        """对象存储这 RGB 三色的数值"""
		return hash((self._red, self._green, self._blue))
    ...
```

### 2.3 压缩函数

**压缩函数**的目的是将哈希码压缩到 [0, N-1] 范围：
$$
h_2: \N \to [0,\ N-1]
$$
最终**哈希函数**即为
$$
h(k) = h_2(h_1(k))
$$

#### 2.3.1 模函数取余/划分方法

哈希表的大小 `N` （通常取质数），则对于某个键 `k` ，用模 N 的方法将其压缩到 [0, N-1]
$$
h_2(k) \equiv y \mod N \quad \Rightarrow \quad y \in [0,\ N-1]
$$
如 N 不为质数，则出现冲突的概率大幅提升。例：哈希码为 {200, 205, 210, 215, 220, …, 600}。如 N = 100，则每个哈希码将至少与另三个哈希码冲突；但如 N = 101，则不会发生冲突。

#### 2.3.2 MAD 方法

有一个更复杂的压缩函数，即 **Multiply-Add-and-Divide, MAD 方法**。这个方法通过
$$
h_2(k) = [(a\cdot k+b)\mod p] \mod N
$$
其中 p 为比 N 大的质数， a 和 b 为区间内任意选择的整数，且 a > 0 。该函数使得哈希函数得到的结果更好地被分散在 [0, N − 1] 中。

### 2.4 处理冲突

当两个不同的键被映射到同一个索引时，就发生了**冲突**。哈希函数的设计可以减少冲突，但往往不能完全避免冲突的发生。

我们将表概念化为**桶数组（bucket array）**，每个桶里可能装着多个由哈希函数映射到该桶的键值对，例如下面的例子：

![出现冲突时，一种存储方式：桶数组](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1744204546431.png)

两类常见的冲突处理方式：**链地址法 (sepearate chaining)** 和 **开放寻址法 (open addressing)**

#### 2.4.1 链地址法/分离链表

**链地址法（sepearate chaining）**：在桶数组中的每个位置建立一个二级容器，存储所有映射到该位置的键值对，此容器通常为数组或链表。

- 链地址法实现简单，但需要额外的空间

例如下面直观的例子：

![链地址法](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1744204591880.png)

#### 2.4.2 开放寻址法

链地址法需要占用额外空间存储链，所以开放寻址法成为了一个替代方法。**开放寻址法（open addressing）**直接将键值对存储在对应索引处，并采取更复杂的机制处理冲突。

- 开放寻址法需要哈希表长度 N 始终大于所需存储的键值对数目 n
- 冲突发生时，当前键值对的位置已被另一个键值对占据，则根据某种规则探测下一个位置尝试进行插入，而探测的方法有：**线性探测法**、**二次探测法**、**双重哈希法**。

##### 线性探测法

**线性探测法（linear probing）：**冲突发生时，尝试将新键值对插入紧邻的下一个位置。

例如：不断 $j+1\mod N,\ j+2\mod N,\ \cdots$ 

![线性探测](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1744204839541.png)

**可能存在的问题**：

- 倾向于将键值对集中连续地存储，很大程度上影响搜索效率。
- 冲突时，因为查找和插入会不断向后直到遇到 `None` ，所以删除元素时不可以简单置空，可以填充一个特殊的对象，例如自定义一个对象 `AVAIL` 用作删除时填充。同样的，下次插入时 `AVAIL` 是可插入位置。具体实现可见后文的 Python 实现。

**总结：**

查找操作 `get(k)` ：从索引 h(k) 处开始探测连续探测下一个位置，直到发生以下某种情况

- 找到一个键为 k 的键值对
- 找到一个未存储键值对的空位置
- 遍历 N 个位置后未出现以上两种情况

删除操作 `remove(k)` ：

- 使用查找操作 `get(k)` 寻找键为 k 的元素
- 如果找到这样的元素 (k, v) ，则将其替换为 AVAIL ，并返回 v
- 否则，返回 None

插入操作 `set(k)`：从索引 h(k) 处开始探测，连续探测下一个位置，直到发生以下情况

- 找到一个空位置或存储着 AVAIL 的位置。如成功找到插入位置，则将键值对 (k, v) 存在此处。
- 遍历 N 个位置后未出现以上情况，插入不成功

##### 二次探测法

**二次探测法（quadratic probing）**：冲突发生时，尝试依次探测以下位置，直到发现一个空位置：
$$
[\ h(k) + f(i)\ ] \mod N,\quad i = 0,\ 1,\ 2,\ \cdots
$$
其中 $h(k)$ 为哈希码，对与线性探索 $f(i) = i$ 但对于二次探索则 $f(i) = i^2$ 。

##### 双重哈希法

**双重哈希法（double hashing）**：使用第二个哈希函数 h'(k) 确定下一个探测的位置。具体来说，冲突发生时，依次探索以下位置，直到发现一个空位置：
$$
h(k) + i\cdot h'(k) \mod N,\quad i = 0,\ 1,\ 2,\ \cdots
$$
第二个哈希函数 $h'(k) \neq 0$ 以避免原地寻找。哈希表的长度 N 应保证为质数，以使得所有位置都可被探测到。

常用的第二个哈希函数 h'(k) 为：
$$
h'(k) = q - (k \mod q)
$$
其中 q < N 且为质数。

### 2.5 负载因子、重新哈希和效率

#### 2.5.1 负载因子

对需要存放 n 个元素且长为 N 的哈希表，定义其**负载因子（load factor）**为：
$$
\lambda = \frac{n}{N}
$$
若 𝜆 为 **O(1)** ，则哈希表的核心操作时间复杂度也为 **O(1)** 。𝜆 应选择较小的常数，最好不大于 1 。

- 对于链地址法，冲突发生后找到目标键的时间与链的长度成正比；𝜆 接近 1 时，冲突发生的概率急剧上升。一般来说，建议将链地址法的负载因子控制在 𝜆 < 0.9 。
- 当 N 为质数，且负载因子小于 0.5 时，二次探测能保证找到一个空位置。
- 随着负载因子 𝜆 增长到 0.5 以上并向 1 逼近时，开放寻址法下桶数组中元素的集群开始增加，这使得各探测策略均需花费较长时间寻找空位置。

**结论：**实验表明，对于线性探测法，应保持 𝜆 < 0.5，对其他探测法负载因子可略高（Python实现的开放寻址法规定 𝜆 < 2/3）。

#### 2.5.2 重新哈希

当对哈希表的插入操作导致负载因子超过给定阈值时，需要调整哈希表的大小并将所有对象重新插入新的哈希表，这被称为**重新哈希（rehashing）**

- 不需要重新定义哈希码，但需要基于新哈希表重新设计一个压缩函数
- 新哈希表大小通常约为原表大小的 2 倍
- 建立新哈希表的时间被摊销到所有插入操作上

#### 2.5.3 哈希表的效率

**哈希表的时间复杂度：**

- 最坏情况下，哈希表的查找、插入和删除操作均需花费 **O(n)** 的时间。

- 平均情况下，哈希表的查找、插入和删除操作仅需花费 **O(1)** 的时间。

**负载因子 𝜆 对哈希表的效率有很大的影响：**

- 假设哈希值的分布是随机的，则在开放寻址法下，期望的探测次数为 $\frac{1}{1-\lambda}$ 。

- 在实践中，当负载因子 𝜆 显著小于1时，哈希表的速度非常快

**哈希表的应用：**

- 小型数据库
- 编译器
- 浏览器缓存

![哈希表实现映射与列表实现映射的性能比较](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1744206564848.png)



## 3 Python 实现哈希表

在这部分，根据前面的知识，实现两种哈希表，一种使用**链地址法**，而另一种使用**线性探测的开放寻址**。

### 3.1 哈希表基类

扩展 `MapBase` 类来定义一个新的哈希表基类 `HashMapBase` 类。HashMapBase 类主要的设计元素是：

- 桶数组由一个 Python 列表表示，名为 `self._table` ，并且所有的条目初始为 None 。
- `self._n` 的实例变量用来表示当前存储在哈希表中不同元组的个数。
- 如果表格的负载因子 `n / N` 增加到超过 0.5 ，我们会将哈希表的大小扩大 2 倍并且将所有元组重新哈希到新的表中。
- 我们定义一个`_hash_` 方法，该方法依靠 Python 内置哈希函数 `hash()` 来生成键的哈希码，并用 `MAD` 公式生成压缩函数。

**代码实现**

```python
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
```

在我们的设计中，`HashMapBase` 类假定有以下抽象方法，且每一个方法必须**在具体子类中实现**：

- `_bucket_getitem(i, k)` ：这个方法在桶 j 中搜索查找键为 k 的元组，如果找到了则返回对应的值，如果找不到则抛出 KeyError 。 
- `_bucket_setitem(i, k, v)` ：这个方法将桶 j 中键 k 的值修改为 v 。如键 k 的值已经存在，则新的值覆盖已经存在的值。否则，将这个新元组插入桶中，并且这个方法负责增加 self._n 的值。
- `_bucket_delitem(i, k)` ：这个方法删除桶 j 中键为 k 的元组，如果这样的元组不存在则抛出 KeyError 异常（在这个方法之后 self._n 的值会减小）。
- `__iter__` ：迭代器的方式遍历所有键。

### 3.2 链地址法/分离链表

`ChainHashMap` 类的形式实现链地址法的哈希表。它采用 `UnsortedTableMap` 类的一个实例来表示单个的桶。

**代码实现**

```python
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
```

测试：注意到，不同于 `UnsortedTableMap` 非有序列表实现的映射（使用逐个检索列表的 key 从而找到元素值）。这里的哈希表采用了先计算 hash 值，再寻找键值对的位置，所以顺序由键 `key` 和哈希函数决定。速度也非常的快，平均意义上的 **O(1)** 。

```python
if __name__ == '__main__':
    chain_hash_map = ChainHashMap()
    chain_hash_map['A'] = 1
    chain_hash_map['B'] = 2
    chain_hash_map['C'] = 3
    for key in chain_hash_map:
        print("key: {}, value: {}".format(key, chain_hash_map[key]))

# key: B, value: 2
# key: A, value: 1
# key: C, value: 3
```

### 3.3 开放寻址法的线性探测法

使用**线性探测的开放寻址**实现 `ProbeHashMap` 类。为了支持删除操作，我们使用了在已被删除的表的位置上做一个特殊的标记（声明一个类级的属性 `_AVAIL` ），以此来将它和一个空 `None` 的位置区分开来。

**代码实现**

```python
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
```

测试：正如前面所分析的，平均意义下查找、插入、修改、删除均是 **O(1)** 。

```python
if __name__ == '__main__':
    probe_hash_map = ProbeHashMap()
    probe_hash_map['Avail'] = 100
    probe_hash_map['Bucket'] = 200
    probe_hash_map['Capacity'] = 300
    for key in probe_hash_map:
        print("key: {}, value: {}".format(key, probe_hash_map[key]))
        
# key: Avail, value: 100
# key: Bucket, value: 200
# key: Capacity, value: 300
```









