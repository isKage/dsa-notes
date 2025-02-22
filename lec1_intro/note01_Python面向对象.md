# Python 面向对象编程

教材：[《数据结构与算法 Python 实现》](https://book.douban.com/subject/30323938/)

## 1 类定义

类是面向对象程序设计中抽象的主要方法。下面以创建 `CreditCard` 类作为例子讲解面向对象如何定义类。

### 1.1 例：CreditCard 类

```python
class CreditCard:
    """有关一个用户的信用卡"""

    def __init__(self, customer, bank, acnt, limit):
        """初始化一个信用卡实例

        Args:
            customer (str): 用户名
            bank (str): 银行名
            acnt (str): 用户账户ID
            limit (float): 信用卡限额
        """
        self._customer = customer
        self._bank = bank
        self._acnt = acnt
        self._limit = limit
        self._balance = 0.  # 初始账户额度为 0

    def get_customer(self):
        """返回用户名"""
        return self._customer

    def get_bank(self):
        """返回银行名"""
        return self._bank

    def get_acnt(self):
        """返回账户ID"""
        return self._acnt

    def get_limit(self):
        """返回额度"""
        return self._limit

    def charge(self, price):
        """
        返回是否能继续提款，即检查是否超出额度
        :param price: 希望提取的额度
        :return: True 如果加上目前所用额度没有超出限度，否则 False
        """
        if self._balance + price > self._limit:
            return False
        else:
            self._balance += price
            return True

    def make_payment(self, amount):
        """用现金抵消了部分信用卡贷款"""
        self._balance -= amount
```

#### 1.1.2 `self` 标识符

`self` 代表了一个实例，可以理解为对象自己。同时，`self` 也确定了调用方法时作用的对象。例如 `obj.get_customer()` 表示对实例化后的对象 `obj` 调用方法 `get_customer()` 。

#### 1.1.3 `__init__()` 方法

在面向对象编程中，我们称位于类定义 `class` 之中的各种函数 `def` 为方法。而 `__init__()` 称为初始化方法，它是当实例化对象时首先被执行的。在这个例子中，参数除了对象自己 `self` ，也包含了 `customer, bank, acnt, limit` 这些都是初始化时需要传入的。

#### 1.1.4 其他方法

类似于初始化方法，其他的函数也是接受参数，返回结果。例如：`charge()` 方法，使用 `obj.charge(100)` 表示对于对象 `obj` ，传入参数 `price = 100` ，然后返回一个结果。

#### 1.1.5 `_` 变量名

在数据成员名称中的前加下划线，比如 `_balance` ，表明它被设计为非公有的（nonpublic）。类的用户不应该直接访问这样的成员。可以提供类似于 `get_balance` 的访问函数，以提供拥有只读访问特性的类的用户。



### 1.2 实例化

```python
cc = CreditCard(customer="John Doe", bank="Nation Bank", acnt="123 456 789", limit=1000.)
```

使用 `cc = CreditCard()` 并传入初始化参数的方式实例化对象。此时就可以对对象 `cc` 进行操作，调用方法。

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1740044330309.png)

### 1.3 错误检查

`CreditCard` 类的实现方法不够稳健：

- 例如：没有明确地检查参数的类型，如果用户创建了一个类似于 `visa.charge('candy)` 的调用，代码可能会崩溃。所以应该设计一些抛出异常。
- 例如：逻辑错误的。如果允许用户收取一个类似于 `visa.charge(-300)` 的负价格，这将导致用户的余额变少，这是不和逻辑的

所以，这个例子只是介绍面向对象编程时，定义类、实例化和调用方法的基础知识。之后需要不断完善。



### 1.4 对类进行测试

一般对类的定义会单独放在一个 `.py` 文件中，那么我们需要对类进行检查，测试其是否合理，是否报错。但是，如果通过 `from ... import ...` 的方法导入主程序测试显然不是我们希望的。所以，我们可以在定义类的 `.py` 文件下使用 `if __name__ = '__main__':` 的方法。

- `if __name__ = '__main__':` ：这个判断表示，只有当当前文件以主程序的方式运行时，`if` 语句后面的内容才运行。这样可以避免在 `from ... import ...` 代入类时，连带运行 `if` 语句后的测试语句。

