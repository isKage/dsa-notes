from utils import ArrayStack
from utils import ArrayQueue


def maze_path(maze, M, N):
    """找出一条可能的路径: 栈 ｜ 回溯法"""
    # 初始化栈
    stack = ArrayStack()

    stack.push((1, 1))  # 起始点入栈
    visited = set()  # 已经走过的路
    visited.add((1, 1))  # 起始点入路

    # 定义四个方向：左、右、上、下
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    # 最后栈空说明无解
    while not stack.is_empty():
        current = stack.top()  # 栈顶元素

        if current == (M, N):  # 到达终点
            path = [None] * len(stack)
            i = len(stack) - 1
            while not stack.is_empty():
                path[i] = stack.pop()
                i -= 1
            return path  # 返回路径

        found = False  # 是否找到新的位置可走
        for d in directions:
            i, j = current[0] + d[0], current[1] + d[1]  # 新位置

            # 检查新坐标是否未访问，且是否是通路
            if maze[i][j] == 0 and (i, j) not in visited:
                stack.push((i, j))  # (i, j) 通路且不在之前的路中
                visited.add((i, j))  # 入路，保证未来不会重走
                found = True  # 找到下一步
                break

        if not found:
            # 无路可走则回溯
            stack.pop()

    return None  # 无解


def maze_shortest_path(maze, M, N):
    """找出最短的路径: 队列 ｜ 洪水算法"""

    def backtrack_path(parent: dict, start: tuple, end: tuple):
        """从 end 回溯到 start，生成路径"""
        path = []
        current = end
        while current != start:
            path.append(current)
            current = parent[current]  # 找到当前点的父节点
        path.append(start)  # 添加起点
        path.reverse()  # 反转路径，使其从 start 到 end
        return path

    queue = ArrayQueue()
    queue.enqueue((1, 1))
    parent = {}  # 记录当前点的上一个点位置

    # 定义四个方向：左、右、上、下
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    while not queue.is_empty():
        current = queue.dequeue()  # 当前位置
        maze[current[0]][current[1]] = 2  # 记当前位置为 2 放置重复走

        if current == (M, N):  # 在广度优先下，最先找到终点，即为最短路径
            return backtrack_path(parent, (1, 1), (M, N))

        for d in directions:  # 四个方向都要考虑并入队
            i, j = current[0] + d[0], current[1] + d[1]
            if maze[i][j] == 0 and maze[i][j] != 2:  # 不是墙/且不重复
                queue.enqueue((i, j))  # 入队
                parent[(i, j)] = current  # 记录当前点的上一个点

    return None  # 无解


if __name__ == '__main__':
    # M = N = 5 外面一圈 1 为了方便表示边界
    maze = [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1]
    ]

    ans = maze_path(maze, len(maze) - 2, len(maze[0]) - 2)
    print(ans)

    shortest_ans = maze_shortest_path(maze, len(maze) - 2, len(maze[0]) - 2)
    print(shortest_ans)
