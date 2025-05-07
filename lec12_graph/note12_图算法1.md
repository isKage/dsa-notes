# 图与图算法（1）：图与图的遍历算法

本章介绍图的基本概念、图的存储结构（边列表、邻接表、邻接矩阵）、图的抽象数据类型 ADT 与 Python 实现。图的遍历算法：深度优先搜索 DFS 、广度优先搜索 BFS 及它们的应用。

## 1 图

### 1.1 图

图 **G** 可由一个二元组 **(V, E)** 表示，其中：

- **V** 中的元素为图中的顶点（vertex），被称为顶点集
- **E** 中的元素为由一对 V 中的顶点表示的图中的边（edge），被称为边集

例如下面的图， 顶点表示机场，存储机场的代码，边表示机场间的航线，存储航线里程。

![图的例子](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746595341486.png)

### 1.2 图的相关概念

**有向 & 无向**

有向边：有序的顶点对 (u, v) 表示从 u 到 v 的边

无向边：无序的顶点对 (u, v)

有向图（directed graph/digraph）：所有边均为有向边

无向图（undirected graph）：所有边均为无向边

**点 & 边 & 相邻**

端点（end vertices/endpoints）：被一条边连接的两个顶点

边入射（incident）到顶点：一条边连接一个顶点时

相邻顶点（adjacent vertices）：两个顶点间有边相连

**度 & 特殊的边**

顶点 v 的度（degree）：deg(v) 为入射到顶点的边数

平行边（parallel edges）/ 多重边（multiple edges）：即连接两个顶点的不同边

自环（self-loop）：即连接两个同样顶点的边

简单图（simple graph）：没有平行边和自环的图

**起点终点 & 出度入度**

如果一个有向边从顶点 u 指向顶点 v ，则：

- u 为其起点（origin）， v 为其终点（destination）
- 这条边是从顶点 u 出射的边（outgoing edge），且是入射到顶点 v 的边（incoming edge）

在有向图中：

- 顶点 v 的出度（out-degree）是从其出射的边数，记为 outdeg(v)
- 顶点 v 的入度（in-degree）是入射到其的边数，记为 indeg(v)

**路径**

路径（path）：路径为顶点与边交替的序列，从一个顶点开始，到另一顶点结束，每条边连接前后两个顶点

简单路径（simple path）：所有顶点和边均不相同的路径

**环**

环/回路（cycle）：环为开始、结束于同一顶点的路径

简单环（simple cycle）：简单环为除开始点和结束点之外的顶点、边均不相同的环

**完全图**

无向完全图（undirected complete graph）：图中每个顶点和其余任一顶点都恰有一条边相连

有向完全图（directed complete graph）：图中每个顶点都恰有一条有向边连向其余任一顶点

拥有边数很少（小于 n log n）的图为稀疏图（sparse graph），否则为稠密图（dense graph）

**子图 & 生成子图**

图 G = (V, E) 的子图（subgraph）即其顶点集和边集各为 V 和 E 的子集的图

图 G 的生成子图（spanning subgraph）为含有图 G 所有顶点的子图

如果从一个顶点 u 有一条路径通向另一个顶点 v，则称 v 是从 u 可达的（reachable）

**可达 & 连通**

如果从一个顶点 u 有一条路径通向另一个顶点 v，则称 *v* 是从 u 可达的（reachable）

如图中任两个顶点间有路径，则图为连通的（connected）

图 G 的最大连通子图称为其连通分支或连通分量（connected component）

有向图中任意两点间互相可达，则图为强连通的（strongly connected）

**树 & 森林 & 生成树**

树（tree）T 是一个图，且：

- T 是连通的
- T 中没有环

森林（forest）是一个没有环的图：

- 森林的连通分支为树

图 G 的生成树（spanning tree）是图 G 的生成子图，且其为树

- 生成树不是唯一的，除非图本身为树 

### 1.3 图的性质

