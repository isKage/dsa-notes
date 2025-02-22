from lec1utils import CreditCard
from lec1utils import Vector
from lec1utils import SequenceIterator
from lec1utils import Range

from lec1utils import PredatoryCreditCard

from lec1utils import Progression
from lec1utils import ArithmeticProgression
from lec1utils import GeometricProgression
from lec1utils import FibonacciProgression

from lec1utils import NewRange

print("CreditCard===============================================================================")
# 实例化
cc = CreditCard("John", "Bank1", "123 456 789", 3010.)

# 获取基本信息
print(cc.get_customer())
print(cc.get_bank())
print(cc.get_acnt())
print(cc.get_limit())
print(cc.get_balance())

# 调用 charge
print(cc.charge(1000.))
print(cc.get_balance())

# 调用 make_payment
cc.make_payment(100.)
print(cc.get_balance())

print("Vector===============================================================================")
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

print("SequenceIterator===============================================================================")
l = [1, 2, 3, 4, 5]
t = (9, 8, 7, 6, 5)

l_seq = SequenceIterator(l)
print(next(l_seq))
print(next(l_seq))
print(next(l_seq))

t_seq = SequenceIterator(t)
print(next(t_seq))
print(next(t_seq))
print(next(t_seq))

print("Range===============================================================================")
r = Range(0, 10, 3)
for i in r:
    print(i)

print("PredatoryCreditCard===============================================================================")
pcc = PredatoryCreditCard("John", "Bank1", "123 456 789", 1000., 0.24)
print(pcc.charge(500))
print(pcc.get_balance())

print(pcc.charge(1000))
print(pcc.get_balance())

# 收利息
pcc.process_month()
print(pcc.get_balance())

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

print("NewRange===============================================================================")
r = NewRange(0, 10)
print(r)

print(4 in r)  # 判断 4 是否在序列中 __contains__ 方法
print(r.index(0))  # 返回下标 index 方法
print(r.count(1))  # 查看多少值等于 1
