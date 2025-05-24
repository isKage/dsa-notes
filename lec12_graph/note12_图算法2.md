# 图与图算法（2）：最短路径、传递闭包和最小生成树

上一章 [图与图算法（1）：图与图的遍历算法](https://zhuanlan.zhihu.com/p/1903566835674244067) 介绍了图和图的遍历（DFS 和 BFS）。本章介绍图算法：最短路径（Dijkstra 算法）、传递闭包（Floyd-Warshall 算法）和最小生成树（Prim-Jarnik 算法和 Kruskal 算法）。



## 1 最短路径问题 Dijkstra 算法

### 1.1 加权图与最短路径

**加权图（weighted graph）**中，每条边均有一个与之关联的数值，即权重。

**最短路径（shortest path）**：给定两个顶点 u 和 v，寻找两个顶点间的最短路径。路径的长度定义为构成路径的所有边的权重之和。

- 最短路径的一条子路径也是最短路径
- 从一个顶点出发到其他所有顶点的最短路径构成一个树

![从某个点（点 PVD）出发的最短路径构成的树](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746629327788.png)

### 1.2 Dijkstra 算法

**Dijkstra 算法：**计算从一个源顶点 s 出发到其他所有顶点的最短路径，因此又被称为一种单源最短路径算法。

**Dijkstra 算法的假设：**

- 图为连通图
- 图的所有边权重非负

**算法思路：**

- 我们生成一个由顶点构成的“云”，此云中一开始只有源顶点 s，最后包含所有顶点
- 对于每个顶点 v，我们定义并记录其标签值 `d(v)` ，此标签值表示从 s 经过“云”中的顶点最终到达顶点 v 的最短路径值
- 算法的每一步执行如下操作：找到标签值 `d(u)` 最小的顶点 u，并将其加入“云”中；更新与 u 相邻且不在“云”中的顶点的标签值，这一步又称为边的松弛操作（relaxation）

**边的松弛操作：**

考虑满足如下条件的一条边 `e = (u, z)` ：u 是刚刚被加入到“云”中的一个顶点； z 不在“云”中。对边 e 的松弛操作如下：
$$
d(z) \leftarrow \min\left\{\ d(z),\ d(u) + weight(e)\ \right\}
$$
例如下面的例子：原来的 `d(z) = 75` 大于 `d(u) + weight(e) = 50 + 10 = 60` 故更新点 z 的标签值 `d(z) = 60` 。

![边的松弛操作](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746629902591.png)

**伪代码：**

```python
Algorithm ShortestPath(G, s):
    [Input]: A weighted graph G with nonnegative edge weights, and a distinguished vertex s of G
    [Output]: The length of a shortest path from s to v for each vertex v of G
    [Algorithm]:
    # 初始化, 点 s 标签为 0, 其他点均为正无穷
    Initialize D[s] = 0 and D[v] = +inf for each vertex v != s.

    Q = PriorityQueue()  # 优先级队列: key = D[v] value = v 且先包含所有点
    while not Q.isEmpty() do
    	# Q 是“非云” Q.remove(u) 相当于点 u 入云
        u = value returned by Q.remove_min()  # 挑出最小的 D[u]
        for each vertex v adjacent to u such that v is in Q do  # 所有与 u 相邻的 v
            if D[u] + w(u, v) < D[v] then
            	D[v] = D[u] + w(u, v)
            	Change to D[v] the key of vertex v in Q  # 边松弛操作, 改变 D[v]
    return the label of each vertex v
```

**完整的 Dijkstra 算法案例：**

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746630488031.png)

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746630568055.png)

### 1.3 Dijkstra 算法 Python 实现

