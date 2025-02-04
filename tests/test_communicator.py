import unittest
from communicator import Communicator
import io
import sys
from unittest.mock import Mock

class MockDatabase:
    def __init__(self, candidates_data, class_data):
        self.candidates_data = candidates_data
        self.class_data = class_data
    
    def find_candidates(self, word):
        return self.candidates_data
    
    def select_one_get_class_from_custom_name(self, id):
        return self.class_data.get(id)

class TestCommunicator(unittest.TestCase):
    def setUp(self):
        self.candidates_data = [
            (1, "apple"),
            (2, "appl"),
            (3, "orange")
        ]
        self.class_data = {
            1: (10, 'apple'),
            2: (10, 'apple'),
            3: (20, 'orange')
        }
        self.db = MockDatabase(self.candidates_data, self.class_data)
        self.communicator = Communicator(self.db)

    def test_pretty_print(self):
        store_info = ("Test Store", "2023-10-01", 10000)
        assigned_products = [
            {'name': 'Product 1', 'total_price': 1000, 'amount': 1, 'units': 'pcs', 'class': {(1,'A')}, 'flag': 10},
            {'name': 'Product 2', 'total_price': 2000, 'amount': 2, 'units': 'pcs', 'class': {(2,'B'), (3,'C')}, 'flag': 20},
            {'name': 'Product 3', 'total_price': 3000, 'amount': 3, 'units': 'pcs', 'class': None, 'flag': 21},
        ]
        
        # Capture the output of pretty_print
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.communicator.pretty_print(store_info, assigned_products)
        sys.stdout = sys.__stdout__
        print(captured_output.getvalue())
        output = captured_output.getvalue()
        
        # Check if the output contains expected strings
        self.assertIn("A | Store: Test Store", output)
        self.assertIn("B | Date: 2023-10-01", output)
        self.assertIn("C | Total: 100.00", output)
        self.assertIn("1. | Product 1", output)
        self.assertIn("2. | Product 2", output)
        self.assertIn("3. | Product 3", output)
        self.assertIn("DB", output)
        self.assertIn("AI", output)
        self.assertIn("AI (Not Found)", output)
        self.assertIn("Note: Rows 2, 3 need verification (assigned by AI).", output)
        
    def test_iteratible_pretty_print(self):
        store_info = ("Test Store", "2023-10-01", 10000)
        assigned_products = [
            {'name': 'Product 1', 'total_price': 1000, 'amount': 1, 'units': 'pcs', 'class': {(1,'A')}, 'flag': 10},
            {'name': 'Product 2', 'total_price': 2000, 'amount': 2, 'units': 'pcs', 'class': {(2,'B'), (3,'C')}, 'flag': 20},
            {'name': 'Product 3', 'total_price': 3000, 'amount': 3, 'units': 'pcs', 'class': None, 'flag': 21},
        ]
        # result = self.communicator.edit_receipt(store_info, assigned_products)
        # print(result)
        

    def test_get_source(self):
        self.assertEqual(self.communicator._get_source(10), "DB")
        self.assertEqual(self.communicator._get_source(20), "AI")
        self.assertEqual(self.communicator._get_source(21), "AI (Not Found)")
        self.assertEqual(self.communicator._get_source(99), "Unknown")
        

if __name__ == '__main__':
    unittest.main()