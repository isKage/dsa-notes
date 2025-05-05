# 搜索树（2）：伸展树、红黑树

上一章介绍了常见的搜索树 [二叉搜索树、平衡搜索树、AVL 树](https://zhuanlan.zhihu.com/p/1896957409303454453) ，它们的主要思想就是尽可能地使树保持平衡属性，高度维持在对数级别从而加快搜索。本章介绍的红黑树继承了这一思想，并进一步完善了一些缺点。除此之外，伸展树给出了新的思路，即完全不考虑树的结构，而是通过把最新访问的节点伸展到根节点来加快搜索。

## 1 伸展树

首先介绍相对简单的**伸展树（splay tree）**——与其他平衡搜索树有显著的不同

- 伸展树的高度没有严格的对数上界
- 伸展树的节点处无需存储额外的高度、平衡或其他辅助信息

**核心：**在伸展树上进行搜索、插入、删除操作后，均需在到达的最后一个节点处进行**伸展（splaying）**操作。直观上，伸展操作使得被频繁操作的节点更靠近树根。

### 1.1 伸展

对某一节点 x 的伸展操作即**通过一系列重构将其移动到根节点**的操作：

根据节点 x 是否有祖父节点及其与父节点及祖父节点（如存在）间的位置关系，可以采用 `zig-zig` 、 `zig-zag` 或 `zig`  重构：

- 有祖父节点时执行 `zig-zig` 或 `zig-zag` （旋转 2 次）

- 没有祖父节点时执行 `zig` （旋转 1 次）

#### 1.1.1 zig-zig 型

zig-zig 型伸展操作：如下图所示，旋转 2 次从而将节点 x 旋转到根节点位置。

![zig-zig 型伸展操作](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1745397643877.png)

#### 1.1.2 zig-zag 型

zig-zag 型伸展操作：如下图所示，旋转 2 次从而将节点 x 旋转到根节点位置。

![zig-zag 型伸展操作](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1745397705908.png)

#### 1.1.3 zig 型

zig 型伸展操作：如下图所示，旋转 1 次从而将节点 x 旋转到根节点位置。

![zig 型伸展操作](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1745397728408.png)


### 1.2 伸展树的操作和伸展

#### 1.2.1 搜索/查看

搜索键 k 时，如果发现键 k 在位置 p ，则伸展 p；否则，在搜索失败的位置伸展叶子节点。

下面的例子展示了一个节点的完整伸展过程：查找到了节点 14 ，伸展 14 一直旋转到根节点。

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1745397996477.png)

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1745398031958.png)

#### 1.2.2 插入

插入键 k 时，在新插入的叶子节点 p 处进行伸展。

例如上面的节点 14 即可以是查找到了 14 伸展 14 ，也可以是插入 14 然后伸展 14 。下面的例子展示了一个从零搭建伸展树的插入过程。

![从零搭建伸展树](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1745398267629.png)

#### 1.2.3 删除

删除键 k 时，在被删除节点的父节点 p 处进行伸展。需要注意的是，如果删除的是度为 2 的节点，则实际上是替换后再删除。则此时伸展的是实际被删除的节点的父节点。

例如下图所示，删除的是度为 2 的节点 8 ，但实际上是用其（中序遍历的）前一个节点替换后，删除前一个节点 w = 7 ，所以在 w = 7 的父节点 p = 6 处进行伸展。

![删除根节点 8 的例子](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1745398384145.png)

### 1.3 Python 实现

