def select_one_config(self, key: str) -> str:
    self.cursor.execute("""
    SELECT config_value FROM Config WHERE config_key = %s;
    """, (key,))
    return self.cursor.fetchone()[0]

def select_one_shop(self, shop_id: int) -> str:
    self.cursor.execute("""
    SELECT shop_name FROM Shops WHERE shop_id = %s;
    """, (shop_id,))
    return self.cursor.fetchone()[0]

def select_one_product_class(self, class_id: int) -> str:
    self.cursor.execute("""
    SELECT class_name FROM Product_Classes WHERE class_id = %s;
    """, (class_id,))
    return self.cursor.fetchone()[0]

def select_one_bought_item(self, bought_id: int) -> tuple:
    self.cursor.execute("""
    SELECT amount, units, price, date_time, shop_id, product_id
    FROM Bought_Items WHERE bought_id = %s;
    """, (bought_id,))
    return self.cursor.fetchone()

def select_one_custom_product_name(self, custom_product_id: int) -> str:
    self.cursor.execute("""
    SELECT name FROM Custom_Product_Names WHERE custom_product_id = %s;
    """, (custom_product_id,))
    return self.cursor.fetchone()[0]

def select_one_signature(self, id_custom_name: int, hash_index: int) -> int:
    self.cursor.execute("""
    SELECT hash_value FROM Signatures WHERE id_custom_name = %s AND hash_index = %s;
    """, (id_custom_name, hash_index))
    return self.cursor.fetchone()[0]