import datetime
import math



class Customer:
    last_id = 0
    def __init__(self, name, address):
        self.name = name
        self.address = address
        Customer.last_id += 1
        self.id = Customer.last_id

    def __repr__(self):
        return f'Cust[{self.id}, {self.name}]'



class AccountTransaction:
    def __init__(self, transaction_type, amount, balance_after, related_account_id = None):
        self.transaction_type = transaction_type
        self.amount = amount
        self.balance_after = balance_after
        self.related_account_id = related_account_id
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return ( f'{self.timestamp} | {self.transaction_type} | ' f'Amount: {self.amount:.2f} | '
                    f'Balance: {self.balance_after:.2f} | 'f'Related Account: {self.related_account_id}')


class Account:
    last_id = 1000
    yearly_interest_rate = 0.02  # TODO - will be used to update the interest rate

    def __init__(self, customer):
        self.customer = customer
        Account.last_id += 1
        self.id = Account.last_id
        self.balance = 0
        self.transactions = []

    @staticmethod
    def validate_amount(amount):
        if isinstance(amount, bool) or not isinstance(amount, (int,float)):
            raise BankException('amount must be a number')

        if  amount <= 0 or  not math.isfinite(amount):
            raise BankException('amount cannot be negative and infinite')

        if round(amount, 2) != amount:
            raise BankException('amount cannot have more than 2 decimal places')

        return round(amount, 2)

    def add_transaction(self, transaction_type, amount, related_account_id = None):
        transaction = AccountTransaction(transaction_type, amount, self.balance, related_account_id)
        self.transactions.append(transaction)


    def deposit(self, amount):
        amount = self.validate_amount(amount)
        self.balance += amount
        self.balance = round(self.balance, 2)
        self.add_transaction('deposit', amount)



    def withdraw(self, amount):
        amount = self.validate_amount(amount)
        if amount > self.balance:
            raise BankException('amount cannot be greater than balance')
        self.balance -= amount
        self.balance = round(self.balance, 2)
        self.add_transaction('withdraw', amount)


    def get_history_of_transactions(self):
        return list(self.transactions)


    def __repr__(self):
        return f'Ac[{self.id}, {self.customer.name}, {self.balance}]'


class Bank:
    def __init__(self, name):
        self.name = name
        self.acc_list = []
        self.cust_list = []

    def create_customer(self, name, address):
        customer = Customer(name, address)
        self.cust_list.append(customer)
        return customer

    def create_account(self, customer):
        account = Account(customer)
        self.acc_list.append(account)
        return account



    def find_account(self, account_id):
        if type(account_id) != int:
            raise BankException('account_id must be an integer')
        for account in self.acc_list:
            if account.id == account_id:
                return account
        raise BankException('account_id does not exist')


    def transfer_money(self, from_account_id, to_account_id, amount):
       amount = Account.validate_amount(amount)

       if from_account_id == to_account_id:
           raise BankException('cannot transfer money from one account to the same one')
       from_account = self.find_account(from_account_id)
       to_account = self.find_account(to_account_id)

       if from_account.balance < amount:
           raise BankException('Poor funds')

       from_account.balance = round(from_account.balance - amount, 2)
       to_account.balance = round(to_account.balance + amount, 2)

       from_account.add_transaction('outer transfer', amount, to_account_id)
       to_account.add_transaction('inner transfer', amount, from_account_id)


    def run_daily_interest_updater(self):
        for account in self.acc_list:
            daily_interest = round( account.balance * Account.yearly_interest_rate /365, 2)
            account.balance = round(account.balance + daily_interest, 2)
            account.add_transaction('daily interest', daily_interest)
        pass

    def __repr__(self):
        return f'Bank[{self.name}, {self.cust_list}, {self.acc_list}]'

class BankException(Exception):
    pass

#TODO
# Add deposit and withdraw (charge) methods and code that will demonstrate their use


if __name__ == '__main__':
    bank = Bank('Imaginary Bank')

    customer1 = bank.create_customer('John Doe', 'Warszawa')
    customer2 = bank.create_customer('Jan Kowalski', 'Poznań')

    account1 = bank.create_account(customer1)
    account2 = bank.create_account(customer2)

    account1.deposit(1234)
    account2.deposit(2024)

    account1.withdraw(234)
    bank.transfer_money(account1.id, account2.id, 150)
    bank.run_daily_interest_updater()
    print(f'Final account balances:{account1} | {account2}')

    print("-"* 60)
    print("First customer account transaction history:")
    for transaction in account1.get_history_of_transactions():
        print(transaction)

    print("-"* 60)

    print("Second customer account transaction history:")
    for transaction in account2.get_history_of_transactions():
        print(transaction)


    try:
        account1.deposit(-100)
    except BankException as Error:
        print(f'Expected error:{Error}')

    try:
        account1.deposit("qwe")
    except BankException as Error:
        print(f'Expected error:{Error}')

    try:
        account1.withdraw(12345)
    except BankException as Error:
        print(f'Expected error:{Error}')
