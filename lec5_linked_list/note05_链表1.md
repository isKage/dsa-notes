# 链表 (1) 单向链表、循环链表与双向链表

数组因为其紧凑的内存空间分配，使得其在索引时非常高效，但是却浪费了许多空间，它存储了远大于实际实例所需的空间。相对应的，**链表**数据结构依赖于分布式表达方法，采用节点的方式，不连续的存放数据。

本周讲解的链表实现了栈、队列、双端队列三种数据结构。它们的特点就是：可以在头部或者尾部进行插入或删除操作，无法在任意位置进行耗时为常数的操作。

## 1 单向链表

### 1.1 单向链表概念

单向链表是由多个节点共同构成的一个线性序列，从头指针开始，每个节点存储：元素值和下一个节点的指针。

<img src="https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1741601117586.png" alt="每一个节点的示意图" style="zoom:50%;" />

- 单向链表的第一个节点为头节点，最后一个节点为尾节点。
- 头指针 `head` 指向头节点，尾指针 `tail` 指向尾节点，且尾节点指向下一节点的指针为空指针。
- 从头指针开始，通过每个节点的next指针可以到达下一个节点，直至到达尾指针，完成对链表的遍历。

![一个单向链表的示意](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1741601218479.png)

### 1.2 在单向链表头部插入元素

链表由一个一个的节点组成，所以不需要预先分配空间，十分灵活。但是对链表的操作要十分谨慎，必须保留相关的指针。例如：对单向链表而言，丢失一个节点的信息，该节点之后的所有信息都会丢失。

以在单向链表头部插入元素为例：先建立新的节点，新节点的 `next` 指针指向原链表的头节点，头指针指向最新的节点，链表长度加一。

- 伪代码

```python
Algorithm add_first(L, e):
	newest = Node(e)           # 1. 建立新的节点
	newest.next = L.head 	   # 2. 新节点的 `next` 指针指向原链表的头节点
	L.head = newest			   # 3. 头指针指向最新的节点
	L.size = L.size + 1		   # 4. 链表长度加一
```

- 图示

<img src="https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1741611806111.png" alt="在链表头部插入元素" style="zoom:100%;" />

### 1.3 在单向链表尾部插入元素

当保存了尾指针时，可以容易的在尾部插入元素：首先创建一个新节点，将新节点 `next` 指针设为空，然后设置原链表最后一个节点的 `next` 指针指向新节点，最后设置尾指针指向新节点，链表长度加一。

> 一定要先将原链表最后一个节点的 `next` 指针指向新节点，再设置尾指针指向新节点。否则会丢失原链表的信息！！！

- 伪代码

```python
Algorithm add_last(L, e):
	newest = Node(e)           	# 1. 创建一个新节点
	newest.next = None			# 2. 将新节点 `next` 指针设为空
	L.tail.next = newest		# 3. 设置原链表最后一个节点的 `next` 指针指向新节点
	L.tail = newest				# 4. 设置尾指针指向新节点
	L.size = L.size + 1			# 5. 链表长度加一
```

- 图示

<img src="https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1741612913677.png" alt="在单向链表尾部插入元素" style="zoom:100%;" />

### 1.4 从单向链表头部删除元素

与在单向链表的头部插入元素相反，从单向链表头部删除元素：将头指针直接指向头节点的下一个节点，然后链表长度减一，这样运来的头指针信息丢失，空间被释放。

> 最后一步的空间释放，在 Python 中无需手动进行，Python 采用**引用计数**管理，当对象的引用计数归零时（即没有变量名保存这个对象的地址时），Python 会自动释放空间。
>
> 但对于其他语言，例如 C 语言，链表的删除需要手动释放内存。

- 伪代码

```python
Algorithm remove_first(L):
	if L.head is None then
		# 链表本身为空

	L.head = L.head.next		# 1. 头指针直接指向头节点的下一个节点
	L.size = L.size - 1			# 2. 链表长度减一
```

- 图示

![从单向链表头部删除元素](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1741613592560.png)

### 1.5 从单向链表尾部删除元素？

即使保留了尾指针，也无法在常数 `O(1)` 时间内删除尾节点。因为根据单向链表的组成原理，删除尾节点，必须知道倒数第二个节点的信息。但想得到倒数第二节点的信息，必须要遍历整个链表，复杂度为 `O(n)` ，这是很低效的，在后面的双向链表里可以快速实现。

### 1.6 单向链表实现栈

