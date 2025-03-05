from array import array

x = array('i', [1, 2, 3, 4])
print(id(x[1]) - id(x[0]))
print(id(x[2]) - id(x[1]))

# %%
primes = [2, 3, 5, 7, 11, 13, 17, 19]
temp = [7, 11, 13]
print(
    id(7) == id(primes[3]) == id(temp[0])
)

# %%
import sys

data = []
for k in range(20):
    length = len(data)
    size = sys.getsizeof(data)
    print("数组大小: {}, 数组内存分配: {} Byte (字节)".format(length, size))
    data.append(None)
