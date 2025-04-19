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
