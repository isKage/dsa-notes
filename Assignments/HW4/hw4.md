# Homework 4

> about `graph` `text` `dynamic programming`

## Question 1

对一个有 V 个顶点和 E 条边的无向简单图，求其连通分量个数的上界和下界。

**Solution** 

当 $V$ 和 $E$ 可变：对一个简单无向图 $G = (V,\ E)$ 其连通分量的个数 $n$ 满足 $1 \leq n \leq |V|$ 。

- 当 $G$ 为简单完全图时，图 $G$ 本身就是唯一一个连通分量；
- 当 $G$ 由 $|V|$ 个孤立点构成时，即 $|E| = 0$ 无边，图 $G$ 每个顶点都是一个连通分量，共 $|V|$ 个。

当 $V$ 和 $E$ 给定：

- 为了使连通分量尽可能大，则要让孤立点尽可能多，假设已有 $k$ 个点之间是连通的，则要让 $E$ 完全分配在这 $k$ 个点之间，其他点均为孤立点，从而使得连通分量个数 $n \leq |V| - k + 1$ ：

$$
\binom{k}{2} \geq |E|
$$

$$
n \leq |V| - \left[\frac{1+\sqrt{1+ 8 \cdot |E|}}{2} \right] + 1
$$

- 为了使连通分量尽可能小，则要尽可能使得图为完全图，当 $|E| \geq |V| - 1$ 时可以构成完全图，故 $n = 1$ ；当 $|E| \leq |V|$ 时则连成一条路，则 $n = |V| - |E|$ 。

综上，连通分量的上界为 $|V| - \left[\frac{1+\sqrt{1+ 8 \cdot |E|}}{2} \right] + 1$ ，而下界为 $1$ 或 $|V| - |E|$ 。

## Question 2

请补全 `Graph` 类，实现 `remove_vertex()` 方法和 `remove_edge()` 方法。

**Solution** 完整代码见 [hw4_2_graph.py](hw4_2_graph.py) ，删除点和边的部分代码见下：

```python
class Graph:
    """使用邻接矩阵实现图结构"""
    ...

	def remove_edge(self, u, v):
        """
        删除顶点 u 到顶点 v 的边
        :param u: 边的起点
        :param v: 边的终点
        :return: 被删除边的元素
        """
        if u not in self._outgoing or v not in self._outgoing[u]:
            raise ValueError("Edge not in graph")

        e = self.get_edge(u, v)
        del self._outgoing[u][v]
        del self._incoming[v][u]

        return e.element()

    def remove_vertex(self, v):
        """
        删除顶点 v 及其所有关联边
        :param v: 要删除的顶点
        :return: 被删除顶点的元素
        """
        if v not in self._outgoing:
            raise ValueError("Vertex not in graph")

        # 首先删除所有与 v 关联的边
        neighbors = list(self._outgoing[v].keys())  # 所有邻接顶点

        # 对于无向图, 需要避免重复删除
        if self.is_directed():
            # 有向图: 删除所有出边和入边
            for u in neighbors:
                del self._incoming[u][v]  # 删除入边
            for w in self._incoming[v]:
                del self._outgoing[w][v]  # 删除出边
        else:
            # 无向图: 只需要删除一次
            for u in neighbors:
                del self._outgoing[u][v]

        # 删除顶点本身
        del self._outgoing[v]
        if self.is_directed():  # 有向
            del self._incoming[v]

        return v.element()
```

## Question 3

平面直角坐标系上将以下各点依次标记为顶点 0～5：(1, 3)，(2, 1)，(6, 5)，(3, 4)，(3, 7)，(5, 3) 。取边长度（欧氏距离）为权值，考虑由这 6 个顶点及以下边所定义的无向图：1-0，3-5，5-2，3-4，5-1，0-3，0-4，4-2，2-3 。

1. 画出邻接表结构。（二级结构的元素可直接用顶点表示）
2. 分别用 Prim 算法和 Kruskal 算法求出最小生成树，按照加入最小生成树的顺序写出各条边。
3. 求从顶点 0 出发的最短路径树。
4. 画出邻接矩阵结构，并借助邻接矩阵结构，用 Floyd-Warshall 算法计算全源最短路径。

| 顶点 |   0    |   1    |   2    |   3    |   4    |   5    |
| ---- | :----: | :----: | :----: | :----: | :----: | :----: |
| 坐标 | (1, 3) | (2, 1) | (6, 5) | (3, 4) | (3, 7) | (5, 3) |

