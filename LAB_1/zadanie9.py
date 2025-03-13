import re
import unittest

def is_palindrome(s):
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    return cleaned == cleaned[::-1]




class TestIsPalindrome(unittest.TestCase):
    def test_palindromes(self):
        self.assertTrue(is_palindrome("Kobyła ma mały bok"))
        self.assertTrue(is_palindrome("A to kanapa pana Kota"))
        self.assertTrue(is_palindrome("Zakopane na pokaz"))
        self.assertTrue(is_palindrome(""))

    def test_non_palindromes(self):
        self.assertFalse(is_palindrome("przykład"))
        self.assertFalse(is_palindrome("przykład"))
        self.assertFalse(is_palindrome("przykład"))

if __name__ == '__main__':
    unittest.main()