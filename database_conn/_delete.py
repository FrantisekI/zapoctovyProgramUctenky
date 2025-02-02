def delete_config(self, key):
    self.cursor.execute("""
    DELETE FROM Config WHERE config_key = %s;
    """, (key,))
    self.conn.commit()
    
def delete_shop_cascade(self, shop_id: int):
    self.cursor.execute("""
    DELETE FROM Shops WHERE shop_id = %s;
    """, (shop_id,))
    self.conn.commit()
    
def delete_product_class_cascade(self, class_id: int):
    self.cursor.execute("""
    DELETE FROM Product_Classes WHERE class_id = %s;
    """, (class_id,))
    self.conn.commit()
    
def delete_bought_item(self, bought_id: int):
    self.cursor.execute("""
    DELETE FROM Bought_Items WHERE bought_id = %s;
    """, (bought_id,))
    self.conn.commit()
    
def delete_custom_product_name_cascade(self, custom_product_id: int):
    self.cursor.execute("""
    DELETE FROM Custom_Product_Names WHERE custom_product_id = %s;
    """, (custom_product_id,))
    self.conn.commit()
    
def delete_band(self, id_custom_name: int, band_id: int, band_hash: int):
    self.cursor.execute("""
    DELETE FROM Bands WHERE id_custom_name = %s AND band_id = %s AND band_hash = %s;
    """, (id_custom_name, band_id, band_hash))
    self.conn.commit()
