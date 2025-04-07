"""
利用哨兵节点 _sentinel 简化 _delete 方法
"""


class BinaryTree:
    # ---------- nested class: _Node ----------
    class _Node:
        __slots__ = '_element', '_parent', '_left', '_right'

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

        def element(self):
            return self._element

    # ---------------- 二叉树公有方法具体实现 ----------------
    def __init__(self):
        """初始化，哨兵节点"""
        self._sentinel = self._Node(None)  # 哨兵节点
        self._size = 0

    def __len__(self):
        """节点数"""
        return self._size

    def is_empty(self):
        """是否为空"""
        return self._size == 0

    def root(self):
        """返回根节点"""
        return self._sentinel._left  # 哨兵节点的左子节点

    def parent(self, p):
        """返回父节点"""
        if isinstance(p, self._Node):
            return p._parent
        else:
            raise TypeError('p must be proper _Node type')

    def left(self, p):
        """返回左子节点"""
        if isinstance(p, self._Node):
            return p._left
        else:
            raise TypeError('p must be proper _Node type')

    def right(self, p):
        """返回右子节点"""
        if isinstance(p, self._Node):
            return p._right
        else:
            raise TypeError('p must be proper _Node type')

    def num_children(self, p):
        """返回孩子节点数目"""
        if not isinstance(p, self._Node):
            raise TypeError('p must be proper _Node type')

        count = 0
        if p._left is not None:
            count += 1
        if p._right is not None:
            count += 1
        return count

    def add_root(self, e):
        return self._add_root(e)

    def add_left(self, p, e):
        return self._add_left(p, e)

    def add_right(self, p, e):
        return self._add_right(p, e)

    def delete(self, p):
        return self._delete(p)

    # ---------------- 二叉树非公有方法具体实现：一些对树的操作 ----------------
    def _add_root(self, e):
        """填入根元素，并返回封装后的 _Node 类"""
        if self._sentinel._left is not None:
            raise ValueError('Root exists')

        self._size = 1
        self._sentinel._left = self._Node(e, parent=self._sentinel)  # 创建节点
        return self._sentinel._left  # 封装返回

    def _add_left(self, p, e):
        """在节点 p 下加左子节点，并返回封装后的类"""
        if not isinstance(p, self._Node):
            raise TypeError('p must be proper _Node type')

        if p._left is not None:
            raise ValueError('Left node exists')

        self._size += 1
        p._left = self._Node(e, parent=p)  # 父节点为 node
        return p._left

    def _add_right(self, p, e):
        """在节点 p 下加右子节点，并返回封装后的类"""
        if not isinstance(p, self._Node):
            raise TypeError('p must be proper _Node type')

        if p._right is not None:
            raise ValueError('Right node exists')

        self._size += 1
        p._right = self._Node(e, parent=p)
        return p._right

    def _replace(self, p, e):
        """替换节点 p 的元素值，并返回旧元素"""
        if not isinstance(p, self._Node):
            raise TypeError('p must be proper _Node type')

        old = p._element
        p._element = e
        return old

    # ==================== 覆写 _delete 方法 ====================
    def _delete(self, p):
        """删除节点 p 用其孩子替代。当 p 非法或有两个孩子则报错"""
        if not isinstance(p, self._Node):  # p is not valid
            raise TypeError('p must be proper _Node type')

        if self.num_children(p) == 2:  # p 有 2 个孩子
            raise ValueError('p has two children')

        # 取 p 的孩子节点
        child = p._left if p._left is not None else p._right

        if child is not None:  # [这一步无需判断 p 是否为根节点]
            # 子节点连接父节点的父节点
            child._parent = p._parent  # 根节点的父节点为哨兵节点

        # 更新父节点的父节点的孩子节点
        parent = p._parent
        if p is parent._left:
            parent._left = child
        else:
            parent._right = child

        self._size -= 1  # 节点数减一
        p._parent = p  # p 被删除，惯例：self.parent -> self
        return p._element
    # ==========================================================


if __name__ == '__main__':
    #   _sentinel
    #      /
    #     0
    #    / \
    #   1   2
    #  / \   \
    # 3   4   5

    tree = BinaryTree()

    root = tree.add_root(0)

    left1 = tree.add_left(root, 1)
    right1 = tree.add_right(root, 2)

    left2left = tree.add_left(left1, 3)
    left2right = tree.add_right(left1, 4)

    right2 = tree.add_left(right1, 5)

    print(tree.delete(right1))  # 2
    print(tree.delete(right2))  # 5
    print(tree.delete(root))  # 0

    # _sentinel
    #    /
    #   1
    #  / \
    # 3   4

    print(tree.root().element())  # 1