**命题：如果 G 是有 m 条边和顶点集 V 的图，那么**
$$
\sum\limits_{v\ \in\ V} \deg(v) = 2m
$$
证明：一旦通过其端点 u 和通过其端点 v 一次，在上述求和计算中边 (u, v) 就计算了两次。因此，边对顶点度数的总贡献数是边数目的两倍。

**命题：如果 G 是有 m 条边和顶点集 V 的有向图，那么**
$$
\sum\limits_{v\ \in\ V} \deg^+(v) = \sum\limits_{v\ \in\ V} \deg^-(v) = m
$$
即图的所有点的出度的和等于入度的和。

证明：在有向图中，边 (u, v) 对它的起点 u 的出度贡献了一个单元，对终点 v 的入度贡献了一个单元。因此，边对顶点出度的总贡献和边的数目相等，入度也是一样的。

**命题：给定 G 为具有 n 个顶点和 m 条边的简单图。如果 G 是无向的，那么 $m \leq n(n-1)/2$ ，如果 G 是有向的，那么 $m \leq n(n-1)$ 。**

证明：假设 G 是无向的。因为没有两条边可以有相同的端点并且没有自循环，在这种情况下 G 的顶点的最大度是 n-1 。因此，通过 $\sum_{v\ \in\ V} \deg(v) = 2m$，有 $2m \leq n(n-1)$ 。现在假设G是有向的。因为没有两条边具有相同的起点和终点，并且没有自循环，在这种情况下 G 的顶点的最大入度是 n-1 。因此，通过 $\sum_{v\ \in\ V} \deg^-(v) = m \leq n(n-1)$ 。

**命题：树、森林和连通图的简单属性。**给定 G 是有 n 个顶点和 m 条边的无向图：

- 如果 G 是连通的，那么 $m \geq n-1$ 。
- 如果 G 是一棵树，那么 $m = n-1$ 。
- 如果 G 是森林，那么 $m \leq n-1$ 。

### 1.4 图的抽象数据类型

#### 1.4.1 点和边的 ADT

顶点 ADT 需要支持一个方法 `element()` 以返回存储在顶点的元素

边 ADT 存储一个与边相关的元素，并支持一个方法 `element()` 以返回该元素。另外，边 ADT 还应支持以下两个方法：

- `endpoints()` ：返回一个元组 (u, v)，其中 u 为顶点，v 为终点（无向图的方向任意）
- `opposite(v)` ：假设顶点 v 为边的一个端点，返回另一个端点

#### 1.4.2 图的 ADT

图 ADT 应支持以下方法：

- `vertex_count()` ：返回图中顶点的数目
- `vertices()` ：返回图中所有顶点的迭代器
- `edge_count()`：返回图中边的数目
- `edges()`：返回图中所有边的迭代器
- `get_edge(u, v)`：返回从顶点 u 到顶点 v 的边，如不存在则返回 None
- `degree(v, out = True)`：对于无向图，返回入射顶点 v 的边数；对于有向图，根据 out 的值返回出射或入射的边数
- `incident_edges(v, out = True)` ：返回入射顶点 v 的边的迭代器。对于有向图，根据 out 的值返回出射或入射的边的迭代器
- `insert_vertex(x = None)`：创建并返回一个存储元素 x 的新顶点
- `insert_edge(u, v, x = None)` ：创建并返回一个从顶点 u 到顶点 v 的存储元素 x 的新边
- `remove_vertex(v)` ：删除顶点 v 和其所有入射边
- `remove_edge(e)` ：删除边 e

### 1.5 图的存储结构

图的存储结构有很多种，如：

- 边列表
- 邻接表（邻接映射）
- 邻接矩阵

#### 1.5.1 边列表

**边列表（edge list）**分别用两个列表存放顶点和边，这两个列表可使用双向链表存储

- 顶点对象：存储顶点元素的引用；存储其在顶点序列中位置的引用

