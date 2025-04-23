from time import time

''' # 实验分析 # '''

start = time()

# run algorithm
total = 0
for i in range(100000):
    total += i

end = time()

print(end - start)
