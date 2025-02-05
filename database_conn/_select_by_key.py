from typing import TYPE_CHECKING
import mysql.connector

if TYPE_CHECKING:
    from .__init__ import Database

def _find_custom_names_by_bands(self: 'Database', keys: tuple[tuple[int, int]]) -> list[tuple[int, str]]:
    """from bands it finds custom names id and name as a list of tuples"""
    self.cursor.execute(f"""
        SELECT DISTINCT c.custom_product_id, c.name
        FROM Custom_Product_Names c
        JOIN Bands b ON c.custom_product_id = b.id_custom_name
        WHERE (b.band_id, b.band_hash) IN {keys};
        """)
    return self.cursor.fetchall()

def find_similar_shops(self: 'Database', shop_name: str) -> list[tuple[int, str]]:
    self.cursor.execute("""
        SELECT shop_id, shop_name
        FROM Shops
        WHERE shop_name LIKE %s;
        """, (f"%{shop_name}%",))
    return self.cursor.fetchall()
def find_all_products(self: 'Database') -> list[tuple[int, str]]:
    self.cursor.execute("""
        SELECT *
        FROM Product_Classes;
        """)
    return self.cursor.fetchall()

def select_all_classes(self: 'Database') -> list[tuple[int, str]]:
    self.cursor.execute("""
        SELECT class_name
        FROM Product_Classes;
        """)
    return self.cursor.fetchall()

def select_all_products_by_class(self: 'Database', class_name: str) -> list[tuple[int, str]]:
    self.cursor.execute("""
        SELECT Bought_Items.*, Product_Classes.class_name, Shops.shop_name
        FROM Bought_Items, Product_Classes, Shops
        WHERE Bought_Items.product_id = Product_Classes.class_id AND Bought_Items.shop_id = Shops.shop_id AND Product_Classes.class_name = %s;
        """, (class_name,))
    return self.cursor.fetchall()