- 边对象：存储边元素的引用；存储起点、终点的引用；存储其在边序列中位置的引用

![边列表的图存储](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746607405226.png)

#### 1.5.2 邻接表

**邻接表（adjacency list）**使用列表存放顶点，并在每一顶点处存放其入射的边

- 顶点处存储的入射序列
- 顶点 v 处存储一个二级结构 I(v) 的引用，该结构存储其入射的所有边的引用

![邻接表的图存储](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746607864997.png)

#### 1.5.3 邻接矩阵

**邻接矩阵（adjacency matrix）**采用一个矩阵来存储边：

- 如图有 n 个顶点，则建立一个 n x n 的矩阵，矩阵每一行/列代表一个顶点
- 矩阵中任一位置存储对应的两个顶点间的边的引用，如两个顶点间无边则存储 None
- 忽略边信息时，可以用 1 表示存在边， 0 表示不存在边

![邻接矩阵的图存储](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746607974500.png)

#### 1.5.4 图的存储结构的性能

![不同图的存储结构的空间复杂度比较](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746608043733.png)

### 1.6 Python 实现

我们使用邻接列表的一种改进方式，即**邻接映射（adjacency map）**

- 与邻接表不同的是，我们使用字典来存储二级结构 `I(v)` ：字典中存储的键为该边的另一端点，值为边。这样的改进使得 `get_edge()` 方法的时间复杂度降为 O(1) 。
- 一级列表 `V` 使用一个顶级字典 `D` 来实现，其将每个顶点 `v` 映射到其入射边的二级结构 `I(v)` 。通过遍历字典 `D` 的所有键即可访问所有顶点。
- 顶点不需要存储指向其在 `D` 中的引用，因为它可以在 O(1) 的时间内被找到。
- 原邻接表的运行时间变为期望运行时间

![邻接映射的图示](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746608304065.png)

**Python 实现**

```python
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
```

测试：

```python
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
```

```python
Graph is directed or not: False
=============== All Vertices ===============
Vertex: 1
Vertex: 2
Vertex: 3
Vertex: 4
=============== All Edges ===============
Edge: f
Edge: b
Edge: d
Edge: c
Edge: a
Edge: e
```



## 2 图的遍历

图的遍历可以解决很多关于图的可达性的问题：

- 找到任意两个顶点间的路径（或验证两个顶点间无路径）
- 找到从图的一个特定顶点出发可以到达的所有顶点及相应的路径
- 测试图是否是连通的
- 找到图的所有连通分支
- 判断图是否为强连通的

我们常常使用如下两种算法进行图的遍历：

- **深度优先搜索**
- **广度优先搜索**

### 2.1 深度优先搜索 DFS

**深度优先搜索（DFS）**是一种常用的图遍历算法，可实现以下功能：

- 访问图 G 的所有顶点和边
- 判断图 G 是否是连通的
- 找到图 G 的所有连通分支
- 对图 G 的所有连通分支，计算其生成树

DFS 还可被用来解决其他问题，如：

- 找到两个顶点间的一条路径
- 找到图中的环

#### 2.1.1 深度优先搜索算法

图的 DFS 算法使用一种记录并查询顶点和边的“标签”的方式来判断顶点和边是否被访问过，下面以无向图为例给出 DFS 算法。此算法将所有边分为 `discovery` 和 `back` 两类。

【伪代码】从图 G 的某一个顶点 v 开始深度优先搜索：

```python
Algorithm DFS(G, v)
    [Input]: graph G and a start vertex v of G
    [Output]: labeling of the edges of G in the connected component of v as discovery edges and back edges
    [Algorithm]:
    setLabel(v, VISITED)  # v 已被访问过

    for all e = G.incidentEdges(v)  # v 的所有邻边 e
        if getLabel(e) = UNEXPLORED  # 若边 e 未被访问
        	w = opposite(v,e)  # 找到边 e 的非 v 的顶点 w
            
            if getLabel(w) = UNEXPLORED  # 若点 w 未被访问
            	setLabel(e, DISCOVERY)  # 标记边 e 为 discovery
            	DFS(G, w)  # 从点 w 继续递归探索
            else
            	setLabel(e, BACK)  # 否则, 点 w 被访问过, 则标记边 e 为 back
```

