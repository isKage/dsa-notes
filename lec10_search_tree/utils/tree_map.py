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

    # --------------- 钩子函数挂钩存根，由子类实现 ---------------
    def _rebalance_insert(self, p):
        pass

    def _rebalance_delete(self, p):
        pass

    def _rebalance_access(self, p):
        pass

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
            self._relink(z, x, make_left_child=(y == z._left))  # x 成为 z 的子节点
        if x == y._left:
            self._relink(y, x._right, make_left_child=True)  # x 右子树成为 y 左子节点
            self._relink(x, y, make_left_child=False)  # y 成为 x 的右子节点
        else:
            self._relink(y, x._left, make_left_child=False)  # x 左子树成为 y 的右子节点
            self._relink(x, y, make_left_child=True)  # y 成为 x 的左子节点

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


if __name__ == '__main__':
    tree = TreeMap()
    print(tree)
