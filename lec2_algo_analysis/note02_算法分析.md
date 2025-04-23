# 算法分析：原子操作与时间复杂度

教材：[《数据结构与算法 Python 实现》](https://book.douban.com/subject/30323938/)

研究算法运行的时间非常重要，我们往往关注：

1. 算法运行时间与输入大小的关系
2. 往往考虑最差的情况

## 1 实验研究

如果算法是准确的，且已经可以正常运行。可以采用最简单的方法检验时间，即直接计算算法执行的时间差：

```python
from time import time

start = time()

# run algorithm
# 算法执行

end = time()

print(end - start)
```

显然这种方法简单，但缺点明显【不推荐使用】：

- 比较不同算法时，要控制硬件等条件相同
- 算法的输入可能并不够，例如对于巨量数据输入，每次都测试显然是不明智的
- 这个方法必须要求算法能过成功运行



## 2 原子操作

### 2.1 伪代码

所以为了解决上面的问题，我们往往分析伪代码，例如：

```python
Algorithm method (arg [, arg, ...])
	Input: ...
    Output: ...
    # 一些操作
    ...
```

不关注代码能否执行，只用于评价算法的好坏。

### 2.2 原子操作

原子操作是算法进行的一些基本运算：

- 在伪代码中可被识别出来（无须算法成立即可进行评价）
- 很大程度上独立于编程语言而存在（即适用于各种环境）
- 执行时间为常数（基本单元，与输入大小 `n` 无关）

按照原子操作的观点，我们可以根据操作总时间与输入大小的关系，评价一个算法的好坏。即寻找某种函数关系：
$$
t = f(n)
$$
其中 $t$ 为算法执行的时间，$n$ 为算法输入的大小。下面是常见的函数 $f$ 形式。



## 3 常见函数

### 3.1 常见 7 个函数

算法分析里常见的 7 个函数为：

- 常数函数

$$
f(n) = C
$$

这表明，无论算法输入的大小 `n` 如何变化，算法所有原子操作的执行时间总和大约为一个常数。这是算法分析里最好的情况，表示这个算法非常的迅速。

- 对数函数

$$
f(n) = \log n
$$

注意，这里的对数底数并不重要。

- 线性函数

$$
f(n) = n
$$

注意，添加常数系数不影响，即 $C \times n$ 等价于 $n$ 。

- $n\log n$ 函数

$$
f(n) = n \log n
$$

注意，$\log n$ 是一个比 $n$ 更小的函数，可以理解为
$$
\lim_\limits{n \to \infty} \frac{\log n}{n} = 0
$$

- 二次函数

$$
f(n) = n^2
$$

常见的输入大小为 `n` 却要执行 $n^2$ 次的算法为两层 `for` 循环（嵌套循环）。

- 三次函数和其他多项式

$$
f(n) = a_0 + a_1 \times n + a_2 \times n^2 + \cdots + a_d \times n^d
$$

与二次函数类似，这一类问题的操作数满足一个多项式函数。

- 指数函数

$$
f(n) = b^n
$$

其中 $b$ 为某一个常数，指数增长非常迅速。

### 3.2 比较增长率

一般而言，我们希望

- 数据结构的操作运行时间与常数函数或对数函数成正比
- 算法以线性函数或 $n \log n$ 函数运行
- 运行时间与二次、三次函数相关的难以应对大规模输入数据的情形
- 指数函数则完全不可行

使用双对数刻度画出这 7 个函数的图像，即可直观地体悟它们的增长速度。

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1740560780545.png)

> 双对数刻度：指的是对坐标轴刻度进行放缩，按照 $10^1, 10^2, 10^3, \cdots$ 的数值等距标注刻度。



## 4 渐进分析

实际分析中，我们不用求出 $f(n)$ 的确切表达。只需知道算法操作时间与哪个形式的函数成正比即可。

### 4.1 大 O 符号

**定义**：令 $f(n),\ g(n): \N \to \R$ 的函数，如果对任意常数 $c > 0$ ，都存在整数 $n_0 \geq 1$ 使得
$$
f(n) \leq c \cdot g(n),\quad \text{when}\ \ n \geq n_0
$$
成立，则称 $f(n)$ 是 $O(g(n))$ 。

<img src="https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1740564008502.png" alt="QQ_1740564008502" style="zoom:50%;" />

例如：对于 $f(n) = 3n+5$ 我们寻找 $n_0$ 使得 $f(n) = 3n+5 \leq c\cdot g(n) = c \cdot n$ 不难发现，当 $n \geq [\frac{5}{c-3}] + 1 := n_0$  时 $f(n) \leq c\cdot g(n)$ 。所以可知  $f(n)$ 是 $O(n)$ 。

