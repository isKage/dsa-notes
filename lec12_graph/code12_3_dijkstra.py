from utils import Graph, AdaptableHeapPriorityQueue


def shortest_path_lengths(g: Graph, src: Graph.Vertex, threshold=None) -> dict:
    """
    最短路径问题: Dijkstra 算法
    :param g: 图 Graph 类
    :param src: 源点 Graph.Vertex 类
    :param threshold: 阈值
    :return: 源点 src 到所有可达点 v 的最短距离 dict: {v: d[v]}
    """
    d = {}  # 记录所有点的标签 d[v]
    cloud = {}  # 存储最终结果 {v: d[v]} 在云内的标签 (即最终最短路)
    pq = AdaptableHeapPriorityQueue()  # 优先级队列, 能够 O(1) 找到特定点, 值 (点 v)为 locator 字典的键
    pqlocator = {}  # 存储点 v 在优先级队列中的位置 {v: loc of v in pq (AdaptableHeapPriorityQueue.Locator 类)}

    # 初始化所有点 v 的标签 d[v]
    for v in g.vertices():
        if v is src:
            d[v] = 0  # 源点为 0
        else:
            d[v] = float('inf')  # 暂时记为正无穷大
        pqlocator[v] = pq.add(d[v], v)  # (最短路 d[v], 点 v) 放入优先级队列, 同时记录位置在 pqlocator

    while not pq.is_empty():
        key, u = pq.remove_min()  # 取出云外最小路 min d[v] out of cloud
        cloud[u] = key  # 放入云内 cloud[u] = key 因为存的时候 key = d[u]
        del pqlocator[u]  # pqlocator 删去点 u 在优先级队列里的位置

        for e in g.incident_edges(u):  # 所有通向点 u 的边 e
            v = e.opposite(u)  # 对面的点 v
            if v not in cloud:  # 若 v 不在云里
                wgt = e.element()  # 边权重
                new_dist = d[u] + wgt
                # 阈值判断
                if threshold is not None and new_dist >= threshold:
                    continue  # 超过阈值
                # 否则, 正常 Dijkstra
                if new_dist < d[v]:
                    d[v] = new_dist
                    pq.update(pqlocator[v], d[v], v)
    return cloud


if __name__ == '__main__':
    g = Graph(directed=True)

    A = g.insert_vertex("A")
    B = g.insert_vertex("B")
    C = g.insert_vertex("C")
    D = g.insert_vertex("D")
    E = g.insert_vertex("E")
    F = g.insert_vertex("F")

    AB = g.insert_edge(A, B, 8)
    AC = g.insert_edge(A, C, 2)
    AD = g.insert_edge(A, D, 4)
    BC = g.insert_edge(B, C, 7)
    CD = g.insert_edge(C, D, 1)
    BE = g.insert_edge(B, E, 2)
    CE = g.insert_edge(C, E, 3)
    CF = g.insert_edge(C, F, 9)
    DF = g.insert_edge(D, F, 5)

    toA_shortest_path = shortest_path_lengths(g=g, src=A)
    for k in toA_shortest_path:
        print(f"From A to {k.element()}: "
              f"{toA_shortest_path[k] if toA_shortest_path[k] < float('inf') else None}")
