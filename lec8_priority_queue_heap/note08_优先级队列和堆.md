# 优先级队列 (Priority Queue) 和堆 (Heap)

本章讲解优先级队列、基于堆实现的优先级队列、一些常用的排序算法（选择排序、插入排序和高级排序算法——堆排序）。特别地，堆是一种特殊的二叉树，我们基于 Python 数组实现堆；Python 实现排序算法。

## 1 优先级队列

### 1.1 优先级队列的抽象数据类型

#### 1.1.1 优先级

队列这一数据结构，遵循 **FIFO（先入先出）**的规则进行元素的插入和删除。然而，现实生活中有时我们需要一个除 FIFO 功能外还有额外删除功能的队列。我们引入**优先级队列（Priority Queue）**这一概念来描述这一类队列，其删除操作为删除具有**最高优先级**的元素。

- 例如：航空公司的候补等待（standby）队列中，优先级更高的乘客即使到的更晚，也有可能更早获得候补机会。

#### 1.1.2 优先级队列 ADT

优先级队列中存储：一个元素和其优先级，构成键-值对结构 `(key, value)` 。在优先级队列 `P` 上定义的优先级队列 ADT 支持以下方法（本章的优先级不妨设为**最小值 min**）：

- `P.add(k, v)` ：向优先级队列 P 中插人一个键值对 `(k, v)` 。
- `P.min()` ：返回一个元组 `(k, v)` ，代表优先级队列 P 中一个键值对，该元组的键值是最小值（但是没有移除该元组）；如果队列为空，将发生错误。
- `P.remove_min()` ：从优先级队列 P 中移除一个拥有最小键值的元组，并且返回这个被移除的元组，`(k, v)` 代表这个被移除的元组的键和值；如果优先级队列为空，将发生错误。
- `P.is_empty()` ：如果优先级队列不包含任何元组，将返回 `True` 。
- `len(P)` ：返回优先级队列中元组的数量。

下面的例子展示了这些功能的具体过程：

![优先级队列的 ADT](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1743831618569.png)

### 1.2 优先级队列的实现

#### 1.2.1 组合设计模式

组合设计模式：定义一个 `_Item` 类，用它来确保在主要的数据结构中每个元组保存它相关计数值。

对于优先级队列，我们将使用组合设计模式来存储内部元组，该元组包含键 `k` 和值 `v` 构成的数值对。为后续的构建提供方便，这里构建了一个基础父类，未来的类均继承于 `PriorityQueueBase` 类，其中包含一个嵌套类 `_Item` 的定义。对于元组实例 `a` 和 `b` ，重载比较符 `<` 。

```python
class PriorityQueueBase:
    """
    优先级队列的抽象数据类型基础类 ADT
    """

    # ---------- 嵌套的 _Item 类 ----------
    class _Item:
        """每一个元素的存储方式：(k, v)"""
        __slots__ = '_key', '_value'

        def __init__(self, k, v):
            """初始化键值对 (k, v)"""
            self._key = k
            self._value = v

        def __lt__(self, other):
            """重载运算符 <"""
            return self._key < other._key  # 根据 key 键值比较大小

    # ---------- 优先级队列 ADT ----------
    def is_empty(self):
        """__len__ 方法暂时未定义，由子类定义"""
        return len(self) == 0
```

> 这里的键值需要满足**全序关系**：

**全序关系：**一个集合 $A$ 上的全序关系需满足

- 自反性

$$
\forall\ x \in A,\quad x \leq x
$$

- 反对称性

$$
\forall\ x,\ y \in A,\quad x \leq y\ \and y \leq x \quad\Rightarrow\quad x = y
$$

- 传递性

$$
\forall\ x,\ y,\ z \in A,\quad x\leq y,\ y\leq z \quad\Rightarrow\quad x \leq z
$$

- $A$ 中任意两个元素均可比较

#### 1.2.2 未排序列表实现优先级队列

创建未排序的列表实现优先级队列的 `UnsortedPriorityQueue` 类，它继承优先级队列 ADT `PriorityQueueBase` 类。未排序指的是，每次 `add` 增加新元素时，直接在列表后面加入；但每次查找/删除元素时 `min()` `remove_min()` 都需要遍历列表找到最小值。

