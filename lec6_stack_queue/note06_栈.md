# 栈 Stack

本章介绍**栈**数据类型，包括栈的概念、如何用 Python 实现栈（数组、链表）、栈的实际使用（数据逆置、匹配问题、算数计算原理、函数调用等原理）以及**回溯法**的概念和使用，包括常见案例（全排列、子集问题、求和谜题以及著名的 N 皇后问题）。

## 1 栈的概念

**栈 (stack)**：限制数据插入、删除操作只能在一端进行的特殊序列，遵循后进先出的原则（Last In First Out, LIFO）。

- 允许插入、删除的一端为**栈顶**（top），另一段为**栈底**（bottom）。
- 在栈顶插入元素称为**入栈**（push），删除元素称为**出栈**（pop）。
- 栈中元素个数称为栈的长度。



## 2 栈的抽象数据类型 

对于栈的抽象数据类型 (stack ADT) ，它应该满足如下操作：

1. `S.push(e)` ：将元素 e 从栈顶插入栈。
2. `S.pop()` ：将栈顶的元素出栈，即删除头部元素，并返回元素的值。如果栈为空，则报错。
3. `S.top()` ：返回栈顶元素的值。如果栈为空，则报错。
4. `S.is_empty()` ：如果栈中无元素，则返回 `True` 。
5. `len(S)` ：重载运算符 `__len__()` ，返回栈的元素个数。

以下是栈的抽象数据类型的一些操作示意：

![栈的抽象数据类型的操作示意](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1741869902612.png)



## 3 基于数组实现栈

Python 提供的 `list` 类是数组的一种，它已经提供了 `append()` 和 `pop()` 方法，所以可以自然的利用 `list` 类来实现栈，只需要将列表类的尾部视作栈的顶部即可。但 `list` 类支持从列表中间插入元素，这违反了栈的规定。所以我们要利用 `list` 类重新定义一个新的栈类 `ArrayStack` 。

### 3.1 适配器模式

对于创建一个新类，可以包含一个现存类的实例作为隐藏域，然后用这个隐藏实例变量的原有方法实现新类的方法。

例如：对于栈，可以在 Python 的 `list` 类上进行修改。那么在初始化 `ArrayStack` 时，可以包含 `list` 类的实例对象。如下：

```python
class ArraryStack:
    def __init__(self):
        self._data = []
    ...
```

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1741870532231.png)

### 3.2 代码实现

特别地，在判断栈为空时，需要自定义一个异常类，以免触发 `list` 类自带的异常：

```python
class Empty(Exception):
    """栈为空的异常类"""
    pass
```

完整 `ArrayStack` 类实现：

```python
class ArrayStack:
    """基于数组的栈数据类型 LIFO"""

    def __init__(self):
        """初始化空栈"""
        self._data = []  # 适配器模式，隐藏 list 实例化对象

    def __len__(self):
        """栈的元素个数"""
        return len(self._data)

    def is_empty(self):
        """判断是否为空"""
        return len(self._data) == 0

    def push(self, e):
        """向栈顶插入元素"""
        self._data.append(e)

    def top(self):
        """返回栈顶元素"""
        if self.is_empty():
            raise Empty("Stack is empty")
        return self._data[-1]

    def pop(self):
        """从栈顶删除元素"""
        if self.is_empty():
            raise Empty("Stack is empty")
        return self._data.pop()
```

### 3.3 算法分析

