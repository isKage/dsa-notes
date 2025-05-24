from utils import Graph, Partition, ListPartition, HeapPriorityQueue


def MST_Kruskal(g):
    """最小生成树 Kruskal 算法"""
    tree = []  # 最小生成树的边序列
    pq = HeapPriorityQueue()  # 优先级队列 key = edge's weight
    forest = Partition()  # 集群管理
    position = {}  # {Vertex: Partition}

    for v in g.vertices():
        position[v] = forest.make_group(v)  # 每个点建群
    for e in g.edges():
        pq.add(e.element(), e)  # 存储所有边 key = edge's weight

    size = g.vertex_count()
    while len(tree) != size - 1 and not pq.is_empty():
        weight, edge = pq.remove_min()  # 最小权重边
        u, v = edge.endpoints()
        a = forest.find(position[u])
        b = forest.find(position[v])
        if a != b:
            tree.append(edge)  # 边加入最小生成树
            forest.union(a, b)  # 合并群
    return tree


if __name__ == '__main__':
    g = Graph()

    A = g.insert_vertex("A")
    B = g.insert_vertex("B")
    C = g.insert_vertex("C")
    D = g.insert_vertex("D")
    E = g.insert_vertex("E")
    F = g.insert_vertex("F")

    AB = g.insert_edge(A, B, 2)
    AC = g.insert_edge(A, C, 8)
    AE = g.insert_edge(A, E, 7)

    BC = g.insert_edge(B, C, 5)
    BD = g.insert_edge(B, D, 7)

    CD = g.insert_edge(C, D, 9)
    CE = g.insert_edge(C, E, 8)

    DF = g.insert_edge(D, E, 4)
    EF = g.insert_edge(E, F, 3)

    MST = MST_Kruskal(g)
    for e in MST:
        print(e)