### 4.2 大 O 的性质

大 O 符号能让我们忽略那些常量因子和低阶项。常见的有

- 多项式保留最高阶即可

$$
O(a_0 + a_1 \times n + a_2 \times n^2 + \cdots + a_d \times n^d) = O(n^d)
$$

- $n$ 比 $\log n$ 增长的更快

$$
O(n + \log n) = O(n)
$$

$$
O(n^2 + n \log n) = O(n^2)
$$

- $1 \sim n$ 的 $k$ 次方求和

$$
\sum\limits_{i=1}^n \ i^k = O(n^{k+1})
$$

- 指数项含有常数

$$
O(b^{n+c}) = O(b^n)
$$

因为 $b^{n+c} = b^c \cdot b^{n} := C\cdot b^n$

> 但需要注意的是，不可以更换底数 $b$。

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1740563935444.png)



## 5 算法分析实例

### 5.1 寻找最大数

输入一个列表，输出列表中的最大值。列表的长度可以理解为输入大小 `n` 。

```python
def find_max(data):
    """ # 寻找最大数 # """
    biggest = data[0]
    for val in data:
        if val > biggest:
            biggest = val
    return biggest


data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(find_max(data))
```

一层循环，所以大约执行 n 次。其他操作均为常数次，故这个算法时间复杂度为 `O(n)`

### 5.2 计算前缀平均值

输入一个列表，计算前 `i` 个数字的平均值。列表的长度可以理解为输入大小 `n` 。

#### 5.2.1 二次算法

整个列表循环一层，然后在循环中再次循环加和

```python
def prefix_average1(data):
    """ 计算前缀平均值 二次算法 """
    n = len(data)
    ave = []
    for i in range(n):
        total = 0
        for j in range(i + 1):
            total += data[j]
        ave.append(total / (i + 1))
    return ave


data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(prefix_average1(data))
```

第二层循环执行 i + 1 次，而 i 在第一层循环里从 0 到 n - 1 ，故整个算法操作次数大约为 $\sum_{i=0}^{n-1}\ (i+1)$ 省略低阶项，大致为 `O(n^2)` 

#### 5.2.2 线性算法

```python
def prefix_average2(data):
    """ 计算前缀平均值 线性算法 """
    n = len(data)
    total = 0
    ave = []
    for i in range(n):
        total += data[i]
        ave.append(total / (i + 1))
    return ave


data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(prefix_average2(data))
```

如此只有一层循环，大致为 `O(n)`

### 5.3 三集不相交

输入三个序列 `A, B, C` ，输出是否存在交集。如果存在交集，则返回 `True` 否则返回 `False`

#### 5.3.1 三层循环

```python
def disjoint1(A, B, C):
    """ 三集不相交 三层循环 O(n^3) """
    for a in A:
        for b in B:
            for c in C:
                if a == b == c:
                    return True
    return False


A = [1, 2, 3]
B = [3, 4, 5, 6]
C = [3, 7, 8, 9, 10]
print(disjoint1(A, B, C))
```

显然，使用了三层循环。复杂度大致为 `O(n^3)` 。（准确而言应该为三个集合大小的乘积，但本质一样）

#### 5.3.2 循环中加入判断

```python
def disjoint2(A, B, C):
    """ 三集不相交 循环中加入判断 O(n^3) """
    for a in A:
        for b in B:
            if a == b:
                for c in C:
                    if a == c:
                        return True
    return False


A = [1, 2, 3]
B = [4, 5, 6, 3]
C = [7, 8, 9, 10, 3]
print(disjoint2(A, B, C))
```

仍然为 `O(n^3)` 例如上面的例子，当 `A, B, C` 的相同元素在最后时，不得不完全遍历。

### 5.4 元素唯一性

给定一个长为 `n` 的序列，判断是否元素互不相同，是则为 `True`

#### 5.4.1 简单的迭代

```python
def unique1(data):
    """ 元素唯一性 简单迭代 O(n^2) """
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[i] == data[j]:
                return False
    return True


data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 9]
print(unique1(data))
```

与 5.2.1 节 计算前缀平均值的二次算法类似，复杂度为 `O(n^2)`

#### 5.4.2 先排序

```python
def unique2(data):
    """元素唯一性 先排序 O(n * log n)"""
    temp = sorted(data)
    for i in range(1, len(temp)):
        if temp[i] == temp[i - 1]:
            return False
    return True


data = [1, 3, 2, 6, 5, 4, 7, 10, 9, 9]
print(unique2(data))
```

循环执行了 n 次，Python 内置的 sorted 方法执行了 log n 次，故最后的复杂度为 `O(n * log n)`























