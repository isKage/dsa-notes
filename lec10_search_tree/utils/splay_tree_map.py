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
