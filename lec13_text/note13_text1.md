# 文本处理

本章介绍常见的文本处理算法：模式匹配问题的 KMP 算法、文本压缩的 Huffman 编码树。

## 1 模式匹配

设字符串 P 的长度为 m 。P 的一个子串（substring）`P[i:j+1]` 是 P 中从第 i 个到第 j 个字符构成的字符串

- P 的一个前缀（prefix）为：`P[0:i]`
- P 的一个后缀（suffix）为：`P[i:m-1]`

**文本的模式匹配（pattern matching）问题：**给定一个文本（text）字符串 `T` 和一个模式（pattern）字符串 `P` ，在 T 中找到一个与 P 一致的子串。

### 1.1 穷举

蛮力法/穷举法（brute-force）即列举所有可能的情况，并检查是否有符合要求的情况或寻找最优情况。模式匹配中，蛮力法即考虑所有 P 与 T 的子串可能匹配上的情况。

- 具体操作：将 P 与 T 从头部对齐开始，每一步把 P 相对于 T 向后移动一位，直到找到一个匹配的位置或所有 P 与 T 的相对位置均被探索过。
- 蛮力法的时间复杂度为 **O(nm)** ，其中 n 为 T 的长度，m 为模式 P 的长度。
- 蛮力法的最坏情况例如：`T = "aaaaaaaah"` `P = "aaah"`

![穷举法示例](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1748681572546.png)

**代码实现**

```python
def find_brute(P, T):
    """
    穷举法模式匹配
    :param P: 寻找的模式
    :param T: 被查找的对象
    :return: T 的索引位置, 若失败返回 -1
    """
    n, m = len(T), len(P)
    for i in range(n - m + 1):
        k = 0
        while k < m and T[i + k] == P[k]:
            k += 1  # 当前匹配成功, 继续匹配
        if k == m:
            return i  # 完整匹配, 返回位置
    return -1
```

### 1.2 KMP 算法

KMP（**K**nuth-**M**orris-**P**ratt ）算法：预先计算模式部分之间的自重叠，从而当不匹配发生在一个位置时，我们在继续搜寻之前就能立刻知道移动模式的最大数目。

- 先对模式字符串进行预处理，以寻找其前缀与其本身匹配的位置：定义**失败函数（failure function）**`F(j)` 为最长的既为 `P[0:j+1]` 前缀又为 `P[1:j+1]` 后缀的子串长度。
- KMP 算法在蛮力法上进行的改进为：匹配失败发生在 `P[j] != T[i]` 时，令 `j = F(j-1)` 继续尝试匹配。

KMP 算法示例：现有文本字符串 `abaababaabababaca` 和模式串 `ababac` 。请求出模式串的失败函数，画出用 KMP 算法进行匹配的过程，并统计出比较的次数。

模式串 `ababac` 的失败函数为：`F(j)` 为最长的既为 `P[0: j]` 前缀又为 `P[1: j]` 后缀的子串长度

| `j`    |  0   |  1   |  2   |  3   |  4   |  5   |
| :----- | :--: | :--: | :--: | :--: | :--: | :--: |
| `P[j]` | `a`  | `b`  | `a`  | `b`  | `a`  | `c`  |
| `F[j]` |  0   |  0   |  1   |  2   |  3   |  0   |

KMP 算法总共比较了 $22$ 次（若匹配成功就退出）

![KMP 算法的比较过程](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1748682341243.png)

**代码实现**

```python
def compute_kmp_fail(pattern):
    """计算模式的失败函数"""
    m = len(pattern)
    fail = [0] * m
    j = 1
    k = 0
    while j < m:
        if pattern[j] == pattern[k]:
            fail[j] = k + 1
            j += 1
            k += 1
        elif k > 0:
            k = fail[k - 1]
        else:
            j += 1
    return fail


def find_kmp(pattern, text):
    """
    从 text 中找到第一个完全匹配 pattern 的位置
    :param pattern: 寻找的模式
    :param text: 被查找的对象
    :return: text 的索引位置, 若失败返回 -1
    """
    m, n = len(pattern), len(text)
    if m == 0:
        return 0

    fail = compute_kmp_fail(pattern)
    j = 0
    k = 0
    while j < n:
        if text[j] == pattern[k]:
            if k == m - 1:
                return j - m + 1
            j += 1
            k += 1
        elif k > 0:
            k = fail[k - 1]
        else:
            j += 1
    return -1
```

**性能分析**

- 失败函数：匹配成功 `i` 加一，匹配失败则 `i or j` 至少加一，最多 2m 次操作，复杂度为 **O(m)** ，m 为模式长度。

- KMP 算法：匹配成功 `i` 加一，匹配失败则 `i or j` 至少加一，最多 2n 次操作，加之失败函数的复杂度，KMP 算法的复杂度为 **O(n + m)** ，m 为模式长度，n 为被匹配字符串长度。



## 2 文本压缩与贪心算法

**文本压缩（text compression）问题：**将给定字符串 **X** 压缩为一个更小的二进制字符串 **Y** 。

**霍夫曼编码（Huffman encoding）**是一种变长编码方式，可以得到字符串的最优二进制表示，其思路如下：

- 对字符串中的每个字符 `c` ，计算其出现频率 `f(c)`
- 用长度较短的码表示高频字符，所有码字均不为其他码字的前缀
- 使用一棵最优编码树决定编码方式

### 2.1 霍夫曼编码 Huffman

**前缀码（prefix code）：**所有码字均不为其他码字的前缀的一种编码方式