> 注意：这里使用了之前章节 [链表](https://zhuanlan.zhihu.com/p/29813136429) 定义的 `PositionalList` 。也可以在我的 [Github 库](https://github.com/isKage/dsa-notes/blob/main/lec8_priority_queue_heap/utils/positional_list.py) 中找到代码内容。

```python
class UnsortedPriorityQueue(PriorityQueueBase):
    """未排序的列表实现优先级队列"""

    def __init__(self):
        """初始化，利用队列类 PositionalList"""
        self._data = PositionalList()

    def __len__(self):
        """返回长度"""
        return len(self._data)

    def add(self, key, value):
        """增加元素 (key, value)"""
        # 向 PositionalList 队列类新增 _Item 类实例
        self._data.add_last(self._Item(key, value))

    def _find_min(self) -> PositionalList.Position:
        """最小键值元素 _Item"""
        if self.is_empty():
            raise Empty('Priority queue is empty')

        # 遍历
        small = self._data.first()
        walk = self._data.after(small)
        while walk is not None:
            # 这里的 element 返回的是一个 _Item 类
            if walk.element() < small.element():
                small = walk  # 记录最小值
            walk = self._data.after(walk)  # 向后更新一步
        return small  # 遍历完后得到最小值 (返回的是 PositionalList.Position 类)

    def min(self) -> tuple:
        """返回最小 (key, value)"""
        p = self._find_min()
        item = p.element()  # PositionalList.Position._node._element -> _Item 类
        return (item._key, item._value)

    def remove_min(self) -> tuple:
        """返回最小 (key, value) 并删除"""
        p = self._find_min()
        item = self._data.delete(p)
        return (item._key, item._value)
```

例如：

```python
if __name__ == '__main__':
    upq = UnsortedPriorityQueue()
    upq.add(1, 'small')
    upq.add(3, 'median')
    upq.add(5, 'large')
    print("The min is:", upq.min())
    print("Delete the min:", upq.remove_min())
    print("Now, the min is:", upq.min())
# The min is: (1, 'small')
# Delete the min: (1, 'small')
# Now, the min is: (3, 'median')
```

#### 1.2.3 排序列表实现优先级队列

创建排序的列表实现优先级队列的 `SortedPriorityQueue` 类，它继承优先级队列 ADT `PriorityQueueBase` 类。排序指的是，每次 `add` 增加新元素时，都进行比较，使得队列一直都是有序状态，例如从小到大；每次查找/删除元素时 `min()` `remove_min()` 只需要拿出队列第一个元素即可。

```python
class SortedPriorityQueue(PriorityQueueBase):
    """排序的列表实现优先级队列"""

    def __init__(self):
        """初始化，利用队列类 PositionalList"""
        self._data = PositionalList()

    def __len__(self):
        """返回长度"""
        return len(self._data)

    def add(self, key, value):
        """增加元素 (key, value)"""
        newest = self._Item(key, value)  # 创建新的 _Item 类实例
        walk = self._data.last()  # 从最后开始检查

        # 找到第一个比 newest 大的元素
        while walk is not None and newest < walk.element():
            walk = self._data.before(walk)  # go ahead

        # 向 PositionalList 队列类新增 _Item 类实例
        if walk is None:
            self._data.add_first(newest)  # 第一个位置插入
        else:
            self._data.add_after(walk, newest)  # 在 walk 后插入

    def min(self) -> tuple:
        """返回最小 (key, value)"""
        if self.is_empty():
            raise Empty('Priority queue is empty')
        # 有序队列：第一个元素即为最小
        p = self._data.first()
        item = p.element()
        return (item._key, item._value)

    def remove_min(self) -> tuple:
        """返回最小 (key, value) 并删除"""
        if self.is_empty():
            raise Empty('Priority queue is empty')
        # 同理，第一个元素即为最小
        item = self._data.delete(self._data.first())
        return (item._key, item._value)
```

例如：结果相同

```python
if __name__ == '__main__':
	spq = SortedPriorityQueue()
    spq.add(1, 'small')
    spq.add(3, 'median')
    spq.add(5, 'large')
    print("The min is:", spq.min())
    print("Delete the min:", spq.remove_min())
    print("Now, the min is:", spq.min())
# The min is: (1, 'small')
# Delete the min: (1, 'small')
# Now, the min is: (3, 'median')
```

#### 1.2.4 算法分析&比较

排序与未排序列表实现优先级队列的主要区别在于 (1) 插入 (2) 删除/查找最小元素

- **未排序列表**：每次直接在尾部插入新元素，所以复杂度为 `O(1)` ；但查找和删除最小元素却需要遍历列表寻找，复杂度为 `O(n)` 。
- **排序列表**：排序列表则相反。每次插入新元素，都需要遍历来找到最佳位置，所以复杂度为 `O(n)` ；但查找和删除最小元素只需要对队列第一个元素操作，复杂度为 `O(1)` 。

![排序与否的比较](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1743837646130.png)



## 2 堆

**二进制堆的数据结构**：一个更加有效的优先级队列的实现。这个数据结构允许我们以对数时间复杂度 `O(log(n))` 来实现插人和删除操作。

### 2.1 堆的数据结构

**堆是一棵二叉树 T **，该树的节点上存储了集合中的元组并且满足两个附加的属性：关系属性以存储键的形式在 T 中定义；结构属性以树 T 自身形状的方式定义。

#### 2.1.1 Heap-Order 属性

**在堆 T 中，对于除了根的每个位置 p ，存储在 p 中的键值大于或等于存储在 p 的父节点的键值。即 $key(p) \geq key(parent(p))$ 。**

作为 Heap-Order 属性的结果，T 中从根到叶子的路径上的键值是以非递减顺序排列的。也就是说，一个**最小的键总是存储在 T 的根节点**中。这使得调用 `min` 或 `remove_min` 时，能够比较容易地定位这样的元组，一般情况下它被认为“在堆的顶部”。

#### 2.1.2 完全二叉树属性

**一个高度为 h 的堆 T 是一棵完全二叉树：即 T 的 $0,\ 1,\ 2,\ \cdots,\ h - 1$ 层上尽可能达到节点数的最大值 $2^i$ ，并且剩余的节点在 h 层尽可能保存在最左的位置。**

完全二叉树属性是为了尽可能提高遍历效率，后面我们会看到，影响高度 h 是影响堆效率的主要因素，而完全二叉树能保证在节点数固定为 n 时使得高度最小，大概为 $\log n$ 。

#### 2.1.3 堆的高度

**堆/完全二叉树的高度 $h = [\log n]$ 。其中 [] 表示取整。**

这是完全二叉树的性质，我们假设节点数为 n 的高度为 h ，则完全二叉树需要满足：
$$
1+ (1 + 2 + \cdots + 2^{h-1}) = 2^h \leq n \leq 2^h - 1 + 2^h = 2^{h+1} - 1
$$
于是可以推出 $n = [\log n]$ 。

下面是一个标准的堆的例子：

![堆的完全二叉树结构例子](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1743840261916.png)

### 2.2 使用堆实现优先级队列

`min()` 方法的实现很简单，由于堆的 Heap-Order 属性，位于根节点的元素一定是 `min()` ，所以时间复杂度为 `O(1)` 。

#### 2.2.1 插入和向上冒泡

优先级队列的 `add(k, v)` 操作对应于在堆中插入一个新元组

堆中元素的插入由三个步骤组成：

- 找到插入新节点的位置 z
- 将新元组放在位置 z 处
- 通过**向上冒泡**恢复堆的 Heap-Order 属性

插入新元组后，堆可能变得不满足 Heap-Order 性质：

- 通过对新节点和其父节点的键值进行比较，并在必要时交换两个节点的位置，不断重复即可恢复其Heap-Order 性质，这种操作被称为**堆向上冒泡 Up-Heap Bubbling** 
- 堆向上冒泡操作在新节点成为根节点或其键值大于其父节点键值时停止
- 堆向上冒泡操作的时间复杂度为 `O(log n)` （即最坏情况要遍历树的每一层，而树的高度为 `[log n]` ）

下面的图示，展示了一个插入和向上冒泡的过程：

![a 为原始堆，b 在堆尾部插入元素 (2,T)](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1743927952888.png)

![c 对新元素 (2,T) 进行冒泡，因为 2 < 20 ，得到 d](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1743928016199.png)

![e 同理进行父子节点比较，向上冒泡，得到 f](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1743928073600.png)

![同样操作，直到冒泡到根节点/键值关系满足 Heap-Order 属性](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1743928122435.png)

#### 2.2.2 删除和向下冒泡

因为 Heap-Order 属性保证了根节点即为 min ，所以优先级队列的 `remove_min()` 操作对应于在堆中删除根节点。

堆中元素的删除由三个步骤组成：

- 将**根节点用最后一个节点 w 代替**
- 移除最后一个节点 w
- 通过**向下冒泡**恢复堆的 Heap-Order属性

用最后一个节点将根节点替代后，堆可能变得不满足 Heap-Order 性质：

- 通过对新的根节点和其孩子节点的键值进行比较，并在必要时交换根节点和有较小键值的孩子节点的位置，不断重复即可恢复其 Heap-Order 性质，这种操作被称为**堆向下冒泡 Down-Heap Bubbling**
- 堆向下冒泡操作在最后一个节点成为叶子节点或其键值小于其所有孩子节点键值时停止
- 堆向下冒泡操作的时间复杂度为 `O(log n)` （即最坏情况要遍历树的每一层，而树的高度为 `[log n]` ）

下面的图示，展示了一个删除和向下冒泡的过程：

![a 将最后节点 (13,W) 替换到根节点，并删除根节点 (4,C) ，得到 b 图](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1743928511145.png)

![c 父节点 13 大于子节点最小键值 5 ，故向下冒泡，得到 d](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1743928578370.png)

![类似地，重复冒泡过程](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1743928664804.png)

![继续冒泡，直到到达叶子节点/键值均小于子节点时，恢复 Heap-Order 性质](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1743928679120.png)

> 【注意】每次向下冒泡，都需要找 **2 个子节点最小键值** 进行交换。

### 2.3 基于数组的堆/完全二叉树表示

基于数组实现树，对于完全二叉树十分适用。这是因为完全二叉树尽可能的用满了每一层的空间，且剩余的叶子节点都在左侧，这非常符合数组的结构。

那么假设一个基于数组 A 的完全二叉树 T 已经实现，则对于在 A 中索引为 p 的节点，则有：

- 若 p 为根节点，则 `p = 0`
- 若 q 为 p 的左子节点，则 `q = 2 * p + 1`
- 若 q 为 p 的右子节点，则 `q = 2 * p + 2`

下面是一个堆/完全二叉树存储在数组里的例子：

![堆/完全二叉树](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1743929197105.png)

它存储在数组里为：

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1743929444547.png)

