from utils import LinkedQueue


def merge(S1: LinkedQueue, S2: LinkedQueue, S: LinkedQueue):
    """合并链表 (利用链表队列) 返回顺序链表队列"""
    while not S1.is_empty() and not S2.is_empty():
        if S1.first() < S2.first():
            S.enqueue(S1.dequeue())
        else:
            S.enqueue(S2.dequeue())

    while not S1.is_empty():
        # move remaining elements of S1 to S
        S.enqueue(S1.dequeue())
    while not S2.is_empty():
        # move remaining elements of 52 to S
        S.enqueue(S2.dequeue())


def merge_sort(S: LinkedQueue):
    """对链表使用归并排序"""
    n = len(S)
    if n < 2:
        return  # list is already sorted

    # divide
    S1 = LinkedQueue()
    S2 = LinkedQueue()
    while len(S1) < n // 2:  # move the first n//2 elements to S1
        S1.enqueue(S.dequeue())
    while not S.is_empty():  # move the rest to S2
        S2.enqueue(S.dequeue())

    # conquer (with recursion)
    merge_sort(S1)  # sort first half
    merge_sort(S2)  # sort second half

    # merge results
    merge(S1, S2, S)  # merge sorted halves back into S


if __name__ == '__main__':
    S = LinkedQueue()
    S.from_list([45, 24, 85, 63, 50, 31, 96, 17])
    print("=" * 15, "Original List", "=" * 15)
    print(S)  # LinkedQueue 已经定义了 __str__ 方法

    print("=" * 15, "After Sorted", "=" * 15)
    merge_sort(S)
    print(S)
