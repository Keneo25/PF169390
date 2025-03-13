import unittest

class InsufficientFundsError(Exception):
    pass

class BankAccount:
    def __init__(self):
        self.balance = 0.0

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Kwota wpłaty musi być dodatnia")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Kwota wypłaty musi być dodatnia")
        if amount > self.balance:
            raise InsufficientFundsError("Niewystarczające środki na koncie")
        self.balance -= amount

    def get_balance(self):
        return self.balance


class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount()

    def test_deposit(self):
        self.account.deposit(200)
        self.assertEqual(self.account.get_balance(), 200)
        with self.assertRaises(ValueError):
            self.account.deposit(-1500)

    def test_withdraw(self):
        self.account.deposit(100)
        self.account.withdraw(50)
        self.assertEqual(self.account.get_balance(), 50)
        with self.assertRaises(ValueError):
            self.account.withdraw(-50)
        with self.assertRaises(InsufficientFundsError):
            self.account.withdraw(100)

    def test_get_balance(self):
        self.assertEqual(self.account.get_balance(), 0)
        self.account.deposit(100)
        self.assertEqual(self.account.get_balance(), 100)


if __name__ == '__main__':
    unittest.main()