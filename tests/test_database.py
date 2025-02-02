import unittest
from database_conn import Database
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
        self.signature = self.db.insert_band(self.custom_name_id, 12345, 67890)

    def tearDown(self):
        try:
            self.db.cursor.fetchall()  # Clear any unread results
        except Exception:
            pass
        self.db.cursor.execute("DELETE FROM Bands;")
        self.db.cursor.execute("DELETE FROM Custom_Product_Names;")
        self.db.cursor.execute("DELETE FROM Bought_Items;")
        self.db.cursor.execute("DELETE FROM Product_Classes;")
        self.db.cursor.execute("DELETE FROM Shops;")
        self.db.conn.commit()
        # self.db.close()

    def test_delete_shop(self):
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

    def test_delete_band(self):
        self.db.select_one_band(self.custom_name_id, 12345, 67890)
        self.db.delete_band(self.custom_name_id, 12345, 67890)
        self.assertIsNone(self.db.cursor.fetchone())
        
    def test_minhash(self):
        shingles = self.db.hash_and_insert_custom_name("Test Custom Name", self.product_class_id)
        self.assertEqual(1, 1)
        
    def test_create_bands(self):
        words = [
            "cat", "cats", "category",  # similar words
            "dog", "dogs", "dogma",    # another similar set
            "car", "care", "career",    # another similar set
            "computer", "computation",  # technical words
            "mouse", "house", "spouse", # rhyming words
            "mice", "ice", "dice",      # another rhyming set
            "sport", "sports", "sporting", # more sport related
            "apple", "apples", "applesauce", # fruit variations
            "banana", "bananas", "bananabread", # more fruit variations
            "table", "tables", "tablecloth", # furniture words
            "chair", "chairs", "chairlift", # more furniture words
            "book", "books", "bookstore", # reading related
            "read", "reads", "reading", # more reading related
            "run", "runs", "running", # action words
            "walk", "walks", "walking", # more action words
            "talk", "talks", "talking",  # communication words
            "listen", "listens", "listening", # more communication words
            "create", "creates", "creating", # creative words
            "imagine", "imagines", "imagination", # more creative words
            "unimaginativelyproliferating", "unimaginativelyproliferates", "unimaginativelyproliferation", # long, made-up words
            "discombobulatinglyintertwining", "discombobulatinglyintertwines", "discombobulatinglyintertwiningly", # more long, made-up words
            "supercalifragilisticexpialidociouslysimilar", "supercalifragilisticexpialidociouslysimilarly", "supercalifragilisticexpialidociousness", # even longer!
            "Applesauceandcranberries", "Applesauceandcranberry", "Applesauceandcranberriesly", # combined words
            "Elephantiasticallymagnanimous", "Elephantiastically", "Magnanimous", # combined words
            "Flibbertigibbetisticallyinclined", "Flibbertigibbetistically", "Inclined", # combined words
            "Whatchamacallitandthingamajig", "Whatchamacallit", "Thingamajig", # combined words
            "Kerfuffleandhullabaloo", "Kerfuffle", "Hullabaloo", # combined words
            "boots", 
        ]
        
        for word in words:
            # print(word, ':')
            self.db.hash_and_insert_custom_name(word, self.product_class_id)
        candidates = self.db.find_candidates("boobs")
        print(candidates)
        self.assertEqual(1, 1)
        
    def test_find_candidates(self):
        shingles = self.db.find_candidates("Test Custom Name")
        # print(shingles)
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()