由于 `ArrayStack` 类基于 Python 的 `list` 类实现，如之前所述（[基于数组的序列](https://blog.iskage.online/posts/340249a9.html)），由于数组的紧凑/连续内存分布，使得其索引操作都是在常数时间内完成的。而删除与插入操作，又因为栈的特性，每次操作均是在栈顶进行，故复杂度也为 $O(1)$ 。但不得不考虑 Python 在数组是以动态数组的方式存在，存在着**摊销时间**成本，如果没有扩大数组内存空间然后复制，则为 $O(1)$ ，但遇到最坏情况则为 $O(n)$ 。

![基于数组的栈的算法复杂度分析](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1741871355451.png)

> 也正是因为摊销成本的存在，一开始如果先初始化一个有长度的数组，会比空数组更为划算。

## 4 基于链表实现栈

正是因为栈的特殊性（插入、删除、查看均在头部进行），这使得链表是实现栈的良好选择。而相比数组，链表不需要连续的内存分布，也不存在摊销成本。这一部分可参见上一章 [链表](https://blog.iskage.online/posts/9241942.html) 。这里给出一个用单向链表实现栈的抽象类：

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



## 5 栈的实际使用

### 5.1 使用栈实现数据的逆置

由于栈的特殊性，即后进先出，用栈实现逆置是一个十分自然的想法。主要思想是：先将元素一个一个压入栈中，然后再一个一个返回，而返回的过程其实就是逆置的过程。

例如：读取 `example.txt` 的内容，按照每行为一个元素，逆置写入原文档。即将原文档行行逆置。

```python
def reverse_file(filename):
    """逆置文件句子，覆写进原文档"""
    S = ArrayStack()  # 实例化栈对象

    # 读原文件
    original = open(filename)
    for line in original:
        # 将每一行 push 进栈
        S.push(line.rstrip('\n'))
    original.close()

    # 读文档，准备写入逆置文本
    output = open(filename, 'w')
    while not S.is_empty():
        # 出栈，写入原文档
        output.write(S.pop() + '\n')
    output.close()
```

原文档如下：

```TEXT
File name: example.txt
Create time: 2025/3/13
Objective: for reverse
Body:
By using stack data structure,
we read this file
and push every lines into the stack.
After that,
pop the objects (lines)
one by one.
And that is the result
--- a reversed file
End!
```

经过逆置后

```python
reverse_file('example.txt')
```

```TEXT
End!
--- a reversed file
And that is the result
one by one.
pop the objects (lines)
After that,
and push every lines into the stack.
we read this file
By using stack data structure,
Body:
Objective: for reverse
Create time: 2025/3/13
File name: example.txt
```

### 5.2 括号和 HTML 标签匹配

很多需要匹配，且匹配对象往往是相邻最近的对象进行匹配的问题，大多可以使用栈的思想来解决。

#### 5.2.1 括号匹配

例如**括号匹配**问题：对于三种括号 `{}` `[]` `()` 它们都需要左括号和右括号相匹配。对于一个括号序列例如 `{[()]}` 它是否满足括号匹配要求。

匹配原则：对于右括号，必须保证在它的左边第一个出现的未匹配成功左括号一定与自己相匹配，否则这一串括号序列就是匹配失败的。例如下面的例子：

1. `()(()){([()])}` ：匹配成功
2. `((()()){([()])})` ：匹配成功
3. `({[])}` ：匹配失败。因为对于位于位置 5 的右小括号 `)` ，它的左边第一个为匹配成功的左括号为 `{` ，所以匹配失败。（不是 `[` 因为其已经和 `]` 匹配成功）

括号匹配栈算法思路：将括号序列从左到右逐个压入栈，对于左括号直接压入。一旦遇到右括号，则比较其和现在的栈顶括号是否匹配，不匹配则算法结束，返回 `False` ；否则匹配成功，该右括号不入栈，栈顶元素也出栈，如此继续。如果最后成功将栈清空，则匹配成功。

**代码实现**

```python
def is_matched(expr):
    """判断左右括号是否匹配"""
    # 左右括号集，注意同一类型括号位置相同
    lefty = "{[("
    righty = "}])"

    S = ArrayStack()
    for c in expr:
        if c in lefty:
            # 左括号入栈
            S.push(c)
        elif c in righty:
            # 右括号比较
            if S.is_empty():
                return False  # 如果右括号前没有栈元素，肯定不匹配
            if righty.index(c) != lefty.index(S.pop()):
                return False  # 删去栈顶，查看栈顶左括号和现在右括号是否匹配
    # 栈清空，则匹配成功
    return S.is_empty()
```

```python
print(is_matched("((()()){([()])})"))  # True
print(is_matched("({[])}"))  # False
print(is_matched("{(5 + x) - [1 + (y - z) * 4]}"))  # True
```

> 只需遍历一次，故时间复杂的为 $O(n)$ 。

#### 5.2.2 HTML 标签匹配

HTML 标签以 `<item>` 和 `</item>` 的方式成对出现。判断匹配方式与括号相同，只是需要多考虑一层：标签内容要一致，即左标签内容 `item` 和右标签去除 `/` 后的内容 `item` 相同。

**代码实现**

```python
def is_matched_html(raw):
    """判断 html 标签匹配与否"""
    S = ArrayStack()
    j = raw.find('<')

    while j != -1:
        k = raw.find('>', j + 1)  # 从 j + 1 开始找 '>'
        if k == -1:  # 找到结尾都没找到，则匹配失败
            return False

        tag = raw[j + 1:k]  # 提取 '<' '>' 之间的字符
        if not tag.startswith('/'):  # 是否以 '/' 开头
            # 不以 '/' 开头，说明为左标签，入栈
            S.push(tag)
        else:
            # 否则以 '/' 开头，为右标签，判断
            if S.is_empty():
                return False  # 如果为空，说明没有左标签匹配
            if tag[1:] != S.pop():
                # 右标签去除 '/' 后是否与此时栈顶左标签匹配
                return False
        # 从 k + 1 寻找下一对标签
        j = raw.find('<', k + 1)
    # 栈清空，则匹配成功
    return S.is_empty()
```

- 使用案例：读取下面的 `example.html` 文件，判断标签是否匹配。

```html
<body>
<center>
    <h1> The Little Boat </h1>
</center>
<p> The storm tossed the little
    boat like a cheap sneaker in an
    old washing machine. The three
    drunken fishermen were used to
    such treatment, of course, but
    not the tree salesman, who even as
    a stowaway now felt that he
    had overpaid for the voyage. </p>
<ol>
    <li> Will the salesman die?</li>
    <li> What color is the boat?</li>
    <li> And what about Naomi?</li>
</ol>
</body>
```

```python
html_file = open('example.html')
html_content = html_file.read()

row = "".join(html_content.split('\n'))

print(is_matched_html(row))  # True

html_file.close()
```

> 只需遍历一次，故时间复杂的为 $O(n)$ 。

### 5.3 函数调用

当调用新函数时，系统需要保存当前调用的所有局部变量，否则新函数将覆盖这些变量。此外，必须保存例程中的当前位置，以便新功能在完成后知道返回何处。所有这些工作都可以通过**操作系统自动使用栈**来完成。

可以理解为：当程序进行时，最先出现的变量和其对应的值会被放入栈底，逐个放入这些变量和结果。当遇到函数时，将函数压入栈中，函数调用的参数实际值来自之前栈中存储的数据。当函数结束时，函数出栈，（函数中的局部变量全部出栈，空间被释放），然后压入程序后面的其他数据。

例如：在内存中，递归实际上是通过栈操作来完成的

### 5.4 升序序列跨度

跨度问题：对于数组 `X` ，其任意位置的 `X[i]` 的跨度 `S[i]` 定义为 `X[i]` 前符合 `X[j] <= X[i]` 的连续元素个数。

**代码实现**

```python
def spans(X, n):
    """
    计算最长升序跨度
    :param X: 原序列
    :param n: 考察序列 X 的前 n 项
    :return S 跨度列表
    """
    
    S = []  # 记录跨度
    A = ArrayStack()  # 栈

    for i in range(n):
        # 遍历 X 的每个元素
        while (not A.is_empty()) and X[A.top()] <= X[i]:
            # 当栈非空并且栈顶元素仍然更小时，不断出栈，直到找到比当前元素更大的数
            A.pop()
        
        if A.is_empty():
            # 如果栈空，当前位置 i 前所有数都比当前数小，那跨度为 i + 1
            S.append(i + 1)
        else:
            # 否则，跨度为当前位置 i 减去比自己大的数的位置 A.top()
            S.append(i - A.top())
            
        # 记录目前最大值的位置
        A.push(i)
    
    return S
```

例如：对于 `X = [6, 3, 4, 5, 2, 1, 4, 9, 10, 1, 3, 20, 11, 9]` 

```python
X = [6, 3, 4, 5, 2, 1, 4, 9, 10, 1, 3, 20, 11, 9]
print(spans(X, len(X)))
# [1, 1, 2, 3, 1, 1, 3, 8, 9, 1, 2, 12, 1, 1]
```

### 5.5 计算算数表达式

在计算算数表达式时，计算机需要比较各个运算符的优先级，然后计算。这一过程可以使用栈来实现。

**主要思路**：分别创建两个栈 `opStk` 存储运算符和 `valStk` 存储值。每次遇到值则压入 `valStk` ，遇到运算符则比较其和 `opStk` 栈顶的运算符优先级，要是优先级高，则直接入栈；否则值栈 `valStk` 出栈 2 个值进行此时 `opStk` 栈顶的运算（栈顶运算符出栈），运算结果再进栈 `valStk` 。然后继续比较此时 `opStk` 栈顶运算符的优先级，如此类推。这样，最后 `valStk` 剩余的元素即为计算结果。

**代码实现**

```python
from utils import ArrayStack


def eval_exp(tokens):
    def precedence(op):
        """为运算符定义优先级"""
        if op == '$':
            return -1  # 结束符优先级最低
        elif op in ('<', '>', '='):
            return 0  # 比较运算符
        elif op in ('+', '-'):
            return 1  # 加减
        elif op in ('*', '/'):
            return 2  # 乘除
        else:
            raise ValueError(f"Invalid operator: {op}")

    def repeat_ops(ref_op, opStk, valStk):
        """判断优先级"""
        while len(valStk) >= 2 and precedence(ref_op) <= precedence(opStk.top()):
            # 如果当前运算符优先级比 opStk 栈顶低，则先计算栈顶运算符
            do_op(opStk, valStk)  # 直到栈顶的低，或 valStk 不足 2 个元素可以计算

    def do_op(op_stk, val_stk):
        """正式计算过程"""
        op = op_stk.pop()  # 提取运算符

        # 提取栈顶计算的两个元素
        x = val_stk.pop()
        y = val_stk.pop()

        # 按照运算符的含义进行计算
        if op == '+':
            val_stk.push(y + x)
        elif op == '-':
            val_stk.push(y - x)
        elif op == '*':
            val_stk.push(y * x)
        elif op == '/':
            val_stk.push(y / x)
        elif op == '<':
            val_stk.push(y < x)
        elif op == '>':
            val_stk.push(y > x)
        elif op == '=':
            val_stk.push(y == x)
        else:
            raise ValueError(f"Invalid operator: {op}")

    # 开始计算
    tokens = tokens + ['$']  # $ 代表算数式起始
    valStk = ArrayStack()  # 记录值
    opStk = ArrayStack()  # 记录运算符
    opStk.push('$')

    for token in tokens:
        if str(token).isdigit():
            # 如果为数字，直接入栈 valStk
            valStk.push(int(token))
        else:
            # 如果为运算符
            repeat_ops(token, opStk, valStk)  # 检查优先级
            opStk.push(token)  # 当前运算符入栈 opStk

    # 返回最后 valStk 栈顶元素，即为结果
    return valStk.top()
```

例如：

```python
expr = ['3', '+', '5', '*', '2']  # 3 + 5 * 2 = 13
print(f"{' '.join(expr)} is {eval_exp(expr)}")

# 新增比较运算测试
expr = ['3', '+', '5', '<', '2', '*', '4']  # (3 + 5) < (2 * 4) -> 8 < 8 -> False
print(f"{' '.join(expr)} is {eval_exp(expr)}")

expr = ['5', '>', '2', '*', '3']  # 5 > (2 * 3) -> 5 > 6 -> False
print(f"{' '.join(expr)} is {eval_exp(expr)}")

expr = ['7', '=', '3', '+', '4']  # 7 = (3 + 4) -> True
print(f"{' '.join(expr)} is {eval_exp(expr)}")
```

```python
3 + 5 * 2 is 13
3 + 5 < 2 * 4 is False
5 > 2 * 3 is False
7 = 3 + 4 is True
```



## 6 算法：回溯法

### 6.1 概念

回溯法是一种通过**试错**寻找问题解的算法。它通过深度优先的方式遍历所有可能的路径，当发现当前路径无法得到有效解时，回退到上一步（**回溯 Backtracking**）并将之前找不到解的路径减去，以后不再寻找，即**剪枝 pruning**，尝试其他可能性。

### 6.2 常见步骤

与递归类似，回溯法可分解为很多步，每一步的常见做法为：

- 首先从该步可以尝试的所有元素的集合 `U` 中选出一个元素 `e`
- 将该元素 `e` 加入到当前尝试的解中，进入下一步
- 在某些条件下可以在该步判定当前尝试的解是否为真解，以及当前情况可否进行剪枝
- 将元素 `e` 从当前解中移除（有必要时需将 `U` 放回集合 `U`）

### 6.3 实际应用和代码实现

#### 6.3.1 全排列问题

**思路**：从 `U` 取出 `e` ，然后从 `U` 去除 `e` 。不同于子集问题，因为全排列允许重复，所以只需要去除 `e` 。子集问题和全排列问题都不需要设置约束条件。

```python
def permute_stack(nums):
    res = []
    stack = ArrayStack()
    stack.push(([], nums))  # 初始状态：空排列 []，剩余元素 nums

    while not stack.is_empty():
        # Step 1: 每次拿出栈顶元素检查，如果不是全排列则进入 Step 2
        path, remaining = stack.pop()
        if not remaining:  # 如果剩余元素为空，说明 path 是一个完整的排列
            res.append(path)
            continue

        # Step 2: 遍历元素，直到将 remaining 的所以剩余元素都加入新的排列中
        for i in reversed(range(len(remaining))):  # 从剩余的 remaining 中取
            e = remaining[i]  # 取出当前元素
            new_remaining = remaining[:i] + remaining[i + 1:]  # 从剩余元素中移除 e
            new_path = path + [e]  # 将 e 加入排列 []
            stack.push((new_path, new_remaining))  # 压入新状态

    return res
```

例如：

```python
print(permute_stack([1, 2, 3]))  # 全排列
# [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
```

#### 6.3.2 子集问题

**思路**：从 `U` 取出 `e` ，然后从 `U` 去除 `e` 。不过不同于全排列问题，由于子集不运行重复，所以需要去除 `e` 和之前的剩余元素，避免重复。子集问题和全排列问题都不需要设置约束条件。

```python
def subsets_stack(nums):
    res = []
    stack = ArrayStack()
    stack.push(([], nums))  # 初始状态：空子集，剩余元素为 nums

    while not stack.is_empty():
        # Step 1: 取栈顶元素，直接加入结果集，因为是子集问题
        path, remaining = stack.pop()
        res.append(path)  # 将当前子集加入结果集

        # Step 2: 遍历剩余元素，加入子集
        for i in reversed(range(len(remaining))):
            e = remaining[i]  # 取出当前元素
            # 从剩余元素中移除 e 及其之前的元素，因为子集不允许重复
            new_remaining = remaining[i + 1:]
            new_path = path + [e]  # 将 e 加入子集
            stack.push((new_path, new_remaining))  # 压入新状态

    return res
```

例如：

```python
print(subsets_stack([1, 2, 3]))  # 子集
# [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
```

#### 6.3.3 求和谜题

**思路**：求和谜题，需要考虑得到的解是否满足求和要求。所以在上述的思路基础下，需要设置约束条件。

```python
def combinationSum_stack(candidates, target):
    res = []
    stack = ArrayStack()
    # 初始状态：空组合，剩余目标值 target 即离 target 的差，起始位置 0
    stack.push(([], target, 0))

    while not stack.is_empty():
        path, remaining, start = stack.pop()
        if remaining == 0:  # 如果剩余目标值为 0，说明 path 是一个有效组合
            res.append(path)
            continue

        # 从 candidates 的 start 开始选择元素
        for i in range(start, len(candidates)):
            e = candidates[i]
            if e > remaining:
                continue  # 剪枝：如果当前元素大于剩余目标值，跳过
            new_path = path + [e]  # 将 e 加入组合
            new_remaining = remaining - e  # 更新剩余目标值
            stack.push((new_path, new_remaining, i + 1))  # 压入新状态，不允许重复选择

    return res
```

> `stack.push((new_path, new_remaining, i + 1))` 的 `i + 1` 表示从下一个位置开始寻找，即不允许重复；若改为 `i` 则允许重复。

例如：

```python
print(combinationSum_stack([1, 2, 3, 4, 5, 6, 7, 8], 9))  # 组合总和Q
# [[4, 5], [3, 6], [2, 7], [2, 3, 4], [1, 8], [1, 3, 5], [1, 2, 6]]
```

#### 6.3.4 N 皇后问题

**问题**：在 NxN 格的国际象棋上摆放 N 个皇后，使其不能互相攻击，即任意两个皇后都不能处于同一行、同一列或同一斜线上，问有多少种摆法？

**思路**：

- 每行只能放置一个皇后，逐行处理。
- 在放置皇后时，需要确保当前列、正对角线（`row - col`）和反对角线（`row + col`）没有被其他皇后占据。
- 当发现当前路径无法继续时，回退到上一步，尝试其他可能性。

```python
def solveNQueens_stack(N):
    res = []  # 存储所有有效解
    stack = ArrayStack()
    # 初始状态：空路径，第 0 行，第一个 set 表示列，第二个表示正对角线，第三个表示反对角线
    stack.push(([], 0, set(), set(), set()))

    while not stack.is_empty():
        # Step 1: 出栈当前状态
        path, row, cols, diag1, diag2 = stack.pop()
        # 如果所有行都处理完毕，说明 path 是一个有效解
        if row == N:
            # 转换为棋盘表示
            res.append([' · ' * i + ' Q ' + ' · ' * (N - i - 1) for i in path])
            continue

        # Step 2: 在当前行选择列的位置
        for col in range(N):
            # 计算当前列所在的正对角线和反对角线
            curr_diag1 = row - col  # 正对角线：行 - 列
            curr_diag2 = row + col  # 反对角线：行 + 列
            
            # 如果当前列或对角线已经被占用，则跳过
            if col in cols or curr_diag1 in diag1 or curr_diag2 in diag2:
                continue

            # 创建新的集合
            new_cols = set(cols)  # 创建新的列冲突集
            new_diag1 = set(diag1)  # 创建新的正对角线冲突集
            new_diag2 = set(diag2)  # 创建新的反对角线冲突集
            
            # 更新
            new_cols.add(col)  # 将当前列加入列冲突集
            new_diag1.add(curr_diag1)  # 将当前正对角线加入冲突集
            new_diag2.add(curr_diag2)  # 将当前反对角线加入冲突集
            new_path = path + [col]  # 将当前列加入路径
            
            # 压入新状态：更新路径、下一行、新的冲突集
            stack.push((new_path, row + 1, new_cols, new_diag1, new_diag2))

    return res
```

例如：

```python
for row in solveNQueens_stack(4):  # 4 皇后问题
    print("Answer:")
    for i in row:
        print(i)
```

```python
Answer:
 ·  ·  Q  · 
 Q  ·  ·  · 
 ·  ·  ·  Q 
 ·  Q  ·  · 
Answer:
 ·  Q  ·  · 
 ·  ·  ·  Q 
 Q  ·  ·  · 
 ·  ·  Q  · 
```

























