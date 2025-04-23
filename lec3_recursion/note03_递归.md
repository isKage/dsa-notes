# 递归算法

教材：[《数据结构与算法 Python 实现》](https://book.douban.com/subject/30323938/)

**递归**：通过一个函数在执行过程中一次或者多次调用其本身，或者通过一种数据结构在其表示中依赖于相同类型的结构更小的实例。简而言之：递归就是自己调用自己。

本文依据四个例子介绍递归算法的原理和如何搭建：

- 阶乘函数 $n!$
- 标尺刻度（分形）
- 二分查找
- 计算机文件目录的嵌套

除此之外，还有一些常见的递归例子：递归求和、逆置序列、递归产生斐波那契数列、求和谜题等。以及什么是尾递归，如何将尾递归转换为非递归算法。

## 1 常见递归案例

### 1.1 阶乘函数

由阶乘函数的定义，我们可知
$$
n! = n \times (n-1) \times (n-2) \times \cdots \times 2 \times 1
$$
当 $n = 0$ 时，我们规定 $0! = 1$

根据阶乘的定义，可以写出函数的递推形式，如果我们构造了一个函数 `factorial()` 应该满足

```python
# 伪代码
if n == 0:
	factorial(n) = 1
else:
    factorial(n) = n * factorial(n - 1)
```

于是我们可以得到阶乘函数的递归算法：

```python
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

print(factorial(4))  # 24
```

- 迭代是通过函数的递归实现的，每次进入函数，查看 `n` 是否为 `0` ，如果不为零，则返回 `n * f(n)` 如此反复调用，直到 `n = 0` 时才真正开始进行计算。

<img src="https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1740813281185.png" style="zoom:50%;" />



### 1.2 标尺刻度（分形）

对于一个刻度尺，每刻度之间距离减半时，刻度线长度也减小。例如：0 - 1 cm 的刻度间，假设 0 和 1 刻度线长 4 个单位，于是有 0.5 cm 刻度线长 3 个单位，0.25 cm 刻度线长 2 个单位，以此类推。

<img src="https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1740813701382.png" style="zoom:47%;" />

我们定义函数 `draw_ruler()` ，用来模仿这种分形的过程：

```python
def draw_line(tick_length, tick_label=''):
    """绘制刻度

    Args:
        tick_length (int): 刻度长度，即 '-' 字符个数
        tick_label (str, optional): 刻度数，不重要. Defaults to ''.
    """
    line = '-' * tick_length
    if tick_label:
        line += ' ' + tick_label
    print(line)


def draw_interval(center_length):
    """记录分型个数的辅助函数

    Args:
        center_length (int): 负责传入刻度长度给 draw_line 函数，即 '-' 字符个数
    """
    if center_length > 0:
        draw_interval(center_length - 1)
        draw_line(center_length)
        draw_interval(center_length - 1)


def draw_ruler(len_of_ruler, num_scale):
    """绘制刻度尺

    Args:
        len_of_ruler (int): 刻度尺长度，即最大刻度
        num_scale (int): 最大刻度的长度，即最大刻度的 '-' 字符个数，决定了分形次数
    """
    draw_line(num_scale, '0')
    for j in range(1, 1 + len_of_ruler):
        draw_interval(num_scale - 1)
        draw_line(num_scale, str(j))
```

```python
draw_ruler(len_of_ruler=1, num_scale=3)
'''
--- 0
-
--
-
--- 1
'''
```

- 细节 & 原理

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1740900901780.png)

每一个 `draw_interval(n)` 下都嵌套着一个结构为

```python
draw_interval(n)
├── draw_interval(n-1)  # 继续嵌套，直到 n = 0
│ 	├── ...
├──	draw_line(n)        # 真正画刻度的函数 输出 '-' 字符
└──	draw_interval(n-1)
	├── ...
```

### 1.3 二分查找

二分查找是一种高效的查找序列元素的算法。当序列无序时，通过循环遍历的方式查找某一个元素，复杂度为 `O(n)` 。但当**序列有序**时，可以使用二分查找。