### 2.4 Python 实现堆

#### 2.4.1 Python 实现

基于堆的优先级队列的 Python 实现。我们使用基于数组的表示，保存了元组组合表示的 Python 列表。采用递归来实现 `_upheap` 和 `_downheap` 中的重复调用。继承之前的 `PriorityQueueBase` 基础类。

```python
class HeapPriorityQueue(PriorityQueueBase):
    """
    堆的实现：完全二叉树，根节点为 min
    """

    # ---------- 非公有方法：二叉树结构 ----------
    def _parent(self, j):
        """返回父节点"""
        return (j - 1) // 2

    def _left(self, j):
        """当前位置的左子节点"""
        return 2 * j + 1

    def _right(self, j):
        """当前位置的右子节点"""
        return 2 * j + 2

    def _has_left(self, j):
        """左子节点是否存在/合法"""
        return self._left(j) < len(self._data)

    def _has_right(self, j):
        """右子节点是否存在/合法"""
        return self._right(j) < len(self._data)

    def _swap(self, i, j):
        """交换 i j 位置上的元素 <=> 冒泡"""
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _upheap(self, j):
        """向上冒泡"""
        parent = self._parent(j)  # j 的父节点
        if j > 0 and self._data[j] < self._data[parent]:  # 非根节点/不满足 Heap-Order
            self._swap(j, parent)  # 冒泡/交换
            self._upheap(parent)  # 递归实现，向上 (parent) 冒泡

    def _downheap(self, j):
        """向下冒泡"""
        # 找到最小的子节点 small_child
        if self._has_left(j):  # 左/非叶节点
            left = self._left(j)
            small_child = left

            if self._has_right(j):  # 右/非叶节点
                right = self._right(j)
                if self._data[right] < self._data[left]:
                    small_child = right

            # 不满足 Heap-Order
            if self._data[small_child] < self._data[j]:
                self._swap(small_child, j)  # 冒泡/交换
                self._downheap(small_child)  # 递归实现，向下 (small_child) 冒泡

    # ---------- 公有方法：堆结构 ----------
    def __init__(self):
        """列表用来存储完全二叉树"""  # 可优化，见后
        self._data = []

    def __len__(self):
        """重载 len()"""
        return len(self._data)

    def add(self, key, value):
        """增加元素"""
        self._data.append(self._Item(key, value))  # 尾部新增
        self._upheap(len(self._data) - 1)  # 从最后一个向上冒泡

    def min(self):
        """查看 min 不删除"""
        if self.is_empty():
            raise Empty('Priority queue is empty')

        item = self._data[0]  # 由 Heap-Order 性质，第一个元素为 min
        return (item._key, item._value)

    def remove_min(self):
        """删除 min"""
        if self.is_empty():
            raise Empty('Priority queue is empty')

        self._swap(0, len(self._data) - 1)  # 交换最后一个元素和根节点
        item = self._data.pop()  # 删除最后一个元素，即交换来的根节点/min
        self._downheap(0)  # 从根/第一个开始向下冒泡
        return (item._key, item._value)
```

