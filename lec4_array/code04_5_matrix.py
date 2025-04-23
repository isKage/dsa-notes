# %% 误用
m = 3
n = 6
data = [[0] * n] * m
data[0][0] = 1
print(data)

# %% 正确创建方式
m = 3
n = 6
data = [[0] * n for _ in range(m)]
data[0][0] = 1
print(data)