- 二分查找的想法

需要在一个有序序列中查找 `x` ，首先将序列分半，检查 `x` 落入哪个区间，例如落入左边，则抛去右边，在左边继续分半查找。

- 伪代码

```python
left = 0     		  	    # 最左边下标
right = len(seq) - 1        # 最右边下标

mid = (left + right) // 2   # 计算中间下标

if x == seq[mid]:
    # 完成
elif x < seq[mid]:
    # 到左半寻找
    # 调用函数，更新参数
else:
    # 到右半寻找
    # 调用函数，更新参数
```

- 复杂度

每次递归调用，序列长度为 `right - left + 1` 。而二分查找每次调用后，传入 `mid = (left + right) // 2` ，序列长度减半 `(right - left + 1) / 2` 。于是有
$$
\text{Algorithms end when} \quad \frac{n}{2^k} \sim 1
$$
所以 $k \sim \log_2 n$ 其中 $k$ 为操作数（调用递归次数）。故复杂度为 `O(log n)`

- 算法代码实现

```python
def binary_search(data, target, left, right):
    if left > right:
        # 全遍历后仍然没找到
        return False

    mid = (left + right) // 2
    if target == data[mid]:
        return True
    elif target < data[mid]:
        return binary_search(data, target, left, mid - 1)
    else:
        return binary_search(data, target, mid + 1, right)
```

```python
seq = [2, 4, 5, 7, 8, 9, 12, 14, 17, 19, 22, 25, 27, 28, 33, 37]
print(binary_search(seq, target=22, left=0, right=len(seq) - 1))  # True
```

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1740821735351.png)

### 1.4 文件系统

一般主机的文件目录大致为 `a/b/c.py` 其中 `a/` `b/` 表示其为文件夹，而有文件后缀的 `c.py` 则为文件。下面编写一个递归算法，计算某个目录下所有文件（文件夹）各自的存储大小。

- 伪代码

```python
def disk_usage(path)
    Input: 文件路径
    Output: 存储空间总和

    total = size(path)  # 当前目录的大小
    if path 是文件夹:
        for child_path in path  # 查看父目录下的子目录
            total += disk_usage(child_path)  # 递归
	return total
```

- `os` 模块

`os.path.getsize(path)` 获取 `path` 路径文件的大小或文件夹本身的大小（针对文件夹，只返回文件夹自身大小，不包含其下文件和其他子文件夹的大小）

`os.path.isdir(path)` 判断 `path` 是否是一个合法且存在的路径

`os.listdir(path)` 返回一个列表，列表元素为 `path` 路径下所有文件和文件夹的名称

`os.path.join(path, filename)` 根据传入的字符串组合成一条合法的路径

- 算法代码实现

```python
def disk_usage(path):
    total = os.path.getsize(path)  # 当前目录自身的大小
    if os.path.isdir(path):
        for filename in os.listdir(path):
            # 遍历其下子目录的名称
            child_path = os.path.join(path, filename)
            total += disk_usage(child_path)  # 递归调用 计算子目录的大小

    print("{}  {}".format(total, path))
    return total
```

```python
print(os.path.getsize(os.getcwd()))
# 128 代表目录自身的大小，不包含其下子目录

total = disk_usage(os.getcwd())      # os.getcwd() 获取当前目录路径
'''
2262 /Users/<username>/dsa-notes/lec3_recursion/code03_recursion.py
6326 /Users/<username>/dsa-notes/lec3_recursion/note03_递归.md
8716 /Users/<username>/dsa-notes/lec3_recursion  	# 父目录
'''

print(total)
# 8716
```



## 2 递归分类

- 如果一个递归最多调用一次，称之为**线性递归**
- 如果一个递归可以同时进行两次调用，称之为**二路递归**
- 如果一个递归可以同时进行三次及以上调用，称之为**多重递归**

### 2.1 线性递归

递归函数内可能有多个递归调用，但函数内必须最多只能执行一次递归调用。例如：

