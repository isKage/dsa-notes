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


if __name__ == '__main__':
    lbt = LinkedBinaryTree()
    print(len(lbt))
    print(lbt.root())