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


def pruneTree(root: TreeNode):
    def should_prune(node: TreeNode):
        if not node:
            return False

        # 处理左子树
        left_prune = should_prune(node.left)  # 递归查看是否能剪枝
        if left_prune:
            node.left = None  # 剪去

        # 处理右子树
        right_prune = should_prune(node.right)  # 递归查看是否能剪枝
        if right_prune:
            node.right = None  # 剪去

        # 判断当前节点是否可以被剪掉
        return node.val == 0 and node.left is None and node.right is None

    if should_prune(root):
        return None  # root 也被剪去

    return root


if __name__ == '__main__':
    """
    1
    0 1
    0 0 0 1
    ->
    1
    1
    1
    """

    root = TreeNode(1)

    l1 = root.add_left(0)

    l1.add_left(0)
    l1.add_right(0)

    r1 = root.add_right(1)

    r1.add_left(0)
    r1.add_right(1)

    print("=" * 15, "Before Prune", "=" * 15)

    print(root.val)
    print(root.left.val, root.right.val)
    print(root.left.left.val, root.left.right.val, root.right.left.val, root.right.right.val)

    print("=" * 15, "After pruning", "=" * 15)

    root = pruneTree(root)
    print(root.val)
    print(root.right.val)
    print(root.right.right.val)