继承上一章的 `TreeMap` 类（[TreeMap 的完整代码](https://github.com/isKage/dsa-notes/blob/main/lec10_search_tree/utils/tree_map.py)）。因为伸展树无需存储多余信息，所以不用覆写节点类。最后，伸展树不再需要平衡操作，所有增、删、改、查操作后的平衡操作改为伸展操作。

```python
try:
    from .tree_map import TreeMap
except ImportError:
    from tree_map import TreeMap


class SplayTreeMap(TreeMap):
    """伸展树"""

    # ------------ 不用覆写节点类 ------------
    # 因为伸展树无需存储多余信息

    # ------------ 伸展树操作 ------------
    def _splay(self, p):
        """在 p 点进行伸展，将 p 旋转到根节点"""
        while p != self.root() and p is not None:
            parent = self.parent(p)
            grand = self.parent(parent)

            if grand is None:
                # zig 型，旋转 1 次
                self._rotate(p)
            elif (parent == self.left(grand)) == (p == self.left(parent)):
                # zig-zig 型，在同一边，旋转 2 次
                self._rotate(parent)
                self._rotate(p)
            else:
                # zig-zag 型，在不同边，旋转 2 次
                self._rotate(p)
                self._rotate(p)

    # ------------ 覆写平衡操作的钩子函数 ------------
    # 伸展树不再需要平衡操作，所有增删改查操作后进行伸展即可
    def _rebalance_access(self, p):
        self._splay(p)

    def _rebalance_delete(self, p):
        self._splay(p)

    def _rebalance_insert(self, p):
        self._splay(p)
```

测试：

```python
"""=============== Splay Tree Map ==============="""
splay_tree = SplayTreeMap()
print("=" * 15, "Splay Tree Map", "=" * 15)
splay_tree[1] = 'splay1'
splay_tree[2] = 'splay2'
splay_tree[3] = 'splay3'
splay_tree[4] = 'splay4'
splay_tree[5] = 'splay5'
splay_tree[6] = 'splay6'

print(f"key = 4, value = {splay_tree[4]}\n")
print("from 1 to 4")
for item in splay_tree.find_range(1, 4):
    print(item)

print(f"\nmin = {splay_tree.find_min()}")
print("del key = 1 and 2")
del splay_tree[1]
del splay_tree[2]
print(f"min = {splay_tree.find_min()}")

# =============== Splay Tree Map ===============
# key = 4, value = splay4
# 
# from 1 to 4
# (1, 'splay1')
# (2, 'splay2')
# (3, 'splay3')
# 
# min = (1, 'splay1')
# del key = 1 and 2
# min = (3, 'splay3')
```

### 1.4 算法分析/性能

伸展操作的摊销运行时间为 **O(log n)** ，故搜索、插入、删除的摊销运行时间也为 **O(log n)** 。

优势：

- 无需在节点处存储额外信息，且操作简单。

- 某些情况下运行时间远小于 **O(log n)** ，如当操作经常被操作的节点时。



## 2 红黑树

红黑树依旧继承了“平衡”的思想，但是避免了多次旋转重构的——**红黑树只需要 O(1) 次结构变化就能保持平衡**。

### 2.1 红黑树

从形式上讲，**红黑树**是一棵带有红色和黑色节点的二叉搜索树（不妨设：左小右大），可以理解为一个涂上了“红色”和“黑色”的二叉搜索树，其具有下面的属性：

- 根属性：根节点是黑色的。
- 红色属性：红色节点（如果有的话）的子节点是黑色的。
- 深度属性：具有零个或一个子节点的所有节点都具有相同的黑色深度（被定义为黑色祖先节点的数量）—— 即叶子节点和度为 1 的节点具有同样多的黑色祖先节点数目。

例如下面的例子（白色代表“红色”）：根节点 12 是黑色的，所有红色节点的子节点都是黑色的（例如节点 10）。叶子节点（4、8、6、14）的黑色祖先数目为 3 ，而叶子节点（11、17）的黑色祖先树也为 3 （定义自己是自己的祖先），度为 1 的节点（3、13）的黑色祖先数目也为 3 。

<img src="https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1745402114180.png" alt="红黑树的一个例子" style="zoom:50%;" />

**性质：**对于 n 个节点的红黑树，其高度为 **O(log n)**。

### 2.2 红黑树的操作

#### 2.2.1 搜索/查看

红黑树同时也是二叉搜索树，采用相同的方式查找，因此复杂度为 **O(h) = O(log n)** 。

#### 2.2.2 插入

考虑将 x 插入树 T 中：

1. 如果 T 只有 1 个节点，则 x 插入在根节点的下面，将根节点染为黑色，于是满足根属性；

2. 如果 x 的父节点不是根节点，则将 x 染为红色，则深度属性满足（因为 x 红色不会计算自身黑色深度）：
    - 如果 x 的父节点是黑色，则红色属性不违背；
    - 但当 x 的父节点是红色，由红色属性知产生矛盾！

对于最后一种特殊情况，我们进一步考虑：此时 x 为红色，x 的父节点 y 为红色，则 y 的父节点一定为黑色（否则 y、z 违背红色属性）。此时的情况称为 **双红色** 矛盾：

| z (grand) | y (parent) | x (child) |
| :-------: | :--------: | :-------: |
|   黑色    |    红色    |   红色    |

 **双红色**矛盾： `z -> y -> x` 的 x 和 y 都为红色，矛盾。

**情况 1：y 的兄弟姐妹节点 s 为黑色或空**

对节点 x 进行 trinode 重构操作 `restructure(x)` ：

- 对节点 x ，其父节点 y 和祖先节点 z ，按照从左到右的顺序，暂时重新标记它们为 a 、b 和 c ，以使 a 、 b 和 c 被有序地遍历（a < b < c）。
- 将祖先节点 z 用标记节点 b 取代，使 a 和 c 成为 b 的子节点，并保持次序关系不变。

在进行 `restructure(x)` 的操作后，我们将 b 着色为黑色，将 a 和 c 着色红色。即将三个键从小到大排序为 a < b < c 按照 b 为根，a 在左， c 在右的方式重新构建树，并把 b 染为黑，a、c 染为红。

如下图所示：a) 图展示了 4 中可能情况，经过重构后变为 b) 图的情况。

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1745403817572.png)