【伪代码】图 G 每一个点都进行 DFS：

```python
Algorithm DFS(G)
    [Input]: graph G
    [Output]: labeling of the edges of G as discovery edges and back edges
    [Algorithm]:
    for all u = G.vertices()  
    	setLabel(u, UNEXPLORED)  # 图 G 的所有点初始化为未访问

    for all e = G.edges()  # 图 G 的所有边初始化为未访问
    	setLabel(e, UNEXPLORED)
        
    for all v = G.vertices()  # 使用上面定义的 DFS(G, v) 对每个点 DFS
    	if getLabel(v) = UNEXPLORED
    		DFS(G, v)
```

DFS 深度优先搜索的例子：

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746612421410.png)

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746612483755.png)

#### 2.1.2 Python 实现

【无向图】实现 `DFS(G, v)` 即任一顶点出发的 DFS 算法，图 `Graph` 类代码见上面图的 Python 实现。

```python
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
```

测试：先创建一个图，这个图大致为如下所示：

```python
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
    
    """
    1 ----- 2
    | \   / |  
    |   X   |
    | /   \ |
    4 ----- 3
    """
```

使用如下的 `discovered = {v1: None}` 即可从 `v1` 开始搜索。

```python
	discovered = {v1: None}
    DFS(g, v1, discovered)

    for v, e in discovered.items():
        if e is not None:
            print(f"Vertex {v.element()} : Edge {e.element()}")
        else:
            print(f"Vertex {v.element()} : Initial")
```

结果：从 `1` 开始，经过 `(1, 2)` 到达 `2` ，经过 `(2, 3)` 到达 `3` ，经过 `(3, 4)` 达到 `4` 。

> 【注意】这里的结果只是一种可能，不过只要得到这一种可能，就已经遍历了全图的每个顶点和边。

```python
Vertex 1 : Initial
Vertex 2 : Edge (1, 2)
Vertex 3 : Edge (2, 3)
Vertex 4 : Edge (3, 4)
```

#### 2.1.3 DFS 的性质和性能

**性质：**

- `DFS(G, v)` 访问了顶点 v 所在的连通分支的所有顶点和边

- 由 `DFS(G, v)` 标记的所有边均为 discovery 边，且这些边形成了顶点 v 所在的连通分支的一个生成树

**性能：**

- 记录或查询顶点和边的标签需要 O(1) 的时间
- 每个顶点被标记一次，即第一次被访问时被标记为“已访问”
- 每条边被标记一次并检查两次：第一次被访问时标记为“已访问”；在两个端点被访问时，该边均被检查一次
- 每个顶点调用一次 `incident_edges()` 方法（以迭代器的形式返回顶点 v 的边）

对于顶点数为 n ，边数为 m 的图，存储方式为邻接表或邻接映射时，DFS 的运行时间为 **O(n + m)** 。

#### 2.1.4 寻找任意 2 点间的路径

我们可以将 DFS 算法特化并应用于寻找两个顶点 v 和 z 间的路径：

- 使用一个栈记录起点到当前顶点的路径
- 找到目标顶点 z 后，将栈中内容输出即为两顶点间的路径

伪代码：