边权重：$e(1-0) = \sqrt{5}$ ，$e(3-5) = \sqrt{5}$ ，$e(5-2) = \sqrt{5}$ ，$e(3-4) = 3$ ，$e(5-1) = \sqrt{13}$ ，$e(0-3) = \sqrt{5}$ ，$e(0-4) = 2\sqrt{5}$ ，$e(4-2) = \sqrt{13}$ ，$e(2-3) = \sqrt{10}$ 。

**Solution 1** 邻接表结构如下

```python
{
  0: {
    1: sqrt(5),
    3: sqrt(5),
    4: 2 * sqrt(5)
  },
  1: {
    0: sqrt(5),
    5: sqrt(13)
  },
  2: {
    3: sqrt(10),
    4: sqrt(13),
    5: sqrt(5)
  },
  3: {
    0: sqrt(5),
    2: sqrt(10),
    4: 3,
    5: sqrt(5)
  },
  4: {
    0: 2 * sqrt(5),
    2: sqrt(13),
    3: 3
  },
  5: {
    1: sqrt(13),
    2: sqrt(5),
    3: sqrt(5)
  }
}
```

**Solution 2** 最小生成树

 Prim 算法的最小生成树权重和为 $\sqrt{5} + \sqrt{5} + \sqrt{5} + \sqrt{5} + 3 = 3 + 4 \sqrt{5}$ 。边的加入顺序为：

```python
(0-1) -> (0-3) -> (3-5) -> (5-2) -> (3-4)
```

Kruskal 算法的最小生成树权重和为 $\sqrt{5} + \sqrt{5} + \sqrt{5} + \sqrt{5} + 3 = 3 + 4 \sqrt{5}$ 。边的加入顺序为：

```python
(0-1) -> (5-2) -> (0-3) -> (3-5) -> (3-4)
```

生成树的例子：

```python
0 -> [1, 3]
3 -> [4, 5]
5 -> 2
```

**Solution 3** 从 0 出发的最短路 

我们使用 Dijkstra 算法，最短路径为：

```python
"0 -> 1" sqrt(5) : 0-1
"0 -> 2" sqrt(5) + sqrt(10) : 0-3-2
"0 -> 3" sqrt(5) : 0-3
"0 -> 4" 2 * sqrt(5) : 0-4
"0 -> 5" 2 * sqrt(5) : 0-3-5
```

**Solution 4** 邻接矩阵，用 Floyd-Warshall 算法计算全源最短路径

首先写出邻接矩阵，不可达则用 $\inf$ 初始化

| 顶点 |      0      |      1      |      2      |      3      |      4      |      5      |
| :--: | :---------: | :---------: | :---------: | :---------: | :---------: | :---------: |
|  0   |      0      | $\sqrt{5}$  |   $\inf$    | $\sqrt{5}$  | $2\sqrt{5}$ |   $\inf$    |
|  1   | $\sqrt{5}$  |      0      |   $\inf$    |   $\inf$    |   $\inf$    | $\sqrt{13}$ |
|  2   |   $\inf$    |   $\inf$    |      0      | $\sqrt{10}$ | $\sqrt{13}$ | $\sqrt{5}$  |
|  3   | $\sqrt{5}$  |   $\inf$    | $\sqrt{10}$ |      0      |     $3$     | $\sqrt{5}$  |
|  4   | $2\sqrt{5}$ |   $\inf$    | $\sqrt{13}$ |     $3$     |      0      |   $\inf$    |
|  5   |   $\inf$    | $\sqrt{13}$ | $\sqrt{5}$  | $\sqrt{5}$  |   $\inf$    |      0      |

逐步更新邻接矩阵，递推公式：对于任意中间顶点 $k$ ，有顶点 $u$ 和 $v$ 通过 $k$ 连接，则有
$$
d'_{uv} = \min \ \{ d_{uv} ,\ d_{uk} + d_{kv} \}
$$

例如：顶点 0 与 2 通过顶点 3 连接，则有 $d_{02} = \min\ \{ \inf,\ \sqrt{5} + \sqrt{10} \} = \sqrt{5} + \sqrt{10}$ 。同理可计算其他的路径，即对邻接矩阵 $A$ 位于 $(i,\ j)$ 的元素可以根据下式更新：
$$
A(i,\ j) = \min_{k = 0,\ 1,\ \cdots,\ 5} \{ A(i,\ j),\ A(i,\ k) + A(k,\ j) \}
$$
最终得到的全源最短路径矩阵为：