- 阶乘的递归式定义
- 二分查找

> 二分查找虽然有两处出现了递归调用，但因为处于 `if - else` 语句中，实际最多只执行一次，故仍然是线性递归

#### 2.1.1 递归求和

递归求和和阶乘的实现如出一辙，都是采用递推的方式构建。

- 伪代码

```python
Algorithm LinearSum(A, n):
Input: 序列和求和长度
Output: 序列前 n 项和

if n == 1 then
	return A[0]
else
	return LinearSum(A, n - 1) + A[n - 1]
```

- 算法代码实现

```python
def linear_sum(seq: list, n: int):
    if n == 1:
        return seq[0]
    else:
        return linear_sum(seq, n - 1) + seq[n - 1]
```

```python
# 递归求前 n 项和
seq = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(linear_sum(seq, 3))  # 6
```

#### 2.1.2 逆置序列

对于输入一个序列，将其第一项和最后一项交换，第二项与倒数第二项交换，以此类推从而得到逆置后的序列。基本想法是每次调用交换首尾，然后剔除首尾后作为新的序列再次调用。

- 伪代码

```python
Agorithm ReverseArray(A, i, j):
Input: 序列 A 和首尾下标 i, j (也可任意指定非首尾下标 i, j)
Output: 无输出，因为序列是可变的，函数操作直接对序列进行

if i < j then
	交换 A[i] 和 A[j]
	ReverseArray(A, i + 1, j - 1)  # 剔除首尾后作为新的序列再次调用
```

- 算法代码实现

```python
def reverse(seq, i, j):
    if i < j:
        seq[i], seq[j] = seq[j], seq[i]
        reverse(seq, i + 1, j - 1)
```

```python
# 逆置序列
seq = [1, 2, 3, 4, 5, 6, 7, 8, 9]
reverse(seq, i=0, j=len(seq) - 1)
print(seq)
# [9, 8, 7, 6, 5, 4, 3, 2, 1] 从 seq[0]=1 到 seq[n-1]=9 开始逆序

reverse(seq, i=3, j=len(seq) - 1)
print(seq)
# [9, 8, 7, 1, 2, 3, 4, 5, 6] 从 seq[3]=6 到 seq[n-1]=1 开始逆序
```

### 2.2 二路递归

当函数内部执行两次递归调用时，即为二路递归。例如：

- 标尺刻度

#### 2.2.1 二路递归求和

基本思想是将序列拆分为两半，分布调用求和再相加。

- 伪代码

```python
Algorithm BinarySum(A, i, n):
Input: 序列 A 和起始下标 i 和加和长度 n
Output: 从 i 开始的 n 个元素求和

if n == 1 then
	return A[i]
else:
	return BinarySum(A, i, n / 2) + BinarySum(A, i + n / 2, n / 2)
```

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1740892869633.png)

- 算法代码实现

```python
def binary_sum(seq, i, n):
    if n == 1:
        return seq[i]
    else:
        half = n // 2
        return binary_sum(seq, i, half) + binary_sum(seq, i + half, n - half)
```

```python
# 二路递归求和
seq = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(binary_sum(seq, i=0, n=len(seq)))
# 55
print(binary_sum(seq, i=1, n=len(seq) - 1))
# 54
```

> 代码实现并不良好，因为需要手动计算起始下标和长度，没有检查溢出问题

#### 2.2.2 二路递归产生斐波那契数列

产生递推式为 $F_0 = 0,\ F_1 = 1,\ F_{i} = F_{i - 1} + F_{i - 2}$ 的斐波那契数列，可以尝试使用二路递归方法。

- 伪代码

```python
Algorithm BinaryFib(k)
Input: 序列下标 k
Output: 第 k 个斐波那契数列值

if k == 0 or k == 1 then
	return k
else
	return BinaryFib(k - 1) + BinaryFib(k - 2)
```

- 算法代码实现