例如：在当前目录下创建文件夹 `utils` 内部放置文件 `cc.py` ，在 `cc.py` 书写类的定义，于是可以代入类

```python
from utils.cc import CreditCard

cc_new = CreditCard("John", "Bank1", "123 456 789", 3010.)
```

而在文件 `./utils/cc.py` 中就可以书写 `if __name__ = '__main__':` 的测试代码

```python
class CreditCard: ...

if __name__ == '__main__':
    wallet = []
    wallet.append(CreditCard("John", "Bank1", "123 456 789", 3010.))
    wallet.append(CreditCard("Mike", "Bank2", "456 123 789", 6210.))
    wallet.append(CreditCard("Ann", "Bank3", "789 456 123", 4010.))

    print(wallet[0].charge(1000.))
    print(wallet[1].charge(2000.))
    print(wallet[2].charge(5000.))

    for account in wallet:
        print("Customer: {}".format(account.get_customer()))
        print("Balance: {}".format(account.get_balance()))

        if account.get_balance() > 100.:
            account.make_payment(100.)
            print("New Balance: {}".format(account.get_balance()))
```



## 2 运算符重载

### 2.1 介绍

Python 的内置类为许多操作提供了自然的语义。比如，`a + b` 可以是数值相加，也可以是字符串相连。

默认情况下，对于新的类来说，`+` 操作符是未定义的，可通过**操作符重载**来定义它。例如：在类的定义里定义方法 `__add__()` 即可定义 `+` 的含义。

以 `a + b` 为例，其中 `a` 和 `b` 均为字符串，则 `a + b` 能成立是因为 Python 内置类 `字符串` 定义了方法 `__add__()` 将其表达为字符串相连，于是 `a + b` 才会正常使用。类似地，自定义类时也可以去重载这些运算符，下面是常见的重载：

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1740048941341.png)

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1740048963901.png)

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1740049031958.png)

### 2.2 例：多维向量类

下面通过定义向量，来解释如何自定义重载。

```python
class Vector:
    """多维向量"""

    def __init__(self, d):
        """d 维度向量"""
        self._coords = [0] * d  # 初始化 d 维向量

    def __len__(self):
        """获取维度: 重载 len(a)"""
        return len(self._coords)

    def __getitem__(self, k):
        """返回第 k 个维度的值: 重载 a[k]"""
        return self._coords[k]

    def __setitem__(self, k, v):
        """设置第 k 个维度的值为 v: 重载 a[k] = v"""
        self._coords[k] = v

    def __add__(self, other):
        """定义向量加法: 重载 a + b"""
        if len(self) != len(other):  # 此处可以直接使用重载后的定义
            raise ValueError("Dimensions must be the same!")

        result = Vector(len(self))
        for i in range(len(self)):
            result[i] = self[i] + other[i]
        return result

    def __sub__(self, other):
        """定义向量减法: 重载 a - b"""
        if len(self) != len(other):
            raise ValueError("Dimensions must be the same!")

        result = Vector(len(self))
        for i in range(len(self)):
            result[i] = self[i] - other[i]
        return result

    def __eq__(self, other):
        """判断向量坐标是否相等: 重载 a == b"""
        return self._coords == other._coords

    def __ne__(self, other):
        """判断向量坐标是否不相等: 重载 a != b"""
        return not self == other  # 等价于 self.__eq__(other) 直接使用重载后的定义

    def __str__(self):
        """以字符串的形式展现这个向量类: 重载 str(a) 或 a 可以以字符串形式展示"""
        return '<' + str(self._coords)[1:-1] + '>'
```

以上的方法各个方法都重载了一些运算符，具体解释见代码注释。



### 2.3 补：自定义 Python 的包

在上面引入类时，我们使用了 `from utils.cc import CreditCard` ，这并不规范。我们可以将类定义写入一个 python 文件，然后统一放在文件夹 utils 中，并且再写一个 `__init__.py` 文件将 utils 文件夹整个变成一个标准的 python 包，目录结构见下：

```bash
./utils
├── __init__.py
├── cc.py
└── vector.py
```

然后在 `__init__.py` 文件中写入：

```python
# coding=utf-8
from .cc import CreditCard
from .vector import Vector
```

如此便可在其他文件中直接引用

