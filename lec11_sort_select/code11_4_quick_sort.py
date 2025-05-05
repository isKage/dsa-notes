from utils import LinkedQueue


def quick_sort(S: LinkedQueue) -> None:
    """基于链表的快速排序"""
    n = len(S)
    if n < 2:
        return  # list is already sorted

    # divide
    p = S.first()  # 取第一个值为划分基准
    L = LinkedQueue()
    E = LinkedQueue()
    G = LinkedQueue()

    # divide S into L, E, and G
    while not S.is_empty():
        if S.first() < p:
            L.enqueue(S.dequeue())
        elif p < S.first():
            G.enqueue(S.dequeue())
        else:  # S.first() must equal pivot 等于基准值
            E.enqueue(S.dequeue())

    # conquer (with recursion) 递归排序
    quick_sort(L)  # sort elements less than p
    quick_sort(G)  # sort elements greater than p

    # concatenate results 合并
    while not L.is_empty():
        S.enqueue(L.dequeue())
    while not E.is_empty():
        S.enqueue(E.dequeue())
    while not G.is_empty():
        S.enqueue(G.dequeue())


if __name__ == '__main__':
    S = LinkedQueue()
    S.from_list([85, 24, 63, 45, 17, 31, 96, 50])

    print("=" * 15, "Original List", "=" * 15)
    print(S)

    print("=" * 15, "After Sorted", "=" * 15)
    quick_sort(S)
    print(S)
