from utils import Graph


def DFS(g: Graph, u: Graph.Vertex, discovered: dict) -> None:
    """
    图 g 中任意顶点 u 的深度优先搜索
    :param g: 图 Graph 类
    :param u: 顶点 Graph.Vertex 类
    :param discovered: 字典, 存储探索结果
    :return: None
    """
    for e in g.incident_edges(u):  # 经过顶点 u 的所有边 e
        v = e.opposite(u)  # 获取 e 非 u 的顶点 v
        if v not in discovered:  # 顶点 v 未被访问
            discovered[v] = e  # 标记边 e 为 discovery; 同时标记点 v 访问过
            DFS(g, v, discovered)  # 从 v 继续递归探索


def construct_path(u: Graph.Vertex, v: Graph.Vertex, discovered: dict) -> list:
    """
    返回从点 u 到 v 的路径
    :param u: 起始顶点 Graph.Vertex 类
    :param v: 终止顶点 Graph.Vertex 类
    :param discovered: 字典, 存储路径 (依赖于从 点 u 开始的 DFS 遍历结果的 discovered)
    :return: 路径 Python.list 类
    """
    path = []  # 存储路径

    if v in discovered:  # 开始从终点 v 向前探索, 回到 u
        path.append(v.element())
        walk = v
        while walk is not u:
            e = discovered[walk]  # 获取到点 walk 的边 e = (?, walk)
            parent = e.opposite(walk)  # 获取路径上 walk 的上一个点 ?
            path.append(parent.element())  # 加入路径
            walk = parent  # 继续向前

        path.reverse()  # 最终路径逆转就是 u -> v
    return path


if __name__ == '__main__':
    g = Graph(directed=False)
    v1 = g.insert_vertex(1)
    v2 = g.insert_vertex(2)
    v3 = g.insert_vertex(3)
    v4 = g.insert_vertex(4)

    e12 = g.insert_edge(v1, v2, "(1, 2)")
    e23 = g.insert_edge(v2, v3, "(2, 3)")
    e34 = g.insert_edge(v3, v4, "(3, 4)")
    e14 = g.insert_edge(v4, v1, "(1, 4)")
    e24 = g.insert_edge(v2, v4, "(2, 4)")
    e13 = g.insert_edge(v1, v3, "(1, 3)")

    discovered = {v1: None}
    DFS(g, v1, discovered)

    print("=" * 15, "DFS path: from one vertex", "=" * 15)
    for v, e in discovered.items():
        if e is not None:
            print(f"Vertex {v.element()} : Edge {e.element()}")
        else:
            print(f"Vertex {v.element()} : Initial")

    print("=" * 15, "DFS path: from one vertex to another", "=" * 15)
    path = construct_path(v2, v4, discovered)  # 使用之前的 DFS(g, v1, discovered) 的 discovered 结果
    print(f"From v2 to v4: {path}")