```python
from utils import CreditCard, Vector
```



## 3 迭代器

### 3.1 介绍

集合迭代器（iterator）提供了一个关键功能：它支持一个名为 `__next__` 的特殊方法，如果集合有下一个元素，该方法返回该元素，否则产生一个 `StopIteration` 异常来表明没有下一个元素。

Python 为实现了 `__len__` 和 `__getitem__` 方法的的类提供了一个自动的迭代器，每次调用 `__next__` 方法时便会索引递增。例如，下面的 `SquenceIterator` 类。

### 3.2 例：SequenceIterator 类

> 【注意】迭代器的实现必须要求【已经实现了 `__len__` 和 `__getitem__` 方法】

```python
class SequenceIterator:
    """为已经定义了__len__和__getitem__的对象实现迭代器方法"""

    def __init__(self, seq):
        """迭代器初始化"""
        self._seq = seq
        self._k = -1  # 只有迭代器调用时才从 0 开始

    def __next__(self):
        """迭代器"""
        self._k += 1
        if self._k < len(self._seq):
            return self._seq[self._k]  # 返回向前一步后的值
        else:
            raise StopIteration()

    def __iter__(self):
        """一般__iter__方法都要返回自己，一种书写规范"""
        return self
```



### 3.3 练习：实现一个类模拟 Python 的 Range

```python
class Range:
    """模拟Python的Range类: range(start, stop, step)"""

    def __init__(self, start, stop=None, step=1):
        """
        初始化
        :param self: 对象自身
        :param start: 起始数字
        :param stop: 终止数字
        :param step: 每步跨度
        :return: Range类
        """
        if step == 0:
            raise ValueError("step can not be zero")

        if stop is None:
            # 应对输入 Range(n), 则当作 Range(0, n) 处理
            start = 0
            stop = start

        # 计算真实长度，应对有余数的情形
        self._length = max(0, (stop - start + step - 1) // step)
        # 考虑到已经计算长度，故无需记录 stop
        self._start = start
        self._step = step

    def __len__(self):
        """长度"""
        return self._length

    def __getitem__(self, index):
        """取数值"""
        if index < 0:
            index += self._length  # 从后向前取

        if index >= self._length or index < 0:
            raise IndexError("index out of range")

        return self._start + index * self._step

    def __str__(self):
        """只是以列表的形式展示，不重要。因为Range是模仿Python的range功能"""
        result = ""
        for i in Range(self._start, self._length):
            result += str(self._start + i * self._step) + ", "
        result = "[" + result[:-2] + "]"
        return result
```



## 4 继承

### 4.1 介绍

**继承**技术允许基于一个现有的类作为起点定义新的类。在面向对象的术语中，通常描述现有的类为基类 (base class)、父类 (parent class) 或者超类 (superclass)，而称新定义的类为子类 (subclass 或者 child class)

子类可以覆盖父类方法，也可以在父类的基础上扩展方法。

下面以第一节中定义的 `CreditCard` 类为父类，定义新的子类 `PredatoryCreditCard` 。

### 4.2 例：PredatoryCreditCard 子类

我们希望实现的新功能：

- 当尝试收费由于超过信用卡额度被拒绝时，将会收取 5 美元的费用
- 将有一个对未清余额按月收取利息的机制，即基于参数年利率 `apr` 计算利息

<img src="https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1740131659710.png" style="zoom:35%;" />

```python
class PredatoryCreditCard(CreditCard):
    """继承父类，扩展方法"""

    def __init__(self, customer, bank, acnt, limit, apr):
        """
        继承父类，常见新的一个账户
        :param customer: 用户名
        :param bank: 银行名
        :param acnt: 账户ID
        :param limit: 额度限制
        :param apr: 年利率，用以计算利息
        """
        super().__init__(customer, bank, acnt, limit)  # 调用父类的初始化方法 __init__
        self._apr = apr
        # self._balance 在调用父类初始化时也已经赋值 0

    def charge(self, price):
        """覆盖父类的charge方法，添加扣除手续费功能"""
        success = super().charge(price)  # 调用父类方法，检查是否仍在限额内
        if not success:
            self._balance += 5  # 如果失败收取 5 元手续费，贷款 balance 提高
        return success  # 返回结果 True or False

    def process_month(self):
        """收取每月利息"""
        if self._balance > 0:
            # 月贴现因子，apr 为年利率，故除以 12 年化
            monthly_factor = pow(1 + self._apr, 1 / 12)
            self._balance *= monthly_factor
```