| 顶点 |           0            |          1           |           2            |      3      |       4        |       5        |
| :--: | :--------------------: | :------------------: | :--------------------: | :---------: | :------------: | :------------: |
|  0   |           0            |      $\sqrt{5}$      | $\sqrt{5} + \sqrt{10}$ | $\sqrt{5}$  |  $2\sqrt{5}$   |  $2 \sqrt{5}$  |
|  1   |       $\sqrt{5}$       |          0           |  $\sqrt{5}+\sqrt{13}$  | $2\sqrt{5}$ |  $3\sqrt{5}$   |  $\sqrt{13}$   |
|  2   | $\sqrt{5} + \sqrt{10}$ | $\sqrt{5}+\sqrt{13}$ |           0            | $\sqrt{10}$ |  $\sqrt{13}$   |   $\sqrt{5}$   |
|  3   |       $\sqrt{5}$       |     $2\sqrt{5}$      |      $\sqrt{10}$       |      0      |      $3$       |   $\sqrt{5}$   |
|  4   |      $2\sqrt{5}$       |     $3\sqrt{5}$      |      $\sqrt{13}$       |     $3$     |       0        | $3 + \sqrt{5}$ |
|  5   |      $2 \sqrt{5}$      |     $\sqrt{13}$      |       $\sqrt{5}$       | $\sqrt{5}$  | $3 + \sqrt{5}$ |       0        |

补充：下面的代码实现了 Floyd 算法的最短路问题，图 `Graph` 类的实现可见代码 [hw4_2_graph.py](hw4_2_graph.py)  

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

## Question 4

请用序列实现 Kruskal 算法中的 Partition 结构，可参考：

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

**Solution** 基于序列的实现的 `ListPartition` 类，见 [hw4_4_list_partition.py](hw4_4_list_partition.py) 

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

## Question 5

现有文本字符串 `abaababaabababaca` 和模式串 `ababac` 。请求出模式串的失败函数，画出用 KMP 算法进行匹配的过程，并统计出比较的次数。

**Solution**

模式串 `ababac` 的失败函数为：`F(j)` 为最长的既为 `P[0: j]` 前缀又为 `P[1: j]` 后缀的子串长度

| `j`    |  0   |  1   |  2   |  3   |  4   |  5   |
| :----- | :--: | :--: | :--: | :--: | :--: | :--: |
| `P[j]` | `a`  | `b`  | `a`  | `b`  | `a`  | `c`  |
| `F[j]` |  0   |  0   |  1   |  2   |  3   |  0   |

KMP 算法总共比较了 $22$ 次（若匹配成功就退出）

|  a   |  b   |    a     |             a              |  b   |    a     |    b     |    a     |             a              |  b   |                 a                  |                 b                  |                 a                  |              b              |              a              |              c              |  a   | 次数 |
| :--: | :--: | :------: | :------------------------: | :--: | :------: | :------: | :------: | :------------------------: | :--: | :--------------------------------: | :--------------------------------: | :--------------------------------: | :-------------------------: | :-------------------------: | :-------------------------: | :--: | :--: |
|  a   |  b   |    a     | <font color="red">b</font> |      |          |          |          |                            |      |                                    |                                    |                                    |                             |                             |                             |      |  4   |
|      |      | <u>a</u> | <font color="red">b</font> |      |          |          |          |                            |      |                                    |                                    |                                    |                             |                             |                             |      |  1   |
|      |      |          |             a              |  b   |    a     |    b     |    a     | <font color="red">c</font> |      |                                    |                                    |                                    |                             |                             |                             |      |  6   |
|      |      |          |                            |      | <u>a</u> | <u>b</u> | <u>a</u> | <font color="red">b</font> |      |                                    |                                    |                                    |                             |                             |                             |      |  1   |
|      |      |          |                            |      |          |          | <u>a</u> | <font color="red">b</font> |      |                                    |                                    |                                    |                             |                             |                             |      |  1   |
|      |      |          |                            |      |          |          |          |             a              |  b   |                 a                  |                 b                  |                 a                  | <font color="red">c</font>  |                             |                             |      |  6   |
|      |      |          |                            |      |          |          |          |                            |      | <font color="blue"><u>a</u></font> | <font color="blue"><u>b</u></font> | <font color="blue"><u>a</u></font> | <font color="blue">b</font> | <font color="blue">a</font> | <font color="blue">c</font> |      |  3   |

> 下划线（例如 <u>a</u> ）代表 KMP 算法通过失败函数跳过的字符，即没有进行比较。

## Question 5

试证明霍夫曼编码的最优性。