需要使用上一章构建的图的类 `Graph` 代码见 [graph.py](https://github.com/isKage/dsa-notes/blob/main/lec12_graph/utils/graph.py) ；同时需要辅助结构 `AdaptableHeapPriorityQueue` 类，它是一个实现了定位器的优先级队列（基于堆实现），即可以在 O(1) 的时间内快速查找到节点的位置。代码见 [adaptable_heap_priority_queue.py](https://github.com/isKage/dsa-notes/blob/main/lec12_graph/utils/adaptable_heap_priority_queue.py) 。

特别地，`d = {}` 用于存储标签/最短路，`d[v]` ；`cloud = {}` 用于最终结果 `{v: d[v]}` 在云内的标签 (即最终最短路)；`pqlocator = {}`  用于存储点 v 在优先级队列中的位置 `{v: loc of v in pq}` 。

```python
from utils import Graph, AdaptableHeapPriorityQueue


def shortest_path_lengths(g: Graph, src: Graph.Vertex) -> dict:
    """
    最短路径问题: Dijkstra 算法
    :param g: 图 Graph 类
    :param src: 源点 Graph.Vertex 类
    :return: 源点 src 到所有可达点 v 的最短距离 dict: {v: d[v]}
    """
    d = {}  # 记录所有点的标签 d[v]
    cloud = {}  # 存储最终结果 {v: d[v]} 在云内的标签 (即最终最短路)
    pq = AdaptableHeapPriorityQueue()  # 优先级队列, 能够 O(1) 找到特定点, 值 (点 v)为 locator 字典的键
    pqlocator = {}  # 存储点 v 在优先级队列中的位置 {v: loc of v in pq}

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
                if d[u] + wgt < d[v]:  # 比较
                    d[v] = d[u] + wgt  # 更新为最小值
                    pq.update(pqlocator[v], d[v], v)  # 同时更新优先级队列里的 (d[v], v)
    return cloud
```

测试：以上图为例，可求得

```python
if __name__ == '__main__':
    g = Graph(directed=False)

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
        print(f"From Vertex {k.element()}: {toA_shortest_path[k]}")
```

```python
From Vertex A: 0
From Vertex C: 2
From Vertex D: 3
From Vertex E: 5
From Vertex B: 7
From Vertex F: 8
```

### 1.4 Dijkstra 算法性能分析和正确性

#### 1.4.1 性能分析

图操作：

- 访问了所有顶点
- 并在将顶点放入“云”这一步访问了所有的边

标签操作：

- 查询/修改一个顶点 z 的标签 O(deg(z)) 次
- 我们可以在 O(1) 的时间内完成这一工作

优先级队列操作：

- 每个顶点被插入、移出刚好一次：如使用堆实现，则需要 O(log n) 的时间，所有顶点则需要 $O(n \log n)$ ；如使用无序列表实现，则需要 O(n) 的时间，所有顶点则需要 $O(n^2)$ 。
- 优先级队列中一个顶点 z 的键最多被修改 deg(z) 次；如使用堆实现，则需要 O(log n) 的时间；如使用无序列表实现，则需要 O(1) 的时间。因为 $\sum_z \deg (z) = O(m)$ ，故使用堆则总共需要 $O(m \log n)$ ，使用无序列表则总共需要 $O(m)$ 。

当图使用邻接表或邻接映射实现时，Dijkstra 算法的运行时间为：

- 优先级队列堆实现：$O((n+m)\log n)$ 。
- 优先级队列无序列表：$O(n^2+m)$ ，图是简单图则可以简化为 $O(n^2)$ 。

不难发现，当处理稀疏图时，即 m 较小时，使用堆实现更为方便。

#### 1.4.2 正确性

Dijkstra算法是一个典型的**贪心算法（greedy algorithm）**，每次都将通过“云”到达的最近的顶点加入“云”。这一算法的正确性依赖于**边权重的非负性**。我们可以使用反证法证明 Dijkstra 算法的正确性：

**证明：**假设 Dijkstra 算法并未找到所有的最短路径，设 z 是第一个出错的顶点

设此时从 s 到 z 的最短路径上的第一个不在“云”中的顶点为 y，且其前一个顶点为 x

由于此时的 D[y] 已经在 x 被加入“云”时访问被修改过了，因此 D[y] 即为 s 到 y 最短路径的长度 d(s, y) 。但此时 y 未被考虑加入“云”，因此有：
$$
D[z] \leq D[y] = d(s, y) \leq d(s, y) + d(y, z) = d(s, z)
$$
这与 z 的假设（z 未找到最短路）矛盾！

![反证法图示](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746759393409.png)

#### 1.4.3 负权重的反例

如出现负权重边，则当负权重边在较晚时刻被加入到“云”中时，云中与之相连的顶点及其可达的其他顶点的最短路径均可能发生变化。

例：右图中 A 为源顶点，C 的最短路径为 1 ，但将 F 加入“云”时已经有“云”中的 d(C) = 5 ，但从 A - D - F - C 可以得到更短路 d(C) = 9 - 8 = 1 ，矛盾。

![负权重](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746759588311.png)



## 2 传递闭包问题 Floyd-Warshall 算法

Dijkstra 算法要求边的权重非负，且只能求从单个源顶点出发的所有最短路径。是否有求所有顶点对之间最短路径，且不要求边的权重非负的算法？

**Floyd-Warshall 算法：**

- 可用于计算传递闭包
- 可用于计算所有顶点对间的最短路径
- 没有边权重非负的要求（但要求不能有一个权重和为负的环，否则可以一直在这个环上循环，直至负无穷）

### 2.1 传递闭包

给定一个有向图 $\overrightarrow{G}$ ，其**传递闭包（transitive closure）** $\overrightarrow{G}^*$ 是满足下列条件的有向图：

- 二者顶点数相同
- 在 $\overrightarrow{G}$ 中从点 u 到 v 的路，与 $\overrightarrow{G}^*$ 的边 (u, v) 即从 u 出射，入射到 v 的边等价（包括原始图的 (u, v) 边）

传递闭包为有向图提供了关于顶点间可达性的信息。

![传递闭包](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746760539259.png)

### 2.2 计算传递闭包

最简单的想法：在每个顶点处执行 DFS ，然后对 DFS 路径上的每一个点都直接连边（若没有直接连边）。总共 n 个点，DFS 的时间复杂度为 O(n + m) 所以这个方法的时间复杂度为 **O(n(n + m))** 。

另一种基于动态规划的想法：**Floyd-Warshall 算法**

### 2.3 Floyd-Warshall 算法

Floyd-Warshall 算法的基本思路：

- 将所有顶点从 1 到 n 进行编号
- 在第 k 步，考虑仅经过顶点 1, 2 …, k 的所有路径

算法的第 k 步示意图：

![Floyd-Warshall 算法第 k 步](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746760761512.png)

具体思路：

- 将顶点编号为 $v_1,\ v_2,\ \cdots,\ v_n$ ，按顺序计算 $G_0,\ G_1,\ \cdots,\ G_n$ ：
- 初始化 $G_0 \leftarrow G$ 
- 在第 k 步，使用 $G_{k-1}$ 计算 $G_k$ ：如果 $G$ 从点 $v_i$ 到点 $v_j$ 有只经过 $\{v_1, v_2,\ \cdots,\ v_k \}$ 的路径，则在 $G_k$ 中添加一条有向边 $(v_i,\ v_j)$ 
- 最终有 $G^* \leftarrow G_n$ 

伪代码：

```python
Algorithm FloydWarshall(G)
    [Input]: digraph G
    [Output]: transitive closure G* of G
	[Algorithm]:

    i = 1
    for all v = G.vertices()  # 所有顶点
	    # 标记所有点
        denote v as vi
        i = i + 1

   	G{0} = G  # 初始 G{0}
    for k = 1 to n do
        G{k} = G{k−1}
        for i = 1 to n (i != k) do  # vi
            for j = 1 to n (j != i, k) do  # vi
            	# G{k-1} 中 vi vk 相邻, vk vj 相邻
                if G{k−1}.areAdjacent(vi, vk) and G{k−1}.areAdjacent(vk, vj)
                	# 但 G{k} 中 vi vj 不相邻
                    if not G{k}.areAdjacent(vi, vj) 
                    	# 则在 G{k} 中连边 vi vj
                        G{k}.insertDirectedEdge(vi, vj, k)
    return G{n}
```

示例：

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746761710050.png)

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746761741081.png)

