import unittest

def ciag_fibonacciego(n):
    if n < 0:
        raise ValueError("Wartość wejściowa powinna być nieujemną liczbą całkowitą")
    elif n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b


class TestCiagFibonacciego(unittest.TestCase):
    def test_ciag_fibonacciego(self):
        self.assertEqual(ciag_fibonacciego(0), 0)
        self.assertEqual(ciag_fibonacciego(1), 1)
        self.assertEqual(ciag_fibonacciego(2), 1)
        self.assertEqual(ciag_fibonacciego(3), 2)
        self.assertEqual(ciag_fibonacciego(10), 55)
        self.assertEqual(ciag_fibonacciego(20), 6765)
        self.assertEqual(ciag_fibonacciego(30), 832040)

    def test_ujemna_wartosc(self):
        with self.assertRaises(ValueError):
            ciag_fibonacciego(-1)

if __name__ == '__main__':
    unittest.main()