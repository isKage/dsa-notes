import matplotlib

matplotlib.use('TkAgg')  # 或者 'Agg'
import matplotlib.pyplot as plt


def code1(N):
    sum = 0
    for i in range(N):
        for j in range(N * N):
            sum += 1


def code2(N):
    sum = 0
    for i in range(N):
        for j in range(0, i * N, N):
            sum += 1


def code3(N):
    sum = 0
    for i in range(N):
        for j in range(i * i):
            for k in range(j):
                sum += 1


def code4(N):
    sum = 0
    for i in range(N):
        for j in range(i * i):
            if j % i == 0:
                for k in range(j):
                    sum += 1


def time_cost(f, N):
    import time
    start = time.time()
    f(N)
    end = time.time()
    return end - start


if __name__ == '__main__':
    res = []
    scale = 1
    length = 10
    N_values = range(10, 10 + length * scale, scale)
    names = [code1, code2, code3, code4]
    for name in names:
        tmp = []
        for N in N_values:
            tmp.append(time_cost(name, N))
        res.append(tmp)
    print(res)

    # 绘图
    plt.figure(figsize=(10, 6))
    labels = ['code1 (O(N^3))', 'code2 (O(N^2))', 'code3 (O(N^5))', 'code4 (O(N^4))']

    for i in range(len(names)):
        plt.plot(N_values, res[i], marker='o', markersize=4, label=labels[i])

    plt.xlabel('N')
    plt.ylabel('Time (s)')
    plt.title('Time Cost Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()