#### 2.4.2 基于堆的优先级队列的算法分析

注意到，基于堆的优先级队列，在 `min()` 操作时，由于 Heap-Order 性质，可以在 `O(1)` 内完成。而在新增元素和删除/查看最小元素时，最坏的情况都是遍历每一层，而不是每一个节点，这使得对于 n 个节点完全二叉树/堆，其高度/层数仅 `log n` 级别，故复杂度也只有 `O(log n)` ，这明显是大大提高了效率。

![算法复杂度分析](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1743931198577.png)

**结论**：堆数据结构都是优先级队列非常有效的实现方式。与基于未排序或已排序列表的实现不同，基于堆的实现在插人和移除操作中均能快速地获得运行结果。

#### 2.4.3 自底向上构建堆

在初始化构建堆时，从一个空堆开始连续调用 n 次 `add()` 操作的时间复杂度为 `O(n log n)` （因为每次新增元素在最坏的情况下都是 `O(log n)` 级别的复杂度，调用 n 次则为 `O(n log n)` 这是不高效的）。

**自底向上构建堆**可将此操作的时间复杂度降为 `O(n)` 。初始化的是非空的堆，堆中元素由 n 个。为了叙述简单，我们设：
$$
n = 2^{h+1} - 1
$$
即这个初始的堆为一个满二叉树（即每一次都满了，每层 $2^i$ 个节点）。那么，自底向上构建堆进行如下操作：

