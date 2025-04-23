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
