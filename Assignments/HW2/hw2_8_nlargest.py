"""
在无序列表中寻找最大的 k 个元素
该算法的复杂度为 O(n + k log n) 或 O(n log k)
"""


def downheap(arr, cur, start, end, top_is_max=True):
    """从 cur 开始向下冒泡，堆的范围是 [start, end)
    :param cur: 当前节点
    :param start: 堆的起始索引
    :param end: 堆的终止索引
    """
    parent = cur

    left = 2 * parent + 1
    right = 2 * parent + 2

    if top_is_max:
        # 堆的根节点为 max
        largest_child = parent
        if start < left < end and arr[left] > arr[largest_child]:
            largest_child = left
        if start < right < end and arr[right] > arr[largest_child]:
            largest_child = right

        if largest_child == parent:
            return None  # 如果父节点已经是最大的，停止

        arr[parent], arr[largest_child] = arr[largest_child], arr[parent]
        downheap(arr, cur=largest_child, start=0, end=end)  # 继续向下冒泡
    else:
        # 堆的根节点为 min
        smallest_child = parent
        if start < left < end and arr[left] < arr[smallest_child]:
            smallest_child = left
        if start < right < end and arr[right] < arr[smallest_child]:
            smallest_child = right

        if smallest_child == parent:
            return None  # 如果父节点已经是最大的，停止

        arr[parent], arr[smallest_child] = arr[smallest_child], arr[parent]
        downheap(arr, cur=smallest_child, start=0, end=end)  # 继续向下冒泡


def nlargest1(k: int, arr: list) -> list:
    """
    原地找出 k 个最大元素 in-place `O(n + k log n)`
    :param k: 个数
    :param arr: 序列
    :return: arr 中最大的 k 个元素
    """
    n = len(arr)
    if n < k:  # 检查是否越界
        raise IndexError('Out of the range!')

    """自底向上构建最大堆 O(n)"""
    if n > 1:
        # 自底向上构建最大堆（从最后一个非叶子节点开始）
        for i in range((n // 2) - 1, -1, -1):
            # <=> 整个序列为一个暂未满足 heap-order 的堆，进行冒泡调整
            downheap(arr, cur=i, start=0, end=n, top_is_max=True)  # 自底向上的构建

    """最大元素根节点出堆 O(k log n)"""
    res = []  # 存储结果

    def get_max(size):
        """
        获取堆的根节点，即 max 并交换根节点和最后节点后向下冒泡
        :param size: [0, size) 为堆的范围
        :return: 最大值 max
        """
        max_element = arr[0]  # get the max
        arr[0] = arr[size]  # 交换根节点和最后节点
        arr[size] = None  # convention 置空 None 表示删除

        downheap(arr, cur=0, start=0, end=size)  # 向下冒泡使得 heap-order

        return max_element

    for _ in range(k):
        res.append(get_max(n - 1))  # 添加最大值
        n -= 1  # 同时减少堆大小

    return res


def nlargest2(k: int, arr: list) -> list:
    """
    原地找出 k 个最大元素 in-place `O(n log k)`
    :param k: 个数
    :param arr: 序列
    :return: arr 中最大的 k 个元素
    """
    n = len(arr)
    if n < k:  # 检查是否越界
        raise IndexError('Out of the range!')

    """arr 前 k 个自底向上构建最小堆 O(k)"""
    if k > 1:
        # 自底向上构建最小堆（从最后一个非叶子节点开始）
        for i in range((n // 2) - 1, -1, -1):
            # <=> 整个序列为一个暂未满足 heap-order 的堆，进行冒泡调整
            downheap(arr[:k], cur=i, start=0, end=k, top_is_max=False)  # 自底向上的构建 root is min

    """剩下 n - k 个元素逐个与根节点比较，更大则加入 O((n - k) log k)"""
    # 因为此时的堆顶为 k 个元素的 min
    for j in range(k, n):
        if arr[j] > arr[0]:  # 更大则加入 k-堆 并冒泡使得 heap-order
            arr[0], arr[j] = arr[j], arr[0]  # 交换
            downheap(arr, cur=0, start=0, end=k, top_is_max=False)
    # 如此得到 k-堆 存储着最大的 k 个元素

    """按序返回 k 个最大值 O(k)"""
    res = []

    def postorder(cur, heap_size):
        """
        后序遍历，不过先右再左：右 -> 左 -> 根
        :param cur: 开始遍历的位置
        :param heap_size: 堆大小
        :return: 前 k 个最大值
        """

        if cur >= heap_size:  # 到叶子节点，跳出
            return

        # 先右子节点
        right = 2 * cur + 2
        postorder(right, heap_size)

        # 再左子节点
        left = 2 * cur + 1
        postorder(left, heap_size)

        # 最后根节点
        res.append(arr[cur])

    # 后序遍历得到最终的 res
    postorder(cur=0, heap_size=k)
    return res


if __name__ == '__main__':
    print("=" * 15, "nlargest1: O(n + k log n)", "=" * 15)
    l = [3, 1, 4, 7, 5, 9, 2, 6, 8]
    k = 3
    res1 = nlargest1(k, l)
    print(res1)
    # print(l)  # for Debug

    print("=" * 15, "nlargest2: O(n log k)", "=" * 15)
    l = [3, 1, 4, 7, 5, 9, 2, 6, 8]
    k = 3
    res2 = nlargest2(k, l)
    print(res2)
    # print(l)  # for Debug
