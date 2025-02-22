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


if __name__ == "__main__":
    print("Progression===============================================================================")
    prog = Progression()
    print(next(prog))
    print(next(prog))
    prog.print_progression(3)

    prog5 = Progression(5)
    print(next(prog5))
    print(next(prog5))
    prog5.print_progression(3)

    print("ArithmeticProgression===============================================================================")
    aprog1 = ArithmeticProgression(4)
    aprog2 = ArithmeticProgression(4, 1)

    aprog1.print_progression(7)
    aprog2.print_progression(7)

    print("GeometricProgression===============================================================================")
    gprog1 = GeometricProgression()
    gprog2 = GeometricProgression(3, 2)

    gprog1.print_progression(7)
    gprog2.print_progression(7)

    print("FibonacciProgression===============================================================================")
    fcprog1 = FibonacciProgression()
    fcprog2 = FibonacciProgression(1, 1)
    fcprog1.print_progression(7)
    fcprog2.print_progression(7)
