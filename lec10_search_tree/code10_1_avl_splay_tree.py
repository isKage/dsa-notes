from utils import AVLTreeMap, SplayTreeMap

"""=============== AVL Tree Map ==============="""
avl_tree = AVLTreeMap()
print("=" * 15, "AVL Tree Map", "=" * 15)
avl_tree[1] = 'avl1'
avl_tree[2] = 'avl2'
avl_tree[3] = 'avl3'
avl_tree[4] = 'avl4'
avl_tree[5] = 'avl5'
avl_tree[6] = 'avl6'

print(f"key = 4, value = {avl_tree[4]}\n")
print("from 1 to 4")
for item in avl_tree.find_range(1, 4):
    print(item)

print(f"\nmin = {avl_tree.find_min()}")
print("del key = 1")
del avl_tree[1]
print(f"min = {avl_tree.find_min()}")

"""=============== Splay Tree Map ==============="""
splay_tree = SplayTreeMap()
print("=" * 15, "Splay Tree Map", "=" * 15)
splay_tree[1] = 'splay1'
splay_tree[2] = 'splay2'
splay_tree[3] = 'splay3'
splay_tree[4] = 'splay4'
splay_tree[5] = 'splay5'
splay_tree[6] = 'splay6'

print(f"key = 4, value = {splay_tree[4]}\n")
print("from 1 to 4")
for item in splay_tree.find_range(1, 4):
    print(item)

print(f"\nmin = {splay_tree.find_min()}")
print("del key = 1 and 2")
del splay_tree[1]
del splay_tree[2]
print(f"min = {splay_tree.find_min()}")
