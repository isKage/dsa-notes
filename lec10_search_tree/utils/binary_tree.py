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

    # ---------------- 深度优先：二叉树的中序遍历 ----------------
    def __iter__(self):
        """定义迭代器：遍历方式可选"""
        for p in self.positions():  # positions() 可选不同的遍历方式
            yield p.element()

    def positions(self):
        """由子类具体指定 positions 方法"""
        raise NotImplementedError('must be implemented by subclass')

    def inorder(self):
        """中序遍历"""
        raise NotImplementedError('must be implemented by subclass')

    def _subtree_inorder(self, p):
        """中序遍历子树"""
        raise NotImplementedError('must be implemented by subclass')


if __name__ == '__main__':
    # 仅仅检查是否能运行，虽然实例化没有意义
    bt = BinaryTree()
