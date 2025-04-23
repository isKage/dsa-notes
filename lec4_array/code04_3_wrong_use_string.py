import time

document = "hello world, welcome to Python :) Having a nice day! ...." * 10000

# 误用
letter = ""
start = time.time()
for char in document:
    if char.isalnum():
        # 使用重载后的 + 进行组合
        letter += char
end = time.time()
# print(letter)
print("直接组成消耗的时间: {}".format(end - start))

# 正确
tmp = []  # 临时表
start = time.time()
for char in document:
    if char.isalpha():
        # append 操作平均为 O(1)
        tmp.append(char)
# 最后再组成字符串
letter = "".join(tmp)
end = time.time()
# print(letter)
print("使用临时表消耗的时间: {}".format(end - start))
