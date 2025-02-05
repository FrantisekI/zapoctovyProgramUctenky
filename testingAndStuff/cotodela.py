import unicodedata
from datetime import datetime 
for idx, product in enumerate([], 1):
    print('fff')


print(unicodedata.normalize('NFKD', input().upper()).encode('ASCII', 'ignore').decode('ASCII'))

print(datetime.strptime('ffdsf', "%d.%m.%Y").date())


def get_shopping_patterns(self) -> 'Dict':
    """Analyze shopping patterns (which days/times user shops most)"""
    query = """
        SELECT 
            DAYNAME(date_time) as day_of_week,
            COUNT(*) as visit_count
        FROM Bought_Items
        GROUP BY day_of_week
        ORDER BY visit_count DESC;
    """
    return self.db.fetch_all(query)

def get_frequently_bought_together(self, time_value: int, time_unit: 'TimeFrame') -> 'List[Tuple[str, str, int]]':
    """Find products that are often bought together"""
    start_date = self._parse_timeframe(time_value, time_unit)
    query = """
        SELECT 
            pc1.name as product1,
            pc2.name as product2,
            COUNT(*) as together_count
        FROM Bought_Items bi1
        JOIN Bought_Items bi2 ON 
            bi1.date_time = bi2.date_time AND
            bi1.shop_id = bi2.shop_id AND
            bi1.product_id < bi2.product_id
        JOIN Product_Classes pc1 ON bi1.product_id = pc1.class_id
        JOIN Product_Classes pc2 ON bi2.product_id = pc2.class_id
        WHERE bi1.date_time >= %s
        GROUP BY pc1.name, pc2.name
        HAVING together_count > 1
        ORDER BY together_count DESC
        LIMIT 10;
    """
    return self.db.fetch_all(query, (start_date,))