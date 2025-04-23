# 树 Tree & 二叉树 Binary Tree

本章介绍了重要的数据结构：树。并详细讲解了二叉树。包括：树的定义、树的图论性质。并通过 Python 实现了树（基于链表 vs 基于数组），同时分析了时间复杂度。

## 1 树 Tree

### 1.1 树的定义

**树 Tree**是一种将元素分层次存储的抽象数据类型。除了最顶部的元素，每个元素在树中都有一个 *双亲节点* 和零个或者多个 *孩子节点* 。

**正式定义**：通常我们将树 T 定义为存储一系列元素的有限节点集合，这些节点具有 parent-children 关系并且满足如下属性：

- 如果树 T 不为空，则它一定具有一个称为 *根节点* root 的特殊节点，并且该节点没有父节点。
- 每个非根节点 v 都具有唯一的父节点 w ，每个具有父节点 w 的节点都是节点 w 的一个孩子。

### 1.2 相关术语

**根节点** `root` ：只有直接后继，没有先驱节点

**节点** `node` ：树的基本组成单位，包含一个数据元素和指向子树的分支

**节点的度** `degree` ：每个节点拥有的子树的数目

**叶子节点** `leaf` ：度为 0 的节点，也称为**外部节点** `external node`

**分支节点** ：度不为 0 的节点，也称为**内部节点** `internal node`

**孩子节点** `child` ：某个节点的直接后继

**父节点** `parent` ：一个节点是其孩子节点的父节点，也称为双亲节点

**兄弟节点** `sibling` ：具有相同父节点的节点

**边** `edge` ：一对节点 `(u, v)`，u 是 v 的父节点或反之

**路径** `path` ：一条从 `ni` 到 `nj` 的路径，其中任意两个相邻的节点前者是后者的父节点

**祖先节点** `ancestor` ：根节点到某节点的路径上所有的节点都是该节点的祖先节点

**子孙节点** `descendant` ：某节点的所有子树上的节点都是其子孙节点

**树的度** ：树中节点度的最大值

**节点的深度** `depth` ：节点的祖先节点的个数，也称为**层次** `level`

**节点的高度** `height` ：节点的高度是连接它与它的子孙节点中叶子节点的最长路径的长度

**树的高度** ：根节点的高度为树的高度

**有序树/无序树** ：树中节点的子树从左到右安排有序/无序，各子树位置不能/可以交换

**森林** `forest` ：数棵互不相交的树的集合

![树的例子：文件系统](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1742982398986.png)

![树的例子：有序树](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1742982331017.png)

### 1.3 树的图论性质

#### 1.3.1 节点数与度

**树的节点数等于所有节点度的总和加 $1$**
$$
\sum\limits_{i=1}^n\ d_i = n - 1
$$
**证明** 每个节点的度等于后继节点（子节点）的数量；而除了根节点外，每个节点都有一个分支指向它；总的分支数目等于除根节点外所有节点的数目，即 $n - 1$ 。 $\square$

#### 1.3.2 树的第 i 层的节点数

**节点度为 $k$ 的树，第 $i$ 层至多有 $𝑘^i$ 个节点**
$$
n_i \leq k^i
$$
其中 $n_i$ 表示第 $i$ 层层的节点数。

**证明** 第 0 层仅有根节点， $k_0 = 1$ ；假设结论对第 $i - 1$ 层成立，即该层最多有 $k^{i-1}$ 个节点；而根据定义，树的度为节点度的最大值，即第 $i-1$ 层每个节点最多有 $k$ 个后继节点，因此第 $i$ 层至多有 $k \times k^{i-1} = k^i$ 个节点。由归纳法，证毕。 $\square$

#### 1.3.3 树的最大节点数

