# 排序算法与选择

本章详细介绍排序算法，包括：归并排序、快速排序、排序下界、桶排序、字典序排序的知识。

排序（sorting）算法是一类重要算法，已被众多学者充分研究过，且在实践中有重大价值：

- 许多解决不同问题的算法均依赖于排序算法的实现

- 数据分析与处理中经常会用到排序算法

Python对排序提供 list 类的 sort 及对任意元素集合的 sorted 函数。这些函数使用高度优化后的高级排序算法。学习排序算法后可以对这些函数的效率有直观的认知。

之前已经介绍过了插入排序、选择排序、冒泡排序和高级排序方法——堆排序。

> 【补充】冒泡排序：
>
> 假设序列为 $a_1, a_2, ..., a_n$ 
>
> 第一次扫描：从序列尾向序列头进行，比较相邻两个元素的大小，如出现逆序 $a_j > a_j+1$ 则交换两个元素（第一次扫描结束后，最小的元素被排在第一位）；第二次扫描：依然从序列尾向序列头进行，出现逆序则交换相邻元素，一直进行到第二个元素为止
>
> 如此下去，最终即可排序整个序列。最坏的情况下（完全逆序）需要交换 $\sum_{i=1}^{n-1} n-i \sim O(n^2)$ 。

## 1 归并排序

### 1.1 分治法

接下来描述的两个算法（归并排序和快速排序）均由分治法思想产生。**分治法（Divide-and-Conquer）**是一种通用的算法设计范式：

- 分解（Divide）：如输入数据 S 规模较小则直接解决；否则，将其分成两个或多个互斥子集 S1, S2, ...
- 解决子问题（Conquer）：递归解决与子集相关的子问题

- 合并（Combine）：将子问题 S1, S2, ... 的解合并为 S 的解

### 1.2 归并排序

**归并排序（merge-sort）**基于分治法思想。在有 n 个元素的序列 S 上执行归并排序的过程如下：

- 分解（Divide）：当序列 S 长度大于 1 时，将其分为两个长度大致为 n/2 的子序列 S1 和 S2
- 解决子问题（Conquer）：递归地对 S1 和 S2 进行排序
- 合并（Combine）：将排好序的 S1 和 S2 合并为一个有序的序列

归并排序伪代码：

```python
Algorithm mergeSort(S)
	Input sequence S with n elements 
	Output sequence S sorted
	
    if S.size() > 1
		(S1, S2) = partition(S, n/2)  	# 拆分
        mergeSort(S1)					# 递归排序
        mergeSort(S2)
		S = merge(S1, S2)				# 合并
```

在归并排序的最后一步（合并）中，需要将两个有序序列 A 和 B 合并为一个有序序列 S 这一合并操作的时间复杂度为 **O(n)** 。

合并操作的伪代码：

```python
Algorithm merge(A, B)
	Input sequences A and B with n/2 elements each 
	Output sorted sequence of A + B

    S = empty sequence
	while not A.isEmpty() and not B.isEmpty()
		if A.first().element() < B.first().element()
			S.addLast(A.remove(A.first()))				# 从小到大插入
		else
			S.addLast(B.remove(B.first()))
	
    while not A.isEmpty() 								# 将剩余部分插入
		S.addLast(A.remove(A.first()))
	while not B.isEmpty()
		S.addLast(B.remove(B.first()))
	return S
```

### 1.3 归并排序树

归并排序的执行过程可以用一棵二叉树很好地表示，我们称之为**归并排序树（merge-sort tree）**

- 归并排序树的每一个节点代表一次递归调用
- 根节点：首次调用归并排序的位置
- 叶子节点表示：对长为 0 或 1 对序列进行排序

![归并排序的例子](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746362404181.png)

### 1.4 Python 实现

#### 1.4.1 基于数组的归并排序

下面的代码是基于数组的归并排序方法：

