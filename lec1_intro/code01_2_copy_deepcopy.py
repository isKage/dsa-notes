import copy

""" 1. 简单赋值，复制了地址 """
print("1. 简单赋值，复制了地址")
a = [1, 2]
b = a
b.append(3)

print(a)  # [1, 2, 3]

""" 2. 浅拷贝，简历了新地址，但仍然指向同一不可变数据 """
print("2. 浅拷贝，简历了新地址，但仍然指向同一不可变数据")
warmtones = ['red', 'green', 'blue']
palette = list(warmtones)  # 浅拷贝
palette[0] = 'yellow'

print(warmtones)  # ['red', 'green', 'blue']
print(palette)  # ['yellow', 'green', 'blue']

""" 3. 深拷贝，完全拷贝一份 """
print("3. 深拷贝，完全拷贝一份")
warmtones = ['red', 'green', 'blue']
palette = copy.deepcopy(warmtones)  # 深拷贝
palette[0] = 'yellow'

print(warmtones)  # ['red', 'green', 'blue']
print(palette)  # ['yellow', 'green', 'blue']
