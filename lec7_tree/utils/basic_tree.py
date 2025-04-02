try:
    from .linked_queue import LinkedQueue
except ImportError:
    from linked_queue import LinkedQueue


class Tree:
    """树的抽象基础类，基础方法需要子类定义"""

    # ---------------- 抽象方法: 节点类 具体实现由子类实现 ----------------
    class Position:
        """每个元素的位置/节点类"""

        def element(self):
            # 由子类定义
            raise NotImplementedError('must be implemented by subclass')

        def __eq__(self, other):
            """比较节点是否相同"""
            # 由子类定义
            raise NotImplementedError('must be implemented by subclass')

        def __ne__(self, other):
            """比较节点是否不同"""
            return not (self == other)

    # ---------------- 抽象方法: 树的抽象基础类 具体实现由子类实现 ----------------
    def root(self):
        """返回根节点"""
        raise NotImplementedError('must be implemented by subclass')

    def parent(self):
        """返回父节点"""
        raise NotImplementedError('must be implemented by subclass')

    def num_children(self, p):
        """返回节点 p 下的子节点数目"""
        raise NotImplementedError('must be implemented by subclass')

    def children(self, p):
        """迭代器方式返回 p 节点的子类"""
        raise NotImplementedError('must be implemented by subclass')

    def __len__(self):
        """树的所有节点数目"""
        raise NotImplementedError('must be implemented by subclass')

    # ---------------- 具体方法: 如果抽象方法被子类定义后 ----------------
    def is_root(self, p):
        """判断 p 节点是否为根节点"""
        return self.root() == p

    def is_leaf(self, p):
        """判断 p 节点是否为叶子节点"""
        return self.num_children(p) == 0

    def is_empty(self):
        """判断树是否为空"""
        return len(self) == 0

    # 计算深度算法
    def depth(self, p):
        """返回节点 p 的深度，即到根节点的路径距离"""
        if self.is_root(p):
            # 根节点深度为 0
            return 0
        else:
            # 递归：当前节点的深度 = 父节点的深度 + 1
            return 1 + self.depth(self.parent(p))

    # 计算高度算法
    def height(self, p):
        """返回节点 p 的高度，即距离其最远叶子节点的路径长"""
        if self.is_root(p):
            # 叶子节点高度为 0
            return 0
        else:
            # 当前节点的高度 = 所有子节点高度最大值 + 1
            return 1 + max(self.height(c) for c in self.children(p))

    # ---------------- 深度优先：前/后序遍历 ----------------
    def __iter__(self):
        """定义迭代器：遍历方式可选"""
        for p in self.positions():  # positions() 可选不同的遍历方式
            yield p.element()

    def positions(self):
        """由子类具体指定 positions 方法"""
        raise NotImplementedError('must be implemented by subclass')

    def preorder(self):
        """前序遍历"""
        raise NotImplementedError('must be implemented by subclass')

    def _subtree_preorder(self, p):
        """前序遍历子树"""
        raise NotImplementedError('must be implemented by subclass')

    def postorder(self):
        """后序遍历"""
        raise NotImplementedError('must be implemented by subclass')

    def _subtree_postorder(self, p):
        """后序遍历子树"""
        raise NotImplementedError('must be implemented by subclass')

    # ---------------- 广度优先：层序遍历 ----------------
    def breadthfirst(self):
        """广度优先：层序遍历"""
        if not self.is_empty():
            fringe = LinkedQueue()  # 队列实现
            fringe.enqueue(self.root())  # 根节点入队

            while not fringe.is_empty():
                p = fringe.dequeue()  # 取出头部
                yield p  # 生成

                for c in self.children(p):  # 将子节点入队
                    fringe.enqueue(c)


if __name__ == '__main__':
    # 仅仅检查是否能运行，虽然实例化没有意义
    t = Tree()
