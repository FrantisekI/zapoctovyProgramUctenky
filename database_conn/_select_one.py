import unicodedata
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

def select_one_band(self, id_custom_name: int, band_id: int, band_hash: int) -> int:
    self.cursor.execute("""
    SELECT id_custom_name FROM Bands WHERE 
    id_custom_name = %s AND band_id = %s AND band_hash = %s;
    """, (id_custom_name, band_id, band_hash))
    return self.cursor.fetchone()[0]

def select_one_get_class_from_custom_name(self, custom_product_id: int) -> tuple[int, str]:
    """by custom name id it finds it's product_class and returns 
    product_id and class_name"""
    self.cursor.execute("""
    SELECT pc.class_id, pc.class_name 
    FROM Product_Classes pc
    JOIN Custom_Product_Names cu ON pc.class_id = cu.product_id
    WHERE cu.custom_product_id = %s;
    """, (custom_product_id,))
    return self.cursor.fetchone()