#### 4.2.1 继承语法

定义子类 B 继承父类 A 时，采用下面的格式

```python
class B(A):
    pass
```

#### 4.2.2 初始化语句

在子类中首先需要调用父类的初始化语句和传参

```python
def __init__(self, param1, param2, sub_param):
    
    super().__init__(param1, param2)  # 调用父类的初始化方法 __init__
    
    self.sub_param = sub_param  # 子类的参数
```

#### 4.2.3 调用父类方法

在子类中调用父类方法，使用 `super()` 代替父类对象。例如：在使用父类的方法 `charge()` 时，直接采用

```python
super().charge(param1)  # 传入相应参数
```

> 【注意】在子类中，我们直接调用了父类的受保护数据 `_balance` (以 `_` 开头的数据视为受保护数据)，这不是最好的方法。只是在这里，我们需要在子类中修改 balance ，但如果调用 `get_balance` 方法是无法修改 balance 的，所以只好直接修改 `._balance` 。
>
> 【改进】不过可以在父类中定义非公有/受保护的方法 `_set_balance()` 让子类能使用它改变 `._balance` 而外界则不使用这个方法。如此可以做到子类使用父类方法改变父类受保护数据，而不是直接在父类数据上改变。

### 4.3 例：迭代数列的类的层次

Progression 类的分层如图。我们希望之后定义的各种数列均以 Progression 类为父类。

- Progression 类产生 `0, 1, 2, ...` 的无穷数列。

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1740193477222.png)

#### 4.3.1 父类：Progression 类

- 定义 `__next__, __iter__` 方法，实现 `next(obj)` 的方法迭代，同时也支持 `for i in obj`  的方法
- 定义 `_advance` 方法，为更新提供了非公有方法，为未来子类不同的更新形式提供方法
- 定义 `print_progression` 方法，方便以字符串的方式展示当前值的后 n 位数值，以序列的形式展示

```python
class Progression:
    """
    定义普适的数列父类
    默认产生 0, 1, 2, ... 的无穷数列
    """

    def __init__(self, start=0):
        """初始化记录起始默认值"""
        self._current = start

    def _advance(self):
        """
        非公有方法，用于更新 self._current
        为后续子类覆盖提供方法，子类不同的数列需要覆写不同的更新方法
        父类默认的更新方式为 += 1
        """
        self._current += 1

    def __next__(self):
        """迭代下一个值，或抛出异常 StopIteration"""
        if self._current is None:
            raise StopIteration
        else:
            result = self._current
            self._advance()
            return result

    def __iter__(self):
        """
        习惯于 iter 与 next 合并使用
        By convention, an iterator must return itself as an iterator.
        """
        return self

    def print_progression(self, n):
        """打印当前值之后的 n 个值"""
        print(" ".join(str(next(self)) for _ in range(n)))
```

> 注意此个例子，使用 `for i in obj` 会进入无穷序列。

#### 4.3.2 子类：等差数列类

我们希望等差数列 ArithmeticProgression 类产生等差数列，只需要继承父类后，覆写 `_advance` 方法。

```python
class ArithmeticProgression(Progression):
    """继承基础数列类，定义等差数列类"""

    def __init__(self, increment=1, start=0):
        """
        初始化等差数列
        :param increment: 公差
        :param start: 首项
        """
        super().__init__(start)
        self._increment = increment

    def _advance(self):
        """覆写新更新规则"""
        self._current += self._increment
```

```python
aprog1 = ArithmeticProgression(4)
aprog2 = ArithmeticProgression(4, 1)

aprog1.print_progression(7)
aprog2.print_progression(7)

"""
0 4 8 12 16 20 24
1 5 9 13 17 21 25
"""
```

#### 4.3.3 子类：等比数列类

类似地定义等比数列 GeometricProgression 类，需要注意首选不能为 0 

