"""
写一段 python 程序，计算 1 + 2 + 3 + ... + 1,000,000 输出计算所需时间。
"""

# time 模块记录时间

import time

sum = 0  # 记录求和结果
start = time.time()  # 开始时间
for i in range(1, 1000000 + 1):
    sum = sum + i
end = time.time()  # 结束时间
print("Calculate Result: {}\nTime Cost: {:.4f}s".format(sum, end - start))