- 第 1 步，任意取 `(n + 1)/2` 个节点最为最底部的叶子节点；
- 第 2 步，再任意取 `(n + 1)/4` 个节点，作为最后 1 层的父节点，同时对倒数第 2 层每个节点进行一次**向下冒泡**，使得满足 Heap-Order 属性；
- ······
- 第 i 步，再任意取 `(n+1)/2^i` 个节点，作为倒数第 i+1 层的父节点，同时对本层（倒数第 i 层）每个节点进行向下冒泡，使得满足 Heap-Order 属性；
- ······
- 第 h + 1 = log(n + 1) 步，按照同样的方式，此次创建的是根节点，仍然进行最后 1 次向下冒泡，最终得到初始堆。

例如：如下图，15 = 2^4 - 1 个节点的堆，任意取 8 个元素构成最底部的节点；然后任意取 4 个构成倒数第二层节点，进行向下冒泡，使得满足 Heap-Order 性质；如此重复得到初始化后的堆。

![15 个节点的堆](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1743933519764.png)

**Python 实现**：修改之前的 `HeapPriorityQueue` 的 `__init__()` 方法，使得可以根据 `contents` 序列类快速初始化，复杂度为 `O(n)` 。

```python
class HeapPriorityQueue(PriorityQueueBase):
    ...
    
	# ---------- 公有方法：堆结构 ----------
	def __init__(self, contents=()):
        """列表用来存储完全二叉树，可根据 contents 自底向上初始化"""
        if not isinstance(contents[0], tuple): # 若 contents 元素不是元组
            # 则键值对存储 (e, e) for e in contents
            self._data = [self._Item(e, e) for e in contents]
        else: # 为元组就可以正常按照 (k, v) 存储
            self._data = [self._Item(k, v) for k, v in contents]  
            
        if len(self._data) > 1:  # 确实需要初始化，若为空或只有 1 个则不需要冒泡
            self._heapify()  # 自底向上，逐个冒泡，使得满足 Heap-Order

    def _heapify(self):
        """从底向上初始化堆的冒泡过程"""
        start = self._parent(len(self) - 1)  # 从最后一个节点的父节点开始向下冒泡
        for j in range(start, -1, -1):  # 从后向前，一直到根节点
            self._downheap(j)

	...
```

如此可以一开始指定初始化的堆：

```python
if __name__ == '__main__':
	# a example
    print("=" * 15, "Heap Priority Queue by Array", "=" * 15)
    l = [(1, 'small'), (2, 'median'), (3, 'large')]
    hpq = HeapPriorityQueue(l)
    print("The min is:", hpq.min())
    print("Delete the min:", hpq.remove_min())
    print("Now, the min is:", hpq.min())
    
# =============== Heap Priority Queue by Array ===============
# The min is: (1, 'small')
# Delete the min: (1, 'small')
# Now, the min is: (2, 'median')
```

**时间复杂度为 `O(n)` 的证明：**

在最坏的情况下，如何进行冒泡，即冒泡的路径，并不影响复杂度。所以我们不妨假设每个节点处的堆向下泡冒路径均先向右走，然后一直向左走，直到堆底部。

每个节点最多被两条路径经过，因此所有路径经过的边数总和为 `O(n)` 。因此，自底向上构建堆的时间为 `O(n)` 。

![可视化证明图示](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1743934486425.png)

#### 2.4.4 heapq 模块