- 一棵编码树（encoding tree）表示一种前缀码
- 每个叶子节点存储一个被编码的字符
- 字符的码字由从根节点到该字符所在的叶子节点的路径确定（向左即编码为0，向右即编码为1）

**霍夫曼编码**步骤：

- 将所有字符用一棵单节点的树表示，节点权重为字符出现的频率
- 在每一步，将两棵权重最小的树合并为一棵，计算其权重
- 重复以上步骤直到只有一棵树

霍夫曼编码得到的编码树为**霍夫曼树（Huffman tree）**。

![霍夫曼编码树示例](https://blog-iskage.oss-cn-hangzhou.aliyuncs.com/images/QQ_1748682890546.png)

### 2.2 Huffman 代码实现和算法分析

#### 2.2.1 代码实现

霍夫曼编码可以使用堆实现的优先级队列 [code13_2_huffman.py](code13_2_huffman.py) 

```python
from utils import HeapPriorityQueue


class HuffmanNode:
    """霍夫曼树节点"""

    def __init__(self, freq, char=None, left=None, right=None):
        """
        实例化一个霍夫曼树的节点
        :param freq: 字符的频率
        :param char: 字符, 当为内部节点时不存储字符
        :param left: 左子节点
        :param right: 右子节点
        """
        self.freq = freq  # 字符的频率
        self.char = char  # 叶子节点存储字符
        self.left = left
        self.right = right

    def __lt__(self, other):
        """定义比较方法, 用于自下而上建堆时比较频率"""
        return self.freq < other.freq


class HuffmanTree:
    """霍夫曼编码树类"""

    def __init__(self, text):
        """
        输入 text 进行霍夫曼树编码
        :param text: 被压缩的文本
        """
        self.text = text
        self.freq_map = self._build_freq_map(text)  # 频率表
        self.root = self._build_tree()  # 建立编码树
        self.code_map = self._generate_codes()  # 获取编码结果

    def _build_freq_map(self, text):
        """
        根据文本建立每个字符的频率表
        :param text: 被压缩的文本
        :return: 每个字符的频率表 {char: freq}
        """
        freq_map = {}
        for ch in text:
            freq_map[ch] = freq_map.get(ch, 0) + 1
        return freq_map

    def _build_tree(self):
        """利用基于堆实现的优先级队列 HeapPriorityQueue 建立 Huffman 编码树"""
        pq = HeapPriorityQueue()

        # 1. 为每一个字符创建节点
        for ch, freq in self.freq_map.items():
            pq.add(freq, HuffmanNode(freq, ch))  # key = freq

        # 2. 自底向上合并节点
        while len(pq) > 1:
            f1, n1 = pq.remove_min()
            f2, n2 = pq.remove_min()
            merged = HuffmanNode(f1 + f2, left=n1, right=n2)
            pq.add(merged.freq, merged)

        return pq.remove_min()[1]  # 返回根节点

    def _generate_codes(self):
        """生成编码结果 {char: encoding code}"""
        code_map = {}

        def _generate(node, code):
            """根据左右子树不断更新编码"""
            if node is None:
                return
            if node.char is not None:
                code_map[node.char] = code
                return
            _generate(node.left, code + '0')
            _generate(node.right, code + '1')

        _generate(self.root, '')  # 从根节点开始遍历
        return code_map

    def encode(self):
        """编码: text 编码后的结果"""
        return ''.join(self.code_map[ch] for ch in self.text)

    def decode(self, encoded_text):
        """解码: encoded_text 解码后的结果"""
        result = []
        node = self.root
        for bit in encoded_text:
            node = node.left if bit == '0' else node.right
            if node.char is not None:
                result.append(node.char)
                node = self.root
        return ''.join(result)
```

例子：

```python
if __name__ == "__main__":
    text = "this is an example of a huffman tree"

    huff_tree = HuffmanTree(text)
    encoded = huff_tree.encode()
    decoded = huff_tree.decode(encoded)

    print("\nCode Map:")
    print(huff_tree.code_map)

    print("\nEncoded Code:")
    print(encoded)

    print("\nDecoded Text:")
    print(decoded)
```

结果：

```python
Code Map:
{'e': '000', 'x': '00100', 'p': '00101', 'i': '0011', 'n': '0100', 'o': '01010', 'u': '01011', 'a': '011', 't': '1000', 'm': '1001', 'h': '1010', 's': '1011', 'r': '11000', 'l': '11001', 'f': '1101', ' ': '111'}

Encoded Code:
100010100011101111100111011111011010011100000100011100100101110010001110101011011110111111010010111101110110010110100111100011000000000

Decoded Text:
this is an example of a huffman tree
```

#### 2.2.2 算法分析

长度为 n 的文本，不同字符（包括各种特殊字符）的个数为 d ，构造最优编码/霍夫曼编码的时间复杂度为：

- 统计字符出现频率：O(n)
- 优先级队列的插入与删除： O(d log d)

总运行时间： **O(n + d log d)**

#### 2.2.3 Huffman 编码最优性证明


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

### 2.3 贪心算法

**贪心算法（greedy method）**是一种通用算法设计范式，贪心算法在问题有贪心选择（greedy-choice）性质时表现最佳。

- 贪心选择性质：全局最优解可以通过解决一系列局部最优问题来解决

贪心算法常按以下步骤设计：

- 将最优化问题转化为这样的形式：对其作出一次选择后，只剩下一个子问题需要求解
- 证明作出贪心选择后，原问题总是存在最优解，即贪心选择是安全的
- 证明作出贪心选择后，剩余子问题的最优解与贪心选择组合即可得到原问题的最优解

**贪心算法例：**

- Prim 算法
- Kruskal 算法
- Dijkstra 算法
- Huffman 编码
