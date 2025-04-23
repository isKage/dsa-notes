try:
    from .binary_tree import BinaryTree
except ImportError:
    from binary_tree import BinaryTree


class InorderTree(BinaryTree):
    # ---------------- 遍历算法 ----------------
    # 迭代器
    def __iter__(self):
        """定义迭代器：遍历方式可选"""
        for p in self.positions():  # positions() 可选不同的遍历方式
            yield p.element()

    # 前序遍历
    def inorder(self):
        """中序遍历"""
        if not self.is_empty():
            for p in self._subtree_inorder(self.root()):  # 递归实现
                yield p

    def _subtree_inorder(self, p):
        """中序遍历子树"""
        if self.left(p) is not None:  # 遍历左子树
            for other in self._subtree_inorder(self.left(p)):
                yield other
        yield p  # 访问根节点
        if self.right(p) is not None:  # 遍历右子树
            for other in self._subtree_inorder(self.right(p)):
                yield other

    def positions(self):
        """指定遍历方法"""
        return self.inorder()


if __name__ == '__main__':
    # 仅仅检查是否能运行，虽然实例化没有意义
    inorder_tree = InorderTree()
    print(inorder_tree.inorder())