### 2.4 Floyd-Warshall 算法 Python 实现

```python
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
```

测试：图 G 有 A B C 三点，有边 (A -> B) (B -> C) 则闭包增加边 (A -> C)

```python
if __name__ == '__main__':
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
```

```python
Before Floyd Warshall: Edge has 2
After Floyd Warshall: Edge has 3
```



### 2.5 Floyd-Warshall 算法的性能

**结论：**假设可在 O(1) 时间内完成判断顶点间是否有边的操作（如使用邻接矩阵），则算法时间复杂度为 $O(n^3)$ 。

**Floyd-Warshall 算法 vs 每个点深度优先 DFS 算法**

Floyd-Warshall 算法的时间复杂度为 $O(n^3)$ ，而逐个点使用 DFS 算法实现传递闭包的时间复杂度为 $O(n(n+m))$ 。

- Floyd-Warshall 算法在图是稠密的或使用邻接矩阵表示图时与重复调用 DFS 的渐进性能相同
- Floyd-Warshall 算法更容易实现，且实践中运行非常快，尤其当图使用邻接矩阵实现时
- 图是稀疏的且使用图的邻接表或邻接映射实现时，DFS 有更好的性能
- Floyd-Warshall 算法通常使用图的邻接矩阵实现，在这一实现下其效率最高

