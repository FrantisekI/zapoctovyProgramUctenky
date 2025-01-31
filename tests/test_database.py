import unittest
from database_conn.Database import Database
from datetime import datetime

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()
        # Insert test data
        self.shop_id = self.db.insert_shop("Test Shop")
        self.product_class_id = self.db.insert_product_class("Test Class")
        self.bought_id = self.db.insert_bought_item(10.5, "kg", 100.0, datetime.now(), 
                                                    self.shop_id, self.product_class_id)
        self.custom_name_id = self.db.insert_custom_product_name("Custom Test", self.product_class_id)
        self.signature = self.db.insert_signature(self.custom_name_id, 12345, 111111)

    def tearDown(self):
        try:
            self.db.cursor.fetchall()  # Clear any unread results
        except Exception:
            pass
        self.db.cursor.execute("DELETE FROM Signatures;")
        self.db.cursor.execute("DELETE FROM Custom_Product_Names;")
        self.db.cursor.execute("DELETE FROM Bought_Items;")
        self.db.cursor.execute("DELETE FROM Product_Classes;")
        self.db.cursor.execute("DELETE FROM Shops;")
        self.db.conn.commit()
        # self.db.close()

    def test_delete_shop_(self):
        self.db.select_one_shop(self.shop_id)
        self.db.delete_shop_cascade(self.shop_id)
        self.assertIsNone(self.db.cursor.fetchone())

    def test_delete_product_class(self):
        self.db.select_one_product_class(self.product_class_id)
        self.db.delete_product_class_cascade(self.product_class_id)
        self.assertIsNone(self.db.cursor.fetchone())

    def test_delete_bought_item(self):
        self.db.select_one_bought_item(self.bought_id)
        self.db.delete_bought_item(self.bought_id)
        self.assertIsNone(self.db.cursor.fetchone())

    def test_delete_custom_product_name(self):
        self.db.select_one_custom_product_name(self.custom_name_id)
        self.db.delete_custom_product_name_cascade(self.custom_name_id)
        self.assertIsNone(self.db.cursor.fetchone())

    def test_delete_signature(self):
        self.db.select_one_signature(self.custom_name_id, 12345)
        self.db.delete_signature(self.custom_name_id, 12345)
        self.assertIsNone(self.db.cursor.fetchone())

if __name__ == '__main__':
    unittest.main()