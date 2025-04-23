# 搜索树（1）：二叉搜索树、平衡搜索树、AVL 树

本章使用树结构来高效地实现有序映射，例如：二叉搜索树、平衡搜索树、 AVL 树。二叉搜索树根据比较左右节点和根节点的大小决定存储，例如 `左 > 根 > 右` 。平衡搜索树和 AVL 实现高度平衡属性，则进一步保证了树的高度为 log n ，从而使得时间复杂度为 O(log n) 。

## 1 二叉搜索树

映射 M 最重要的 5 类行为（查找、增添、删除、修改、遍历）：

- `M[k]` ：如果存在，返回映射 M 中键 k 对应的值，否则抛出 KeyError 。Python 中该功能由特殊方法 `__getitem__` 实现。
- `M[k] = v` ：使得映射 M 中键 k 对应于值 v 。如 k 有之前对应的值，则替换掉该值。Python 中该功能由特殊方法 `__setitem__` 实现。
- `del M[k]` ：从映射 M 中删除键为 k 的键值对。如键 k 不存在则抛出 KeyError 。Python 中该功能由特殊方法 `__delitem__` 实现。
- `len(M)` ：返回映射 M 中键值对的数量。Python 中该功能由特殊方法 `__len__` 实现。
- `iter(M)` ：返回一个包含映射 M 所有键的迭代器。Python 中该功能由特殊方法 `__iter__` 实现。

有序映射的映射 ADT 的扩展，它包括标准映射的所有行为，还增加了以下方法：

- `M.find_min()` ：用最小键返回键值对（或None，如果映射为空）
- `M.find_max()` ：用最大键返回键值对（或 None，如果映射为空）
- `M.find_It(k)` ：用严格小于 k 的最大键返回键值对（或 None，若没有这样的项存在）
- `M.find_le(k)` :用严格小于等于 k 的最大键返回键值对（或 None，若没有这样的项存在）
- `M.find_gt(k)` ：用严格大于 k 的最小的键返回键值对（或 None，若没有这样的项存在）
- `M.fnd_ge(k)` ：用严格大于或等于 k 的最小的键返回键值对（或None，若没有这样的项存在）
- `M.fnd_range(start, stop)` ：用 start <= 键 < stop 迭代遍历所有键值对。如果 start 指定为 None ，从最小的键开始迭代；如果 stop 指定 None，到最大键迭代结束
- `iter(M)` ：根据自然顺序从最小到最大迭代遍历映射中的所有键
- `reversed(M)` ：根据逆序迭代映射中的所有键 r ，这在 Python 中是用 reversed 来实现的

**二叉搜索树：**二叉树的每个节点 p 存储一个键值对 `(k, v)` ，使得：

- 存储在 p 的左子树的键都小于 k 。
- 存储在 p 的右子树的键都大于 k 。

![二叉搜索树的例子](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1744966390556.png)

### 1.1 遍历二叉搜索树

采用**中序遍历**可以按照键的顺序遍历二叉搜索树。中序遍历即利用的递归的方式先访问左子树，再访问节点，最后访问右子树。中序遍历的复杂度为 **O(n)** 其中 n 为树的节点个数。

对于树的 ADT ，除了常见的 `parent(), left(), right()` 方法，二叉搜索树还提供根基中序遍历返回元素的方法：

- `frist()` ：返回一个包含最小键的节点，如果树为空，则返回 None 。
- `last()` ：返回一个包含最大键的节点，如果树为空，则返回 None 。
- `before(p)` ：返回比节点 p 的键小的所有节点中键最大的节点（即中序遍历中在 p 之前的节点），如果p是第一个节点，则返回 None 。
- `after(p)` ：返回比节点 p 的键大的所有节点中键最小的节点（即中序遍历中在 p 之后的节点），如果p是最后一个节点，则返回 None 。

以 `after()` 为例，展示如何返回在中序遍历时 p 后面的节点：

