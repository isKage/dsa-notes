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


if __name__ == '__main__':
    v1 = Vector(3)
    v1[1] = 1
    v1[2] = 2
    print(v1)

    v2 = Vector(3)
    print(v2[1])
    v2[0] = 2
    v2[1] = 1
    print(v2)

    v3 = v1 + v2
    v4 = v1 - v2
    print(v3)
    print(v4)

    print(len(v3))

    print(v1 == v2)