**Proof** 原始论文 [A Method for the Construction of Minimum-Redundancy Codes (David A, Huffman, et al. 1952)](https://ieeexplore.ieee.org/abstract/document/4051119) 。

对于字符集合 $C = \{ c_1,\ c_2,\ \cdots,\ c_n \}$ 每个字符出现的频率为 $f(c_i)$ 。构造编码树 $T$ 是一个二叉树，叶子节点代表字符，路径代表 0 (Left) or 1 (Right) 。则字符 $c_i$ 的编码长度 $l(c_i)$ 为 $c_i$ 所在节点在 $T$ 中的深度。那么对这个字符集 $C$ 的编码树 $T$ 带来的期望编码总长为：
$$
L(T) = \sum\limits_{i=1}^n f(c_i) \cdot l(c_i)
$$
现在要证明：Huffman 编码树 $T_H$ 就是最优的，它使得 $L(T_H)$ 最小。

**引理 1** 在最优编码树 $T^*$ 中，频率最低的 2 个字符 $x$ 和 $y$ 一定位于最深的节点中，且他们拥有相同的父节点。

<u>证明 引理 1</u> 若字符 $z$ 比 $x$ 更深，但 $x$ 频率更低 $f(x) \leq f(z)$ 。那么交换 $x$ 和 $z$ 的节点位置，总编码期望长度 $L(T)$ 不增（因为频率低的字符变得更深）。这与 $L(T^*)$ 最优矛盾。同理，存在 2 个频率最低的字符 $x,\ y$ 那么他们肯定在同一层，否则将频率低的换到更深，长度不增，矛盾。$\square$

**引理 2** 将频率最低的两个字符 $x$ 和 $y$ 合并为一个新字符 $z$ ，新问题与原问题等价。

<u>证明 引理 2</u> 对于新问题：字符集 $C' = C - \{x,\ y\} + \{z\}$ 编码树为 $T'$ 。得到的最优解为 $T'^*$ 和最小编码长度 $L(T'^*)$ 。由引理 1 知，$x,\ y$ 位于同一节点下的兄弟节点，则有 $l(z) = l(x) + 1 = l(y) + 1$ ，而显然 $z$ 的频率是二者的和 $f(z) = f(x) + f(y)$ 。所以有：
$$
L(T) = L(T') + (l(z) - l(x)) \cdot f(z) = L(T') + f(x) + f(y)
$$
所以，当新问题 $B(T'^*)$ 最优时，原问题 $B(T^*)$ 也最优。$\square$

下面通过归纳法证明：Huffman 编码树 $T_H$ 是最优的

1. 当 $|C| = n = 2$ 时，显然 $T_H$ 最优，只有 $0$ 和 $1$ 两种情况；
2. 假设 $|C| = n$ 时，$T_H$ 是最优的；
3. 对于 $|C| = n + 1$ 时，我们选择频率最低的 2 个字符 $x$ 和 $y$ ，合并为 $z$ 组成新问题，此时字符集 $C'$ 满足 $|C'| = n$ ，通过归纳假设，新问题是最优的。

再由引理 2 知，新问题与原问题等价，故 Huffman 编码树 $T_H$ 是最优的。$\square$

## Question 6

请写出解决背包问题的动态规划算法。

**Solution** 

背包问题的数学模型：
$$
\max \quad z = \sum\limits_{i=1}^n\ C_i(x_i)
$$

$$
s.t. \quad \sum\limits_{i=1}^n\ a_i \cdot x_i \leq A,\quad x_i \in \N
$$

其中 $x_i$ 为第 $i$ 种物品装入背包的个数，为非负整数。$C_i(\cdot)$ 为第 $i$ 种物品的价值。$a_i$ 为单个第 $i$ 种物品的重量。$A$ 为背包限重。

动态规划：

- 阶段 $k$ ：$k = 1,\ 2,\ \cdots,\ n$ 表示第 $k$ 个阶段决策装第 $k$ 种物品。
- 状态变量 $s_{k+1}$ ：从第 $k+1$ 阶段开始，背包中允许装入前 $k$ 中物品的总重。
- 决策变量 $x_k$ ：第 $k$ 种物品装入背包的个数。
- 状态转移方程：$s_k = s_{k+1} - a_k\cdot x_k$
- 允许决策集合：$D_k(s_{k+1}) = \{ x_k | 0 \leq x_k \leq [\frac{s_{k+1}}{a_k}],\ x_k \in \N \}$
- 动态规划的递归方程：

$$
f_k(s_{k+1}) = \max\limits_{x_k \in D_k(s_{k+1})}\quad \{ C_k(x_k) + f_{k-1}(s_{k+1} - a_k\cdot x_k) \}
$$

其中 $f_0(s_1) = 0$ 为边界条件。