```python
class GeometricProgression(Progression):
    """等比数列"""

    def __init__(self, base=2, start=1):
        """
        初始化等比数列
        :param base: 公比，默认为 2
        :param start: 首项，不可为 0
        """
        super().__init__(start)
        self._base = base

    def _advance(self):
        """覆写更新规则"""
        self._current *= self._base
```

#### 4.3.4 子类：斐波那契数列类

定义斐波那契数列 FibonacciProgression 类。除了提供父类需要的参数首项和自己的参数第二项，还需要增加一个非公有参数记录相邻两项的差 `_prev` 。

```python
class FibonacciProgression(Progression):
    """斐波那契数列"""

    def __init__(self, first=0, second=1):
        """
        初始化，提供第一第二项
        :param first: 第一项，作为参数传给父类的 start
        :param second: 第二项
        """
        super().__init__(first)
        self._prev = second - first

    def _advance(self):
        """覆写更新规则"""
        self._prev, self._current = self._current, self._prev + self._current
```

```python
fcprog1 = FibonacciProgression()
fcprog2 = FibonacciProgression(1, 1)
fcprog1.print_progression(7)
fcprog2.print_progression(7)

"""
0 1 1 2 3 5 8
1 1 2 3 5 8 13
"""
```

### 4.4 抽象基类

**抽象基类**：一个类的唯一目的是作为继承的基类。其中被继承的我们称之为抽象基类，而其他的类则为具体的类。

- 一般而言，抽象类不能直接实例化，而具体的类可以被实例化。
- 理论上之前的例子中， Progression 类虽然严格来说是具体的类，但我们希望把它设计为一个抽象基类。

#### 4.4.1 `abc` 模块

Python 的 `abc` 模块提供了正式的抽象基类的定义，例如我们定义一个抽象基类 Sequence

- 其一，我们不需要这个抽象基类 Sequence 提供 `__len__` 和 `__getitem__` 的具体实现，这两个方法的实现由继承它的子类完成。
- 其二，我们希望这个基类能完成功能：通过整数查看序列元素，所以要具体实现 `__contains__` `index` 和 `count` 方法。

```python
from abc import ABC, abstractmethod


class Sequence(ABC):
    """抽象基类 Sequence"""

    @abstractmethod
    def __len__(self):
        """返回序列长度，由子类实现"""
        pass

    @abstractmethod
    def __getitem__(self, j):
        """返回第 j 位置的值，由子类实现"""
        pass

    def __contains__(self, val):
        """查看 val 是否在序列中，返回 True or False"""
        for j in range(len(self)):
            if val == self[j]:
                return True
        return False

    def index(self, val):
        """返回 val 在序列中的下标"""
        for j in range(len(self)):
            if val == self[j]:
                return j
        raise ValueError("Value not found")

    def count(self, val):
        """计数多少值等于 val"""
        k = 0
        for j in range(len(self)):
            if val == self[j]:
                k += 1
        return k
```

> 这一类与 Python 的 collections 模块的 `collections.abc.Sequence` 类似。
>
> 因为采用抽象定义，故类 `Sequence` 不能被实例化。

- 继承 `abc.ABC` 类，表明这是一个抽象基类，只能被继承不可被实例化。

- 上述的修饰器 `@abstractmethod` 表名这个方法必须由子类实现，抽象基类无需实现。

#### 4.4.2 `collections` 模块

使用 `abc` 模块定义过于复杂，可以直接使用 Python 的 `collections` 模块，它已经封装了常见的抽象基类。

- 例如在第 3.3 节实现的 Range 类，已经实现了 `__len__` 和 `__getitem__` 方法，但没有实现抽象基类中的`__contains__` `index` 和 `count` 方法。
- 而这与 `collections.abc.Sequence` 类相匹配，可以让我们定义的 `Range` 类继承 `collections.abc.Sequence` 类，从覆写 `__len__` 和 `__getitem__` ，同时也依靠父类实现 contains、index 和 count 方法。

```python
from collections.abc import Sequence

# 改写 Range 的定义
class Range(Sequence):
    ...
```

> 【注意】在 `Python3.x` 版本后 `collections` 相关抽象基类被移动到了 `collections.abc` 中。故使用时应导入 `from collections.abc import Sequence`

【结果测试】