Python 的标准分布包含一个 `heapq` 模块，该模块提供对基于堆的优先级队列的支持。该模块不提供任何优先级队列类，而是提供一些函数，**这些函数把标准 Python 列表作为堆进行管理**。

**heapq** 的一些常见函数，针对列表类 L 操作（假设 L **已经满足** Heap-Order 属性）：

- `heappush(L, e)`：将元素 e 存入列表 L ，并重新调整列表以满足 heap-order 属性。该函数执行的时间复杂度为 `O(log n)` 。

- `heappop(L)` ：取出并返回列表 L 中拥有最小值的元素，并且重新调整存储以满足 heap-order 属性。该函数执行的时间复杂度为 `O(log n)` 。

- `heappushpop(L, e)` ：将元素 e 存人列表 L 中，同时取出和返回最小的元组。该函数执行的时间复杂度为 `O(log n)` ，但是它较分别调用 push 和 pop 方法的效率稍微高一些。因为如果最新被插入列表的元素值是最小的，那么该函数立刻返回；否则，即为常见的 push + pop 操作。

- `heapreplace(L, e)` ：与 heappushpop 方法类似。

**heapq** 的一些常见函数，针对列表类 L 操作（假设 L **不满足** Heap-Order 属性）：

- `heapify(L)` ：改变未排序的列表，使其满足 heap-order 属性。这个函数使用自底向上的堆构造算法，时间复杂度为 `O(n)` 。
- `nlargest(k, iterable)`：从一个给定的迭代 `iterable` 中生成含有 k 个最大值的列表。执行该函数的时间复杂度为 `O(n + k log n)` 。
- `nsmallest(k, iterable)` ：从一个给定的选代 `iterable` 中生成含有 k 个最小值的列表。该函数使用与 nlargest 相同的技术，其时间复杂度为 `O(n + k log n)` 。

例如：

```python
import heapq

L = [3, 2, 1, 4, 5, 6, 7, 10, 9, 8]  # 不满足 Heap-Order

# 1. 自底向上构建堆
heapq.heapify(L)
print(L)
"""
[1, 2, 3, 4, 5, 6, 7, 10, 9, 8]
1
2 3
4 5 6 7
10 9 8
满足 Heap-Order
"""

# 2. 返回最大最小的 2 个
print(heapq.nlargest(2, L))
print(heapq.nsmallest(2, L))
"""
[10, 9]
[1, 2]
"""

# 3. 去除最小
print(heapq.heappop(L))
print(L)
"""
[2, 4, 3, 8, 5, 6, 7, 10, 9]
2
4 3
8 5 6 7
10 9
满足 Heap-Order
"""
```



## 3 排序

### 3.1 使用优先级队列进行排序

我们可以使用优先级队列对一个可比较元素集合进行排序：

- 首先使用 `add` 操作将集合中的元素一个接一个地插入到优先级队列中
- 再使用 `remove_min` 操作将元素以某种顺序从优先级队列中移出

此算法的运行时间取决于优先级队列的具体实现方式。

通用伪代码：

```python
def pq_sort(C, pq):
    """伪代码：对 C 排序，借用 pq 优先级队列类"""
    n = len(C)
    P = pq()  # 辅助优先级队列
    for j in range(n):
        element = C.delete(C.first())  # 拿出 C 的元素
        P.add(element, element)  # 存储 (e, e)
    for j in range(n):
        (k, v) = P.remove_min()  # 取出最小的 e
        C.add_last(v)  # 放回原来的 C
```

### 3.2 选择排序和插入排序

#### 3.2.1 选择排序

当使用**未排序列表**实现优先级队列时，PQ-sort 即为**选择排序**。

**选择排序的复杂度：`O(n^2)`**

- 将所有元素使用 `add` 操作插入优先级队列需要 n 次操作，运行时间为 `O(n)` 。
- 将元素按顺序移出长为 n 的优先级队列需要每次使用 `remove_min` 操作选择优先级最高的元素，其运行时间正比于：

$$
n + (n-1) + (n-2) + \cdots + 1 = O(n^2)
$$

<img src="https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1743941045902.png" alt="选择排序示例" style="zoom:50%;" />

**代码实现**

```python
from utils import UnsortedPriorityQueue

def selection_sort(C):
    n = len(C)
    P = UnsortedPriorityQueue()  # 见之前定义的 UnsortedPriorityQueue 类
    for j in range(n):
        element = C.pop()
        P.add(element, element)
    for j in range(n):
        (k, v) = P.remove_min()
        C.append(v)


if __name__ == '__main__':
    print("=" * 15, "Selection Sort", "=" * 15)
    l = [7, 4, 8, 2, 5, 3]
    print("Initial list:", l)
    selection_sort(l)
    print("After sort:", l)

# =============== Selection Sort ===============
# Initial list: [7, 4, 8, 2, 5, 3]
# After sort: [2, 3, 4, 5, 7, 8]
```