```python
Algorithm pathDFS(G, v, z)
	[Algorithm]:
    setLabel(v, VISITED)  # 起始点 v 标记为已经访问
    S.push(v)  # 压入栈底
    
    if v = z  # 找到, 则将栈元素全部返回
    	return S.elements()
    
    for all e = G.incidentEdges(v)  # 点 v 的所有边 e
        if getLabel(e) = UNEXPLORED  # 若边 e 未访问
            w = opposite(v,e)  # 找到边 e 另一个端点 w
            if getLabel(w) = UNEXPLORED  # 若点 w 未访问
                setLabel(e, DISCOVERY)  # 标记 e 为 discovery
                S.push(e)  # 并压入栈, 作为路径的一部分
                pathDFS(G, w, z)  # 从 w 点继续递归探索
                
                S.pop(e)  # 从边 e 探索未找到, 则出栈
            else
            	setLabel(e, BACK)  # 若点 w 被访问, 标记 e 为 back
    S.pop(v)  # 所有点 v 的邻点都失败，则将点 v 出栈
```

Python 实现：传入的 `discovered` 参数需要先使用 `DFS(g, u, discovered)` 得到结果（即标记好了的 `discovered`），然后才能反向找出任意 2 点的路径。

```python
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
```

测试：例如找出点 `v2` 到 `v4` 的路径

```python
discovered = {v1: None}
DFS(g, v1, discovered)

# 使用之前的 DFS(g, v1, discovered) 的 discovered 结果
path = construct_path(v2, v4, discovered)
print(f"From v2 to v4: {path}")
```

```python
From v2 to v4: [2, 3, 4]
```

#### 2.1.5 寻找简单环

我们还可以将 DFS 算法特化并应用于寻找一个图中的简单环

- 使用一个栈记录起点到当前顶点的路径
- 找到一个 back 边后，输出栈中内容的一部分即为简单环

伪代码：

```python
Algorithm cycleDFS(G, v, z)
	[Algorithm]:
    setLabel(v, VISITED)  # 起始点 v 标记为已经访问
    S.push(v)  # 压入栈底

    for all e = G.incidentEdges(v)  # 点 v 的所有边 e
        if getLabel(e) = UNEXPLORED  # 若边 e 未访问
            w = opposite(v,e)  # 找到边 e 另一个端点 w
            S.push(e)  # 边 e 压入栈
            
            if getLabel(w) = UNEXPLORED  # 若点 w 未访问
                setLabel(e, DISCOVERY)  # 标记 e 为 discovery
                pathDFS(G, w, z)  # 从 w 点找到到达 z 的路径 (实现见上面代码)

                S.pop(e)  # 从边 e 探索未找到, 则出栈
            else
                T = new empty stack  # 新栈: 存储环的路径
                repeat  # 不断从栈 S 中获取点和边
                    o = S.pop()
                    T.push(o)
                until o = w  # 回到了点 w 形成了环
                return T.elements()  # 于是返回环所有元素
    S.pop(v)  # 没有环, 则将 v 出栈
```

### 2.2 广度优先搜索 BFS

**广度优先搜索（BFS）**是另一种常用的图遍历算法，也可以可实现以下功能：

- 访问图 G 的所有顶点和边
- 判断图 G 是否是连通的
- 找到图 G 的所有连通分支
- 对图 *G* 的所有连通分支，计算其生成树

BFS 还可以用来解决其他问题，如：

- 找到两个顶点间经过边数最少的路径
- 找到图中的环

#### 2.2.1 广度优先搜索算法

与 DFS 类似， BFS 算法使用一种记录并查询顶点和边的“标签”的方式来判断顶点和边是否被访问过。下面以无向图为例给出 BFS 算法，此算法将所有边分为 `discovery` 和 `cross` 两类。

【伪代码】从图 G 的某一个顶点 v 开始广度优先搜索：

```python
Algorithm BFS(G, s)
	[Algorithm]:
    L{0} = new empty sequence
    L{0}.addLast(s)  # 第一层
    setLabel(s, VISITED)
	
    i = 0
    while not L{i}.isEmpty()
        L{i+1} = new empty sequence
        for all v = L{i}.elements()   # 遍历 L{i} 的点 v
            for all e = G.incidentEdges(v)  # 取点 v 的所有邻边 e
                if getLabel(e) = UNEXPLORED  # 若 e 未标记
                w = opposite(v, e)  # 取边 e 的另一个端点 w
                    if getLabel(w) = UNEXPLORED  # 若点 w 未访问
	                    setLabel(e, DISCOVERY)  # 标记边 e 为 discovery
    	                setLabel(w, VISITED)  # 标记点 w 已访问
        	            L{i+1}.addLast(w)  # 并将 w 放入该层 L{i+1}
                    else
                    	setLabel(e, CROSS)  # 若点 w 已访问, 则标记边 e 为 cross
    	i = i +1  # 探索下一层
```