```python
if __name__ == "__main__":
    r = NewRange(0, 10)
    print(r)

    print(4 in r)  # 判断 4 是否在序列中 __contains__ 方法
    print(r.index(0))  # 返回下标 index 方法
    print(r.count(1))  # 查看多少值等于 1
    
"""
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
True
0
1
"""
```

> 其实采用之前我们自定义的 `Sequence` 抽象基类也可以达到相同目的。

```python
from abc import ABC, abstractmethod

class Sequence(ABC):
    ...

class Range(Sequence):
    ...
```



## 5 命名空间和面对对象

### 5.1 实例和类的命名空间

以 CreditCard 类和 PredatoryCreditCard 类为例，展示出其类命名空间和实例命名空间如下：

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1740205039504.png)

### 5.2 类数据成员

**类级别的数据成员**：一些值（如常量）被一个类的所有实例共享

- 在这种情况下，在每个实例的命名空间中存储这个值就会造成不必要的浪费。所以使用如下格式定义这样的类数据成员。

```python
class PredatoryCreditCard(CreditCard):
    OVER_LIMIT_FEE = 5
    ...
    
    def charge(self, price):
        """覆盖父类的charge方法，添加扣除手续费功能"""
        success = super().charge(price)  # 调用父类方法，检查是否仍在限额内
        if not success:
            # 使用 PredatoryCreditCard.OVER_LIMIT_FEE 方式调用类数据成员
            self._balance += PredatoryCreditCard.OVER_LIMIT_FEE
        return success  # 返回结果 True or False
```

### 5.3 嵌套类

**嵌套类**：在一个类的定义里定义另一个类。需要注意的是，二者只是嵌套关系，没有继承关系。

```python
class A:
    class B:
        ...
```

### 5.4 字典和 `__slots__` 声明

Python 提供了一种直接的机制来表示实例命名空间：类定义必须提供一个名为 `__slots__` 的类级别的成员分配给一个固定的字符串序列。例如，在 `CreditCard` 类中，声明如下：

```python
class CreditCard:
    __slots__ = '_customer', '_bank', '_acnt', '_limit', '_balance'
```

当子类继承时，只需要声明子类新增的实例即可

```python
class PredatoryCreditCard(CreditCard):
    __slots__ = '_apr'
```



## 6 深拷贝和浅拷贝

### 6.1 直接赋值复制 

当使用 `a = b` 时，Python 在做的只是拷贝了一个别名，或者说是一个地址。

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1740206027790.png)

当遇到不可变类型时还不会出现问题，一旦二者指向的是可变类型，例如列表。则会出现一方变，整体变。

```python
""" 1. 简单赋值，复制了地址 """
print("1. 简单赋值，复制了地址")
a = [1, 2]
b = a
b.append(3)

print(a)  # [1, 2, 3]
```

### 6.2 浅拷贝

例如：列表中写入颜色对象。 `warmtones` 表示现有的颜色列表。希望创建一个新的 `palette` 列表，复制一份 `warmtones` 列表。但是对 `palette` 不希望影响到 `warmtones` 。

```python
""" 2. 浅拷贝，简历了新地址，但仍然指向同一不可变数据 """
print("2. 浅拷贝，简历了新地址，但仍然指向同一不可变数据")
warmtones = ['red', 'green', 'blue']
palette = list(warmtones)  # 浅拷贝
palette[0] = 'yellow'

print(warmtones)  # ['red', 'green', 'blue']
print(palette)  # ['yellow', 'green', 'blue']
```

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1740206762911.png)

这比直接赋值更好，即复制了一份可变数据类型 (list) ，但指向的不可变数据仍然相同。例如：`warmtones[0]`  和 `palette[0]` 为实例 `_red` 的别名，实际指向相同。

### 6.3 深拷贝

我们希望让 `warmtones` 和 `palette` 之间完全没有关联，就可以使用 `copy.deepcopy()` 方法。

```python
import copy

""" 3. 深拷贝，完全拷贝一份 """
print("3. 深拷贝，完全拷贝一份")
warmtones = ['red', 'green', 'blue']
palette = copy.deepcopy(warmtones)  # 深拷贝
palette[0] = 'yellow'

print(warmtones)  # ['red', 'green', 'blue']
print(palette)  # ['yellow', 'green', 'blue']
```

![](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1740206987932.png)



































