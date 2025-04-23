def preorder_indent(T, p, d):
    """前序遍历：打印目录
    :param T: 目录树
    :param p: 当前节点
    :param d: 记录深度
    """
    print(2 * d * ' ' + str(p.element()))  # 记录深度
    for c in T.children(p):
        preorder_indent(T, c, d + 1)  # 递归打印子树


def disk_space(T, p):
    """计算文件系统树，p 节点后的总磁盘空间
    :param T: 文件系统树
    :param p: 当前节点
    """
    subtotal = p.element().space()  # 节点 p 占有的空间
    for c in T.children(p):  # 计算 p 的子树总空间
        subtotal += disk_space(T, c)  # 递归计算子树空间
    return subtotal
