from utils import SortedPriorityQueue
from utils import UnsortedPriorityQueue
from utils import HeapPriorityQueue


def pq_sort(C, pq):
    """伪代码：对 C 排序，借用 pq 优先级队列类"""
    n = len(C)
    P = pq()  # 辅助优先级队列
    for j in range(n):
        element = C.delete(C.first())  # 拿出 C 的元素
        P.add(element, element)  # 存储 (e, e)
    for j in range(n):
        (k, v) = P.remove_min()  # 取出最小的 e
        C.add_last(v)  # 放回原来的 C


def selection_sort(C):
    n = len(C)
    P = UnsortedPriorityQueue()
    for j in range(n):
        element = C.pop()
        P.add(element, element)
    for j in range(n):
        (k, v) = P.remove_min()
        C.append(v)


def insertion_sort(C):
    n = len(C)
    P = SortedPriorityQueue()
    for j in range(n):
        element = C.pop()
        P.add(element, element)
    for j in range(n):
        (k, v) = P.remove_min()
        C.append(v)


def heap_sort(C):
    # 特别地，利用了自底向上构建堆的初始化方法 O(n)
    P = HeapPriorityQueue(C)  # 见之前定义的 HeapPriorityQueue 类
    for j in range(len(C)):  # O(n log n)
        C[j] = P.remove_min()[0]


def heapsort(arr, descend=False):
    """原地堆排序"""
    n = len(arr)
    if n <= 1:
        return

    def downheap(start, end):
        """从 start 开始向下冒泡，堆的范围是 [0, end)"""
        parent = start
        # while True:
        left = 2 * parent + 1
        right = 2 * parent + 2

        if not descend:
            # 从小到大，堆的根节点为 max
            largest_child = parent

            if left < end and arr[left] > arr[largest_child]:
                largest_child = left
            if right < end and arr[right] > arr[largest_child]:
                largest_child = right

            if largest_child == parent:
                return None  # 如果父节点已经是最大的，停止

            arr[parent], arr[largest_child] = arr[largest_child], arr[parent]
            downheap(largest_child, end)  # 继续向下冒泡
        else:
            # 从大到小，堆的根节点为 min
            smallest_child = parent

            if left < end and arr[left] < arr[smallest_child]:
                smallest_child = left
            if right < end and arr[right] < arr[smallest_child]:
                smallest_child = right

            if smallest_child == parent:
                return None  # 如果父节点已经是最小的，停止

            arr[parent], arr[smallest_child] = arr[smallest_child], arr[parent]
            downheap(smallest_child, end)  # 继续向下冒泡

    # 1. 构建最大堆（从最后一个非叶子节点开始）
    for i in range((n // 2) - 1, -1, -1):
        # <=> 整个序列为一个暂未满足 heap-order 的堆，进行冒泡调整
        downheap(i, n)  # 自底向上的构建

    # 2. 排序阶段：每次将堆顶（最大值）交换到末尾，并向下冒泡
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # 交换堆顶和当前末尾
        downheap(0, i)  # 向下冒泡


if __name__ == '__main__':
    print("=" * 15, "Selection Sort", "=" * 15)
    l = [7, 4, 8, 2, 5, 3]
    print("Initial list:", l)
    selection_sort(l)
    print("After sort:", l)

    print("=" * 15, "Insertion Sort", "=" * 15)
    l = [7, 4, 8, 2, 5, 3]
    print("Initial list:", l)
    insertion_sort(l)
    print("After sort:", l)

    print("=" * 15, "Heap Sort", "=" * 15)
    l = [7, 4, 8, 2, 5, 3]
    print("Initial list:", l)
    heap_sort(l)
    print("After sort:", l)

    print("=" * 15, "The Best! - In-place Heap Sort", "=" * 15)
    l = [7, 4, 8, 2, 5, 3]
    print("Initial list:", l)

    heapsort(l, descend=False)  # 从小到大
    print("sort not descend:", l)

    heapsort(l, descend=True)  # 从大到小
    print("sort descend:", l)
