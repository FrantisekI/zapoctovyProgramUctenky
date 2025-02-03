import unittest
from unittest.mock import Mock
from textAnalyzer.assign_by_database import calculate_levenshtein_distance, assign_by_database
from textAnalyzer import analyzeText
from database_conn import Database
class MockDatabase:
    def __init__(self, candidates_data, class_data):
        self.candidates_data = candidates_data
        self.class_data = class_data
    
    def find_candidates(self, word):
        return self.candidates_data
    
    def select_one_get_class_from_custom_name(self, id):
        return self.class_data.get(id)

class TestAssignByDatabase(unittest.TestCase):
    def setUp(self):
        # Mock data for testing
        self.candidates_data = [
            (1, "apple"),
            (2, "appl"),
            (3, "orange")
        ]
        self.class_data = {
            1: 10,
            2: 10,
            3: 20
        }
        self.db = MockDatabase(self.candidates_data, self.class_data)

    def test_exact_match(self):
        result = assign_by_database("apple", self.db, 0.2)
        self.assertEqual(result, 10)

    def test_close_match(self):
        result = assign_by_database("appel", self.db, 0.2)
        self.assertEqual(result, 10)

    def test_no_match(self):
        result = assign_by_database("banana", self.db, 0.2)
        self.assertIsNone(result)

    def test_conflicting_classes(self):
        # Test when similar words belong to different classes
        conflicting_db = MockDatabase(
            [(1, "test"), (2, "text")],
            {1: 10, 2: 20}
        )
        result = assign_by_database("text", conflicting_db, 0.3)
        self.assertIsNone(result)

    def test_empty_candidates(self):
        empty_db = MockDatabase([], {})
        result = assign_by_database("test", empty_db, 0.2)
        self.assertIsNone(result)

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

class TestAnalyzeText():
    receiptText = """
        13:29 •
        Detail účtenky
        313.50Kč • 2kredity • Ibod
        Díky akcím jste ušetřili 71 Kč
        Získané kredity
        • Kupóny
        Položka
        NP BIO DŽEM MER 270G
        GOUDA PLÁTKY 50
        CHLÉB ŠUMAVA1200GR
        RAJČ.CHERRY OV.500G
        S. KRÁL SÝRŮ PROV.BY
        MANDARINKY
        0.95 x 29.90 Kč /kg
        Získané kredity: 2 kredity
        JABLKA ČERVENÁ
        0.99 x 39.00 Kč /kg
        Celkem
        Získané kredity
        Získané body
        PRODEJNA
        Praha 4, Arkády Pankrác
        Na Pankráci 86, Praha 4
        platební
        900/0i
        29.10.2024
        2
        2
        Cena
        36.90 Kč
        99.90 Kč
        42.90 Kč
        39.90 Kč
        26.90 Kč
        28.40 Kč
        38.60 Kč
        313.50 Kč
        2
        KLIENT
        +420 776 200 517
        """
    db = Database()
    analyzeText(receiptText, db)
    
if __name__ == '__main__':
    unittest.main()