### 2.6 最短路 Floyd-Warshall 算法

Floyd-Warshall 算法还可用于求图中**所有顶点间的最短路径（all-pairs shortest path）**，并且对边权重的非负性没有任何要求：

- 对第 k 步的操作进行修改即可：

$$
d_k(v_i,\ v_j) = \min \{ d_{k-1}(v_i,\ v_j),\ d_{k-1}(v_i,\ v_k) + d_{k-1}(v_k,\ v_j) \}
$$

```python
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
```

测试：

```python
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
    print("=" * 15, "Shortest Path", "=" * 15)
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

    shortest_path_dict = floyd_warshall_shortest_path(g=g)
    print_shortest_paths(g, shortest_path_dict)  # 输出结果
```

```python
=============== Shortest Path ===============
A → B: 8
A → C: 2
A → D: 3
A → E: 5
A → F: 8
B → A: No Path
B → C: 7
...
```



## 3 最小生成树 Prim-Jarnik & Kruskal

### 3.1 最小生成树

生成子图（spanning graph）：图 G 的生成子图包含其所有顶点。生成树（spanning tree）：为树的生成子图

**最小生成树（minimum spanning tree/MST）**：加权图的总权重最小的生成树

**最小生成树的性质：**

- **环性质（cycle property ）：**令 T 为加权图 G 的一棵最小生成树，令 e 为图 G 中不属于 T 的边，且令 e 与 T 形成的环为 C 。则有：对环上的每一条边 f 均有 $weight(f) \leq weight(e)$ 。


因为如果可以找到一条边使得 $weight(f) > weight(e)$ 则用边 e 取代 f 即可得到一棵总权重更小的生成树。


- **分割性质（partition property）：**考虑将 G 的所有顶点分为两个集合 U 和 V 的一个分割。令 e 为连接这两部分顶点集合的权重最小的边。则有：存在一棵包含边 e 的 G 的最小生成树。

考虑 G 的一棵最小生成树 T ，如果 T 不包含 e，考虑由 e 和 T 构成的环 C，及 T 中连接 U 和 V 的边 f 。由最小生成树的环性质可得：$weight(f) \leq weight(e)$ ，$weight(f) = weight(e)$ 。用 e 替代 f 即可得到另一棵最小生成树。

有两种解决最小生成树问题的经典算法，均为贪心算法：

- Prim-Jarnik 算法
- Kruskal 算法

### 3.2 Prim-Jarnik 算法

Prim 算法从一个“根”顶点 s 出发，以构建“云”的方式逐步形成一棵最小生成树，其思想与 Dijkstra 算法类似。

- 对每个顶点 v，其标签 d(v) 存储该顶点与“云”间相连的边的最小权重。

- 将“云”外标签值 d(u) 最小的顶点 u 加入“云”
- 更新与 u 相邻的顶点的标签值

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1748076899672.png)

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1748076956667.png)

#### 3.2.1 算法实现

```python
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
```

#### 3.2.2 性能分析

图操作：我们访问了所有顶点，并在将顶点放入“云”这一步访问了所有的边

标签操作：我们查询/修改一个顶点 z 的标签 O(deg(z)) 次，我们可以在 O(1) 的时间内完成这一工作

优先级队列操作：

- 每个顶点被插入、移出刚好一次；如使用堆实现，则需要 O(log n) 的时间，如使用无序列表实现，则需要 O(n) 的时间。
- 优先级队列中一个顶点 z 的键最多被修改 deg(z) 次；如使用堆实现，则需要 O(log n) 的时间，如使用无序列表实现，则需要 O(1) 的时间

当图使用邻接表或邻接映射实现时，Prim-Jarnik 算法的运行时间为：

