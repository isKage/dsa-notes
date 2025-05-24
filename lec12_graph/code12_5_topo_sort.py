# 拓扑排序, 检查是否为 DAG 有向非循环图 (即没有有向环)

from utils import Graph


def topological_sort(g: Graph):
    """返回拓扑排序, 即不存在排序在后的点指向排序在前的点
    若存在有向环, 则返回的序列不包含图中所有点
    """
    topo = []  # 按拓扑顺序存储 Vertex 类
    ready = []  # 存储满足条件的点, 即不再影响图的成环性 (栈 stack)
    incount = {}  # 存储每个点的入度, 实时更新

    # 1. 获取所有点, 记录 {Vertex: in-degree}
    for u in g.vertices():
        incount[u] = g.degree(u, False)
        if incount[u] == 0:  # 入度为 0 可以作为起始点, 不受其他影响
            ready.append(u)

    # 2. 对每个点处理, 清空 ready
    while len(ready) > 0:
        u = ready.pop()
        topo.append(u)
        # 获取 u 的邻接点
        for e in g.incident_edges(u):
            v = e.opposite(u)
            incount[v] -= 1  # 前一点已加入 topo 结果, 则 v 度减 1
            if incount[v] == 0:
                ready.append(v)  # 直到此时 v 也成为了"起点"
    return topo


def exist_loop(g: Graph):
    """存在有向环"""
    topo = topological_sort(g)  # [Vertex 类, ]
    all_nodes = g.vertices()  # Vertex 类的迭代器
    return len(topo) != len(all_nodes)


if __name__ == '__main__':
    g = Graph(directed=True)

    V = {}
    for node in ["A", "B", "C", "D", "E", "F", "G", "H"]:
        V[node] = g.insert_vertex(node)

    AC = g.insert_edge(V["A"], V["B"])
    AD = g.insert_edge(V["A"], V["D"])

    BD = g.insert_edge(V["B"], V["D"])
    BF = g.insert_edge(V["B"], V["F"])

    CD = g.insert_edge(V["C"], V["D"])
    CE = g.insert_edge(V["C"], V["E"])
    CH = g.insert_edge(V["C"], V["H"])

    DF = g.insert_edge(V["D"], V["F"])

    EG = g.insert_edge(V["E"], V["G"])

    FG = g.insert_edge(V["F"], V["G"])
    FH = g.insert_edge(V["F"], V["H"])

    GH = g.insert_edge(V["G"], V["H"])

    # HF = g.insert_edge(V["H"], V["F"])  # 成环

    X = g.insert_vertex("X")

    topo_sort = topological_sort(g)
    loop_or_not = exist_loop(g)

    print(topo_sort)
    print(loop_or_not)
