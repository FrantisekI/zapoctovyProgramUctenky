import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()



class Database:
    def __init__(self):
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_DATABASE')
        )
        self.conn = conn
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()
        # print("DB closed.")
        
    def close(self):
        self.conn.close()
        print("Database connection closed. via close()")
        
    def fetch_one(self, query, args=None):
        self.cursor.execute(query, args)
        return self.cursor.fetchone()
        
    if __name__ == "__main__":
        PRE = ""
        from _select_one import select_one_bought_item, select_one_config, select_one_custom_product_name, select_one_product_class, select_one_shop, select_one_band, select_one_get_class_from_custom_name
        from _create_structure import create_tables, create_indexes
        from _insert import insert_bought_item, insert_config, insert_custom_product_name, insert_product_class, insert_shop, insert_band
        from _delete import delete_bought_item, delete_config, delete_custom_product_name_cascade, delete_product_class_cascade, delete_shop_cascade, delete_band
        from _minhash import _create_shingles, _create_signature, _store_custom_name_with_bands, hash_and_insert_custom_name, find_candidates, _compute_bands_hash, _marge_functions_to_compute_bands
        from _select_by_key import _find_custom_names_by_bands, find_similar_shops, find_all_products
    else:
        from database_conn._select_one import select_one_bought_item, select_one_config, select_one_custom_product_name, select_one_product_class, select_one_shop, select_one_band, select_one_get_class_from_custom_name
        from database_conn._create_structure import create_tables, create_indexes
        from database_conn._insert import insert_bought_item, insert_config, insert_custom_product_name, insert_product_class, insert_shop, insert_band
        from database_conn._delete import delete_bought_item, delete_config, delete_custom_product_name_cascade, delete_product_class_cascade, delete_shop_cascade, delete_band
        from database_conn._minhash import  _create_shingles, _create_signature, _store_custom_name_with_bands, hash_and_insert_custom_name, find_candidates, _compute_bands_hash, _marge_functions_to_compute_bands
        from database_conn._select_by_key import _find_custom_names_by_bands, find_similar_shops, find_all_products

if __name__ == "__main__":
    DB = Database()
    DB.create_tables()
    DB.create_indexes()
    # DB.add.config("shop_name", "Walmart")

    # create_user("John", "")
    # create_receipt(1, 100.00, "Walmart")
    # create_receipt_item(1, 1, "Apple", 2, 0.50, "each", 1.00)
    # create_receipt_item(1, 1, "Banana", 3, 0.25, "each", 0.75)


