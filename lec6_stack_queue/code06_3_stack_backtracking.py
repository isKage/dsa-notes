from utils import ArrayStack


def permute_stack(nums):
    res = []
    stack = ArrayStack()
    stack.push(([], nums))  # 初始状态：空排列 []，剩余元素 nums

    while not stack.is_empty():
        # Step 1: 每次拿出栈顶元素检查，如果不是全排列则进入 Step 2
        path, remaining = stack.pop()
        if not remaining:  # 如果剩余元素为空，说明 path 是一个完整的排列
            res.append(path)
            continue

        # Step 2: 遍历元素，直到将 remaining 的所以剩余元素都加入新的排列中
        for i in reversed(range(len(remaining))):  # 从剩余的 remaining 中取
            e = remaining[i]  # 取出当前元素
            new_remaining = remaining[:i] + remaining[i + 1:]  # 从剩余元素中移除 e
            new_path = path + [e]  # 将 e 加入排列 []
            stack.push((new_path, new_remaining))  # 压入新状态

    return res


def subsets_stack(nums):
    res = []
    stack = ArrayStack()
    stack.push(([], nums))  # 初始状态：空子集，剩余元素为 nums

    while not stack.is_empty():
        # Step 1: 取栈顶元素，直接加入结果集，因为是子集问题
        path, remaining = stack.pop()
        res.append(path)  # 将当前子集加入结果集

        # Step 2: 遍历剩余元素，加入子集
        for i in reversed(range(len(remaining))):
            e = remaining[i]  # 取出当前元素
            # 从剩余元素中移除 e 及其之前的元素，因为子集不允许重复
            new_remaining = remaining[i + 1:]
            new_path = path + [e]  # 将 e 加入子集
            stack.push((new_path, new_remaining))  # 压入新状态

    return res


def combinationSum_stack(candidates, target):
    res = []
    stack = ArrayStack()
    # 初始状态：空组合，剩余目标值 target 即离 target 的差，起始位置 0
    stack.push(([], target, 0))

    while not stack.is_empty():
        path, remaining, start = stack.pop()
        if remaining == 0:  # 如果剩余目标值为 0，说明 path 是一个有效组合
            res.append(path)
            continue

        # 从 candidates 的 start 开始选择元素
        for i in range(start, len(candidates)):
            e = candidates[i]
            if e > remaining:
                continue  # 剪枝：如果当前元素大于剩余目标值，跳过
            new_path = path + [e]  # 将 e 加入组合
            new_remaining = remaining - e  # 更新剩余目标值
            stack.push((new_path, new_remaining, i + 1))  # 压入新状态，不允许重复选择

    return res


def solveNQueens_stack(N):
    res = []  # 存储所有有效解
    stack = ArrayStack()
    # 初始状态：空路径，第 0 行，第一个 set 表示列，第二个表示正对角线，第三个表示反对角线
    stack.push(([], 0, set(), set(), set()))

    while not stack.is_empty():
        # Step 1: 出栈当前状态
        path, row, cols, diag1, diag2 = stack.pop()
        # 如果所有行都处理完毕，说明 path 是一个有效解
        if row == N:
            # 转换为棋盘表示
            res.append([' · ' * i + ' Q ' + ' · ' * (N - i - 1) for i in path])
            continue

        # Step 2: 在当前行选择列的位置
        for col in range(N):
            # 计算当前列所在的正对角线和反对角线
            curr_diag1 = row - col  # 正对角线：行 - 列
            curr_diag2 = row + col  # 反对角线：行 + 列

            # 如果当前列或对角线已经被占用，则跳过
            if col in cols or curr_diag1 in diag1 or curr_diag2 in diag2:
                continue

            # 创建新的集合
            new_cols = set(cols)  # 创建新的列冲突集
            new_diag1 = set(diag1)  # 创建新的正对角线冲突集
            new_diag2 = set(diag2)  # 创建新的反对角线冲突集

            # 更新
            new_cols.add(col)  # 将当前列加入列冲突集
            new_diag1.add(curr_diag1)  # 将当前正对角线加入冲突集
            new_diag2.add(curr_diag2)  # 将当前反对角线加入冲突集
            new_path = path + [col]  # 将当前列加入路径

            # 压入新状态：更新路径、下一行、新的冲突集
            stack.push((new_path, row + 1, new_cols, new_diag1, new_diag2))

    return res


if __name__ == '__main__':
    # 测试示例
    print(permute_stack([1, 2, 3]))  # 全排列
    print(subsets_stack([1, 2, 3]))  # 子集
    print(combinationSum_stack([1, 2, 3, 4, 5, 6, 7, 8], 9))  # 组合总和

    for row in solveNQueens_stack(4):  # 4 皇后问题
        print("Answer:")
        for i in row:
            print(i)