```python
def merge(S1: list, S2: list, S: list) -> None:
    """
    合并数组/序列 S1 S2 返回新的数组/序列
    :param S1: 顺序序列 S1
    :param S2: 顺序序列 S2
    :param S: 用于存储最终合并的结果，按照从小到大排序的序列
    :return: None
    """
    i = j = 0
    while i + j < len(S):
        if j == len(S2) or (i < len(S1) and S1[i] < S2[j]):
            S[i + j] = S1[i]  # copy i th element of S1 as next item of S
            i += 1
        else:
            S[i + j] = S2[j]  # copy j th element of S2 as next item of S
            j += 1


def merge_sort(S: list) -> None:
    """
    对序列 S 进行归并排序，直接修改原序列
    :param S: 等待排序的序列
    :return: None
    """
    n = len(S)
    if n < 2:
        return  # list is already sorted

    # divide
    mid = n // 2
    S1 = S[0:mid]  # copy of first half
    S2 = S[mid:n]  # copy of second half

    # conquer (with recursion)
    merge_sort(S1)  # sort copy of first half
    merge_sort(S2)  # sort copy of second half

    # merge results
    merge(S1, S2, S)  # merge sorted halves back into S
```

测试：

```python
if __name__ == '__main__':
    S = [85, 24, 63, 45, 17, 31, 96, 50]
    print("=" * 15, "Original List", "=" * 15)
    print(S)

    print("=" * 15, "After Sorted", "=" * 15)
    merge_sort(S)
    print(S)
```

```python
=============== Original List ===============
[85, 24, 63, 45, 17, 31, 96, 50]
=============== After Sorted ===============
[17, 24, 31, 45, 50, 63, 85, 96]
```

#### 1.4.2 基于链表的归并排序

