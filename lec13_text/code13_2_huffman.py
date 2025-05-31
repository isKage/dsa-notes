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
