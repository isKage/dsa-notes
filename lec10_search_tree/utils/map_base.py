try:
    from collections.abc import MutableMapping  # Python 3.3+
except ImportError:
    from collections import MutableMapping  # Python 2.7 - 3.2 (已废弃)


class MapBase(MutableMapping):
    """映射 Map 的基础父类"""

    # ---------- 嵌套的 _Item 类，存储键值对 ----------
    class _Item:
        """存储键值对"""
        __slots__ = '_key', '_value'

        def __init__(self, k, v):
            """初始化键值对"""
            self._key = k
            self._value = v

        def __eq__(self, other):
            """a == b 等价于 a 和 b 键值相等"""
            return self._key == other._key

        def __ne__(self, other):
            """a != b 等价于 a 和 b 键值不等"""
            return not (self == other)

        def __lt__(self, other):
            """比较键值"""
            return self._key < other._key

        def value(self):
            return self._value

        def key(self):
            return self._key