#### 3.2.2 插入排序

当使用**排序列表**实现优先级队列时，PQ-sort 即为**插入排序**。

**插入排序的复杂度：`O(n^2)`**

- 将所有元素使用 `add` 操作插入优先级队列的运行时间正比于：

$$
1 + 2 +3 + \cdots + n = O(n^2)
$$

- 将排好序的元素使用 `remove_min` 操作从优先级队列中移出需要 n 次操作，运行时间为 `O(n)`

<img src="https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1743941482500.png" alt="插入排序示例" style="zoom:50%;" />

**代码实现**

```python
from utils import UnsortedPriorityQueue

def insertion_sort(C):
    n = len(C)
    P = SortedPriorityQueue()  # 见之前定义的 UnsortedPriorityQueue 类
    for j in range(n):
        element = C.pop()
        P.add(element, element)
    for j in range(n):
        (k, v) = P.remove_min()
        C.append(v)


if __name__ == '__main__':
    print("=" * 15, "Insertion Sort", "=" * 15)
    l = [7, 4, 8, 2, 5, 3]
    print("Initial list:", l)
    insertion_sort(l)
    print("After sort:", l)
    
# =============== Insertion Sort ===============
# Initial list: [7, 4, 8, 2, 5, 3]
# After sort: [2, 3, 4, 5, 7, 8]
```

### 3.3 堆排序

正如前面所说，使用优先级队列进行排序，其效率完全取决于优先级队列的实现方式；更具体一点，效率取决于优先级序列 `add` 和 `remove_min` 操作的复杂度。而对于堆，其插入和删除的复杂度均为 `O(log n)` 相对于 `O(n)` 复杂度高效的多。

- add 阶段：由于第 i 次 add 操作完成后堆有 i 个元组，所以第 i 次 add操作的时间复杂度 `O(log i)` 。因此，这一阶段整体的时间复杂度 `O(n log n)` ，但通过**自底向上的构建堆**，时间复杂度能够被提升到 `O(n)` 。
- remove_min 阶段：第 j 次 remove_min 操作执行时堆中有 `(n - j + 1)` 个元组，因此第 j 次 remove_min 操作的时间复杂度为 `O(log (n - j + 1))` 。将所有这些 remove_min 操作累加起来，这一阶段的时间复杂度 `O(n log n)` 。

**结论：当使用堆来实现优先级队列时，整个优先级队列排序算法的时间复杂度为 `O(n log n)` 。这个排序算法就称为堆排序。**

#### 3.3.1 简单实现堆排序

**代码实现**

```python
from utiles import HeapPriorityQueue
def heap_sort(C):
    # 特别地，利用了自底向上构建堆的初始化方法 O(n)
    P = HeapPriorityQueue(C)  # 见之前定义的 HeapPriorityQueue 类
    for j in range(len(C)):  # O(n log n)
        C[j] = P.remove_min()[0]

if __name__ == '__main__':        
    print("=" * 15, "Heap Sort", "=" * 15)
    l = [7, 4, 8, 2, 5, 3]
    print("Initial list:", l)
    heap_sort(l)
    print("After sort:", l)

# =============== Heap Sort ===============
# Initial list: [7, 4, 8, 2, 5, 3]
# After sort: [2, 3, 4, 5, 7, 8]
```

#### 3.3.2 原地堆排序

更进一步，如果需要排序的对象也是用数组存储的，例如上面的例子。则可以原地进行堆排序，如此可以节省空间，也节省了申请一个新空间和摊销的时间成本：

- 重新定义堆的操作，使其成为最大堆（maximum-oriented heap）（并不重要，仅仅影响是升序还是降序），即父节点键值不小于孩子节点；算法执行过程中，始终使用**列表的左半部分表示堆，右半部分表示序列**。
- add 阶段：我们从一个空堆开始，从左向右移动堆与序列之间的边界，一次一步；每一步将序列中的下一个元素追加到堆中。
- remove_add 阶段：我们从一个空的序列开始，从右向左移动堆与序列之间的边界，一次一步；每一步将最大值元素从堆中移除并存储到当前序列的最前方。

<img src="https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1743944140925.png" alt="原地堆排序图示" style="zoom: 45%;" />

**代码实现**：同时实现了升序和降序，只需指定 `descend=False` 则为升序。

