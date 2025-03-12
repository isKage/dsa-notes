from utils import PositionalList


class FavoritesList:
    """有序列表方式实现"""

    # -------------- 内嵌的 _Item 类 --------------
    class _Item:
        __slots__ = '_value', '_count'  # 限制实例属性，优化内存使用

        def __init__(self, e):
            self._value = e  # 用户提供的元素
            self._count = 0  # 访问计数，初始为 0

    # -------------- 非公有方法 --------------
    def _find_position(self, e):
        """返回元素 e 的位置类 Position"""
        walk = self._data.first()  # 在初始化后，self._data 是 PositionalList 类

        # 寻找元素 e 的位置，返回位置类 Position
        while walk is not None and walk.element()._value != e:
            walk = self._data.after(walk)  # 移动到下一个节点
        return walk

    def _move_up(self, p):
        """插入排序思想，按照次数 _count 产生有序列表"""
        # 与之前插入排序 insertion_sort 思路基本相同
        # 甚至更为简单，比较对象只用最后新加入的元素
        if p != self._data.first():
            cnt = p.element()._count
            walk = self._data.before(p)
            if cnt > walk.element()._count:
                while (walk != self._data.first() and
                       cnt > self._data.before(walk).element()._count):
                    walk = self._data.before(walk)
                self._data.add_before(walk, self._data.delete(p))

    # -------------- 公有方法 --------------
    def __init__(self):
        """初始化收藏夹列表类，直接实例化一个 PositionalList 类"""
        self._data = PositionalList()

    def __len__(self):
        """返回长度"""
        return len(self._data)  # PositionalList 已经定义了 __len__()

    def is_empty(self):
        """查看是否为空"""
        return len(self._data) == 0

    def access(self, e):
        """访问元素 e 增加次数/添加元素"""
        p = self._find_position(e)
        if p is None:  # 不存在则插入
            # 向列表增加对象 _Item
            # 可以理解为 PositionalList 的链表的节点 _Node 的 _element 存储着 _Item 对象的地址
            p = self._data.add_last(self._Item(e))
        p.element()._count += 1

        self._move_up(p)  # 排序

    def remove(self, e):
        """从收藏夹列表类中移除元素 e 对应的 _Item 对象"""
        p = self._find_position(e)
        if p is not None:
            self._data.delete(p)  # 这里的 _Item 对象相当于链表的 element 值

    def top(self, k):
        """迭代器的方式产生前 k 个元素"""
        if not 1 <= k <= len(self):
            raise ValueError('Illegal value of k')

        walk = self._data.first()
        for j in range(k):
            # 迭代后移
            item = walk.element()
            yield item._value
            walk = self._data.after(walk)


class FavoritesListMTF(FavoritesList):
    """利用 More-To-Front 启发式算法实现收藏夹列表类"""

    # -------------- 只需要重载/覆写 _move_up() 和 top() 方法即可 --------------
    def _move_up(self, p):
        """每次调用意味着被访问，被访问就移到最前"""
        if p != self._data.first():
            self._data.add_first(self._data.delete(p))

    def top(self, k):
        """因为列表无序，需要找到最大的前 k 个元素"""
        if not 1 <= k <= len(self):
            raise ValueError('Illegal value of k')

        # 临时复制一份原列表
        temp = PositionalList()
        for item in self._data:
            temp.add_last(item)

        for j in range(k):
            # 遍历一边找到最大的
            highPos = temp.first()
            walk = temp.after(highPos)
            while walk is not None:
                if walk.element()._count >= highPos.element()._count:
                    highPos = walk
                walk = temp.after(walk)
            yield highPos.element()._value

            # 删除最大的之后再遍历
            temp.delete(highPos)


if __name__ == '__main__':
    import time

    print("=" * 15, "FavoritesList 有序列表方式", "=" * 15)
    favorites = FavoritesList()

    start = time.time()
    favorites.access("web1")
    favorites.access("web1")
    favorites.access("web1")
    favorites.access("web2")
    favorites.access("web3")
    favorites.access("web3")
    favorites.access("web3")
    favorites.access("web3")
    favorites.access("web4")
    favorites.access("web4")
    favorites.access("web5")
    favorites.access("web6")
    favorites.access("web6")
    end = time.time()

    for top_web in favorites.top(3):
        print(top_web)
    print("time cost: {}".format(end - start))

    # --------------------------------------------------------


    print("=" * 15, "FavoritesListMTF More-To-Front 启发式算法", "=" * 15)
    favorites_mtf = FavoritesListMTF()

    start = time.time()
    favorites_mtf.access("url1")
    favorites_mtf.access("url1")
    favorites_mtf.access("url1")
    favorites_mtf.access("url1")
    favorites_mtf.access("url2")
    favorites_mtf.access("url2")
    favorites_mtf.access("url2")
    favorites_mtf.access("url3")
    favorites_mtf.access("url4")
    favorites_mtf.access("url5")
    favorites_mtf.access("url6")
    favorites_mtf.access("url6")
    favorites_mtf.access("url6")
    end = time.time()

    for top_web in favorites_mtf.top(3):
        print(top_web)
    print("time cost: {}".format(end - start))