```python
Algorithm after(p):
	if right(p) is not None # p 有右子节点
		walk = right(p) 
		while left(walk) is not None do
			walk = left(walk)  # 右子树的最左子节点为 after(p)
		return walk

    else
		walk = p
		ancestor = parent(walk)
        while ancestor is not None and walk == right(ancestor) do
            walk = ancestor
            ancestor = parent(walk)  # 第一个作为祖先节点的左子节点的父节点为 after(p)
        return ancestor
```

显然，利用这种方法最坏情况便是遍历树的每一层，所以复杂度为 **O(h)** 其中 h 为树的层数。

### 1.2 搜索

搜索键 k 时，我们从树根开始向下搜索，在每个节点 p 上，下一步操作由当前节点的键与 k 的比较结果而决定：

- 若 `p.key() > k` ，则继续搜索左子树

- 若 `p.key() == k` ，则搜索成功且终止

- 若 `p.key() < k` ，则继续搜索右子树

- 若最后探查到空子树，则搜索失败

实现可以采用递归的方式，伪代码如下：

```python
Algorithm TreeSearch(T, p, k):
    if k == p.key() then
	    return p  # 搜索成功
    
    else if k < p.key() and T.left(p) is not None then
    	return TreeSearch(T, T.left(p), k)  # 递归搜索左子树

    else if k > p.key() and T.right(p) is not None then
    	return TreeSearch(T, T.right(p), k)  # 递归搜索右子树

    return p
```

类似地，这里的搜索查看也是最坏需要遍历树的每一层，复杂度为 **O(h)** 。

### 1.3 插入和删除

#### 1.3.1 插入

对于插入操作，首先搜索键 k 。如找到则重新对其值进行赋值，否则返回搜索失败时最后一个探查的节点 p ：

- 若 `k < p.key()` ，则将包含  k的新节点作为 p 的左孩子
- 若 `k > p.key()` ，则将包含 k 的新节点作为 p 的右孩子

![插入新元素的例子](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1744968042824.png)

伪代码见下：

```python
Algorithm TreeInsert(T, k, v):
    p = TreeSearch(T, T.root(), k)  # 先搜索键 k
    if k == p.key() then
        Set p’s value to v  # 找到则修改值
	
    # 否则，查看当前 key 与需要插入的 (k, v) 比较
    else if k < p.key() then
        add node with item (k, v) as left child of p
    else
        add node with item (k, v) as right child of p
```

#### 1.3.2 删除

删除操作比插入更复杂，因为删除的可能是度为 2 的节点。首先搜索键 k 。如找到，设找到的节点为 p，则：

- 若 p 无孩子节点，直接删除即可
- 若 p 有一个孩子节点 r，则删除 p 且用其孩子节点替代它

但是，若 p 有两个孩子节点，则：

- 使用 `before(p)` 找到中序遍历中节点 p 的前一个节点 r

- 用节点 r 替代节点 p

- 删除节点 r

> 删除 `before(p)` 的方法一定能保持树的结构完整，前一个节点 r 一定只有 1 个或 0 个孩子节点。

![删除的节点有 2 个字节点，则寻找前一个节点 r 交换后再删除](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1744968441749.png)

### 1.3 Python 实现二叉搜索树

下面实现二叉搜索树的抽象数据类型 ADT `TreeMap` ，它继承了两个基类：一个是基于双向链表实现的二叉树类 `LinkedBinaryTree` ，另一个为映射的基础类 `MapBase` 。

