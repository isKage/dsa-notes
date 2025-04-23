# 队列 Queue

本章介绍了队列 (Queue) 数据类型，并实现了队列的抽象数据类型 (Queue ADT) 。并基于**数组和链表**分别实现了**队列、循环队列和双端队列**。由于队列的先进先出性 (FIFO) 能够实现很多应用，本章介绍了两个实际问题的应用：1. 使用队列实现杨辉三角；2. 使用**栈+回溯法**实现了迷宫问题的路径寻找、使用**队列+洪水算法**实现了迷宫问题的最短路寻找。

## 1 队列的概念

**队列**：限制数据插入在一端进行、删除在另一端进行的特殊序列（FIFO）

- 允许插入的一端称为队尾，允许删除的一端称为队头
- 在队尾插入元素称为入队（enqueue），在队头删除元素称为出队（dequeue）
- 队列中元素个数称为队列的长度



## 2 队列的抽象数据类型

```python
ADT Queue {
	数据对象：Q = {Q1, Q2, ..., QN}
	基本操作：
		Q.enqueue(e): 		向队列 Q 的队尾添加一个元素
		Q.dequeue(): 		从队列 Q 中移除并返回第一个元素
		Q.first(): 			在不移除的前提下，返回队列的第一个元素
        len(Q): 			返回队列 Q 的长度
        Q.init(Q0): 		使用序列 Q0 初始化队列 Q
        Q.is_empty(): 		检查队列 Q 是否为空，如为空则返回 True
        Q.clear(): 			清空队列 Q
} ADT Queue
```

例如：下面给出了一个队列的例子和一些操作的影响

![队列操作例子](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1742524105408.png)



## 3 基于数组的队列实现

对于队列，可以使用**数组**的方式来实现队列：

- 潜在的问题：`append(e)` 高效，但 `pop()` 很低效。
- 解决方案：用一个变量存储当前队头元素的索引，用指针指向 `None` 表示数组中的离队元素。
- 缺点：存储队列的列表长度为 `O(m)` ，其中 m 为自队列创建以来追加元素操作的数量总和，可能远远大于队列长度。即列表可能长度不足，当队列满时，仍然需要进行动态序列扩展，效率会有所较低（摊销成本）。

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1742524506790.png)

例如：上面 `f` 指代了队列的头部，如果队列头部元素出队，则 `f` 指针后移，其前面的元素置空 `None` 从而实现出队操作。

### 3.1 循环使用数组

上面的方法会出现空间的浪费，例如 `f` 前面的出队后的空位，这部分的空间也可以利用起来。于是，**循环使用数组**的方法被发现。即：当新的元素入队时，如果列表在 `f` 的后面全满，则可以将新元素放在列表的头部（之前出队后空出的位置），这一个操作可以通过取模实现 `f = (f + 1) % N` 。

![循环使用数组](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1742524853272.png)

### 3.2 代码实现

```python
class Empty(Exception):
    """队列为空的异常类"""
    pass


class ArrayQueue:
    """FIFO 队列实现"""
    DEFAULT_CAPACITY = 10  # 默认数组长度

    def __init__(self):
        """初始化空队列，预留空间 DEFAULT_CAPACITY"""
        self._data = [None] * ArrayQueue.DEFAULT_CAPACITY  # 真实列表内存大小
        self._size = 0  # 队列大小
        self._front = 0  # 头指针

    def __len__(self):
        """返回长度"""
        return self._size

    def is_empty(self):
        """判断是否为空"""
        return self._size == 0

    def first(self):
        """返回第一个元素"""
        if self.is_empty():  # 是否为空
            raise Empty("Queue is empty")

        return self._data[self._front]  # 返回队列头部元素

    def dequeue(self):
        """从头部出队"""
        if self.is_empty():
            raise Empty("Queue is empty")

        answer = self._data[self._front]  # 获取出队元素值
        self._data[self._front] = None  # 出队位置置空
        self._front = (self._front + 1) % len(self._data)  # 循环利用数组
        self._size -= 1  # 长度减一
        return answer

    def enqueue(self, e):
        """队尾插入元素 e"""
        if self._size == len(self._data):
            # 如果列表已满，则增倍扩展数组
            self._resize(2 * len(self._data))

        avail = (self._front + self._size) % len(self._data)  # 队尾索引
        self._data[avail] = e
        self._size += 1

    def _resize(self, capacity):
        """空间为 capacity 新列表"""
        old = self._data  # 原始列表
        self._data = [None] * capacity  # 扩展后的空列表

        walk = self._front  # 队列的头部
        for k in range(self._size):
            self._data[k] = old[walk]  # 复制 old 到新的队列
            walk = (walk + 1) % len(old)  # old 是循环使用的
        self._front = 0  # 新队列的头部和列表的 0 (列表头部) 是对齐的

    @classmethod
    def from_list(cls, l):
        """从列表快速产生队列"""
        aq = cls()
        for e in l:
            aq.enqueue(e)
        return aq

    def __str__(self):
        """以列表形式展示"""
        tmp = []
        walk = self._front
        for _ in range(self._size):
            tmp.append(self._data[walk])
            walk = (walk + 1) % len(self._data)
        return str(tmp)

    def clear(self):
        """清空队列，保持当前容量，仅清除有效元素"""
        if not self.is_empty():  # 如果队列非空
            walk = self._front
            for _ in range(self._size):  # 遍历所有有效元素
                self._data[walk] = None  # 将元素置为 None
                walk = (walk + 1) % len(self._data)  # 循环数组
        self._size = 0  # 重置队列大小
        self._front = 0  # 重置头指针

    def __iter__(self):
        """返回一个迭代器，用于遍历队列中的元素"""
        walk = self._front  # 从队列的头部开始
        for _ in range(self._size):  # 遍历所有有效元素
            yield self._data[walk]  # 返回当前元素
            walk = (walk + 1) % len(self._data)  # 移动到下一个位置（循环数组）
```

