import math

from utils import Graph
from copy import deepcopy


def floyd_warshall(g: Graph) -> Graph:
    """
    返回图 g 的闭包
    :param g: 图 Graph 类
    :return: 图 g 的闭包 Graph 类
    """
    closure = deepcopy(g)  # 深度拷贝图 g
    verts = list(closure.vertices())  # 图 g 的所有顶点
    n = len(verts)

    for k in range(n):  # 中间顶点 k
        for i in range(n):  # 起始顶点 i

            # 若 i k 相邻 (i, k) is not None
            if i != k and closure.get_edge(verts[i], verts[k]) is not None:
                for j in range(n):  # 终点顶点 j

                    # 若 k j 相邻 (k, j) is not None
                    if i != j != k and closure.get_edge(verts[k], verts[j]) is not None:

                        # 此时 (i, k) (k, j) 均连通, 若 i j 不连通则连边 (i, j)
                        if closure.get_edge(verts[i], verts[j]) is None:
                            closure.insert_edge(verts[i], verts[j])
    return closure


def floyd_warshall_shortest_path(g: Graph) -> dict:
    """
    使用 Floyd-Warshall 算法计算图中所有顶点对的最短路径距离
    :param g: 图 Graph 类
    :return: 返回一个字典 {u: {v: distance}}
    其中 distance 是 u 到 v 的最短距离
    如果 u 和 v 之间不可达 distance = math.inf
    """
    verts = list(g.vertices())  # 获取所有顶点
    n = len(verts)

    # 初始化距离字典, 格式为 dist[u][v] = distance
    dist = {u: {v: math.inf for v in verts} for u in verts}

    # 设置对角线为 0
    for u in verts:
        dist[u][u] = 0

    # 初始化直接相连的边
    for u in verts:
        for v in verts:
            edge = g.get_edge(u, v)
            if edge is not None:
                dist[u][v] = edge.element()

    # Floyd-Warshall 算法
    for k in verts:  # 中间点 k
        for u in verts:  # 起点 u
            for v in verts:  # 终点 v
                # 如果经过 k 的路径更短，则更新
                if dist[u][k] + dist[k][v] < dist[u][v]:
                    dist[u][v] = dist[u][k] + dist[k][v]

    return dist


def print_shortest_paths(g: Graph, shortest_path_dict: dict):
    """打印结果的函数"""
    verts = list(g.vertices())

    # 如果是无向图，按 start < end 输出，避免重复
    if not g.is_directed():
        verts_sorted = sorted(verts, key=lambda x: x.element())  # 按顶点名称排序
        for i in range(len(verts_sorted)):
            start = verts_sorted[i]
            for j in range(i + 1, len(verts_sorted)):
                end = verts_sorted[j]
                distance = shortest_path_dict[start][end]
                print(f"{start.element()} -> {end.element()}: "
                      f"{distance if distance != math.inf else 'No Path'}")

    # 如果是有向图，输出所有可能的 start -> end
    else:
        for start in verts:
            for end in verts:
                if start != end:  # 避免输出自己到自己的情况
                    distance = shortest_path_dict[start][end]
                    print(f"{start.element()} → {end.element()}: "
                          f"{distance if distance != math.inf else 'No Path'}")


if __name__ == '__main__':
    '''
    传递闭包
    '''
    print("=" * 15, "Transitive Closure", "=" * 15)
    g = Graph(directed=True)

    A = g.insert_vertex('A')
    B = g.insert_vertex('B')
    C = g.insert_vertex('C')

    AB = g.insert_edge(A, B)  # A 到 B
    BC = g.insert_edge(B, C)  # B 到 C
    print(f"Before Floyd Warshall: Edge has {g.edge_count()}")

    # 闭包结果应该为: A->B B->C 得到新的边 A->C
    closure = floyd_warshall(g)
    print(f"After Floyd Warshall: Edge has {closure.edge_count()}")
    del g, A, B, C, AB, BC, closure

    '''
    任意 2 点的最短路
    '''
    from math import sqrt

    print("=" * 15, "Shortest Path", "=" * 15)
    g = Graph(directed=False)

    A = g.insert_vertex("A")
    B = g.insert_vertex("B")
    C = g.insert_vertex("C")
    D = g.insert_vertex("D")
    E = g.insert_vertex("E")
    F = g.insert_vertex("F")

    AB = g.insert_edge(A, B, sqrt(5))
    CF = g.insert_edge(C, F, sqrt(5))
    DF = g.insert_edge(D, F, sqrt(5))
    DE = g.insert_edge(D, E, 3)
    BF = g.insert_edge(B, F, sqrt(13))
    AD = g.insert_edge(A, D, sqrt(5))
    AE = g.insert_edge(A, E, 2 * sqrt(5))
    CE = g.insert_edge(C, E, sqrt(13))
    CD = g.insert_edge(C, D, sqrt(10))

    shortest_path_dict = floyd_warshall_shortest_path(g=g)
    print_shortest_paths(g, shortest_path_dict)  # 输出结果
