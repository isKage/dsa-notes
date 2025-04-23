# 链表 (2) 含有位置信息的链表、链表的插入排序和 More-To-Front 启发式算法

在单向链表、循环链表和双向链表的基础上，引入位置信息，定义基于链表的位置列表数据类型，并基于链表实现了插入排序。

对于新的位置列表类，本质上利用链表的方法串联了一个复杂的类 `Position` ，而这个类中包含了链表的节点（`_Node`）以及这个位置所属的位置列表信息。

除此之外，介绍了案例：访问频率列表，构建了一个网页收藏夹列表类，存储网页信息和访问次数。并使用 More-To-Front 启发式算法提高查询访问量最高的前 k 个网页的效率。

## 1 位置列表的抽象数据类型

与内存分布连续的数组相比，链表只要给定特定的节点，便可完成对节点的插入和删除（讨论的是双向链表），正如[上一章](https://zhuanlan.zhihu.com/p/29508680467)（[博客链接](https://blog.iskage.online/posts/9241942.html)）定义的 `_DoublyLinkedBase` 类给出的 `_insert_between()` 和 `_delete_node()` 方法。

但是，数组可以在常数时间，根据整数索引，完成索引操作。对于链表而言，却只能一步一步的遍历，直到找到目标节点，这是非常数时间操作。

### 1.1 位置信息的抽象类

为了方便外部用户调用链表类时，我们可以在继承 `_DoublyLinkedBase` 类后，增加内嵌的**位置类** `Position` ，而这就是**含位置信息的列表抽象类**。

这个列表抽象类 `PositionalList` 应该满足如下的操作例子：

![位置列表类的操作示意](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1741769316869.png)

> `p` 和 `q` 是实例化后的位置类 `Position` ，存储了对应节点的位置信息。

### 1.2 双向链表的实现

使用双向链表完整实现位置列表类 `PositionalList` 的方法。相关解释见后：

```python
class PositionalList(_DoublyLinkedBase):
    """利用双向链表实现位置列表类"""

    # -------------- 内嵌的位置类 --------------
    class Position:
        """抽象的位置类，存储节点的位置信息"""

        def __init__(self, container, node):
            """初始化位置信息"""
            # _container 存储列表类 PositionalList 表明当前位置类属于这个列表类
            self._container = container
            self._node = node

        def element(self):
            """返回当前位置的节点元素值"""
            return self._node._element

        def __eq__(self, other):
            """检查二者是否具有相同的位置信息 重载运算符 =="""
            return type(other) is type(self) and other._node is self._node

        def __ne__(self, other):
            """与上面相反 重载运算符 !="""
            return not self == other

    # -------------- 检查位置类、为节点实例化位置类 --------------
    def _validate(self, p):
        """检查是否是合法的 Position 类，返回位置类存储的节点类"""
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position')
        if p._container is not self:
            # 检查当前位置类 p 是否属于当前列表，以免误操作了别的列表
            raise ValueError('p does not belong to this container')
        if p._node._next is None:
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self, node):
        """对每个节点，实例化它的位置类"""
        if node is self._header or node is self._trailer:
            return None
        else:
            # 创建属于当前列表的位置类
            return self.Position(self, node)

    # -------------- 查看位置列表类的方法 --------------
    def first(self):
        """返回第一个节点的位置类，注意不含哨兵节点"""
        return self._make_position(self._header._next)

    def last(self):
        """返回最后一个节点的位置类，注意不含哨兵节点"""
        return self._make_position(self._trailer._prev)

    def before(self, p):
        """返回位置类 p 前面的位置类"""
        node = self._validate(p)  # 检查是否是合法的位置类
        return self._make_position(node._prev)

    def after(self, p):
        """返回位置类 p 后面的位置类"""
        node = self._validate(p)
        return self._make_position(node._next)

    def __iter__(self):
        """迭代器，逐个生成返回列表的元素值"""
        cursor = self.first()
        while cursor is not None:
            yield cursor.element()
            cursor = self.after(cursor)

    # -------------- 改变位置列表类的方法 --------------
    def _insert_between(self, e, predecessor, successor):
        """使用父类方法，但返回位置类"""
        # 覆写父类插入方法
        node = super()._insert_between(e, predecessor, successor)
        return self._make_position(node)

    def add_first(self, e):
        """在头部插入，返回位置类"""
        return self._insert_between(e, self._header, self._header._next)

    def add_last(self, e):
        return self._insert_between(e, self._trailer._prev, self._trailer)

    def add_before(self, p, e):
        """在位置类 p 前插入"""
        original = self._validate(p)
        return self._insert_between(e, original._prev, original)

    def add_after(self, p, e):
        original = self._validate(p)
        return self._insert_between(e, original, original._next)

    def delete(self, p):
        """删除位置类 p 返回 p 上的值"""
        original = self._validate(p)
        return self._delete_node(original)  # 父类方法

    def replace(self, p, e):
        """替换位置 p 的值为 e，返回 p 位置之前的值"""
        original = self._validate(p)
        old_value = original._element
        original._element = e
        return old_value
```



#### 1.2.1 定义 Position 类

定义位置类 `Position` 用来方便的得到每个节点的位置。因为只要位置信息已知，链表的插入和删除操作的复杂度为 $O(1)$ 。

同时 `Position._container` 属性也为每个节点创建位置类时指定了所属的列表类。以免对别的列表类的位置进行误操作。

而对于 `Position._node` 则存储了链表的节点类 `_Node` ，节点类包含了真正的信息，例如元素值 `_element` 和前后指针 `_prev` `_next` 。

#### 1.2.2 _validate 和 _make_position 方法

首先 `_valudate()` 方法调用，意在检查传入的是否为位置类 `Position` ，以及检查是否为本列表 `PositionalList` 类的位置类。最后返回当前位置的节点类。

而 `_make_position()` 方法则打包处理了将节点转换为位置类的过程。传入链表节点，得到含义位置信息的新类（位置类）。同时对于哨兵节点返回 None。

#### 1.2.3 查看列表/链表信息

`first(), last()` 方法可以得到列表第一个和最后位置的信息，例如 `L.first().element()` 可以得到第一个位置的值。而 `after(), before()` 方法可以根据传入的位置类，查看前后位置的信息，返回的仍然为位置类。

`__iter__()` 方法配合父类的 `__len__()` 方法一起产生了迭代器。 `yield cursor.element()` 不断返回列表各个位置存储的值。

> `return` 和 `yield` 的区别：`return` 是当函数/方法到达时返回结果，同时推出程序；但 `yield` 在返回结果后会暂停程序，下次调用时再次返回结果，直到函数/方法里的迭代结束。

#### 1.2.4 操作列表/链表信息

`_insert_between()` 方法为非公有方法，父类方法返回的是节点类，这里覆写返回位置类。而后的 `add_first(), add_last(), add_before(), add_after()` 方法均是在新的插入方法中，传入位置信息，然后进行操作。

`_delete_node()` 方法为非公有类，父类方法对节点进行操作。这里不做修改，只是定义新的公有方法 `delete()` 直接根据位置类进行删除。



## 2 位置列表的排序

### 2.1 基于链表的插入排序

在之前定义的类 `PositionalList` 之后，我们定义一个排序函数 `insertion_sort()` ，采用插入排序，实现对位置列表的排序操作。（从小到大）

**原理** 定义一个指针 `marker` 遍历链表。当指针 `marker` 对应节点的值小于它后面的指针 `pivot` 对应节点的值，则 `marker` 后移即可；否则，让一个新的指针 `walk` 从现在的位置不断向前移动，寻找最远的一个值比 `pivot` 指针对应节点的值大的位置，将 `pivot` 插入到此时 `walk` 前面。（记录 `pivot` 的值，然后删除它，将这个值插入到 `walk` 前）。 

<img src="https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1741773030496.png" alt="链表插入排序示意" style="zoom:50%;" />

### 2.2 代码实现

```python
def insertion_sort(L: PositionalList):
    """
    对链表插入排序
    :param L: 位置列表类 PositionalList
    :return: no return
    """
    if len(L) > 1:
        marker = L.first()
        while marker != L.last():  # 遍历链表
            pivot = L.after(marker)
            value = pivot.element()  # 保存后一个节点的值
            if value > marker.element():  # 满足排序要求（从小到大）
                marker = pivot
            else:
                walk = marker
                # 当没到第一个元素 并且 walk 前一个元素比 value 大，walk 不断向前找
                while walk != L.first() and L.before(walk).element() > value:
                    walk = L.before(walk)

                L.delete(pivot)
                L.add_before(walk, value)  # 插入到此时 walk 前
```



## 3 More-To-Front 启发式算法

### 3.1 案例：访问频率列表

设计一个对象类，用来记录每个节点被访问的次数。在现实中，这样的对象十分常见，例如网页的点击量列表：存储了各个网页对象和其被访问的次数，同时还能得到排名靠前的网页对象。所以，在这一节中，定义收藏夹列表类 `FavoritesList` 使其满足功能：

- `access(e)` ：访问元素 `e` ，增加访问次数。如果 `e` 不在列表里，则添加到列表里。
- `remove(e)` ：移除元素 `e` ，注意安全移除，需要先判断是否存在。
- `top(k)` ：以迭代器的方式，返回访问量最多的 `k` 个元素。

### 3.2 方案一：有序列表

为了快速实现 `top(k)` 方法，可以在收藏夹列表类的更新中不断排序，使得 `FavoritesList` 的元素一直满足访问量从大到小的顺序。

**Python 实现** 收藏夹列表类直接使用之前定义的 `PositionalList` 存储网页对象 `_Item` （存储了元素 `_value` 和次数 `_count`）。

```python
from utils import PositionalList


class FavoritesList:
    """有序列表方式实现"""

    # -------------- 内嵌的 _Item 类 --------------
    class _Item:
        __slots__ = '_value', '_count'  # 限制实例属性，优化内存使用

        def __init__(self, e):
            self._value = e  # 用户提供的元素
            self._count = 0  # 访问计数，初始为 0

    # -------------- 非公有方法 --------------
    def _find_position(self, e):
        """返回元素 e 的位置类 Position"""
        walk = self._data.first()  # 在初始化后，self._data 是 PositionalList 类

        # 寻找元素 e 的位置，返回位置类 Position
        while walk is not None and walk.element()._value != e:
            walk = self._data.after(walk)  # 移动到下一个节点
        return walk

    def _move_up(self, p):
        """插入排序思想，按照次数 _count 产生有序列表"""
        # 与之前插入排序 insertion_sort 思路基本相同
        # 甚至更为简单，比较对象只用最后新加入的元素
        if p != self._data.first():
            cnt = p.element()._count
            walk = self._data.before(p)
            if cnt > walk.element()._count:
                while (walk != self._data.first() and
                       cnt > self._data.before(walk).element()._count):
                    walk = self._data.before(walk)
                self._data.add_before(walk, self._data.delete(p))

    # -------------- 公有方法 --------------
    def __init__(self):
        """初始化收藏夹列表类，直接实例化一个 PositionalList 类"""
        self._data = PositionalList()

    def __len__(self):
        """返回长度"""
        return len(self._data)  # PositionalList 已经定义了 __len__()

    def is_empty(self):
        """查看是否为空"""
        return len(self._data) == 0

    def access(self, e):
        """访问元素 e 增加次数/添加元素"""
        p = self._find_position(e)
        if p is None:  # 不存在则插入
            # 向列表增加对象 _Item
            # 可以理解为 PositionalList 的链表的节点 _Node 的 _element 存储着 _Item 对象的地址
            p = self._data.add_last(self._Item(e))
        p.element()._count += 1

        self._move_up(p)  # 排序

    def remove(self, e):
        """从收藏夹列表类中移除元素 e 对应的 _Item 对象"""
        p = self._find_position(e)
        if p is not None:
            self._data.delete(p)  # 这里的 _Item 对象相当于链表的 element 值

    def top(self, k):
        """迭代器的方式产生前 k 个元素"""
        if not 1 <= k <= len(self):
            raise ValueError('Illegal value of k')

        walk = self._data.first()
        for j in range(k):
            # 迭代后移
            item = walk.element()
            yield item._value
            walk = self._data.after(walk)
```

> 注意：这里链表节点的存储的值为 `_Item` 对象的地址

### 3.3 方案二：More-To-Front 启发式算法

**Move-to-Front 启发式算法** ：每访问一个元素，都会把该元素移动到列表的最前面。这么做是希望这个元素在近期可以被再次/连续访问（这是符合常识的，被多次点击的网页一般都会在近期被再次访问）。

#### 3.3.1 分析时间复杂度

假设对于一个空的收藏夹列表，我们访问 n 个网页 `1, 2, 3, ..., n` 分别连续 n 次。因为按照访问次数排序，则对于第一个网页，每次访问需要 $O(1)$ ，对于第二个网页每次都要和前一个网页比较（并且在访问 n 次之前都不会排在前一个元素前面），每次访问需要 $O(2)$ ，以此类推，每个访问 n 次：
$$
n + 2n + 3n + \cdots + n \cdot n = n \cdot \frac{n(n+1)}{2} \sim O(n^3)
$$
时间复杂度为 $O(n^3)$ ，这是极其低效的。

但是采用 **More-To-Front** 算法，即按照访问时间排序，最后被访问的网页排在第一。如此对于任何一个网页，连续访问 n 次都是 $O(1)$ ，因为访问第一次后，这个网页就位于第一个位置，链表查询第一个位置只需要 1 次操作。于是，每个访问 n 次的总时间：
$$
n \cdot 1 + n \cdot 1 + n \cdot 1 + \cdots + n \cdot 1 = n \cdot n \sim O(n^2)
$$
时间复杂度为 $O(n^2)$ ，相对高效。

#### 3.3.2 代码实现 MTF 算法

只需覆写 `_move_up()` 和 `top()` 方法即可。

- 因为 `_move_up()` 方法只在访问 `access()` 方法调用时使用，所以每次使用 `_move_up()` 均代表该元素最近被访问，所以直接放在列表最前即可
- 而相比有序列表，查找前 k 个网页的 `top()` 方法就相对耗时，对于查找 k 个最大，没查找一个就要遍历全部，所以复杂度为 $O(kn)$ ，不过利用以后要学习的其他高效方法，复杂度能降低到 $O(n + k\log n)$ 。这也说明 MTF 启发式算法在处理这个问题时相对更加高效。

```python
class FavoritesListMTF(FavoritesList):
    """利用 More-To-Front 启发式算法实现收藏夹列表类"""

    # -------------- 只需要重载/覆写 _move_up() 和 top() 方法即可 --------------
    def _move_up(self, p):
        """每次调用意味着被访问，被访问就移到最前"""
        if p != self._data.first():
            self._data.add_first(self._data.delete(p))

    def top(self, k):
        """因为列表无序，需要找到最大的前 k 个元素"""
        if not 1 <= k <= len(self):
            raise ValueError('Illegal value of k')

        # 临时复制一份原列表
        temp = PositionalList()
        for item in self._data:
            temp.add_last(item)

        for j in range(k):
            # 遍历一边找到最大的
            highPos = temp.first()
            walk = temp.after(highPos)
            while walk is not None:
                if walk.element()._count >= highPos.element()._count:
                    highPos = walk
                walk = temp.after(walk)
            yield highPos.element()._value

            # 删除最大的之后再遍历
            temp.delete(highPos)
```























