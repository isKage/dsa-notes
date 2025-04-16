try:
    from .map_base import MapBase
except ImportError:
    from map_base import MapBase


class UnsortedTableMap(MapBase):
    """基于未排序列表实现映射"""

    def __init__(self):
        """初始化列表"""
        self._table = []

    def __getitem__(self, k):
        """根据键取值 M[k]"""
        for item in self._table:
            if k == item._key:
                return item._value
        raise KeyError('Key Error: ' + repr(k))

    def __setitem__(self, k, v):
        """设置键为 k 的值为 v 若没有则新建 M[k] = v"""
        for item in self._table:
            if k == item._key:
                item._value = v
                return
        # 若没有找到匹配的 key 则新建
        self._table.append(self._Item(k, v))

    def __delitem__(self, k):
        """删除键为 k 的对象"""
        for j in range(len(self._table)):
            if k == self._table[j]._key:
                self._table.pop(j)  # 找到后使用列表的删除方式
                return
        raise KeyError('Key Error: ' + repr(k))

    def __len__(self):
        """对象总数目"""
        return len(self._table)

    def __iter__(self):
        """迭代器，指出 for item in M 操作"""
        for item in self._table:
            yield item._key  # 返回键 key


if __name__ == '__main__':
    m = UnsortedTableMap()
    m['test1'] = 1
    m['test2'] = 2
    m['test3'] = 3
    for key in m:
        print("key: {}, value: {}".format(key, m[key]))