可以借助之前实现的“基于链表的队列”存储数据，实现归并排序。 `LinkedQueue` 类的定义见 [code: LinkedQueue](https://github.com/isKage/dsa-notes/blob/main/lec11_sort_select/utils/linked_queue.py) ，归并排序实现代码见下。

```python
from utils import LinkedQueue


def merge(S1: LinkedQueue, S2: LinkedQueue, S: LinkedQueue):
    """合并链表 (利用链表队列) 返回顺序链表队列"""
    while not S1.is_empty() and not S2.is_empty():
        if S1.first() < S2.first():
            S.enqueue(S1.dequeue())
        else:
            S.enqueue(S2.dequeue())

    while not S1.is_empty():
        # move remaining elements of S1 to S
        S.enqueue(S1.dequeue())
    while not S2.is_empty():
        # move remaining elements of 52 to S
        S.enqueue(S2.dequeue())


def merge_sort(S: LinkedQueue):
    """对链表使用归并排序"""
    n = len(S)
    if n < 2:
        return  # list is already sorted

    # divide
    S1 = LinkedQueue()
    S2 = LinkedQueue()
    while len(S1) < n // 2:  # move the first n//2 elements to S1
        S1.enqueue(S.dequeue())
    while not S.is_empty():  # move the rest to S2
        S2.enqueue(S.dequeue())

    # conquer (with recursion)
    merge_sort(S1)  # sort first half
    merge_sort(S2)  # sort second half

    # merge results
    merge(S1, S2, S)  # merge sorted halves back into S
```

测试：

```python
if __name__ == '__main__':
    S = LinkedQueue()
    S.from_list([45, 24, 85, 63, 50, 31, 96, 17])
    print("=" * 15, "Original List", "=" * 15)
    print(S)  # LinkedQueue 已经定义了 __str__ 方法

    print("=" * 15, "After Sorted", "=" * 15)
    merge_sort(S)
    print(S)
```

```python
=============== Original List ===============
[45, 24, 85, 63, 50, 31, 96, 17]
=============== After Sorted ===============
[17, 24, 31, 45, 50, 63, 85, 96]
```

#### 1.4.3 基于数组的非递归归并排序

自底向上的非递归的归并排序：这是基于数组的归并排序，实践中一般比普通归并排序更快。

这种算法的主要思想是执行自底向上的归并排序，即对整个归并排序树自底向上逐层执行合并。给出元素的一个输入数组，我们将每个连续的元素对合并成有序的，以长度为 2 开始执行。然后再合并至长度为 4 、长度为 8 等，以此类推，直到整个数组已经排序完毕。

```python
import math


def merge(src, result, start, inc):
    """合并序列 src[start : start + inc] 和 src[start + inc : start + 2 * inc] 到 result 里"""
    end1 = start + inc  # 序列 1 的在原序列的结束索引
    end2 = min(start + 2 * inc, len(src))  # 序列 2 的在原序列的结束索引

    x, y = start, start + inc  # x, y 代表被合并的序列的当前索引
    z = start  # z 代表合并后的序列的当前索引

    # 从小到底复制到合并后的序列中
    while x < end1 and y < end2:
        if src[x] < src[y]:
            result[z] = src[x]
            x += 1
        else:
            result[z] = src[y]
            y += 1
        z += 1  # 继续

    # 将剩余的值放入合并后的序列
    if x < end1:
        result[z:end2] = src[x:end1]
    elif y < end2:
        result[z:end2] = src[y:end2]


def merge_sort(S):
    """对序列 S 进行原地归并排序"""
    n = len(S)
    logn = math.ceil(math.log(n, 2))  # log_2 n
    src, dest = S, [None] * n  # dest 用于存储结果

    for i in [2 ** k for k in range(logn)]:  # 2, 4, 8, 16, ..., n
        for j in range(0, n, 2 * i):
            merge(src, dest, j, i)  # 自底向上合并

        # 获取结果
        src, dest = dest, src

    if S is not src:
        S[0:n] = src[0:n]  # 传入最后排序后的结果
```

测试：

```python
if __name__ == '__main__':
    S = [85, 24, 63, 45, 17, 31, 96, 50]
    print("=" * 15, "Original List", "=" * 15)
    print(S)

    print("=" * 15, "After Sorted", "=" * 15)
    merge_sort(S)
    print(S)
```

```python
=============== Original List ===============
[85, 24, 63, 45, 17, 31, 96, 50]
=============== After Sorted ===============
[17, 24, 31, 45, 50, 63, 85, 96]
```

### 1.5 算法分析

归并排序树的高度 h = O(log n) 。在深度为 i 的一层所需的时间为 O(n) 。我们对长度为 $n / 2^i$ 的 $2^i$ 个序列进行合并，并进行 $2^i+1$ 次递归调用。因此，归并排序的运行时间为 **O(n log n)** 。

![归并排序的时间复杂度](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746363258879.png)



## 2 快速排序

### 2.1 快速排序

**快速排序（quick-sort）**是一种基于分治法的随机排序算法，在序列 S 上其执行过程如下：

- 分解（Divide）：随机选取一个元素 x，此元素被称为基准值（pivot），将序列分割为三部分：L 存储小于 x 的元素； E 存储等于 x 的元素； G 存储大于 x 的元素
- 解决子问题（Conquer）：递归地对 L 和 G 排序
- 合并（Combine）：合并 L 、 E 和 G

<img src="https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746414848909.png" alt="快速排序的原理图" style="zoom:50%;" />

### 2.2 分割

我们采用如下方式对一个序列 S 进行分割：

- 我们将 S 中的每一个元素 y 移出序列

- 根据 y 与基准值 x 的比较结果，将其插入 L 、 E 或 G
- 每一次插入或删除操作是在序列的尾或头进行的，因此其运行时间复杂度为 O(1)
- 由此可得，快速排序中每次分割操作的时间复杂度为 **O(n)** 

伪代码：

```python
Algorithm partition(S, p)
    Input sequence S, position p of pivot 
    Output subsequences L, E, G of the elements of S less than, equal to, or greater than the pivot, resp.

    L, E, G <- empty sequences
    x = S.remove(p)
    while not S.isEmpty()
	    y = S.remove(S.first())
        if y < x
        	L.addLast(y)
        else if y = x
	        E.addLast(y)
        else { y > x }
        	G.addLast(y)
    return L, E, G
```

### 2.3 快速排序树

与归并排序一样，快速排序的执行也可以用一棵二叉树表示，称为**快速排序树（quick-sort tree）**：

- 每个节点表示一次快速排序的递归调用，并存储如下信息：执行排序前的无序序列及基准值；执行排序后的有序序列
- 根节点：首次调用快速排序
- 叶子节点：在长度为 0 或 1 的序列上的调用

![快速排序树例子](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746415281846.png)

### 2.4 Python 实现

#### 2.4.1 快速排序（基于链表）

同样，借用之前定义的 `LinkedQueue` 类（链表实现的队列）。

```python
from utils import LinkedQueue


def quick_sort(S: LinkedQueue) -> None:
    """基于链表的快速排序"""
    n = len(S)
    if n < 2:
        return  # list is already sorted

    # divide
    p = S.first()  # 取第一个值为划分基准
    L = LinkedQueue()
    E = LinkedQueue()
    G = LinkedQueue()

    # divide S into L, E, and G
    while not S.is_empty():
        if S.first() < p:
            L.enqueue(S.dequeue())
        elif p < S.first():
            G.enqueue(S.dequeue())
        else:  # S.first() must equal pivot 等于基准值
            E.enqueue(S.dequeue())

    # conquer (with recursion) 递归排序
    quick_sort(L)  # sort elements less than p
    quick_sort(G)  # sort elements greater than p

    # concatenate results 合并
    while not L.is_empty():
        S.enqueue(L.dequeue())
    while not E.is_empty():
        S.enqueue(E.dequeue())
    while not G.is_empty():
        S.enqueue(G.dequeue())
```

测试：

```python
if __name__ == '__main__':
    S = LinkedQueue()
    S.from_list([85, 24, 63, 45, 17, 31, 96, 50])

    print("=" * 15, "Original List", "=" * 15)
    print(S)

    print("=" * 15, "After Sorted", "=" * 15)
    quick_sort(S)
    print(S)
```

```python
=============== Original List ===============
[85, 24, 63, 45, 17, 31, 96, 50]
=============== After Sorted ===============
[17, 24, 31, 45, 50, 63, 85, 96]
```

#### 2.4.2 就地快速排序

快速排序的就地实现：在**分割**这一步骤，我们通过元素的交换，对序列重新进行排布，使得：

- 比基准值小的元素排在第 h 位之前

- 与基准值相等的元素排在第 h 位到第 k 位之间
- 比基准值大的元素排在第 k 位之后

然后，在【第 h 位之前的序列】和【第 k 位之后的序列】递归调用原方法。

**就地分割：**在就地分割这一步骤，我们使用两个索引，将序列 S 分割为 L 和 E ∪ G。不断重复如下步骤，直到 j 与 k 相交：

- 从左向右移动 j ，直到找到一个大于等于 x 的元素
- 从右向左移动 k ，直到找到一个小于 x 的元素
- 将 j 处和 k 处的元素交换

如下图所示，取基准为 (x = 50) ，j 从左向右移动， k 从右向左移动，直到相交：

<img src="https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746417853659.png" alt="就地快速排序例子" style="zoom:50%;" />

**代码实现：**下面基于数组（Python list 类）实现就地快速排序

```python
def inplace_quick_sort(S: list, a: int, b: int) -> None:
    """就地快速排序: 序列 S 从 S[a] 到 S[b]"""
    if a >= b:
        return

    pivot = S[b]  # 取 S[b] 为基准
    left = a  # 从左向右
    right = b - 1  # 从右向左

    while left <= right:  # 直到相交
        # scan until reaching value equal or larger than pivot (or right marker)
        while left <= right and S[left] < pivot:
            left += 1

        # scan until reaching value equal or smaller than pivot (or left marker)
        while left <= right and pivot < S[right]:
            right -= 1

        if left <= right:  # 逆序, 则交换
            S[left], S[right] = S[right], S[left]  # swap values
            left, right = left + 1, right - 1  # 继续移动

    # put pivot into its final place (currently marked by left index)
    S[left], S[b] = S[b], S[left]  # 将基准值放到中间

    # make recursive calls 递归调用
    inplace_quick_sort(S, a, left - 1)
    inplace_quick_sort(S, left + 1, b)
```

测试：

```python
if __name__ == '__main__':
    S = [85, 24, 63, 45, 17, 31, 96, 50]

    print("=" * 15, "Original List", "=" * 15)
    print(S)

    print("=" * 15, "After Sorted", "=" * 15)
    inplace_quick_sort(S, 0, len(S) - 1)
    print(S)
```

```python
=============== Original List ===============
[85, 24, 63, 45, 17, 31, 96, 50]
=============== After Sorted ===============
[17, 24, 31, 45, 50, 63, 85, 96]
```

### 2.5 算法分析

#### 2.5.1 最坏情况 O(n^2)

与归并排序不同，最坏情况下，快速排序效率不甚理想。最坏情况下，快速排序每一次选取的基准值都恰好为序列中唯一的最大值或最小值，这将导致：

- L 和 G 中一个长度为 n - 1，而另一个长度为 0
- 快速排序树高度为 n - 1 （即称为链式结构）
- 运行时间与 n + (n - 1) + ... + 2 + 1 成正比

因此，最坏情况下，快速排序的运行时间为 **$O(n^2)$** 。

#### 2.5.2 随机快速排序

我们分析快速排序时，通常假设基准值总是能将序列以一种合理的方式进行分割，即最坏情况很少出现：

- 实际上，我们可以通过**随机快速排序**使得快速排序运行的时间接近最好情况
- 随机快速排序中，我们每一次进行排序时均**随机选择一个元素作为基准值**
- 在此情况下，我们可以计算快速排序的**期望运行时间**

**命题：一个大小 n 的序列 S ，其随机化快速排序的期望运行时间为 $O(n \log n)$ 。**

**证明：**我们假设 S 中的两个元素可以在 O(1) 的时间内比较。考虑一个单独的随机化快速排序的递归调用，然后用 n 表示该调用的输入序列大小。如果基准值的选择使得每个子序列 L 和 G 均有至少 n/4 、至多 3n/4 的长度，我们可以称之“好”的选择，否则，我们称之为“坏”的选择。

容易证明，一次调用为“好”的概率为 1/2 ，为了得到一个“好”的调用，我们不得不进行的连续调用次数的期望为 2 。对于深度为 i 的节点，在期望意义下，有：

- 其 i/2 的祖先节点处产生了“好”的调用
- 当前节点处序列的长度至多为 $(3/4)^{i/2}n$ 

因此，我们可以得到：

- 深度为 $2 \log _{4/3} n$ 的节点的序列长度期望为 1
- 快速排序树的高度期望为 $O(\log n)$

又因为，在同一深度上进行操作的期望时间为 O(n) ，因此，快速排序的期望运行时间为 $O(n \log n)$ 。



## 3 排序算法

### 3.1 基于比较的排序算法

通过比较各个值的大小，来进行排序的算法有：选择排序、插入排序、冒泡排序、堆排序、归并排序和快速排序。其中堆排序、归并排序、快速排序为高级排序方法，可以达到 O(n log n) 的时间复杂度。具体使用见具体实际情况，可见下表：

![基于比较的排序算法](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746419102610.png)

### 3.2 排序下界

我们可以注意到，相对高效的算法的时间复杂度均为 O(n log n) ，例如堆排序、快速排序、归并排序。是否有更快的排序方法？排序时间是否有下界？

**结论：**对基于比较的排序算法，**O(n log n) 是最好的结果** 。

**证明：**由于我们讨论的是排序下界，因此只计算进行的比较操作的次数：

- 算法的每次可能的运行均可对应于一棵决策树（decision tree）
- 在每个节点处，根据比较的结果，排序算法进行不同的操作

决策树的高度决定了排序算法运行时间的下界：

- 对每一种可能的序列的排列（permutation），必须有唯一的一个叶子节点与之对应：否则，一个排列为 $\cdots,\ x_i,\ \cdots,\ x_j,\ \cdots$ 的序列与一个排列为 $\cdots,\ x_j,\ \cdots,\ x_i,\ \cdots$ 的序列的排序方法是完全一致的，这将导致其中的一个排序结果是错误的
- 叶子节点的数目为 n 个元素的排列数目，即 n!，因此决策树高度至少为 log(n!)

根据性质：
$$
\log (n!) \geq \log \left( \frac{n}{2} \right)^{\frac{n}{2}} = \frac{n}{2} \log \left(\frac{n}{2}\right)
$$
因此，任何基于比较的排序算法的运行时间下界为 $\Omega (n \log n)$



### 3.3 线性时间排序

#### 3.3.1 桶排序

在序列元素有特殊形式的情况下，可以采用**桶排序（bucket-sort）**

- 假设序列 S 中有 n 个键值对，且键为 [0, N - 1] 内的整数
- 阶段 1 ：将序列 S 中的元素插入数组 B 中，具体方式为将元素 (k, v) 放入“桶” B[k] 中
- 阶段 2 ：按序枚举 B[0]，B[1]，…，B[N - 1]，将桶内的元素依次放回序列 S 中

阶段 1 需要 O(n) 的时间，阶段 2 需要 O(N) 的时间。所以，桶排序的运行时间为 **O(n + N)** 。

伪代码：

```python
Algorithm bucketSort(S):
    Input: Sequence S of entries with integer keys in the range [0, N − 1]
    Output: Sequence S sorted in nondecreasing order of the keys let B be an array of N sequences, each of which is initially empty 

    # 阶段 1 : 将 (k, v) 插入 B[k]
    for each entry e in S do
        k = the key of e
        remove e from S and insert e at the end of bucket B[k]
      
    # 阶段 2 : 按顺序返回 B[i]
    for i = 0 to N − 1 do
        for each entry e in B[i] do
        	remove e from B[i] and insert e at the end of S
```

![桶排序例子](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746435740322.png)

桶排序对键的要求：

- 键被用作插入辅助数组的索引，因此对键的类型有所限制
- 不需要使用额外的比较器（comparator）进行比较操作

#### 3.3.2 稳定排序

**稳定排序（stable sorting）：**如果两个键相同的元素在排序前的顺序与排序后的顺序一致，则称此排序方法为稳定的。例如上图例子中 (3, a) (3, b) 的顺序没有改变。

- 归并排序、桶排序是稳定排序算法

#### 3.3.3 字典序排序

一个 d 元组为一个由 d 个键构成的序列 $(k_1,\ k_2,\ \cdots,\ k_d)$ ，其中键 $k_i$ 被称为此 d 元组的第 i 个维度。例如，三维空间中一个点的笛卡尔坐标为一个三元组 (x, y, z)

两个 d 元组的字典序顺序被递归定义为：
$$
(x_1,\ x_2,\ \cdots,\ x_d) < (y_1,\ y_2,\ \cdots,\ y_d)
$$

$$
\Leftrightarrow
$$

$$
x_1 \leq y_1 \quad \wedge \quad (x_2,\ x_3,\ \cdots,\ x_d) < (y_2,\ y_3,\ \cdots,\ y_d)
$$

即 d 元组的比较过程为先比较第 1 维元素，如相等则再比较第 2 维，以此类推。

我们可以设计一个进行字典序排序的方法：

- 假设对第 i 维，我们使用比较器 Ci 对其进行排序
- 假设我们找到了使用任意比较器 C 进行稳定排序的方法 stableSort(S, C)
- 字典序排序通过在对 d 元组的所有维度上依次进行稳定排序 stableSort 而完成
- 字典序排序的运行时间为 **$O(d \cdot T(n))$** ，其中 T(n) 为稳定排序 stableSort 的运行时间

伪代码：

```python
Algorithm lexicographicSort(S)
    Input sequence S of d-tuples
    Output sequence S sorted in lexicographic order
	
    # 从后向前使用稳定排序
    for i = d down to 1
    	stableSort(S, Ci)
```

<img src="https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746436985090.png" alt="字典序排序的例子" style="zoom:67%;" />

#### 3.3.4 基数排序

**基数排序（radix-sort）**是一种特殊的字典序排序方式，它使用**桶排序**作为在每一维度上进行稳定排序的方式（即字典序排序中选择桶排序作为稳定排序的具体实现）：

- 基数排序适用于每一维度上均为 [0, N - 1] 范围内的整数的 d 元组
- 基数排序的运行时间为 **$O(d\cdot (n + N))$** 

伪代码：

```python
Algorithm radixSort(S, N)
    Input sequence S of d-tuples such that 
    	(0, ..., 0) < (x1, ..., xd) 
        and 
        (x1, ..., xd) < (N − 1, …, N − 1)
        for each tuple (x1, ..., xd) in S
    Output sequence S sorted in lexicographic order

    # 从后向前使用桶排序
    for i = d down to 1
	    bucketSort(Si, N)
```



## 4 排序算法的比较

### 4.1 排序算法的比较

下面我们比较一些常见的排序算法：

**插入排序：**如果情况好的话，插入排序的运行时间是 $O(n + m)$ ，其中 m 是逆序的数量（即无序元素对数目）。因此，插入排序是一种进行小序列排序的优秀算法（比如，少于50个元素），因为插入排序是很简单的程序，而且小序列最多只有几个逆序。但是插入排序在最坏情况仍然会达到 $O(n^2)$ 。

**堆排序：**堆排序在最坏的情况下运行时间是 $O(n \log n)$ ，对于基于比较的排序方法是最佳的选择。当输入的数据可以适应主存时，堆排序很容易就地执行，并且在小或中型的序列上是一个理所当然的选择。但是对于超大数据，堆排序无法一次性读入内存，且堆排序不具有稳定排序的特点。

**快速排序：**快速排序在最坏情况下的时间复杂度 $O(n^2)$ ，期望时间复杂度为 $O(n \log n)$ 。并且实验研究表明，在许多测试中它优于堆排序和归并排序，且快速排序提供就地排序。但由于分块步骤中存在元素交换，所以快速排序自然不能提供稳定的排疗。几十年来，快速排序是一种通用的内存排序算法的默认选择。

**归并排序：**归并排序最坏情况下的运行时间为 $O(n \log n)$ 。不提供就地操作很难，并且对于分配临时数组的额外开销无法实现最优化，而且在数组之间复制相比堆排序的就地实现和可以在计算机主存中完全适合的对序列的快速排序而言没有优势。不过，归并排序因其可以分块处理的特点，更适合对于超大规模数据。

**桶排序和基数排序（特殊的字典序排序）：**最后，如果一个应用程序用小的整型键、字符串或者来自离散范围的 d 元组键对条目进行排序，那么桶排序和基数排序是很好的选择，因为它的运行时间为 $O(d \cdot (n + N))$ 。其中，[0, N-1] 是整型键的范围。因此，如果 $d \cdot (n + N)$ 明显小于 $n \log n$ 的函数，那么这个分类方法要比快速排序、堆排序、归并排序更快。

![一些算法的比较总结](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1746419102610.png)

### 4.2 练习

试讨论以下场景中应该使用何种排序算法？

- 客户年消费额完整排序（百万级）：快速排序
- 客户等级分层（如top 10%、bottom 10%）：堆排序、快速排序（基准值取 x% < p < (1-x)% ）
- 将按时间顺序存储的账单按金额排序，要求金额相同的账单之间依然服从原来的时间顺序：归并排序（大数据）或者桶排序（小规模）
- 动态维护前 K 个活跃用户名单：堆排序
- 超大数据（存在不同磁盘中）进行排序：归并排序
- 商品 id 在 0000 - 9999 之间，按 id 进行排序：桶排序



## 5 选择

**选择问题：**从未排序的 n 个可比较元素中选择第 k 个最小的元素。

我们可以通过对集合进行排序然后在已排序序列的索引为 k - 1 的地方插入索引来解决这个问题。根据之前的排序算法，基于比较的排序，最快也要 O(n log n) 。下面，我们可以使用最好的比较排序算法，使得选择出这个第 k 小的元素的时间复杂度为 O(n) 。

### 5.1 随机快速选择

**随机快速选择**的想法来源于快速排序，随机选取一个基准值，然后我们将序列分为 L E G 三部分，每次检查是否有子序列 L（当选第 k 小时） 的长度达到 k ，从而进入递归。

Python 代码实现：

```python
import random


def quick_select(S, k):
    """返回 S 中第 k 小的数"""
    if len(S) == 1:
        return S[0]

    pivot = random.choice(S)  # 随机选取基准
    # 分为 3 个子序列
    L = [x for x in S if x < pivot]
    E = [x for x in S if x == pivot]
    G = [x for x in S if pivot < x]

    if k <= len(L):
        return quick_select(L, k)  # k th smallest lies in L
    elif k <= len(L) + len(E):
        return pivot  # k th smallest equal to pivot
    else:
        j = k - len(L) - len(E)  # new selection parameter
        return quick_select(G, j)  # k th smallest is jth in G
```

测试：

```python
if __name__ == '__main__':
    S = [85, 24, 63, 45, 17, 31, 96, 50]

    print("=" * 15, "Original List", "=" * 15)
    print(S)

    k = 1
    print("=" * 15, f"The {k}th smallest is", "=" * 15)
    k_th = quick_select(S, k)
    print(k_th)
```

```python
=============== Original List ===============
[85, 24, 63, 45, 17, 31, 96, 50]
=============== The 1th smallest is ===============
17
```

### 5.2 算法分析

**命题：假设 S 的两个元素可以在 O(1) 时间内进行比较，大小为 n 的序列 S 的随机快速选择的预期运行时间是 E(t(n)) = O(n) 。**
