def insert_config(self, key: str, value: str):
    
    self.cursor.execute("""
    INSERT INTO Config (config_key, config_value)
    VALUES (%s, %s);
    """, (key, value))
    self.conn.commit()

def insert_shop(self, shop_name: str) -> int:
    self.cursor.execute("""
    INSERT INTO Shops (shop_name)
    VALUES (%s);
    """, (shop_name,))
    self.conn.commit()
    
    self.cursor.execute("SELECT LAST_INSERT_ID();")
    shop_id = self.cursor.fetchone()[0]
    return shop_id

def insert_product_class(self, class_name: str) -> int:
    self.cursor.execute("""
    INSERT INTO Product_Classes (class_name)
    VALUES (%s);
    """, (class_name,))
    self.conn.commit()
    
    self.cursor.execute("SELECT LAST_INSERT_ID();")
    class_id = self.cursor.fetchone()[0]
    return class_id


def insert_bought_item(self, amount: int, units: str, price: int, date_time, shop_id: int, product_id: int) -> int:
    '''Inserts a bought item into the database. with parameters you see in the function signature.
    
    amount and price are in cents. - to get in czech crowns, divide by 100.'''
    print(amount, units, price, date_time, shop_id, product_id)
    self.cursor.execute("""
    INSERT INTO Bought_Items (amount, units, price, date_time, shop_id, product_id)
    VALUES (%s, %s, %s, %s, %s, %s);
    """, (amount, units, price, date_time, shop_id, product_id))
    self.conn.commit()
    
    self.cursor.execute("SELECT LAST_INSERT_ID();")
    bought_id = self.cursor.fetchone()[0]
    return bought_id

def insert_custom_product_name(self, name: str, product_id: int) -> int:
    self.cursor.execute("""
    INSERT INTO Custom_Product_Names (name, product_id)
    VALUES (%s, %s);
    """, (name, product_id))
    self.conn.commit()
    
    return self.cursor.lastrowid

def insert_band(self, id_custom_name: int, band_id: int, band_hash: int) -> int:
    self.cursor.execute("""
    INSERT INTO Bands (id_custom_name, band_id, band_hash)
    VALUES (%s, %s, %s);
    """, (id_custom_name, band_id, band_hash))
    self.conn.commit()
    
    return self.cursor.lastrowid