**情况 2：y 的兄弟姐妹节点 s 为红色**

重新着色：将 y 和 s 着色为黑色，将其父节点 z 着色为红色（除非z是根节点，在这种情况下，
它仍然是黑色的）。

如此，除非 z 是根节点，通过该树的有影响的部分的任何路径部分恰好是一个黑色节点，无论着色前和着色后。因此，树的黑色深度不被重新着色影响。在 z 是根节点情况下，它增加 1 。

如此双红色矛盾或消失，或转移到 x 的祖父节点 z 上，不断重复进行情况 1 和情况 2 ，总能收敛解决矛盾。

如下图所示：将 z 染红，子节点 y 和 s 染黑即可，然后检查，重复操作即可。

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1745404175639.png)

#### 2.2.3 删除

删除同样与二叉搜索树相同，只是造成的不平衡情况需要的操作方式不同：

1. 如果删除的是红色节点，不影响红黑树结构；
2. 如果删除的是黑色节点，它要么是叶子节点；要么只有一个子节点，且这个子节点一定是红色的叶子节点（否则这条路径上的度为 1 和叶子节点的黑色深度肯定矛盾）：
    - 对于第二种情况，即它有一个红色的叶子节点，只需将其接到祖父节点并染为黑色即可。
    - 对于第一种情况，即删除的是一个黑色的叶子节点，则它的父节点变成了度为 1 或 0 的节点，其黑色深度减一，深度属性矛盾，需要特殊考虑。

如果删除的是一个（非根节点的）黑色叶子节点。可以采用如下操作：

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1745405126928.png)

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1745405176279.png)

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1745405202122.png)

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1745405236407.png)

具体的例子：

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1745405282590.png)

### 2.3 算法分析/性能

**性质：**在一棵 n 个节点的红黑树中插入一项可在 **O(log n)** 的时间内完成，并且需要 **O(log n)** 的重新着色且至多需要 **1** 次的 trinode 重组。

**性质：**在一棵 n 个节点的红黑树中删除一项可在 **O(log n)** 的时间内完成，并且需要 **O(log n)** 的重新着色且至多需要 **2** 次的 trinode 重组。

### 2.4 Python 实现

同样继承自 `TreeMap` 类，需要覆写节点类 `_Node` ，添加红黑属性 `_red: bool` 。且需要重新定义“平衡”操作的钩子函数 `_rebalance_insert()` 和 `_rebalance_delete()` 操作。