```python
def heapsort(arr, descend=False):
    """原地堆排序"""
    n = len(arr)
    if n <= 1:
        return

    def downheap(start, end):
        """从 start 开始向下冒泡，堆的范围是 [0, end)"""
        parent = start
        # while True:
        left = 2 * parent + 1
        right = 2 * parent + 2

        if not descend:
            # 从小到大，堆的根节点为 max
            largest_child = parent

            if left < end and arr[left] > arr[largest_child]:
                largest_child = left
            if right < end and arr[right] > arr[largest_child]:
                largest_child = right

            if largest_child == parent:
                return None  # 如果父节点已经是最大的，停止

            arr[parent], arr[largest_child] = arr[largest_child], arr[parent]
            downheap(largest_child, end)  # 继续向下冒泡
        else:
            # 从大到小，堆的根节点为 min
            smallest_child = parent

            if left < end and arr[left] < arr[smallest_child]:
                smallest_child = left
            if right < end and arr[right] < arr[smallest_child]:
                smallest_child = right

            if smallest_child == parent:
                return None  # 如果父节点已经是最小的，停止

            arr[parent], arr[smallest_child] = arr[smallest_child], arr[parent]
            downheap(smallest_child, end)  # 继续向下冒泡

    # 1. 构建最大堆（从最后一个非叶子节点开始）
    for i in range((n // 2) - 1, -1, -1):
        # <=> 整个序列为一个暂未满足 heap-order 的堆，进行冒泡调整
        downheap(i, n)  # 自底向上的构建

    # 2. 排序阶段：每次将堆顶（最大值）交换到末尾，并向下冒泡
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # 交换堆顶和当前末尾
        downheap(0, i)  # 向下冒泡
```

例如：

```python
if __name__ == '__main__':
	print("=" * 15, "The Best! - In-place Heap Sort", "=" * 15)
    l = [7, 4, 8, 2, 5, 3]
    print("Initial list:", l)

    heapsort(l, descend=False)  # 从小到大
    print("sort not descend:", l)

    heapsort(l, descend=True)  # 从大到小
    print("sort descend:", l)

# =============== The Best! - In-place Heap Sort ===============
# Initial list: [7, 4, 8, 2, 5, 3]
# sort not descend: [2, 3, 4, 5, 7, 8]
# sort descend: [8, 7, 5, 4, 3, 2]
```
## 补充：定位器

为了能通过 O(1) 时间就找到指定的节点，并进行更新或删除，可以加入定位器，Python 实现 `AdaptableHeapPriorityQueue` 类如下：

```python
class AdaptableHeapPriorityQueue(HeapPriorityQueue):
    """加入定位器, 使得可以在 O(1) 时间定位某个节点"""

    # ---------------------- nested Locator class ----------------------
    class Locator(HeapPriorityQueue._Item):
        """定位器, 包装 _Item 加入位置索引"""
        __slots__ = '_index'

        def __init__(self, k, v, j):
            super().__init__(k, v)
            self._index = j  # 存入位置索引

    # ---------------------- nonpublic behaviors ----------------------
    def _swap(self, i, j):
        """交换后, 更新位置"""
        super()._swap(i, j)
        self._data[i]._index = j
        self._data[j]._index = i

    def _bubble(self, j):
        """综合的冒泡操作: 向上或向下"""
        if j > 0 and self._data[j] < self._data[self._parent(j)]:
            self._upheap(j)  # 向上
        else:
            self._downheap(j)  # 向下

    def add(self, key, value):
        """加入新元素"""
        token = self.Locator(key, value, len(self._data))  # 加到最后, 即堆的最后一个点下
        self._data.append(token)
        self._upheap(len(self._data) - 1)  # 当前位置向上冒泡
        return token

    def update(self, loc, newkey, newval):
        """更新某个位置的元素 O(1)"""
        j = loc._index  # 获取在 self._data 的索引
        if not (0 <= j < len(self) and self._data[j] is loc):
            raise ValueError('Invalid locator')  # 不合法的位置类
        # 更新
        loc._key = newkey
        loc._value = newkey
        self._bubble(j)  # 冒泡

    def remove(self, loc):
        """移除某个位置的元素 O(1)"""
        j = loc._index  # 获取在 self._data 的索引
        if not (0 <= j < len(self) and self._data[j] is loc):
            raise ValueError('Invalid locator')  # 不合法的位置类
        # 删除
        if j == len(self) - 1:  # 在尾部直接删除
            self._data.pop()
        else:
            self._swap(j, len(self._data) - 1)  # 否则移到尾部
            self._data.pop()  # 仍然删除尾部
            self._bubble(j)  # 冒泡
        return (loc._key, loc._value)
```