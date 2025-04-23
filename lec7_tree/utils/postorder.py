try:
    from .basic_tree import Tree
except ImportError:
    from basic_tree import Tree


class PostorderTree(Tree):
    # ---------------- 遍历算法 ----------------
    # 迭代器
    def __iter__(self):
        """定义迭代器：遍历方式可选"""
        for p in self.positions():  # positions() 可选不同的遍历方式
            yield p.element()

    # 后序遍历
    def postorder(self):
        """后序遍历"""
        if not self.is_empty():
            for p in self._subtree_postorder(self.root()):  # 开始递归
                yield p

    def _subtree_postorder(self, p):
        """后序遍历子树"""
        for c in self.children(p):  # 后序遍历子树
            for other in self._subtree_postorder(c):
                yield other
        yield p  # 访问根节点

    def positions(self):
        """指定遍历方法"""
        return self.postorder()


if __name__ == '__main__':
    # 仅仅检查是否能运行，虽然实例化没有意义
    postorder_tree = PostorderTree()
    print(postorder_tree)
