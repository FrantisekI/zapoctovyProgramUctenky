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