```python
try:
    from .tree_map import TreeMap
except ImportError:
    from tree_map import TreeMap


class RedBlackTreeMap(TreeMap):
    """红黑树"""

    # --------------- 覆写节点类：添加红黑属性 ---------------
    class _Node(TreeMap._Node):
        """添加红黑属性"""
        __slots__ = '_red'

        def __init__(self, element, parent=None, left=None, right=None):
            super().__init__(element, parent, left, right)
            self._red = True

    # --------------- 红黑属性操作 ---------------
    def _set_red(self, p):
        p._node._red = True

    def _set_black(self, p):
        p._node._red = False

    def _set_color(self, p, make_red):
        p._node._red = make_red

    def _is_red(self, p):
        return p is not None and p._node._red

    def _is_red_leaf(self, p):
        return self._is_red(p) and self.is_leaf(p)

    def _get_red_child(self, p):
        """返回 p 的红子节点"""
        for child in (self.left(p), self.right(p)):
            if self._is_red(child):
                return child
        return None

    # --------------- 插入 ---------------
    def _rebalance_insert(self, p):
        """覆写插入后的平衡操作"""
        self._resolve_red(p)

    def _resolve_red(self, p):
        """插入新元素后的平衡重构"""
        if self.is_root(p):
            self._set_black(p)  # 根节点为黑
        else:
            parent = self.parent(p)
            if self._is_red(parent):  # 双红矛盾
                uncle = self.sibling(p)
                # 情况 1: x 的父节点 y 的兄弟姐妹节点 s 为黑色或空
                if not self._is_red(uncle):
                    middle = self._restructure(p)  # trinode 重构
                    self._set_black(middle)
                    self._set_red(self.left(middle))
                    self._set_red(self.right(middle))
                # 情况 2: x 的父节点 y 的兄弟姐妹节点 s 为红色
                else:
                    grand = self.parent(parent)
                    self._set_red(grand)
                    self._set_black(self.left(grand))
                    self._set_black(self.right(grand))
                    self._resolve_red(grand)  # 染色后递归

    # --------------- 删除 ---------------
    def _rebalance_delete(self, p):
        """
        覆写删除后的平衡操作
        :param p: 父类 TreeMap 的 delete(p) 方法传入的是父节点 p.parent
        所以父节点 n == 1 代表删除的是叶子节点，对于黑色叶子节点需要特殊考虑 _fix_deficit
        """
        # 1. 根节点
        if len(self) == 1:
            self._set_black(self.root())  # 根节点为黑
        elif p is not None:
            n = self.num_children(p)
            # 2. 度为 1
            if n == 1:
                c = next(self.children(p))
                if not self._is_red_leaf(c):  # 黑色叶子节点被删除
                    self._fix_deficit(p, c)
            # 3. 度为 2
            elif n == 2:  # 被删除的点的父节点度为 2 只要重新染色即可
                if self._is_red_leaf(self.left(p)):
                    self._set_black(self.left(p))
                else:
                    self._set_black(self.right(p))

        # 4. 度为 0 即黑色叶子节点为特殊情况，见函数 _fix_deficit

    def _fix_deficit(self, z, y):
        """z 为父节点，y 为更重子树的子节点"""
        if not self._is_red(y):  # y 为黑，情形 1 和 2
            x = self._get_red_child(y)
            if x is not None:  # 情形 1
                old_color = self._is_red(z)
                middle = self._restructure(x)
                self._set_color(middle, old_color)
                self._set_black(self.left(middle))
                self._set_black(self.right(middle))
            else:  # 情形 2
                self._set_red(y)
                if self._is_red(z):
                    self._set_black(z)
                elif not self.is_root(z):
                    self._fix_deficit(self.parent(z), self.sibling(z))  # 递归
        else:  # 情形 3: y 为红
            self._rotate(y)
            self._set_black(y)
            self._set_red(z)
            if z == self.right(y):
                self._fix_deficit(z, self.left(z))
            else:
                self._fix_deficit(z, self.right(z))
```

测试：

```python
from utils import RedBlackTreeMap

"""=============== Red Black Tree Map ==============="""
red_black_tree = RedBlackTreeMap()
print("=" * 15, "Red Black Tree Map", "=" * 15)
red_black_tree[1] = 'redblack1'
red_black_tree[2] = 'redblack2'
red_black_tree[3] = 'redblack3'
red_black_tree[4] = 'redblack4'
red_black_tree[5] = 'redblack5'
red_black_tree[6] = 'redblack6'

print(f"key = 4, value = {red_black_tree[4]}\n")
print("from 1 to 4")
for item in red_black_tree.find_range(1, 4):
    print(item)

print(f"\nmin = {red_black_tree.find_min()}")
print("del key = 1 and 2")
del red_black_tree[1]
del red_black_tree[2]
print(f"min = {red_black_tree.find_min()}")

# =============== Red Black Tree Map ===============
# key = 4, value = redblack4
# 
# from 1 to 4
# (1, 'redblack1')
# (2, 'redblack2')
# (3, 'redblack3')
# 
# min = (1, 'redblack1')
# del key = 1 and 2
# min = (3, 'redblack3')
```