### 3.3 算法分析

基于数组的队列实现，在不考虑数组的前提下， 都是常数级的复杂度。考虑数组的动态扩展，则在摊销成本下常数级的复杂度。

![基于数组实现队列的算法复杂度分析](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1742528402140.png)



## 4 基于单向链表的队列实现

这一部分可见链表章节的介绍 [Blog Link](https://blog.iskage.online/posts/9241942.html#1-7-单向链表实现队列) 或 [知乎链接](https://zhuanlan.zhihu.com/p/29508680467) 。代码实现见下：

```python
class LinkedQueue:
    """单向链表实现队列，先进先出"""

    # -------------- 嵌套的节点类 _Node --------------
    class _Node:
        """单向链表的节点，非公有，实现队列"""
        __slots__ = '_element', '_next'  # _Node 类只拥有这 2 个属性

        def __init__(self, element, next):
            self._element = element
            self._next = next

    # -------------- 正式实现队列 --------------
    def __init__(self):
        """初始化空队列"""
        self._head = None
        self._tail = None
        self._size = 0

    def __len__(self):
        """返回队列长度"""
        return self._size

    def is_empty(self):
        """检查是否为空队列"""
        return self._size == 0

    def first(self):
        """展示队列第一个元素值，但不改变队列"""
        if self.is_empty():
            raise Empty('Queue is empty')
        return self._head._element

    def dequeue(self):
        """删除并返回队列第一个节点和元素"""
        if self.is_empty():
            raise Empty('Queue is empty')

        ans = self._head._element  # 获取第一个元素值
        # 头指针指向下一个节点
        self._head = self._head._next
        self._size -= 1
        # 如果节点清空，则设置尾指针为空
        if self.is_empty():
            self._tail = None
        return ans

    def enqueue(self, e):
        """在尾部增加新节点"""
        newest = self._Node(e, None)
        if self.is_empty():
            self._head = newest  # 如果为空，则新节点为头节点
        else:
            self._tail._next = newest  # 否则尾节点的 next 指向新节点
        self._tail = newest  # 尾节点更新
        self._size += 1
```



## 5 循环队列

**轮转调度**程序：以循环的方式迭代地遍历一个元素的集合，并通过执行一个给定的动作为集合中的每个元素进行“服务”。

例如：在队列 `Q` 反复进行下面的步骤，即可轮转调度为每个元素都进行“服务”。

1. `e = Q.dequeue()` ：从队列取出元素 e （下一个元素出队）
2. `f(e)` ：为元素 e 提供服务、进行操作（“服务”下一个元素）
3. `Q.enqueue(e)` ：e 被重新加入队列尾部（所“服务”的元素入队）

利用循环链表实现循环队列见 [Blog Link](https://blog.iskage.online/posts/9241942.html#2-3-循环链表实现循环队列) 或 [知乎链接](https://zhuanlan.zhihu.com/p/29508680467) 。

```python
class LinkedCircularQueue:
    """循环链表实现循环队列"""

    # -------------- 嵌套的节点类 _Node --------------
    class _Node:
        """单向链表的节点，非公有，实现循环队列"""
        __slots__ = '_element', '_next'  # _Node 类只拥有这 2 个属性

        def __init__(self, element, next):
            self._element = element
            self._next = next

    # -------------- 正式实现队列 --------------
    def __init__(self):
        """初始化空队列"""
        self._tail = None  # 只需要一个指针
        self._size = 0

    def __len__(self):
        """返回长度"""
        return self._size

    def is_empty(self):
        """判断是否为空"""
        return self._size == 0

    def first(self):
        """展示队列第一个元素值 tail.next ，但不改变队列"""
        if self.is_empty():
            raise Empty('Queue is empty')
        # 对循环链表而言，定义尾指针指向节点的下一个节点为头节点
        head = self._tail._next
        return head._element

    def dequeue(self):
        """删除并返回队列头节点 tail.next 和元素"""
        if self.is_empty():
            raise Empty('Queue is empty')

        oldhead = self._tail._next  # 获取头节点
        if self._size == 1:
            self._tail = None  # 只有一个节点，删除后变成空队列
        else:
            self._tail._next = oldhead._next
            # 原来的 tail.next 即 oldhead 被释放，因为没有指针指向它
        self._size -= 1
        return oldhead._element

    def enqueue(self, e):
        """在尾部 tail 增加新节点"""
        newest = self._Node(e, None)
        if self.is_empty():
            # 如果为空，则新节点自己指向自己，后面再由 tail 指向 newest
            newest._next = newest
        else:
            newest._next = self._tail._next  # 新节点指向头节点
            self._tail._next = newest  # 原来的尾节点的 next 指针指向新节点
        self._tail = newest  # 尾节点更新
        self._size += 1

    def rotate(self):
        """训练轮转一次"""
        if self.is_empty():
            raise Empty('Queue is empty')
        self._tail = self._tail._next  # 指示指针 (尾指针) tail 向后移动一位
```



## 6 双端队列

### 6.1 双端队列的概念和抽象数据类型

**双端队列**：类队列数据结构，支持在队列的头部和尾部都进行插入和删除。双端队列被称为 `deque` 。

```python
ADT Deque {
     数据对象：D = {D1, D2, ..., DN}
     基本操作：
		D.add_first(e): 		向双端队列 D 的队头添加一个元素
        D.add_last(e): 			向队列 D 的队尾添加一个元素
        D.delete_first(): 		从双端队列 Q 中移除并返回第一个元素
        D.delete_last(): 		从双端队列 Q 中移除并返回最后一个元素
        D.first(): 				在不移除的前提下，返回双端队列的第一个元素
        D.last(): 				在不移除的前提下，返回双端队列的最后一个元素
        len(D): 				返回双端队列 D 的长度
         D.init(D0): 			使用序列 D0 初始化队列 D
        D.is_empty(): 			检查双端队列 D 是否为空，如为空则返回 True
        D.clear(): 				清空队列 D
} ADT Deque
```

### 6.2 基于双向链表实现双端队列

详细的搭建可见 [Blog Link](https://blog.iskage.online/posts/9241942.html#3-双向链表) 或 [知乎链接](https://zhuanlan.zhihu.com/p/29508680467) 。

先实现双向链表的基础类 `_DoublyLinkedBase`

```python
class _DoublyLinkedBase:
    """双向链表的基础类/父类"""

    # -------------- 嵌套的节点类 _Node --------------
    class _Node:
        """双向链表的节点类，包含元素值、prev 指针和 next 指针"""
        __slots__ = '_element', '_prev', '_next'

        def __init__(self, element, prev, next):
            self._element = element
            self._prev = prev
            self._next = next

    # -------------- 正式实现链表 --------------
    def __init__(self):
        """初始化一个空链表"""
        # 创建头哨兵、尾哨兵
        self._header = self._Node(None, None, None)
        self._trailer = self._Node(None, None, None)

        self._header._next = self._trailer  # 头哨兵 next 指向尾哨兵
        self._trailer._prev = self._header  # 尾哨兵 prev 指向头哨兵

        self._size = 0  # 链表长度，不包括头尾哨兵

    def __len__(self):
        """链表长度 len() 重载"""
        return self._size

    def is_empty(self):
        """判断是否为空"""
        return self._size == 0

    def _insert_between(self, e, predecessor, successor):
        """在节点 predecessor, successor 插入插入新节点，并返回这个新节点"""
        # 创建新节点，并将其 prev 指向 predecessor | 其 next 指向 successor
        newest = self._Node(e, predecessor, successor)

        predecessor._next = newest  # predecessor 的 next 指向新节点
        successor._prev = newest  # successor 的 prev 指向新节点

        self._size += 1
        return newest

    def _delete_node(self, node):
        """传入节点并删除，返回被删除的值"""
        # 记录将被删除的节点的前后信息
        predecessor = node._prev
        successor = node._next
        # 连接 predecessor 和 successor
        predecessor._next = successor
        successor._prev = predecessor

        element = node._element
        # 孤立节点 node : 设为空，用于标识这是即将被删除的节点
        node._prev, node._next, node._element = None, None, None

        self._size -= 1
        return element
```

再实现双向队列 `LinkedDeque` ，基础父类 `_DoublyLinkedBase`

```python
class LinkedDeque(_DoublyLinkedBase):
    """双向链表实现双端队列"""

    # -------------- 继承父类 --------------
    """不需要定义 `__init__` `__len__` `is_empty` 方法"""

    # -------------- 添加双端队列的功能 --------------
    def first(self):
        """获取第一个元素的值，注意头节点是哨兵，没有值"""
        if self.is_empty():
            raise Empty('Deque is empty')

        return self._header._next._element

    def last(self):
        """获取最后一个元素的值，注意尾节点是哨兵，没有值"""
        if self.is_empty():
            raise Empty('Deque is empty')

        return self._trailer._prev._element

    def insert_first(self, e):
        """在头部插入元素"""
        # 直接调用父类 _insert_between 方法，在头哨兵和第一个元素节点之间插入
        return self._insert_between(e, self._header, self._header._next)

    def insert_last(self, e):
        """在尾部插入元素"""
        # 直接调用父类 _insert_between 方法，在最后一个元素节点和尾哨兵之间插入
        return self._insert_between(e, self._trailer._prev, self._trailer)

    def delete_first(self):
        """删除第一个元素"""
        if self.is_empty():
            raise Empty('Deque is empty')

        # 直接调用父类 _delete_node 方法，删除头节点的下一个节点
        return self._delete_node(self._header._next)

    def delete_last(self):
        """删除最后一个元素"""
        if self.is_empty():
            raise Empty('Deque is empty')

        # 直接调用父类 _delete_node 方法，删除尾节点的上一个节点
        return self._delete_node(self._trailer._prev)
```



## 7 队列的实际应用

### 7.1 杨辉三角

```python
def YanghuiTri(n):
    """杨辉三角队列实现"""
    TriQ = ArrayQueue()

    # 第一行
    TriQ.enqueue(1)
    print('1'.center(5 * n))

    # 每一次队列中仅仅保存上一行的数据
    for m in range(2, n + 1):  # 第 2 到 n 行
        Line = '1'  # 展示这一行的结果（字符串形式）
        TriQ.enqueue(1)
        p = TriQ.dequeue()

        # 取上一行的两个元素进行加和，放在队尾
        for k in range(2, m):
            q = TriQ.dequeue()
            TriQ.enqueue(p + q)
            Line += ' ' + str(p + q)
            p = q
        TriQ.enqueue(1)
        Line += ' ' + '1'
        print(Line.center(5 * n))
```

```python
if __name__ == '__main__':
    YanghuiTri(7)
    
# 			   1                 
#             1 1                
#            1 2 1               
#           1 3 3 1              
#          1 4 6 4 1             
#        1 5 10 10 5 1           
#       1 6 15 20 15 6 1      
```

### 7.2 迷宫问题

考虑一个长为 M 宽为 N 的迷官。其入口在 `(1, 1)` 处，出口在 `(M, N)` 处。例如，下图中 `M = N = 5` 。请设计一个算法，找到一条从入口到出口的路（也可能没有这样的路），并给出其运行的时间复杂度。

问题一：找出一条可能的路径（栈 ｜ 回溯法）

问题二：找出最短的路径（队列 ｜ 洪水算法）

![迷宫问题样例](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1742550035394.png)

#### 7.2.1 利用栈：回溯法

回溯法的主要想法是**深度优先**，即一直走知道无路可走再回退。

考虑用栈来实现这个问题，每次存入经过的格子的坐标 `(i, j)` ，除去来时的路，下一步有 3 种走法，然后继续将新的位置压入栈。每次进行下一步都要检查是否为墙/是否在栈中，当无路可走时，将栈顶元素出栈，继续寻找。

有关栈的抽象数据类型见 [Blog Link](https://blog.iskage.online/posts/c69bd6a6.html) 或 [知乎链接](https://zhuanlan.zhihu.com/p/30420213013) 。代码实现迷宫问题见下：

```python
def maze_path(maze, M, N):
    """找出一条可能的路径: 栈 ｜ 回溯法"""
    # 初始化栈
    stack = ArrayStack()

    stack.push((1, 1))  # 起始点入栈
    visited = set()  # 已经走过的路
    visited.add((1, 1))  # 起始点入路

    # 定义四个方向：左、右、上、下
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    # 最后栈空说明无解
    while not stack.is_empty():
        current = stack.top()  # 栈顶元素

        if current == (M, N):  # 到达终点
            path = [None] * len(stack)
            i = len(stack) - 1
            while not stack.is_empty():
                path[i] = stack.pop()
                i -= 1
            return path  # 返回路径

        found = False  # 是否找到新的位置可走
        for d in directions:
            i, j = current[0] + d[0], current[1] + d[1]  # 新位置

            # 检查新坐标是否未访问，且是否是通路
            if maze[i][j] == 0 and (i, j) not in visited:
                stack.push((i, j))  # (i, j) 通路且不在之前的路中
                visited.add((i, j))  # 入路，保证未来不会重走
                found = True  # 找到下一步
                break

        if not found:
            # 无路可走则回溯
            stack.pop()

    return None  # 无解
```

例如：使用 `1` 代表墙，即不可走；`0` 表示可以走。最外围的 `1` 只是为了表示边界，减少对边界判断的繁琐工作。	

```python
if __name__ == '__main__':
    # M = N = 5 外面一圈 1 为了方便表示边界
    maze = [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1]
    ]

    ans = maze_path(maze, len(maze) - 2, len(maze[0]) - 2)
    print(ans)
```

结果为：

```python
[(1, 1), (2, 1), (2, 2), (2, 3), (1, 3), (1, 4), (1, 5), (2, 5), (3, 5), (3, 4), (4, 4), (5, 4), (5, 5)]
```

**算法分析** ：按照回溯法，每个位置最多被首次访问一次并入栈，被回溯一次并出栈。在此之间，最多探索该位置周围的位置三次（即常数次操作）故复杂度为 `O(MN)` 。

#### 7.2.2 利用队列：洪水算法

洪水算法主要思想是**广度优先**，即保存每一步可能的所有情况，最后先出最短的路。

我们可以使用队列，从 `(1, 1)` 开始，重复以下操作：取出队头元素，将队头元素可以到达但并未走过的相邻点放入队列，并记录下从队头元素可以立即到达某一相邻点这一信息：

- ﻿如最终抵达终点，则已找到最短路，可根据之前记录的信息复原出这条路。
- ﻿否则，如最终队列为空，则不存在这样的路。

代码实现：

```python
def maze_shortest_path(maze, M, N):
    """找出最短的路径: 队列 ｜ 洪水算法"""

    def backtrack_path(parent: dict, start: tuple, end: tuple):
        """从 end 回溯到 start，生成路径"""
        path = []
        current = end
        while current != start:
            path.append(current)
            current = parent[current]  # 找到当前点的父节点
        path.append(start)  # 添加起点
        path.reverse()  # 反转路径，使其从 start 到 end
        return path

    queue = ArrayQueue()
    queue.enqueue((1, 1))
    parent = {}  # 记录当前点的上一个点位置

    # 定义四个方向：左、右、上、下
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    while not queue.is_empty():
        current = queue.dequeue()  # 当前位置
        maze[current[0]][current[1]] = 2  # 记当前位置为 2 放置重复走

        if current == (M, N):  # 在广度优先下，最先找到终点，即为最短路径
            return backtrack_path(parent, (1, 1), (M, N))

        for d in directions:  # 四个方向都要考虑并入队
            i, j = current[0] + d[0], current[1] + d[1]
            if maze[i][j] == 0 and maze[i][j] != 2:  # 不是墙/且不重复
                queue.enqueue((i, j))  # 入队
                parent[(i, j)] = current  # 记录当前点的上一个点

    return None  # 无解
```

例如：仍然是上面的例子，最短路应该为从左边到底然后向右

```python
if __name__ == '__main__':
    # M = N = 5 外面一圈 1 为了方便表示边界
    maze = [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1]
    ]

    ans = maze_path(maze, len(maze) - 2, len(maze[0]) - 2)
    print(ans)

    shortest_ans = maze_shortest_path(maze, len(maze) - 2, len(maze[0]) - 2)
    print(shortest_ans)
```

```python
"""Output"""
# 利用栈：回溯法，不是最短
[(1, 1), (2, 1), (2, 2), (2, 3), (1, 3), (1, 4), (1, 5), (2, 5), (3, 5), (3, 4), (4, 4), (5, 4), (5, 5)]

# 利用队列：洪水算法，最短路
[(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5)]
```

**算法分析**：每个位置最多被放入队列一次、出队一次，﻿﻿算法复杂度 `O(MN)` 。











