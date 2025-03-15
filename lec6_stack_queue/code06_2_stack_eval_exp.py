from utils import ArrayStack


def eval_exp(tokens):
    def precedence(op):
        """为运算符定义优先级"""
        if op == '$':
            return -1  # 结束符优先级最低
        elif op in ('<', '>', '='):
            return 0  # 比较运算符
        elif op in ('+', '-'):
            return 1  # 加减
        elif op in ('*', '/'):
            return 2  # 乘除
        else:
            raise ValueError(f"Invalid operator: {op}")

    def repeat_ops(ref_op, opStk, valStk):
        """判断优先级"""
        while len(valStk) >= 2 and precedence(ref_op) <= precedence(opStk.top()):
            # 如果当前运算符优先级比 opStk 栈顶低，则先计算栈顶运算符
            do_op(opStk, valStk)  # 直到栈顶的低，或 valStk 不足 2 个元素可以计算

    def do_op(op_stk, val_stk):
        """正式计算过程"""
        op = op_stk.pop()  # 提取运算符

        # 提取栈顶计算的两个元素
        x = val_stk.pop()
        y = val_stk.pop()

        # 按照运算符的含义进行计算
        if op == '+':
            val_stk.push(y + x)
        elif op == '-':
            val_stk.push(y - x)
        elif op == '*':
            val_stk.push(y * x)
        elif op == '/':
            val_stk.push(y / x)
        elif op == '<':
            val_stk.push(y < x)
        elif op == '>':
            val_stk.push(y > x)
        elif op == '=':
            val_stk.push(y == x)
        else:
            raise ValueError(f"Invalid operator: {op}")

    # 开始计算
    tokens = tokens + ['$']  # $ 代表算数式起始
    valStk = ArrayStack()  # 记录值
    opStk = ArrayStack()  # 记录运算符
    opStk.push('$')

    for token in tokens:
        if str(token).isdigit():
            # 如果为数字，直接入栈 valStk
            valStk.push(int(token))
        else:
            # 如果为运算符
            repeat_ops(token, opStk, valStk)  # 检查优先级
            opStk.push(token)  # 当前运算符入栈 opStk

    # 返回最后 valStk 栈顶元素，即为结果
    return valStk.top()


if __name__ == '__main__':
    expr = ['3', '+', '5', '*', '2']  # 3 + 5 * 2 = 13
    print(f"{' '.join(expr)} is {eval_exp(expr)}")

    # 新增比较运算测试
    expr = ['3', '+', '5', '<', '2', '*', '4']  # (3 + 5) < (2 * 4) -> 8 < 8 -> False
    print(f"{' '.join(expr)} is {eval_exp(expr)}")

    expr = ['5', '>', '2', '*', '3']  # 5 > (2 * 3) -> 5 > 6 -> False
    print(f"{' '.join(expr)} is {eval_exp(expr)}")

    expr = ['7', '=', '3', '+', '4']  # 7 = (3 + 4) -> True
    print(f"{' '.join(expr)} is {eval_exp(expr)}")
