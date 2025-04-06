from utils import UnsortedPriorityQueue
from utils import SortedPriorityQueue

# for test

upq = UnsortedPriorityQueue()
print("=" * 15, "Unsorted Priority Queue", "=" * 15)
upq.add(1, 'small')
upq.add(3, 'median')
upq.add(5, 'large')
print("The min is:", upq.min())
print("Delete the min:", upq.remove_min())
print("Now, the min is:", upq.min())

spq = SortedPriorityQueue()
print("=" * 15, "Sorted Priority Queue", "=" * 15)
spq.add(1, 'small')
spq.add(3, 'median')
spq.add(5, 'large')
print("The min is:", spq.min())
print("Delete the min:", spq.remove_min())
print("Now, the min is:", spq.min())
