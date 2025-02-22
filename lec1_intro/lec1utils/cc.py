class CreditCard:
    """有关一个用户的信用卡"""
    __slots__ = '_customer', '_bank', '_acnt', '_limit', '_balance'  # 声明实例命名

    def __init__(self, customer, bank, acnt, limit):
        """初始化一个信用卡实例

        Args:
            customer (str): 用户名
            bank (str): 银行名
            acnt (str): 用户账户ID
            limit (float): 信用卡限额
        """
        self._customer = customer
        self._bank = bank
        self._acnt = acnt
        self._limit = limit
        self._balance = 0.  # 初始账户额度为 0

    def get_customer(self):
        """返回用户名"""
        return self._customer

    def get_bank(self):
        """返回银行名"""
        return self._bank

    def get_acnt(self):
        """返回账户ID"""
        return self._acnt

    def get_limit(self):
        """返回额度"""
        return self._limit

    def get_balance(self):
        """返回目前的账户所用额度"""
        return self._balance

    def charge(self, price):
        """
        返回是否能继续提款，即检查是否超出额度
        :param price: 希望提取的额度
        :return: True 如果加上目前所用额度没有超出限度，否则 False
        """
        if self._balance + price > self._limit:
            return False
        else:
            self._balance += price
            return True

    def make_payment(self, amount):
        """用现金抵消了部分信用卡贷款"""
        self._balance -= amount


class PredatoryCreditCard(CreditCard):
    """继承父类，扩展方法"""
    OVER_LIMIT_FEE = 5  # 类数据成员
    __slots__ = '_apr'

    def __init__(self, customer, bank, acnt, limit, apr):
        """
        继承父类，常见新的一个账户
        :param customer: 用户名
        :param bank: 银行名
        :param acnt: 账户ID
        :param limit: 额度限制
        :param apr: 年利率，用以计算利息
        """
        super().__init__(customer, bank, acnt, limit)  # 调用父类的初始化方法 __init__
        self._apr = apr
        # self._balance 在调用父类初始化时也已经赋值 0

    def charge(self, price):
        """覆盖父类的charge方法，添加扣除手续费功能"""
        success = super().charge(price)  # 调用父类方法，检查是否仍在限额内
        if not success:
            self._balance += PredatoryCreditCard.OVER_LIMIT_FEE  # 如果失败收取 5 元手续费，贷款 balance 提高
        return success  # 返回结果 True or False

    def process_month(self):
        """收取每月利息"""
        if self._balance > 0:
            monthly_factor = pow(1 + self._apr, 1 / 12)  # 月贴现因子，apr 为年故除以 12 年化
            self._balance *= monthly_factor


if __name__ == '__main__':
    print("CreditCard===============================================================================")
    wallet = []
    wallet.append(CreditCard("John", "Bank1", "123 456 789", 3010.))
    wallet.append(CreditCard("Mike", "Bank2", "456 123 789", 6210.))
    wallet.append(CreditCard("Ann", "Bank3", "789 456 123", 4010.))

    print(wallet[0].charge(1000.))
    print(wallet[1].charge(2000.))
    print(wallet[2].charge(5000.))

    for account in wallet:
        print("Customer: {}".format(account.get_customer()))
        print("Balance: {}".format(account.get_balance()))

        if account.get_balance() > 100.:
            account.make_payment(100.)
            print("New Balance: {}".format(account.get_balance()))

    print("PredatoryCreditCard===============================================================================")
    pcc = PredatoryCreditCard("John", "Bank1", "123 456 789", 1000., 0.24)
    print(pcc.charge(500))
    print(pcc.get_balance())

    print(pcc.charge(1000))
    print(pcc.get_balance())

    # 收利息
    pcc.process_month()
    print(pcc.get_balance())
