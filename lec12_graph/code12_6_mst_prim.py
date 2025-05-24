from utils import AdaptableHeapPriorityQueue, Graph


def MST_PrimJarnik(g):
    """最小生成树 返回边列表"""
    d = {}  # d[v] is bound on distance to tree
    tree = []  # 最小生成树的边序列
    pq = AdaptableHeapPriorityQueue()  # d[v] maps to value (v, e=(u,v))
    pqlocator = {}  # {Vertex: pq's locator}

    # 初始化标签 d[v]
    for v in g.vertices():
        if len(d) == 0:  # d 空, 没有节点
            d[v] = 0  # 则设置一个起点
        else:
            d[v] = float('inf')  # positive infinity
        pqlocator[v] = pq.add(d[v], (v, None))

    while not pq.is_empty():
        key, value = pq.remove_min()
        u, edge = value  # unpack tuple from pq
        del pqlocator[u]  # u is no longer in pq

        if edge is not None:
            tree.append(edge)  # add edge to tree
        for link in g.incident_edges(u):
            v = link.opposite(u)  # 寻找邻点
            if v in pqlocator:  # thus v not yet in tree
                # see if edge (u,v) better connects v to the growing tree
                wgt = link.element()
                if wgt < d[v]:  # better edge to v?
                    d[v] = wgt  # update the distance
                    pq.update(pqlocator[v], d[v], (v, link))  # update the pq
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

    MST = MST_PrimJarnik(g)
    for e in MST:
        print(e)
