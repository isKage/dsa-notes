import time


def insertion_sort(arr):
    """
    插入排序：从小到大排序数组
    :param arr: 数组
    :return: None
    """
    for i in range(1, len(arr)):
        # 从第 2 个元素开始
        current = arr[i]
        j = i

        while j > 0 and current < arr[j - 1]:
            # 当前一个元素不是第 0 个元素且比 current 大时
            arr[j] = arr[j - 1]  # 后移
            j -= 1  # 继续向前找

        # 插入
        arr[j] = current


def selection_sort(arr):
    """
    选择排序：从小到大排序数组
    :param arr: 数组
    :return: None
    """
    for i in range(len(arr)):
        # 从起始开始遍历
        min_index = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = j  # 找到后面最小的元素

        # 将后面最小的元素放到前面子列的末尾
        arr[i], arr[min_index] = arr[min_index], arr[i]


if __name__ == '__main__':
    x = [i for i in range(10000)]
    start = time.time()
    insertion_sort(x)
    end = time.time()
    print("insertion sort cost {}s".format(end - start))

    x = [i for i in range(10000)]
    start = time.time()
    selection_sort(x)
    end = time.time()
    print("selection sort cost {}s".format(end - start))