- 优先级队列堆实现：**O((n + m) log n)** ，由于图是连通的，可简化为 **O(m log n)**
- 优先级队列无序列表实现：**O(n^2)**

### 3.3 Kruskal 算法

与 Prim 算法不同，Kruskal 算法将顶点分为很多个集合后进行顶点集群的合并

- 一开始，所有顶点都在一个只有自己的集群中
- 算法执行过程中，对每个集群均记录其最小生成树
- 算法执行的每一步为将“离得最近”的两个集群合并，并得到合并集群的最小生成树
- 与 Prim 算法类似，采用一个优先级队列存储集群之外的边，其键为权重值，值为边
- 最终，算法将得到一个集群及其上的最小生成树，即原图的最小生成树

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1748078020250.png)

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1748078079252.png)

#### 3.3.1 Kruskal 算法的辅助数据结构

与 Prim 算法类似，Kruskal 算法中使用一个优先级队列在每一步选择权重最小的边。Kruskal 算法还需要进行**集群**的管理，这需要一种新的可以存储并管理一系列不相交集合的数据结构 `Partition` 类，此数据结构需要提供如下功能：

- `makeSet(u)` ：创建一个只有 u 的集合
- `find(u)` ：返回包含 u 的集合的位置
- `union(A, B)` ：将 A 和 B 合并

**Partition** 类的实现：

我们使用序列来实现 Partition 结构：

- 集合的每个元素均存储指向集合位置的指针
- `make_group(u)` 需要 O(1) 的时间
- `find(u)` 需要 O(1) 的时间
- `union(A,B)` 操作中，我们将表示较小集合的序列的元素移动到较大的集合中，并更新这些元素的指针。 `union(A,B)` 需要 O(min{|A|, |B|}) 的时间
- 每当元素被从一个集合移动到另一个集合中时，集合的大小都至少会翻倍，因此每个元素最多被移动 log n 次

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1748079072331.png)

也可以使用树结构来实现，见 [partition.py](utils/partition.py)  。

#### 3.3.2 Partition 的代码实现

基于序列：

```python
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

    def union(self, p, q):
        """合并包含 p 和 q 的两个组"""
        # 包含 p 和 q 的两个组
        group_p = p._group
        group_q = q._group

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

            # 从群组 ——groups 中移除较小的组
            self._groups.remove(smaller)

    def __repr__(self):
        return f"ListPartition({self._groups})"
```

基于树：

```python
class Partition:
    class Position:
        __slots__ = '_container', '_element', '_size', '_parent'

        def __init__(self, container, e):
            self._container = container
            self._element = e
            self._size = 1
            self._parent = self

        def element(self):
            return self._element

    def make_group(self, e):
        return self.Position(self, e)

    def find(self, p):
        if p._parent != p:
            p._parent = self.find(p._parent)
        return p._parent

    def union(self, p, q):
        a = self.find(p)
        b = self.find(q)
        if a is not b:
            if a._size > b._size:
                b._parent = a
                a._size += b._size
            else:
                a._parent = b
                b._size += a._size
```

#### 3.3.3 Kruskal 算法的实现

```python
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
```

#### 3.3.4 性能分析

使用这样的 Partition 结构存储集群，则：

- 集群的合并使用 union 方法
- 寻找集群的位置使用 find 方法

Kruskal 算法的运行时间为 **O((n + m) log n)**

- 优先级队列操作运行时间：**O(m log n)**
- 集群定位、合并操作运行时间：**O(n log n)**



## 4 拓扑排序

### 4.1 拓扑排序与有向非循环图 DAG

**拓扑排序**：使得有向图 G 的任何有向路径以增加的顺序遍历顶点（为顶点编号）。同一幅图可能有多个拓扑排序。

拓扑排序可以用来检查图是否为**有向非循环图 DAG** （即没有有向环），当拓扑排序没有包含所有点时，说明这个图存在有向循环/圈。

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1748080212879.png)

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1748080232195.png)

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1748080244812.png)

### 4.1 拓扑排序代码实现

```python
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
```

针对上面图示的例子，进行测试：

```python
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
```

结果为：

```python
[Vertex(element=X), Vertex(element=C), Vertex(element=E), Vertex(element=A), Vertex(element=B), Vertex(element=D), Vertex(element=F), Vertex(element=G), Vertex(element=H)]
False
```

拓扑排序的时间复杂度为 **O(n+m)** 。