> 关于 `LinkedBinaryTree` 和 `MapBase` 类的实现可以分别查看 [LinkedBinaryTree 基于双向链表实现的二叉树](https://github.com/isKage/dsa-notes/blob/main/lec7_tree/utils/linked_binary_tree.py) 和 [MapBase 映射的基类 ADT](https://github.com/isKage/dsa-notes/blob/main/lec9_map_hash/utils/map_base.py) 。或者直接查看本章的代码仓库 [搜索树实现的完整代码](https://github.com/isKage/dsa-notes/tree/main/lec10_search_tree/utils) 。

```python
try:
    from .linked_binary_tree import LinkedBinaryTree
    from .map_base import MapBase
except ImportError:
    from linked_binary_tree import LinkedBinaryTree
    from map_base import MapBase


class TreeMap(LinkedBinaryTree, MapBase):
    """有序映射：二叉搜索树"""

    # --------------- 覆写 LinkedBinaryTree 的 Position 类 ---------------
    class Position(LinkedBinaryTree.Position):
        """负责指明节点是否属于当前树，以及存储了节点类 _Node"""

        def key(self):
            """返回键"""
            return self.element()._key

        def value(self):
            """返回值"""
            return self.element()._value

    # --------------- 非公有方法 ---------------
    def _subtree_search(self, p, k):
        """搜索：从 p 节点开始搜索键为 k 的子节点，或最后一个搜索到的节点"""
        if k == p.key():
            return p
        elif k < p.key():
            if self.left(p) is not None:
                return self._subtree_search(self.left(p), k)
        else:
            if self.right(p) is not None:
                return self._subtree_search(self.right(p), k)
        return p  # 未搜索到则返回自己

    def _subtree_first_position(self, p):
        """从 p 节点开始搜索，一直搜索到最左的子节点"""
        walk = p
        while self.left(walk) is not None:
            walk = self.left(walk)
        return walk

    def _subtree_last_position(self, p):
        """从 p 节点开始搜索，一直搜索到最右的子节点"""
        walk = p
        while self.right(walk) is not None:
            walk = self.right(walk)
        return walk

    # --------------- 引导方法 ---------------
    def first(self):
        """中序遍历第一个元素，即最小元素"""
        if len(self) == 0:
            return None
        return self._subtree_first_position(self.root())

    def last(self):
        """中序遍历最后一个元素，即最大元素"""
        if len(self) == 0:
            return None
        return self._subtree_last_position(self.root())

    def before(self, p):
        """中序遍历 p 节点的前一个元素"""
        self._validate(p)  # 判断是否为当前树的节点，不重要
        if self.left(p):
            return self._subtree_last_position(self.left(p))
        else:
            walk = p
            above = self.parent(walk)
            while above is not None and walk == self.left(above):
                walk = above
                above = self.parent(walk)
            return above

    def after(self, p):
        """中序遍历 p 节点的后一个元素"""
        self._validate(p)
        if self.right(p):
            return self._subtree_first_position(self.right(p))
        else:
            walk = p
            above = self.parent(walk)
            while above is not None and walk == self.right(above):
                walk = above
                above = self.parent(walk)
            return above

    def find_position(self, k):
        """找到键为 k 的节点"""
        if self.is_empty():
            return None
        else:
            p = self._subtree_search(self.root(), k)
            self._rebalance_access(p)  # 平衡树结构的钩子方法，实现方法见后
            return p

    # --------------- 有序映射方法 ---------------
    def find_min(self):
        """最小 k"""
        if self.is_empty():
            return None
        else:
            p = self.first()
            return (p.key(), p.value())

    def find_max(self):
        """最大 k"""
        if self.is_empty():
            return None
        else:
            p = self.last()
            return (p.key(), p.value())

    def find_ge(self, k):
        """大于或等于 k 的最小的键 (key, value)"""
        if self.is_empty():
            return None
        else:
            p = self.find_position(k)
            if p.key() < k:
                p = self.after(p)
            return (p.key(), p.value()) if p is not None else None

    def find_range(self, start, stop):
        """迭代器：(key, value) 使得 start <= key < stop"""
        if not self.is_empty():
            if start is None:
                p = self.first()
            else:
                p = self.find_position(start)
                if p.key() < start:
                    p = self.after(p)

            while p is not None and (stop is None or p.key() < stop):
                yield (p.key(), p.value())
                p = self.after(p)

    # --------------- 访问和插入节点的映射操作 ---------------
    def __getitem__(self, k):
        """查看元素 M[k]"""
        if self.is_empty():
            raise KeyError('Key Error: ' + repr(k))
        else:
            p = self._subtree_search(self.root(), k)
            self._rebalance_access(p)
            if k != p.key():
                raise KeyError('Key Error: ' + repr(k))
            return p.value()

    def __setitem__(self, k, v):
        """更新/插入元素 M[k] = v"""
        if self.is_empty():
            leaf = self._add_root(self._Item(k, v))  # 从零插入根节点
        else:
            p = self._subtree_search(self.root(), k)
            if p.key() == k:
                p.element()._value = v
                self._rebalance_access(p)
                return
            else:
                item = self._Item(k, v)
                if p.key() < k:
                    leaf = self._add_right(p, item)
                else:
                    leaf = self._add_left(p, item)
        self._rebalance_insert(leaf)  # 平衡操作的钩子函数，插入时的平衡变化

    def __iter__(self):
        """按照顺序，以迭代器的方式返回 k"""
        p = self.first()
        while p is not None:
            yield p.key()
            p = self.after(p)

    def delete(self, p):
        """删除节点 p"""
        self._validate(p)
        if self.left(p) and self.right(p):  # 度为 2 特殊处理
            replacement = self._subtree_last_position(self.left(p))  # 前一个节点
            self._replace(p, replacement.element())  # LinkedBinaryTree 的方法
            p = replacement
        # p 的度为 1 或 0
        parent = self.parent(p)
        self._delete(p)  # LinkedBinaryTree 的方法
        self._rebalance_delete(parent)  # 平衡操作的钩子函数，删除时的平衡变化

    def __delitem__(self, k):
        """删除键为 k 元素 del M[k]"""
        if not self.is_empty():
            p = self._subtree_search(self.root(), k)
            if k == p.key():
                self.delete(p)
                return
            self._rebalance_access(p)
        raise KeyError('Key Error: ' + repr(k))
```

### 1.4 算法分析：二叉搜索树的性能

分析**搜索**操作时间：

- 二叉搜索算法为递归算法，每个递归调用执行常数次操作
- 递归调用发生在从根节点向下的一条路径中的每一个节点上
- 因此，二叉搜索的运行时间与树的高度 h 有关，为 **O(h)**

分析**插入、删除**操作，依赖于搜索操作，其运行时间也为 **O(h)** 。

二叉搜索树的性能很大程度上由其高度 h 决定：

- 最好情况下，h 为 **O(log n)** ，此时二叉搜索树为高效数据结构，搜索操作运行时间为 **O(log n)**
- 最坏情况下，二叉搜索树退化为线性的链表，搜索操作运行时间为 **O(n)**

### 1.5 补充练习：查找最近公共祖先

给定一个二又搜索树，请设计一个算法，找到该树中两个指定节点的最近公共祖先。

**思路：**对于两个节点 p 和 q ，它们对应的键值为 `k1` 和 `k2` ，那么它们的最近的公共祖先。即为从根节点向下寻找，直到找到一个节点的键 `k` 满足 `k1 <= k <= k2` 。

因为二叉搜索树每次分叉 2 个字节点，一定是 `左边 < 父节点 < 右边` ，所以对于在公共节点前的每个节点，p 和 q 都是在它的一个分支上，所以不是 p q 同时大于它，就是同时小于它。只有当 `k1 <= k <= k2` 才找到了开始分叉的祖先节点。



## 2 平衡搜索树

注意到，虽然二叉搜索树理论最优是 **O(h) = O(log n)** ，前提是树的结构尽可能矮（即节点尽可能占满前 h - 1 层）。但是每次对二叉搜索树进行插入、删除时，很有可能破坏树的结构，例如退化到一个近似单链的结构，如此就是最坏情况，复杂度为 **O(n)** 。

为了解决这种问题，介绍更加先进的数据结构：**AVL 树**、**伸展树**、**红黑树**。

### 2.1 二叉搜索树的重构

平衡二叉树的主要操作是**旋转**（zig），及基于旋转的 **trinode 重构**（trinode restructuring）。

#### 2.1.1 旋转（zig）

旋转（zig）：将一个孩子节点旋转到其父亲节点上方，左图旋转至右图被称为右旋转（right rotation），反之为左旋转（left rotation）。下图中右旋转后可将子树 T1 的节点深度减 1 ，并将子树T3 的节点深度加 1 。

![旋转的例子](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1745032358311.png)

#### 2.1.2 trinode重构（trinode restructuring）

Trinode重构（trinode restructuring）：考虑对三个节点的操作，使用 1 到 2 次旋转。假设我们考虑的位置为 `x` ，其父节点为 `y` ，祖父节点为 `z` ；以 z 为根节点的树的中序遍历中，这三个节点分别为 `a, b, c` 。

- 目标：重建以 z 为根的子树，缩短到 x 及其子树的总路径长度。
- 两种情况需要 1 次旋转（zig -zig），两种情况需要 2 次旋转（zig -zag）。

`1. ` 需要 1 次旋转（single rotation）的情况（zig-zig）：

![需要 1 次旋转（zig -zig）中序遍历的顺序为 a、b、c](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1745032645510.png)

`2.  `需要2次旋转（double rotations）的情况（zig-zag）：

![需要 2 次旋转（zig -zag）中序遍历的顺序为 a、b、c](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1745032723445.png)

### 2.2 平衡搜索树的 Python 框架

之前定义的 `TreeMap` 类，只是一个具体的映射，不执行显示的平衡操作。下面，我们定义的其他具有平衡操作的类，均继承自 `TreeMap` 类。

<img src="https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1745032900691.png" alt="继承关系框架图" style="zoom:50%;" />

#### 2.2.1 平衡操作的钩子

平衡算法的钩子函数，即 `MapBase` 类暂时未定义的 `_rebalance_insert(p)` `_rebalance_delete(p)` 和 `_rebalance_access(p)` 。它们分别在搜索树插入新元素、删除元素和查看元素时调用（特别地，查看时调用是为了使得更接近根的节点更频繁被访问）。

在 `MapBase` 类后为这三个钩子函数存根：即补充三个函数的定义，但具体实现由子类实现。

```python
class MapBase(...):
    ...
    # --------------- 钩子函数挂钩存根，由子类实现 ---------------
    def _rebalance_insert(self, p):
        pass

    def _rebalance_delete(self, p):
        pass

    def _rebalance_access(self, p):
        pass
```

#### 2.2.2 旋转和重组的非公开方法

第二种支持平衡搜索树的形式是非公开的 `_rotate` 和 `_restructure` 方法，它们分别实现单一旋转和 trinode 重组。

在 `TreeMap` 类后补充这两个方法，让它们被所有平衡树的子类继承，从而促进代码重用。

```python
class MapBase(...):
    ...
	# --------------- 单一旋转和 trinode 重组 ---------------
    def _relink(self, parent, child, make_left_child):
        """重新链接父节点和子节点"""
        if make_left_child:
            parent._left = child
        else:
            parent._right = child
        if child is not None:
            child._parent = parent

    def _rotate(self, p):
        """将子节点 p 旋转上去，p 的父节点选择下来，祖先节点不变"""
        x = p._node
        y = x._parent
        z = y._parent
        if z is None:
            self._root = x
            x._parent = None
        else:
            # x 成为 z 的子节点
            self._relink(z, x, make_left_child=(y == z._left))
        if x == y._left:
            # x 右子树成为 y 左子节点
            self._relink(y, x._right, make_left_child=True)
            # y 成为 x 的右子节点
            self._relink(x, y, make_left_child=False)  
        else:
            # x 左子树成为 y 的右子节点
            self._relink(y, x._left, make_left_child=False)
            # y 成为 x 的左子节点
            self._relink(x, y, make_left_child=True)

    def _restructure(self, x):
        """trinode 重构：将节点 x 与它的父节点和祖先节点重构"""
        y = self.parent(x)
        z = self.parent(y)
        if (x == self.right(y)) == (y == self.right(z)):
            self._rotate(y)  # 一次旋转 (zig-zig)
            return y
        else:  # 两次旋转 (zig-zag)
            self._rotate(x)
            self._rotate(x)
            return x
```



## 3 AVL 树

在传统的二叉搜索树上施加限制，得到 AVL （Adelson-Velskii and Landis）树，从而保证所有基本映射操作最坏都在对数复杂度下完成。

### 3.1 平衡的二叉搜索树

#### 3.1.1 AVL 树的定义

对二叉搜索树的定义添加一条规则：对树维持对数的高度。更改高度的定义，叶子节点的高度为 1 ，定义 null 空节点的高度是 0 。任何满足**高度平衡属性**的二叉搜索树被称为 AVL 树（Adelson-Velskii and Landis）。

#### 3.1.2 高度平衡属性

**高度平衡属性：对树 T 的每一个节点 p ，p 的左右两个子树高度相差最多为 1 。**

例如：下图所示，对任意一个节点，其左右子树的高度相差为 0 或 1 。这里我们定义空节点（即叶子节点的子节点）的子树高度/度为 0 ，图中的 17, 32, 48, 62, 88 。

![具有高度平衡属性的 AVL 树的例子](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1745039817690.png)

#### 3.1.3 数学性质

由于 AVL 树的高度平衡属性，可以推导出下面的命题：

**命题：一颗存有 n 个节点的 AVL 树的高度是 O(log n) 。**

**证明：**设高度 h 的树的节点数为 $n(h)$ 。且容易得到 $n(1) = 1,\ n(2) = 2$ 。对于 $h > 2$ 的情况，如果希望节点数最小，但又满足高度平衡属性，则必有子树高度分别为 $h-1, \ h-2$ 。考虑根节点，则有递推关系式：
$$
n(h) = 1 + n(h-1) + n(h-2)
$$
由类似斐波那契数列的推导，有：
$$
n(h) > 2 \cdot n(h-2) > 2^2 \cdot n(h-4) > \cdots > 2^i \cdot n(h-2i)
$$
再结合 $n(1) = 1,\ n(2) = 2$ 可得：
$$
n(h) > 2^{\frac{h}{2} - 1}
$$
于是有 $h < 2\log(n(h)) + 2$ 。故有 AVL 树的高度是 O(log n) 。

### 3.2 更新操作

#### 3.2.1 插入

首先以二叉搜索树的插入方式进行插入操作。插入操作可能导致新节点 p 及其祖先处的高度平衡属性被破坏，需要通过 trinode 重构恢复。

我们通过一个简单的 “查找-修复” 策略来恢复 AVL 树中节点的平衡：

- z 表示从新节点 p 到根的路径上遇到的第一个不平衡位置
- y 表示 z 具有更高高度的孩子（ y 必为 p 的祖先）
- x 表示 y 具有更高高度的孩子（ x 必为 p 的祖先或 p 自身）

- 在 x 处进行 trinode 重构，即可使以 z 为根的子树重新平衡

![插入 54 后的平衡操作](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1745040939815.png)

![抽象化的操作](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1745041278133.png)

#### 3.2.2 删除

首先以二叉搜索树的删除方式进行删除操作，被删除节点的父节点 p 到根节点的路径上可能存在一个不平衡的节点，需要通过 trinode 重构恢复高度平衡。

我们通过一个简单的 “查找-修复” 策略来恢复 AVL 树中节点的平衡：

- z 表示从新节点 p 到根的路径上遇到的第一个不平衡位置

- y 表示 z 具有更高高度的孩子（ y 必不为 p 的祖先 ）
- x的定义方式如下：如 y 的两个孩子高度不同，则令 x 为 y 较高的孩子；否则，令 x 为与 y 在同一侧的孩子，即 trinode 重构只需一次旋转
- 在 x 处进行 trinode 重构，即可使以 z 为根的子树重新平衡

![删除 32 后的平衡操作](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1745041315182.png)

#### 3.2.3 算法分析：AVL 树的性能

搜索的运行时间为 **O(log n)**

- AVL 树的高度为 O(log n) ，搜索不需要 trinode 重构

插入的运行时间为 **O(log n)**

- 找到插入位置需要的时间为 O(log n)
- 进行一次 trinode 重构需要的时间为 O(1) ，更新节点高度信息需要的时间为 O(log n)

删除的运行时间为 **O(log n)**

- 找到删除位置需要的时间为 O(log n)
- 进行 trinode 重构需要的时间为 O(log n) ，更新节点高度信息需要的时间为 O(log n)

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1745042913398.png)