【伪代码】图 G 每一个点都进行 BFS：

```python
Algorithm BFS(G)
    [Input]: graph G
    [Output]: labeling of the edges of G 
	[Algorithm]:
    for all u = G.vertices()  # 标记所有点未访问
    	setLabel(u, UNEXPLORED)
    for all e = G.edges()  # 标记所有边未访问
	    setLabel(e, UNEXPLORED)

    for all v = G.vertices()  # 取所有点 v
        if getLabel(v) = UNEXPLORED  # 若 v 未访问
            BFS(G, v)  # 进行 BFS
```

BFS 广度优先搜索的例子：

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746623826094.png)

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746623847282.png)

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746623870768.png)

#### 2.2.2 Python 实现

【无向图】实现 `BFS(G, v)` 即任一顶点出发的 BFS 算法，图 `Graph` 类代码见上面图的 Python 实现。

```python
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
```

测试：构造图，如上面 BFS 广度优先搜索的例子的图

```python
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
```

初始化 `discovered = {A: None}` ，用于存储结果

```python
	discovered = {A: None}
    BFS(g, A, discovered)

    for v, e in discovered.items():
        if e is not None:
            print(f"Vertex {v.element()} : Edge {e.element()}")
        else:
            print(f"Vertex {v.element()} : Initial")
```

结果：恰好对应着之前例子里的 `discovery` 边

第 0 到 1 层 `(A, B)`, `(A, C)`, `(A, D)`

第 1 到 2 层 `(B, E)`, `(C, F)`

```python
Vertex A : Initial
Vertex B : Edge (A, B)
Vertex C : Edge (A, C)
Vertex D : Edge (A, D)
Vertex E : Edge (B, E)
Vertex F : Edge (C, F)
```

#### 2.2.3 BFS 的性质和性能

**性质：**我们使用 Gs 表示 s 所属的连通分支

- `BFS(G, s)` 访问了 Gs 的所有顶点和边
- 由 `BFS(G, s)` 标记的所有边均为 discovery 边，且这些边形成了 Gs 的一个生成树
- 对于 Li 层中的每个顶点 v ：从 s 到 v 的路径经过 i 条边；从 s 到 v 的每一条路径经过的边数不小于 i

**性能：**

- 记录或查询顶点和边的标签需要 O(1) 的时间
- 每个顶点被标记一次，即第一次被访问时被标记为“已访问”
- 每条边被标记一次并检查两次：第一次被访问时标记为“已访问”；在两个端点被访问时，该边均被检查一次
- 每个顶点被插入到某一序列/层 Li 一次
- 每个顶点调用一次 `incident_edges()` 方法（以迭代器的形式返回顶点 v 的边）

对于顶点数为 n ，边数为 m 的图，存储方式为邻接表或邻接映射时，DFS的运行时间为 **O(n + m)** 。

### 2.3 DFS vs BFS

深度优先搜索 DFS 和广度优先搜索 BFS 都可用于“生成树、连通分支、顶点间路径、环”的生成。“强连通分量”的生成一般使用 DFS 。寻找“边数最少的路径”一般使用 BFS 。

![DFS 和 BFS 更擅长的应用](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746625135261.png)

**back 边与 cross 边**

- Back 边 (v, w) ：w 是深度搜索树中 v 的祖先

- Cross 边 (v, w) ：w 与 v 在同一层上，或 w 在 v 的下一层

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746625370669.png)