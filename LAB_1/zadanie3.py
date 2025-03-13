import unittest

class StringManipulator:
    def reverse_string(self, s):
        return s[::-1]

    def count_words(self, s):
        return len(s.split())

    def capitalize_words(self, s):
        return ' '.join(word.capitalize() for word in s.split())


class TestStringManipulator(unittest.TestCase):
    def setUp(self):
        self.manipulator = StringManipulator()

    def test_reverse_string(self):
        self.assertEqual(self.manipulator.reverse_string("cześć"), "śćezc")
        self.assertEqual(self.manipulator.reverse_string(""), "")
        self.assertEqual(self.manipulator.reverse_string("123!@#"), "#@!321")

    def test_count_words(self):
        self.assertEqual(self.manipulator.count_words("dzień dobry"), 2)
        self.assertEqual(self.manipulator.count_words(""), 0)
        self.assertEqual(self.manipulator.count_words("jeden dwa trzy"), 3)
        self.assertEqual(self.manipulator.count_words("  wiele   spacji  "), 2)

    def test_capitalize_words(self):
        self.assertEqual(self.manipulator.capitalize_words("dzień dobry"), "Dzień Dobry")
        self.assertEqual(self.manipulator.capitalize_words(""), "")
        self.assertEqual(self.manipulator.capitalize_words("programowanie w pythonie"), "Programowanie W Pythonie")
        self.assertEqual(self.manipulator.capitalize_words("  wiele   spacji  "), "Wiele Spacji")

if __name__ == '__main__':
    unittest.main()