### 3.3 Python 实现 AVL

继承 `TreeMap` 类，实现 AVL 树的 `AVLTreeMap` 类。首先为 `TreeMap._Node` 类补充计算高度的方法。平衡操作的核心方法由 `_rebalance()` 实现。最后补充平衡操作的钩子函数 `_rebalance_insert()` 和 `_rebalance_delete()` 的具体实现。

```python
try:
    from .tree_map import TreeMap
except ImportError:
    from tree_map import TreeMap


class AVLTreeMap(TreeMap):
    """有序映射：AVL 树"""

    # --------------- 覆写内嵌的 _Node 节点类 ---------------
    class _Node(TreeMap._Node):
        """补充节点方法：计算高度"""
        __slots__ = '_height'  # 存储高度

        def __init__(self, element, parent=None, left=None, right=None):
            """初始化，并增加 _height 存储高度"""
            super().__init__(element, parent, left, right)
            self._height = 0

        def left_height(self):
            """左子树高度"""
            if self._left is None:
                return 0
            return self._left._height

        def right_height(self):
            """右子树高度"""
            if self._right is None:
                return 0
            return self._right._height

    # --------------- 平衡的基础操作 ---------------
    def _recompute_height(self, p):
        """计算当前节点的高度 h = 1 + max(h_left, h_right)"""
        p._node._height = 1 + max(p._node.left_height(), p._node.right_height())

    def _isbalanced(self, p):
        """判断是否平衡 if |left - right| <= 1"""
        return abs(p._node.left_height() - p._node.right_height()) <= 1

    def _tall_child(self, p, favorleft=False):
        """返回更高的子节点：favorleft = True 代表左闭右开"""
        # favorleft = True 时 left = right 时返回 left
        if p._node.left_height() + (1 if favorleft else 0) > p._node.right_height():
            return self.left(p)
        else:
            return self.right(p)

    def _tall_grandchild(self, p):
        """返回更高的子节点的子节点"""
        child = self._tall_child(p)  # 更高的子节点
        alignment = (child == self.left(p))  # 判断是否左闭
        return self._tall_child(child, alignment)  # 左右相等时偏好方向相同

    def _rebalance(self, p):
        """平衡操作"""
        while p is not None:
            old_height = p._node._height
            if not self._isbalanced(p):
                # TreeMap 方法 trinode 重构
                p = self._restructure(self._tall_grandchild(p))
                # 更新高度
                self._recompute_height(self.left(p))
                self._recompute_height(self.right(p))
            self._recompute_height(p)

            if p._node._height == old_height:  # 无变化 -> 已经平衡
                p = None
            else:
                p = self.parent(p)  # 从 p 节点向上检查平衡性

    # --------------- 平衡操作的钩子函数 ---------------
    def _rebalance_insert(self, p):
        self._rebalance(p)

    def _rebalance_delete(self, p):
        self._rebalance(p)
```
