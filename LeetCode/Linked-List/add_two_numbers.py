from utils import LinkedList


def addTwoNumbers(ll1: LinkedList, ll2: LinkedList) -> LinkedList:
    res = LinkedList()

    carry = 0  # 进位
    cur1 = ll1.head
    cur2 = ll2.head

    while cur1 or cur2 or carry:  # 有一个不是空节点，或者还有进位，就继续迭代
        if cur1:
            carry += cur1.get_item  # 节点值和进位加在一起
            cur1 = cur1.next  # 下一个节点
        if cur2:
            carry += cur2.get_item  # 节点值和进位加在一起
            cur2 = cur2.next  # 下一个节点

        res.add_first(carry % 10)  # 新节点保存进位一个数字
        carry = carry // 10  # 新的进位
    return res


if __name__ == '__main__':
    # num1 = 342
    # num2 = 465

    num1 = int(input("Enter the first number: "))
    num2 = int(input("Enter the second number: "))

    real = num1 + num2
    print("{} + {} = {}".format(num1, num2, real))

    num1_list = [int(i) for i in reversed(str(num1))]
    num2_list = [int(i) for i in reversed(str(num2))]
    ll1 = LinkedList.from_list(num1_list, reverse=True)
    ll2 = LinkedList.from_list(num2_list, reverse=True)

    res = addTwoNumbers(ll1, ll2)
    res = int("".join([str(i) for i in res]))
    print("{} + {} = {}".format(num1, num2, res))

    print("The Answer is the same:", res == real)
