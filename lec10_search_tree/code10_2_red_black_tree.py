from utils import RedBlackTreeMap

"""=============== Red Black Tree Map ==============="""
red_black_tree = RedBlackTreeMap()
print("=" * 15, "Red Black Tree Map", "=" * 15)
red_black_tree[1] = 'redblack1'
red_black_tree[2] = 'redblack2'
red_black_tree[3] = 'redblack3'
red_black_tree[4] = 'redblack4'
red_black_tree[5] = 'redblack5'
red_black_tree[6] = 'redblack6'

print(f"key = 4, value = {red_black_tree[4]}\n")
print("from 1 to 4")
for item in red_black_tree.find_range(1, 4):
    print(item)

print(f"\nmin = {red_black_tree.find_min()}")
print("del key = 1 and 2")
del red_black_tree[1]
del red_black_tree[2]
print(f"min = {red_black_tree.find_min()}")
