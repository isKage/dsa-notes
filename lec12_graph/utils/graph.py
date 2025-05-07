class Graph:
    """使用邻接矩阵实现图结构"""

    # ------------------------- nested Vertex class -------------------------
    class Vertex:
        """顶点集合"""
        __slots__ = '_element'

        def __init__(self, x):
            """Use Graph's insert_vertex(x). 创建点"""
            self._element = x

        def element(self):
            """返回顶点存储的值"""
            return self._element

        def __hash__(self):  # hash 函数
            return hash(id(self))

    # ------------------------- nested Edge class -------------------------
    class Edge:
        """边集合"""
        __slots__ = '_origin', '_destination', '_element'

        def __init__(self, u, v, x):
            """Use Graph's insert_edge(u,v,x). 创建边"""
            self._origin = u
            self._destination = v
            self._element = x

        def endpoints(self):
            """返回 (u, v): u 为出射点, v 为入射点"""
            return (self._origin, self._destination)

        def opposite(self, v):
            """返回在当前边上 v 的邻接点"""
            return self._destination if v is self._origin else self._origin

        def element(self):
            """返回边上的数据, 例如权重"""
            return self._element

        def __hash__(self):  # hash 函数
            """对边哈希, 方便后面二级结构 I(v) 以字典形式存储"""
            return hash((self._origin, self._destination))

    # ------------------------- Graph methods -------------------------
    def __init__(self, directed=False):
        """
        初始化一个图, 默认为无向图
        :param directed: True 则为有向图
        """
        self._outgoing = {}  # 出射点集

        # 有向图时入射点集合为新, 否则指向出射点集
        self._incoming = {} if directed else self._outgoing

    def is_directed(self):
        """判断是否有方向"""
        return self._incoming is not self._outgoing

    def insert_vertex(self, x=None):
        """插入点, 返回点 Vertex 类"""
        v = self.Vertex(x)  # 创建新点, 值为 x
        self._outgoing[v] = {}  # 放入点集, 此时无边, 故为空

        if self.is_directed():
            self._incoming[v] = {}  # 如果有方向, 则入射点集也要加入
        return v

    def insert_edge(self, u, v, x=None):
        """插入边, 注意, 需要 u v 均为点 Vertex 类"""
        e = self.Edge(u, v, x)  # 从 u 到 v, 值为 x
        self._outgoing[u][v] = e  # 将边放入二级结构 I(u)
        self._incoming[v][u] = e  # 将边放入二级结构 I(v)
        return e

    def vertex_count(self):
        """总点数"""
        return len(self._outgoing)

    def vertices(self):
        """返回点的迭代器"""
        return self._outgoing.keys()

    def edge_count(self):
        """总边数"""
        # 总度数
        total = sum(len(self._outgoing[v]) for v in self._outgoing)

        # 无向图, 度求和要除以 2 . 有向图则不用
        return total if self.is_directed() else total // 2

    def edges(self):
        """返回图的所有边的集合 (已去重)"""
        result = set()  # 存储边集合, 防止重复
        for secondary_map in self._outgoing.values():
            result.update(secondary_map.values())  # 加入新边
        return result

    def get_edge(self, u, v):
        """返回点 u 到点 v 的边, 不相邻则为 None"""
        # 直接使用字典的 get() 方法, 没有则为 None
        return self._outgoing[u].get(v)

    def degree(self, v, outgoing=True):
        """
        返回顶点 v 的度, 默认为出度
        :param v: 顶点 Vertex 类
        :param outgoing: False 则返回入度
        :return: 顶点 v 的度
        """
        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v])

    def incident_edges(self, v, outgoing=True):
        """
        以迭代器的形式返回顶点 v 的边, 默认为出射边
        :param v: 顶点 Vertex 类
        :param outgoing: False 则返回入射边
        :return: 从顶点 v 出射的边 (入射 v 的边)
        """
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            yield edge


if __name__ == '__main__':
    g = Graph(directed=False)
    v1 = g.insert_vertex(1)
    v2 = g.insert_vertex(2)
    v3 = g.insert_vertex(3)
    v4 = g.insert_vertex(4)

    g.insert_edge(v1, v2, "a")
    g.insert_edge(v2, v3, "b")
    g.insert_edge(v3, v4, "c")
    g.insert_edge(v4, v1, "d")
    g.insert_edge(v1, v3, "e")
    g.insert_edge(v2, v4, "f")

    print(f"Graph is directed or not: {g.is_directed()}")

    print("=" * 15, "All Vertices", "=" * 15)
    for v in g.vertices():
        print(f"Vertex: {v.element()}")

    print("=" * 15, "All Edges", "=" * 15)
    for e in g.edges():
        print(f"Edge: {e.element()}")