**栈**是由一系列对象组成的一个集合，这些对象的插入和删除操作遵循后进先出（LIFO）的原则。用户可以在任何时刻向栈中插入一个对象，但只能取得或者删除最后一个插人的对象（即所谓的“栈顶”）。

因为栈满足后进先出的原则，如果我们假定栈顶是头节点，则不需要尾指针也能实现栈的功能。

首先实现各个节点的定义 `class _Node` 表示这是非公有的。`_Node` 嵌套在最终的链表栈类中。

```python
class _Node:
    """单向链表的节点，非公有，实现栈"""
    __slots__ = '_element', '_next'  # _Node 类只拥有这 2 个属性

    def __init__(self, element, next):
        self._element = element
        self._next = next
```

> 为了提高内存的利用率，定义`__slots__` 。指定一个节点只有两个实例变量：`_element` 和 `_next`（元素引用和指向下一个节点的引用）。

下面是完整的链表栈类的实现：

```python
class LinkedStack:
    """单向链表实现栈"""

    # -------------- 嵌套的节点类 _Node --------------
    class _Node:
        """单向链表的节点，非公有，实现栈"""
        __slots__ = '_element', '_next'  # _Node 类只拥有这 2 个属性

        def __init__(self, element, next):
            self._element = element
            self._next = next

    # -------------- 正式实现栈 --------------
    def __init__(self):
        """初始化空栈"""
        self._head = None  # 头指针，指向节点，初始化为空
        self._size = 0  # 元素个数

    def __len__(self):
        """栈元素个数 len(obj) 重载"""
        return self._size

    def is_empty(self):
        """检查是否为空"""
        return self._size == 0

    def push(self, e):
        """向栈顶部增加元素"""
        # 新建节点，指向旧的 head 新的 head 指向新节点
        self._head = self._Node(e, self._head)
        self._size += 1

    def top(self):
        """返回栈顶值，但不改变链表"""
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._head._element

    def pop(self):
        """删除并返回栈顶元素"""
        if self.is_empty():
            raise Empty('Stack is empty')
        ans = self._head._element
        # 删除头部节点
        self._head = self._head._next
        self._size -= 1
        return ans
```

> 其中 `Empty` 类可以定义为

```python
class Empty(Exception):
    """Raised when a value is an empty list."""
    pass
```

对于使用链表方式实现的栈，插入和删除元素都是常数时间完成的，这是相对于数组而言更高效的性质：

![单向链表实现栈的时间复杂度](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1741669388492.png)

### 1.7 单向链表实现队列

**队列**与栈类似，由一系列对象组成的集合，这些对象的插入和删除遵循先进先出（First in First out, FIFO）的原则。也就是说，元素在尾部插入，但是只有处在队列最前面的元素才能被删除。

因为队列的操作需要对头和尾操作，所以需要 `head` 头指针和 `tail` 尾指针。将头节点作为队列的头部，尾指针作为尾部，这样就满足可以在头部删除元素，在尾部插入元素。（因为对单向链表而言，尾部删除元素是复杂的）。

实现代码：

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

使用单向链表实现队列的时间复杂度也是常数。



## 2 循环链表

### 2.1 循环链表概念

在链表中，我们可以使链表的尾节点的 `next` 指针指向链表的头部，由此来获得一个**循环链表**。

![循环链表图示](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1741673718987.png)

在循环链表中，头指针和尾指针并不常用。相反，从任意一个节点都能进入这个循环链表。例如：使用 `current` 指针指向一个节点，则使用 `current.next` 理论上可以取到任意一个节点。

![current 指针取循环链表节点](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1741673829874.png)

### 2.2 轮转调度

轮转调度程序：以循环的方式迭代地遍历一个元素的集合，并通过执行一个给定的动作为集合中的每个元素进行“服务”。

例如：在队列 `Q` 反复进行下面的步骤，即可轮转调度为每个元素都进行“服务”。

1. `e = Q.dequeue()` ：从队列取出元素 e （下一个元素出队）
2. `f(e)` ：为元素 e 提供服务、进行操作（“服务”下一个元素）
3. `Q.enqueue(e)` ：e 被重新加入队列尾部（所“服务”的元素入队）

![队列实现轮转调度示意](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1741674177792.png)

如果使用之前的单向链表，每次取出元素进行操作和插入元素都十分浪费时间。但使用循环链表实现，可以定义一个 `rotate()` 方法，将头部元素 `Q.front()` 服务完成后直接移动到尾部。即重复一下步骤即可实现轮转调度：

