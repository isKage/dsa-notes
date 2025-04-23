class TreeNode:
    def __init__(self, val=1, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def add_left(self, val):
        new = TreeNode(val)
        if self.left is None:
            self.left = new
        return new

    def add_right(self, val):
        new = TreeNode(val)
        if self.right is None:
            self.right = new
        return new


def DFS_rightSideView(root: TreeNode):
    result = []  # 存放右视图

    def dfs(node, depth):
        if not node:
            return
        if depth == len(result):
            result.append(node.val)  # 最右一个元素

        # 递归
        dfs(node.right, depth + 1)
        dfs(node.left, depth + 1)

    dfs(root, 0)  # 初始 root 根节点
    return result


def BFS_rightSideView(root: TreeNode):
    if not root:
        return []

    result = []  # 存放右视图
    queue = [root]  # 辅助队列

    while queue:  # 队列非空
        size = len(queue)  # 树这一层的节点数
        for i in range(size):
            node = queue.pop(0)  # 头部出队

            if i == size - 1:
                # 最后一个节点：进入右视图结果列表 result
                result.append(node.val)

            # 否则子树进队
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return result


if __name__ == '__main__':
    """
    1
    3 2
    0 4 0 3
    ->
    [1, 2, 3]
    """

    root = TreeNode(1)

    l1 = root.add_left(3)

    l1.add_left(0)
    l1.add_right(4)

    r1 = root.add_right(2)

    r1.add_left(0)
    r1.add_right(3)

    print("=" * 15, "Initial Tree", "=" * 15)
    print(root.val)
    print(root.left.val, root.right.val)
    print(root.left.left.val, root.left.right.val, root.right.left.val, root.right.right.val)

    print("=" * 15, "Right Side View", "=" * 15)

    res = DFS_rightSideView(root)
    print(res)

    res = BFS_rightSideView(root)
    print(res)
