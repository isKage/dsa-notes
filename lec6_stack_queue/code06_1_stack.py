from utils import ArrayStack


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


if __name__ == '__main__':
    print("=" * 15, "reverse the file", "=" * 15)
    reverse_file('example.txt')

    print("=" * 15, "is_matched", "=" * 15)
    print(is_matched("((()()){([()])})"))  # True
    print(is_matched("({[])}"))  # False
    print(is_matched("{(5 + x) - [1 + (y - z) * 4]}"))  # True

    print("=" * 15, "is_matched html", "=" * 15)
    html_file = open('example.html')
    html_content = html_file.read()
    row = "".join(html_content.split('\n'))
    print(is_matched_html(row))
    html_file.close()

    print("=" * 15, "span", "=" * 15)
    X = [6, 3, 4, 5, 2, 1, 4, 9, 10, 1, 3, 20, 11, 9]
    print(spans(X, len(X)))
