try:
    from .basic_tree import Tree
except ImportError:
    from basic_tree import Tree


class PreorderTree(Tree):
    # ---------------- 遍历算法 ----------------
    # 迭代器
    def __iter__(self):
        """定义迭代器：遍历方式可选"""
        for p in self.positions():  # positions() 可选不同的遍历方式
            yield p.element()

    # 前序遍历
    def preorder(self):
        """前序遍历"""
        if not self.is_empty():
            for p in self._subtree_preorder(self.root()):  # 递归实现
                yield p

    def _subtree_preorder(self, p):
        """前序遍历子树"""
        yield p  # 访问根节点
        for c in self.children(p):  # 遍历子树
            for other in self._subtree_preorder(c):
                yield other

    def positions(self):
        """指定遍历方法"""
        return self.preorder()


if __name__ == '__main__':
    # 仅仅检查是否能运行，虽然实例化没有意义
    preorder_tree = PreorderTree()
    print(preorder_tree)
