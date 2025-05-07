from utils import Graph


def BFS(g: Graph, s: Graph.Vertex, discovered: dict) -> None:
    """
    图 g 中任意顶点 s 的广度优先搜索
    :param g: 图 Graph 类
    :param s: 顶点 Graph.Vertex 类
    :param discovered: 字典, 存储探索结果
    :return: None
    """
    level = [s]  # 第一层, 只有初始顶点 s

    while len(level) > 0:
        next_level = []  # 下一层的顶点集
        for u in level:  # 遍历本层所有点
            for e in g.incident_edges(u):  # 对 u 遍历所有边 e
                v = e.opposite(u)  # 找到边 e 的另一个端点 v
                if v not in discovered:  # 若 v 未标记
                    discovered[v] = e  # 则标记边 e
                    next_level.append(v)  # 且存储点 v

        level = next_level  # 更新当前层


if __name__ == '__main__':
    g = Graph(directed=False)
    A = g.insert_vertex("A")
    B = g.insert_vertex("B")
    C = g.insert_vertex("C")
    D = g.insert_vertex("D")
    E = g.insert_vertex("E")
    F = g.insert_vertex("F")

    AB = g.insert_edge(A, B, "(A, B)")
    AC = g.insert_edge(A, C, "(A, C)")
    AD = g.insert_edge(A, D, "(A, D)")

    BC = g.insert_edge(B, C, "(B, C)")
    CD = g.insert_edge(C, D, "(C, D)")

    BE = g.insert_edge(B, E, "(B, E)")
    CE = g.insert_edge(C, E, "(C, E)")

    CF = g.insert_edge(C, F, "(C, F)")
    DF = g.insert_edge(D, F, "(D, F)")

    discovered = {A: None}
    BFS(g, A, discovered)

    for v, e in discovered.items():
        if e is not None:
            print(f"Vertex {v.element()} : Edge {e.element()}")
        else:
            print(f"Vertex {v.element()} : Initial")
