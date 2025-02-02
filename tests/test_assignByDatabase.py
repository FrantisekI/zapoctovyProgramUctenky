import unittest
from textAnalyzer.assignByDatabase import calculate_levenshtein_distance

class TestLevenshteinDistance(unittest.TestCase):
    def test_identical_words(self):
        self.assertTrue(calculate_levenshtein_distance("hello", "hello", 0))
        self.assertTrue(calculate_levenshtein_distance("", "", 0))
        
    def test_different_lengths(self):
        self.assertTrue(calculate_levenshtein_distance("hello", "hell", 1))
        self.assertFalse(calculate_levenshtein_distance("hello", "he", 1))
        
    def test_substitutions(self):
        self.assertTrue(calculate_levenshtein_distance("hello", "hallo", 1))
        self.assertFalse(calculate_levenshtein_distance("hello", "hillo", 0))
        
    def test_max_distance(self):
        self.assertTrue(calculate_levenshtein_distance("kitten", "sitting", 3))
        self.assertFalse(calculate_levenshtein_distance("kitten", "sitting", 2))
        
    def test_empty_string(self):
        self.assertTrue(calculate_levenshtein_distance("", "a", 1))
        self.assertFalse(calculate_levenshtein_distance("", "ab", 1))
    def test_long_strings(self):
        self.assertTrue(calculate_levenshtein_distance("abcdefghijklmnopqrst", "abcdefghijklmnopqrsp", 2))
        self.assertFalse(calculate_levenshtein_distance("abcdefghijklmnopqrst", "abcdefghijklmnopqxyz", 2))
        self.assertTrue(calculate_levenshtein_distance("thisisaverylongstring", "thisisanotherstrings", 10))

if __name__ == '__main__':
    unittest.main()