1. `f(Q.front)` ：取出头部元素进行操作/服务
2. `Q.rotate()` ：将其直接移动到尾部

### 2.3 循环链表实现循环队列

使用前面的链表实现队列的代码，但修改尾指针，使得尾指针指向头节点，于是可以舍弃头指针。

- 在这个循环类 `CircularQueue` 中，定义 `tail` 指针目前的位置为尾部，而 `tail.next` 为头部。
- 同时为循环链表类增加一个 `rotate()` 方法，将队首移到队尾，相当于 `tail = tail.next` 更新。

代码实现

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



## 3 双向链表

### 3.1 双向链表概念

**双向链表**：为了提供更好的对称性，我们定义了一个链表，**每个节点都维护了指向其先驱节点以及后继节点的引用**。这样的结构被称双向链表。这些列表支持更多各种时间复杂度为 `O(1)` 的更新操作，这些更新操作包括在列表的任意位置插入和删除节点。用 `next` 表示指向当前节点的后继节点的引用，并引入 `prev` 引用其前驱节点。

为了更方便的引用，在链表的起始位置添加头节点 `header` ，在链表的尾部添加尾节点 `trailer` ，它们并不存储数据，仅仅为链表操作的方便和一些特殊情况，存储链表的头尾信息。称之为**头哨兵**和**尾哨兵**。

![完整的双向链表图示](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1741678367710.png)

- 使用哨兵结构可以简单地处理一些操作。因为每次改变链表只是改变头尾节点的中间部分，而中间部分因为头尾节点的存在变得地位相同，可以采用相同的操作进行处理。例如之前，插入和删除元素还要区分头、尾、中间三部分，现在有了哨兵结构，所有节点都可以采用通适的方法。

### 3.2 双向链表的插入与删除

因为引入了哨兵结构，所以每个节点都是相同的，即使是第一个和最后一个有值的节点也与中间节点相同。

**插入元素图示**

![在具有哨兵结构的双向链表的中间插入元素](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1741680651867.png)

![在具有哨兵结构的双向链表的头部插入元素](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1741680686846.png)

从上面两个的图示可以发现，把 `header` 和 `trailer` 指向的头尾哨兵节点当作普通元素，即可无论是在头部插入还是中间插入，本质上是一样的。

**删除元素图示**

![在具有哨兵结构的双向链表删除一个元素](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1741680740987.png)

### 3.3 双向链表的基本实现

虽然广泛意义的链表的插入和删除已经可以在双向链表中实现，但索引插入和删除的位置却是链表难以高效解决的。对于基于数组的序列而言，利用整数索引非常迅速；但对于链表，由于其不连续的内存空间，无法在常数时间内索引节点，只能逐个遍历。

所以下面**双向链表的基本实现**的插入和删除暂不考虑索引的问题，而是假设如下条件，直接进行操作：

- 假设已知插入节点的前一个和后一个节点的地址
- 假设已知被删除节点的地址

定义用于双向链表的节点类 `_Node` ，同样也是非公有的：

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

`_DoublyLinkedBase` 类是一个非公有类，其目的是作为被继承的父类所定义。其定义了：

1. 双向链表的节点类 `_Node`
2. 初始化了双向链表 `__init__`
3. 定义了如何取链表长度 `__len__` ，这是重载了运算符 `len()`
4. 定义了如何判断链表是否为空 `is_empty`
5. 给出了非公有方法 `_insert_between()` 实现了当给前一个和后一个节点时，如何在它们中间安全地插入新节点，同时返回这个新的节点地址。之后的子链表类可以继承使用。
6. 给出了非公有方法 `_delete_node()` 实现了当给一个节点，如何安全地删除这个节点，返回被删除的节点存储的值。之后的子链表类可以继承使用。

### 3.4 双向链表实现双端队列

**双端队列**：支持在队列的头部和尾部都进行插人和删除操作。这样一种结构被称为双端队列（double-ended queue 或者 `deque`）。

基于上面定义的基础双向链表类 `_DoublyLinkedBase` ，可以实现双端队列。因为继承了父类，所以新的双端队列链表类 `LinkedDeque` 不需要定义 `__init__` `__len__` `is_empty` 方法。

**代码实现**

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

> 需要注意的是，队列的头尾存储着两个空值的节点，即哨兵指针。所以在进行操作时，需要注意传入的节点。





