```python
def binary_fib(k):
    """ 【不推荐】 """
    if k == 0 or k == 1:
        return k
    else:
        return binary_fib(k - 1) + binary_fib(k - 2)

# 二路递归产生斐波那契数列 【不推荐】
for i in range(10):
    print(binary_fib(i), end=' ')
# 0 1 1 2 3 5 8 13 21 34
```

> 二路递归产生斐波那契数列复杂度为指数级，【不推荐】使用

**证明** 记 $n_k$ 表示 `binary_fib(k)` 函数调用递归的次数，则有：
$$
\begin{align} \notag
n_0 &= 1 \\ \notag
n_1 &= 1 \\ \notag
n_2 &= n_1 + n_0 + 1 = 3 \\ \notag
n_3 &= n_2 + n_1 + 1 = 5 \\ \notag
&\cdots \\
n_k &= n_{k-1} + n_{k-2} + 1 \notag
\end{align}
$$
于是可知 $n_k$ 也为斐波那契数列，由斐波那契数列是二阶线性递推，求通项公式 $n_k \sim (\frac{\sqrt{5}- 1}{2})^k$ 可知操作次数 $n_k$ 大约为指数类型的量级。指数增长理论上在算法中是无法实现的。（或者可以证明 $n_k$ 大约是 $n_{k-2}$ 的 2 倍以上，所以 $n_k \sim 2^{k/2}$ 也是指数级别）

#### 2.2.3 线性递归产生斐波那契数列

改进递归，使用线性递归产生斐波那契数列。基本思想是每次返回一组（2 个）斐波那契数，每次返回的时候直接进行加和（递推）

- 伪代码

```python
Algorithm LinearFibonacci(k):
Input: 下标 k
Output: 一次返回 2 个斐波那契数

if k == 1 then
	return 0, 1
else
	i, j = LinearFibonacci(k - 1)
	return j, i + j
```

- 算法代码实现

```python
def linear_fib(k):
    if k == 1:
        return 0, 1
    else:
        i, j = linear_fib(k - 1)
        return j, i + j
```

```python
# 线性递归产生斐波那契数列
for i in range(1, 10):
    front, back = linear_fib(i)
    print(back, end=' ')
# 1 1 2 3 5 8 13 21 34
```

> 线性递归每递归一次就能产生一项，故复杂度为 `O(n)`

### 2.3 多重递归

多重递归中的函数可能执行多于两次递归调用。例如：

- 文件系统

#### 2.3.1 求和谜题

可以简单理解为找出集合 $U = \{1, 2, 3, \cdots, 9 \}$ 所有的三元子集 $S = \{a, b, c\}$ 使得满足 $a + b = c$ 。基本想法是每次向 `S` 中添加一个 `U` 中元素，并删去 `U` 中对应的元素，并 `k - 1` 表示 `S` 还剩 `k - 1` 个元素。从而得到新的 `k, S, U` 此时递归调用。

- 伪代码

```python
Algorithm PuzzleSolve(k, S, U):
Input: S 为结果集合，U 为选取元素来源，k 为要求的 S 集合大小
Output: 所以满足 a + b = c 的 S = {a, b, c} 

for e in U do:
    # 从 U 中逐个挑出元素
    Add e to the end of S  # 将 e 添加到序列 S 的末尾
    Remove e from U        # 将 e 从集合 U 中移除（标记为已使用）

    if k == 1 then:               
        # 如果当前序列长度满足要求
        if is_solution(S) then:    
            # 检查 S 是否是谜题的解
            print("Solution found: " + S)
    else:                         
        # 否则继续递归扩展，递归调用，并传入新参数
        PuzzleSolve(k - 1, S, U)

    Remove e from the end of S     // 回溯：将 e 从序列 S 的末尾移除
    Add e back to U                // 回溯：将 e 添加回集合 U（标记为未使用）
```

- 算法代码实现

