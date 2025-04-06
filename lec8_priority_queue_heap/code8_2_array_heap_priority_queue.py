from utils import HeapPriorityQueue

# for test

hpq = HeapPriorityQueue()
print("=" * 15, "Heap Priority Queue by Array", "=" * 15)
hpq.add(1, 'small')
hpq.add(3, 'median')
hpq.add(5, 'large')
print("The min is:", hpq.min())
print("Delete the min:", hpq.remove_min())
print("Now, the min is:", hpq.min())

print("=" * 15, "Heap Priority Queue by Array (Initialized with a list)", "=" * 15)
l = [(1, 'small'), (2, 'median'), (3, 'large')]
hpq = HeapPriorityQueue(l)
print("The min is:", hpq.min())
print("Delete the min:", hpq.remove_min())
print("Now, the min is:", hpq.min())