**度为 $k$ 且高度为 $h$ 的树，至多有 $\dfrac{k^{h+1} - 1}{k - 1}$ 个节点**
$$
n \leq \dfrac{k^{h+1} - 1}{k - 1}
$$
**证明** 由 [性质 1.3.2](####1.3.2 树的度与第 i 层的节点数) 可知，第 $i$ 层最多有 $k^i$ 个节点。则总共节点数不得超过 $\sum\limits_{i=0}^{h}\ k^i = \dfrac{k^{h+1} - 1}{k - 1}$ 。证明完毕。 $\square$

#### 1.3.4 树的最小高度

**节点数为 $n$ 度为 $k$ 的树的高度至少为 $[\log_k\ (n(k-1)+1)] -1$**
$$
h \leq [\log_k\ (n(k-1)+1)] -1
$$
**证明** 要想达到最小高度，则第 $0,\ 1,\ \cdots,\ h - 1$ 层均需尽可能多地存储节点；由 [性质 1.3.3](####1.3.3 树的最大节点数) 可知
$$
\dfrac{k^{h} - 1}{k - 1}< n \leq \dfrac{k^{h+1} - 1}{k - 1}
$$
变换可得 $h \leq [\log_k\ (n(k-1)+1)] -1$ 。证毕。 $\square$

### 1.4 树的抽象数据类型 ADT

树中的节点 ADT 仅支持一个方法：

- `p.element()` : 返回存储在节点p处的元素

树的基础抽象数据类型 ADT：

```python
ADT Tree {
	数据对象: T
	基本操作
        T.root()			: 返回树 T 的根节点，如 T 为空则返回 None
        T.parent(p)			: 返回 p 的父节点，如 p 为根节点则返回 None
        T.children(p)		: 产生 p 的孩子节点的迭代器
        T.num_children(p)	: 返回 p 的孩子节点的数目
        T.is_root(p)		: 如 p 为 T 的根，则返回 True
        T.is_leaf(p)		: 如 p 为树 T 的叶子节点，则返回 True
        T.depth(p)			: 返回树 T 中 p 节点的深度
        T.height(p)			: 返回树 T 中 p 节点的高度
        T.is_empty()		: 如 T 为空树则返回 True
        len(T)				: 返回树 T 中元素（节点）个数
        T.nodes()			: 生成树 T 所有节点的迭代器
        iter(T)				: 生成树 T 中存储的所有元素的迭代
} ADT Tree
```

### 1.5 树的基类 Python 实现

#### 1.5.1 抽象类的实现

下面实现树的基础抽象类：其中内嵌了节点类 `Position` 。同时，此处只定义了方法名，并没有具体定义，具体定义需要子类继承时具体定义（针对不同类型的树，子类定义方式不同）。

特别地，基于暂时没有具体定义的抽象方法，具体定义了一些树的通用方法 `is_root()` `is_leaf()` `is_empty()` `depth()` `height()`

```python
class Tree:
    """树的抽象基础类，基础方法需要子类定义"""

    # ---------------- 抽象方法: 节点类 具体实现由子类实现 ----------------
    class Position:
        """每个元素的位置/节点类"""

        def element(self):
            # 由子类定义
            raise NotImplementedError('must be implemented by subclass')

        def __eq__(self, other):
            """比较节点是否相同"""
            # 由子类定义
            raise NotImplementedError('must be implemented by subclass')

        def __ne__(self, other):
            """比较节点是否不同"""
            return not (self == other)

    # ---------------- 抽象方法: 树的抽象基础类 具体实现由子类实现 ----------------
    def root(self):
        """返回根节点"""
        raise NotImplementedError('must be implemented by subclass')

    def parent(self):
        """返回父节点"""
        raise NotImplementedError('must be implemented by subclass')

    def num_children(self, p):
        """返回节点 p 下的子节点数目"""
        raise NotImplementedError('must be implemented by subclass')

    def children(self, p):
        """迭代器方式返回 p 节点的子类"""
        raise NotImplementedError('must be implemented by subclass')

    def __len__(self):
        """树的所有节点数目"""
        raise NotImplementedError('must be implemented by subclass')

    # ---------------- 具体方法: 如果抽象方法被子类定义后 ----------------
    def is_root(self, p):
        """判断 p 节点是否为根节点"""
        return self.root() == p

    def is_leaf(self, p):
        """判断 p 节点是否为叶子节点"""
        return self.num_children(p) == 0

    def is_empty(self):
        """判断树是否为空"""
        return len(self) == 0

    # 计算深度算法
    def depth(self, p):
        """返回节点 p 的深度，即到根节点的路径距离"""
        if self.is_root(p):
            # 根节点深度为 0
            return 0
        else:
            # 递归：当前节点的深度 = 父节点的深度 + 1
            return 1 + self.depth(self.parent(p))

    # 计算高度算法
    def height(self, p):
        """返回节点 p 的高度，即距离其最远叶子节点的路径长"""
        if self.is_root(p):
            # 叶子节点高度为 0
            return 0
        else:
            # 当前节点的高度 = 所有子节点高度最大值 + 1
            return 1 + max(self.height(c) for c in self.children(p))
```

#### 1.5.2 递归计算深度和高度

**计算深度**：根据树中节点的深度的定义，节点的祖先节点的个数即为深度，故可以使用**递归**的方式计算深度：

- 如果 `p` 为根节点，则其深度为 `0`
- 否则，`p` 的深度为其父节点的深度加 `1`

**时间复杂度**：对于位置 `p` ，计算深度的复杂度为 $O(d_p + 1)$ ，其中 $d_p$ 指的是节点 `p` 的深度，因为该算法对于p的每个祖先节点执行的时间是常数。最坏的情况下运行时间为 $O(n)$ 。其中n是树中节点的总个数。

```python
# 计算深度算法
def depth(self, p):
    """返回节点 p 的深度，即到根节点的路径距离"""
    if self.is_root(p):
        # 根节点深度为 0
        return 0
    else:
        # 递归：当前节点的深度 = 父节点的深度 + 1
        return 1 + self.depth(self.parent(p))
```



**计算高度**：根据树中节点的高度的定义，连接它与它的子孙节点中叶子节点的最长路径的长度即为高度，故可以使用**递归**的方式计算高度：

- 如果 `p` 为叶子节点，则其高度为 `0`
- 否则，`p` 的高度为其孩子节点中最大的高度加 `1`

**时间复杂度**：如以 `p` 为根节点的子树有 $n_p$ 个节点，则时间复杂度为 $O(n_p)$ 。

```python
# 计算高度算法
def height(self, p):
    """返回节点 p 的高度，即距离其最远叶子节点的路径长"""
    if self.is_root(p):
        # 叶子节点高度为 0
        return 0
    else:
        # 当前节点的高度 = 所有子节点高度最大值 + 1
        return 1 + max(self.height(c) for c in self.children(p))
```



## 2 二叉树 Binary Tree

### 2.1 二叉树的定义

**二叉树**：是具有以下属性的有序树

- 每个节点最多有两个孩子节点。
- 每个孩子节点被命名为左孩子或右孩子。
- 对于每个节点的孩子节点，在顺序上，左孩子先于右孩子。

**二叉树的递归定义**：二叉树或为空树，或满足以下**任一条件**：

- 为一个单独的节点
- 根节点有至多两个有序的孩子节点，且根节点的子树也为二叉树

### 2.2 二叉树的例子

**算式表达树**

二叉树能用于表示算术表达式

- 内部节点：存储操作符
- 叶子节点：存储变量或常数

<img src="https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1742994629723.png" alt="算式表达树" style="zoom:50%;" />

**决策树**

二叉树可以用来描述决策过程

- 内部节点：存储一个回答为“是”或“否”的问题
- 叶子节点：存储决策

<img src="https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1742994742939.png" alt="提供投资决策的决策树" style="zoom:50%;" />

**搜索树**

二叉树可存储有序序列，并使用此二叉树进行搜索

- 节点：存储元素
- 节点左子树（右子树）的元素均小于（大于）节点存储的元素

![实线为搜索36（成功），虚线为搜索70（不成功）](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1742994851160.png)

### 2.3 二叉树的图论性质

记 $n$ 表示二叉树的节点总数； $n_E$ 表示二叉树的叶子节点数目； $n_I$ 表示二叉树的内部节点数目； $h$ 表示二叉树的高度。

#### 2.3.1 基于树的性质

因为二叉树的每个节点的度最多为 2 ，所以基于树的性质可以推出：

**第 $i$ 层至多有 $2^i$ 个节点**

**二叉树的节点总数满足 $h + 1 \leq n \leq 2^{h+1} - 1$** 

**二叉树的高度满足 $h \leq [\log_k\ (n+1)] -1$**

**二叉树叶子节点数目满足 $1 \leq n_E \leq 2^h$** ：叶子节点最少，当整个二叉树为链式结构时成立，此时只有最后一个叶子节点；叶子节点最多，则对于高度 $h$ 的二叉树，每一个节点都是度为 2 ，最后有 $2^h$ 个叶子节点。

**二叉树内部节点数目满足 $h \leq n_I \leq 2^h - 1$** ：内部节点最少，当整个二叉树为链式结构时成立，此时内部节点即为链长 $h$ ；内部节点最多，与叶子节点最多情况相同，排除根节点，所以为 $2^h - 1$ 个。

#### 2.3.2 二叉树独有性质

**对任何非空二叉树，设叶子节点数为 $n_0$，度为 2 的节点数为 $n_2$ ，则有：$n_0 = n_2 + 1$**

**证法1** 设二叉树中度为 1 度节点个数为 $n_1$ ，则有 $n = n_0 + n_1 + n+2$ 。

根据树的 [性质 1.3.1](####1.3.1 节点数与度) ，有 $n = 0 \times n_0 + 1 \times n_1 + 2 \times n_2 = n_1 + 2n_2$ 。

比较以上两式，可得 $n_0 = n_2 + 1$ 。证明完毕 $\square$

**证法2** 我们从树中取下一个（任意的）外部节点 w 和其父节点 v ，v 为内部节点。若 v 有父节点 u ，则将 u 与 w 之前的兄弟节点 z 连接起来，如图所示。

重复上述操作，我们最后将会得到仅有一个节点（根节点）的最终树。

每次操作，叶子节点数目减一；度为 2 的节点数目减一。最后剩下根节点一个孤点（可视作叶子节点），所以 $n_0 = n_2 + 1$ 。证明完毕 $\square$

![归纳过程的变换](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1742998908752.png)

### 2.4 二叉树的类别

**完美二叉树 Perfect Binary Tree** ：高度为 $h$ 且有恰好有 $2^{h+1}-1$ 个节点的二叉树，称为完美二叉树或满二叉树。

**完全二叉树 Complete Binary Tree** ：高度为 $h$ 的完全二叉树，除第 $h$ 层外其他各层结点数均达到最大值 $2^i$ ；第 $h$ 层元素尽可能存放在左侧的节点中，使得若某节点右子树高度为 $l$ ，则其左子树高度为 $l$ 或 $l+1$ 。

**完满二叉树 Full Binary Tree** ：也称为 Proper Binary Tree，所有内部节点度均为 2（均有两个孩子）的二叉树。

![三种二叉树](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/tree.png)

### 2.5 二叉树的抽象数据类型 ADT

二叉树的 ADT 是对树的 ADT 的拓展，它**继承了树的 ADT 的所有基本操作**，并附加了以下操作：

```python
		T.left(p)			: 返回 p 的左孩子节点，若没有则返回 None
		T.right(p)			: 返回 p 的右孩子节点，若没有则返回 None
		T.sibling(p)		: 返回 p 的兄弟节点，若没有则返回 None
```

### 2.6 二叉树新增方法的 Python 实现

```python
try:
    from .basic_tree import Tree
except ImportError:
    from basic_tree import Tree


class BinaryTree(Tree):
    """二叉树的抽象基类，继承 Tree，一些方法暂不定义"""

    # ---------------- 新增的抽象方法: 具体实现由子类实现 ----------------
    def left(self, p):
        """返回当前节点 p 的左孩子节点"""
        raise NotImplementedError('must be implemented by subclass')

    def right(self, p):
        """返回当前节点 p 的右孩子节点"""
        raise NotImplementedError('must be implemented by subclass')

    # ---------------- 具体方法: 如果抽象方法被子类定义后 ----------------
    def sibling(self, p):
        """返回当前节点 p 的兄弟节点"""
        parent = self.parent(p)  # 获取父节点
        if parent is None:
            # 根节点无兄弟节点
            return None
        else:
            # 非左即右
            if p == self.left(parent):
                return self.right(parent)
            else:
                return self.left(parent)

    def children(self, p):
        """以迭代器的方式返回子节点（先左后右）"""
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)
```



## 3 树的实际实现

之前定义的 `Tree` 和 `BinaryTree` 类都只是形式上的抽象基类。尽管给出了许多支持操作，但它们都不能直接被实例化。

特别地，具体实现树要能提供 `Root`、`parent`、`num_children`、`children` 和 `__len__` 这些方法，对于 Binary Tree 类，还要提供 `left` 和 `right` 方法。

我们可以采用**链式结构**存储树，也可采用**数组**存储树。下面基于二叉树的实现介绍：

### 3.1 基于链表：链式存储结构

目标：定义 `BinaryTree` 类的一个具体子类 `LinkedBinaryTree` ，该类能够实现二叉树 ADT。

#### 3.1.1 思路

定义一个简单、非公开的 `_Node` 类表示一个节点，再定义一个公开的 `Position` 类用于封装节点。

一个节点存储以下信息：

- 元素值
- 指向父节点的指针
- 指向左孩子的指针
- 指向右孩子的指针

![二叉树链式结构的图示](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1743054428079.png)

#### 3.1.2 Python 实现

```python
try:
    from .binary_tree import BinaryTree
except ImportError:
    from binary_tree import BinaryTree


class LinkedBinaryTree(BinaryTree):
    """链式结构的二叉树"""

    # ---------------- 非公开节点类 ----------------
    class _Node:
        """非公开节点类"""
        __slots__ = '_element', '_parent', '_left', '_right'

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    # ---------------- 公有的节点类 ----------------
    class Position(BinaryTree.Position):
        """覆写父类 BinaryTree 的显式节点类"""

        def __init__(self, container, node):
            """具体初始化"""
            self._container = container  # 标记属于的树
            self._node = node

        def element(self):
            """具体实现返回元素值"""
            return self._node._element

        def __eq__(self, other):
            """具体实现 =="""
            return type(other) is type(self) and other._node is self._node

    # ---------------- 封装公有节点类 Position ----------------
    def _validate(self, p):
        """在封装 Position 类前判断节点 p 是否合法"""
        if not isinstance(p, self.Position):
            # 不是合法的节点类
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            # 不属于当前树
            raise ValueError('p does not belong to this container')
        if p._node._parent is p._node:
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self, node):
        """根据接受的节点类 _Node 封装为一个 Position 类"""
        if node is not None:
            return self.Position(self, node)
        else:
            return None

    # ---------------- 二叉树具体实现 ----------------
    def __init__(self):
        """初始化一个空的二叉树"""
        self._root = None
        self._size = 0

    # ---------------- 二叉树公有方法具体实现：覆写父类方法 ----------------
    def __len__(self):
        """返回树的节点总数"""
        return self._size

    def root(self):
        """返回根节点"""
        return self._make_position(self._root)  # 返回 self.Position 类

    def parent(self, p):
        """返回父节点"""
        node = self._validate(p)  # 判断合法并返回合法对象
        return self._make_position(node._parent)  # 封装为 Position 返回

    def left(self, p):
        """返回左子节点"""
        node = self._validate(p)
        return self._make_position(node._left)

    def right(self, p):
        """返回右子节点"""
        node = self._validate(p)
        return self._make_position(node._right)

    def num_children(self, p):
        """返回孩子节点数目"""
        node = self._validate(p)
        count = 0
        if node._left is not None:
            count += 1
        if node._right is not None:
            count += 1
        return count

    # ---------------- 二叉树非公有方法具体实现：一些对树的操作 ----------------
    def _add_root(self, e):
        """填入根元素，并返回封装后的 Position 类"""
        if self._root is not None:
            raise ValueError('Root exists')

        self._size = 1
        self._root = self._Node(e)  # 创建节点
        return self._make_position(self._root)  # 封装返回

    def _add_left(self, p, e):
        """在节点 p 下加左子节点，并返回封装后的类"""
        node = self._validate(p)  # 判断是否合法

        if node._left is not None:
            raise ValueError('Left node exists')

        self._size += 1
        node._left = self._Node(e, parent=node)  # 父节点为 node
        return self._make_position(node._left)

    def _add_right(self, p, e):
        """在节点 p 下加右子节点，并返回封装后的类"""
        node = self._validate(p)
        if node._right is not None:
            raise ValueError('Right node exists')
        self._size += 1
        node._right = self._Node(e, parent=node)
        return self._make_position(node._right)

    def _replace(self, p, e):
        """替换节点 p 的元素值，并返回旧元素"""
        node = self._validate(p)
        old = node._element
        node._element = e
        return old

    def _delete(self, p):
        """删除节点 p 用其孩子替代。当 p 非法或有两个孩子则报错"""
        node = self._validate(p)  # p 非法与否

        if self.num_children(p) == 2:  # p 有 2 个孩子
            raise ValueError('p has two children')

        # 取 p 的孩子节点
        child = node._left if node._left is not None else node._right

        if child is not None:
            # 子节点连接父节点的父节点
            child._parent = node._parent
        if node is self._root:
            # 父节点为根节点则子节点成为新根节点
            self._root = child
        else:
            # 更新父节点的父节点的孩子节点
            parent = node._parent
            if node is parent._left:
                parent._left = child
            else:
                parent._right = child
        self._size -= 1  # 节点数减一
        node._parent = node  # 惯例：self.parent -> self
        return node._element

    def _attach(self, p, t1, t2):
        """将子树 t1, t2 作为 p 的左右子节点连入树"""
        node = self._validate(p)
        if not self.is_leaf(p):
            raise ValueError('position must be leaf')
        if not type(self) is type(t1) is type(t2):  # 三个树类型必须相同
            raise TypeError('Tree types must match')

        self._size += len(t1) + len(t2)  # 更新节点数
        if not t1.is_empty():
            t1._root._parent = node
            node._left = t1._root
            t1._root = None
            t1._size = 0
        if not t2.is_empty():
            t2._root._parent = node
            node._right = t2._root
            t2._root = None
            t2._size = 0
```

#### 3.1.3 算法分析

- `len` 方法：在 LinkedBinaryTree 内部实现，使用一个实例变量 `self._size` 存储T的节点数，花费 `O(1)` 的时间。

- `is_empty` 方法：继承自 Tree 类，对 `len` 方法进行一次调用，因此需要花费 `O(1)` 的时间。

- 访问方法 `root`、`left`、`right`、`parent` 和 `num_children` ：直接在 LinkedBinaryTree 中执行，花费 `O(1)` 的时间。
- `sibling` 和 `children` 方法：从 BinaryTree 类派生，对其他访问方法做固定次的调用，因此，它们的运行时间也是 `O(1)` 。
- Tree 类的 `is_ root` 和 `is_leaf` 方法：都运行 `O(1)` 的时间，因为 `is_root` 调用 `root` 方法，之后判定两者的位置是否相等；而 `is_leaf` 调用 `left` 和 `right` 方法，并验证二者是否返回 `None` 。
- `depth` 和 `height` 方法：见 [1.5.2 递归计算深度和高度](####1.5.2 递归计算深度和高度) 。
- 各种更新方法 `add_root`、`add_left`、`add_right`、`replace`、`delete` 和 `attach` ：都运行 `O(1)` 的时间，因为它们每次操作都仅仅重新链接到固定的节点数。

![链式结构的二叉树时间复杂度](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1743059677999.png)

### 3.2 基于数组：数组实现二叉树

二叉树 T 的一种可供选择的表示法是对 T 的位置进行编号。对于 T 的每个位置 p ，设 f(p) 为整数且定义如下：

- 若 p 是 T 的根节点，则 `f(p) = 0`
- 若 p 是位置 q 的左孩子，则 `f(p) = 2 * f(q) + 1`
- 若 p 是位置 q 的右孩子，则 `f(p) = 2 * f(q) + 2`
- 而 p 的父节点的编号为 `(f(p) - 1) / 2`

编号函数 `f` 被称二叉树 T 的位置的**层编号**，因为它将 T 每一层的位置从左往右按递增顺序编号。

#### 3.2.1 思路

层编号函数 `f` 是一种二叉树 T 依据基于数组结构 A（例如，Python 列表）的表示方法，**T 的 p 位置元素存储在数组下标为 `f(p)` 的内存中**。

注意，层编号是基于树内的潜在位置，而不是所给树的实际位置，因此编号不一定是连续的。

<img src="https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1743060184180.png" alt="数组存储树的示例" style="zoom:67%;" />

#### 3.2.2 算法分析/缺点

- 空间使用极大依赖于树的形状，在二叉树为完全二叉树时效率最高；最坏情况下数组长度 N 与节点数 n 有 $N = 2^n - 1$ 的关系
- 删除、插入等更新操作花费时间为 $O(n)$

### 3.3 一般树的链式结构

对于一般的树结构，`parent` 父节点唯一，没有变化；`element` 元素存储也大致相同；唯一不同的是子节点可以是多个，可以通过**存储一个指向指针数组的指针**来实现指向多个子节点。

![一般树的链式结构](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1743060645944.png)

**算法分析**

![一般树链式结构的时间复杂度](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1743060700401.png)













