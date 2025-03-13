import unittest

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item, price):
        self.items.append((item, price))

    def remove_item(self, item):
        self.items = [i for i in self.items if i[0] != item]

    def get_total(self):
        return sum(price for item, price in self.items)

    def clear(self):
        self.items = []

class TestShoppingCart(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    def test_add_item(self):
        self.cart.add_item("jabłko", 1.0)
        self.assertEqual(len(self.cart.items), 1)
        self.assertEqual(self.cart.items[0], ("jabłko", 1.0))

    def test_remove_item(self):
        self.cart.add_item("jabłko", 1.0)
        self.cart.add_item("banan", 2.0)
        self.cart.remove_item("jabłko")
        self.assertEqual(len(self.cart.items), 1)
        self.assertEqual(self.cart.items[0], ("banan", 2.0))

    def test_get_total(self):
        self.cart.add_item("jabłko", 1.0)
        self.cart.add_item("banan", 2.0)
        self.assertEqual(self.cart.get_total(), 3.0)

    def test_clear(self):
        self.cart.add_item("jabłko", 1.0)
        self.cart.add_item("banan", 2.0)
        self.cart.clear()
        self.assertEqual(len(self.cart.items), 0)

if __name__ == '__main__':
    unittest.main()
