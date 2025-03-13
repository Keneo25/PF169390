from collections import Counter
import unittest



def find_most_frequent_word(text):
    if not text:
        return None
    words = text.split()
    word_counts = Counter(words)
    most_common_word, _ = word_counts.most_common(1)[0]
    return most_common_word


class TestFindMostFrequentWord(unittest.TestCase):
    def test_empty_text(self):
        self.assertIsNone(find_most_frequent_word(""))

    def test_single_word(self):
        self.assertEqual(find_most_frequent_word("jabłko"), "jabłko")

    def test_multiple_words(self):
        self.assertEqual(find_most_frequent_word("jabłko banan jabłko"), "jabłko")
        self.assertEqual(find_most_frequent_word("banan jabłko banan"), "banan")

    def test_same_frequency(self):
        self.assertIn(find_most_frequent_word("jabłko banan"), ["jabłko", "banan"])

if __name__ == '__main__':
    unittest.main()