```python
def is_solution(S):
    """ 检查 a + b = c """
    res = False
    if S[0] + S[1] == S[2]:
        res = True
    return res


def puzzle_solve(k, S, U):
    """ 寻找 S """
    for e in list(U):  # 遍历集合 U 中的每一个元素
        S.append(e)  # 将 e 添加到序列 S 的末尾
        U.remove(e)  # 将 e 从集合 U 中移除

        if k == 1:
            if is_solution(S):
                # 检查当前序列 S 是否是谜题的解
                print("Solution found: {} + {} = {}".format(S[0], S[1], S[2]))
        else:
            # 递归调用，继续扩展序列
            puzzle_solve(k - 1, S, U)

        # 回溯
        S.pop()  # 将 e 从序列 S 的末尾移除
        U.add(e)  # 将 e 添加回集合 U
```

```python
# 求和谜题
U = {1, 2, 3, 4}
k = 3
S = []
puzzle_solve(k, S, U)
'''
Solution found: 1 + 2 = 3
Solution found: 1 + 3 = 4
Solution found: 2 + 1 = 3
Solution found: 3 + 1 = 4
'''
```

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1740897518866.png)



## 3 递归算法的不足

### 3.1 不断递归带来的复杂度

- 递归可能会因为不断的调用自身带来复杂度的急剧上升

例如：二路递归产生斐波那契的例子就展示了递归的误用

### 3.2 最大递归深度

- 除了复杂度，递归的误用可能会带来无限深度

例如出现了下面的例子：

```python
def f(x):
    return f(x)
```

这种简单的错误会导致递归无限地调用自身，这会迅速耗尽计算资源。所以，使用递归时，往往会传入**更多的参数**，通过参数的变化和添加终止条件实现递归。

- Python 限制了递归的深度，默认递归不得超过 1000 层，如果超过则会报错 `RuntimeError`

合法的/高效的递归操作，这个限制（1000 层）是完全足够的。例如，二分查找的复杂度为 `O(log n)` ，如果要这个算法消耗 1000 次递归，则有 $\log n = 1000$ 可以计算出 $n = 2^{1000}$ 个输入，这个数字显然在现实中是不可能达到的。所以，1000 层限制对于合法的递归算法是完全足够的。

当然，也可以自定义最大递归深度限制【不推荐】

```python
import sys

old = sys.getrecursionlimit()
sys.setrecursionlimit(1000000)
```

> 无论如何，依靠**参数的加入和限制**对递归算法的设计十分重要。



## 4 消除尾递归

递归算法的优点在于利用问题中的重复结构。然而，递归的成本也十分明显。算法必须记录存储每个调用的状态和结果。这对计算机内存造成负担。

所以，某些情况下，我们希望能够将递归算法变为非递归算法。

### 4.1 尾递归

**定义**：当递归算法进行的递归调用是此算法的最后一步，即递归调用得到的值被立即当作此算法的输出，则此递归为一个尾递归（**递归调用为最后一步 / 递归调用得到的值作为输出**）。

- 尾递归必定是一个线性递归

例如：二分查找

```python
def binary_search(data, target, left, right):
    while left <= right:
        # 利用循环从左右向中间查找
        mid = (left + right) // 2
        if target == data[mid]:
            return True
        elif target < data[mid]:
            right = mid - 1
        else:
            left = mid + 1
    return False
```

### 4.2 非递归算法

#### 4.2.1 阶乘函数（非递归）非尾递归

```python
def factorial(n):
    if n == 0:
        return 1

    res = n
    for i in range(1, n):
        # 使用循环逐个相乘
        res *= i
    return res
```

#### 4.2.2 逆置序列（非递归）

```python
def reverse(seq, i, j):
    while i < j:
        # 利用下标的循环交换
        seq[i], seq[j] = seq[j], seq[i]
        i, j = i + 1, j - 1
```

#### 4.2.3 二分查找（非递归）

```python
def binary_search(data, target, left, right):
    while left <= right:
        # 利用循环从左右向中间查找
        mid = (left + right) // 2
        if target == data[mid]:
            return True
        elif target < data[mid]:
            right = mid - 1
        else:
            left = mid + 1
    return False
```

























































