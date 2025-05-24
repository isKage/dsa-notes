class ListPartition:
    """基于序列实现的Partition结构（每个组用序列表示）"""

    class Position:
        __slots__ = '_element', '_group', '_size'

        def __init__(self, element, group):
            self._element = element
            self._group = group  # 所属组

        def element(self):
            return self._element

        def __repr__(self):
            return f"Position({self._element})"

    def __init__(self):
        self._groups = []  # 存储所有组的的群组

    def make_group(self, e):
        """创建新组, 包含元素 e"""
        new_group = [None]  # 新组
        p = self.Position(e, new_group)  # 创建 Position 类
        new_group[0] = p  # 加入组中

        self._groups.append(new_group)  # 新组加入到 ListPartition 群组中
        return new_group[0]  # return Position(e)

    def find(self, p):
        """Position 类 p 所属的组"""
        return p._group

    def union(self, group_p, group_q):
        """合并 group_p 和 group_q 这两个组"""
        if group_p is not group_q:  # 如果不在同一组, 则合并
            # 找到更小的组
            if len(group_p) < len(group_q):
                smaller, larger = group_p, group_q
            else:
                smaller, larger = group_q, group_p

            # 更小组的 Position 指向合并后的大组
            for pos in smaller:
                pos._group = larger
            # 加入大组
            larger.extend(smaller)

            # 从群组 _groups 中移除较小的组
            self._groups.remove(smaller)

    def __repr__(self):
        return f"ListPartition({self._groups})"


if __name__ == '__main__':
    P = ListPartition()

    p1 = P.make_group(1)
    p2 = P.make_group(2)
    p3 = P.make_group(3)
    p4 = P.make_group(4)
    p5 = P.make_group(5)
    p6 = P.make_group(6)
    p7 = P.make_group(7)

    print("=" * 15, "Initial Partition", "=" * 15)
    print(P)

    print("=" * 15, "Union p1 and p2, p3 and p4, p5 and p6", "=" * 15)
    grp_p1 = P.find(p1)
    grp_p2 = P.find(p2)
    grp_p3 = P.find(p3)
    grp_p4 = P.find(p4)
    grp_p5 = P.find(p5)
    grp_p6 = P.find(p6)

    P.union(grp_p1, grp_p2)
    P.union(grp_p3, grp_p4)
    P.union(grp_p5, grp_p6)

    print(P)

    print("=" * 15, "Find p1 belong to which Group", "=" * 15)
    print(P.find(p1))
