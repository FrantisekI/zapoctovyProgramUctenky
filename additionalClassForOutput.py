from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional, Union
import re
from dataclasses import dataclass
from enum import Enum

class TimeFrame(Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"

    @staticmethod
    def from_string(value: str) -> 'TimeFrame':
        """Convert string to TimeFrame enum"""
        try:
            return TimeFrame(value.lower())
        except ValueError:
            raise ValueError(f"Invalid time frame: {value}. Use day, week, month, or year.")

@dataclass
class ShoppingStats:
    total_spent: float  # Stored as integer * 100, converted to float for display
    item_count: int
    avg_price: float   # Stored as integer * 100, converted to float for display
    first_purchase: datetime
    last_purchase: datetime

    @staticmethod
    def convert_to_decimal(value: int) -> float:
        """Convert integer stored value (× 100) to decimal"""
        return value / 100.0 if value is not None else 0.0

    @staticmethod
    def convert_to_storage(value: float) -> int:
        """Convert decimal value to storage format (× 100)"""
        return int(value * 100) if value is not None else 0

class ShoppingAnalytics:
    def __init__(self, db_handler):
        self.db = db_handler

    def _parse_timeframe(self, time_value: int, time_unit: TimeFrame) -> datetime:
        """Convert a time frame specification into a datetime"""
        current_time = datetime.now()
        if time_unit == TimeFrame.DAY:
            return current_time - timedelta(days=time_value)
        elif time_unit == TimeFrame.WEEK:
            return current_time - timedelta(weeks=time_value)
        elif time_unit == TimeFrame.MONTH:
            return current_time - timedelta(days=time_value * 30)
        elif time_unit == TimeFrame.YEAR:
            return current_time - timedelta(days=time_value * 365)
        raise ValueError(f"Unsupported time unit: {time_unit}")

    def get_total_spending(self, time_value: int, time_unit: TimeFrame) -> float:
        """Get total spending in the specified time period"""
        start_date = self._parse_timeframe(time_value, time_unit)
        query = """
            SELECT SUM(amount * price) / 10000 as total
            FROM Bought_Items
            WHERE date_time >= %s;
        """
        one = self.db.fetch_one(query, (start_date,))
        # print(int(one[0]))
        return float(one[0]) or 0.0

    def get_product_spending(self, product_name: str, time_value: int, time_unit: TimeFrame) -> ShoppingStats:
        """Get spending statistics for a specific product"""
        start_date = self._parse_timeframe(time_value, time_unit)
        query = """
            SELECT 
                SUM(bi.amount * bi.price) / 10000 as total_spent,
                SUM(bi.amount) / 100 as total_items,
                MIN(bi.date_time) as first_purchase,
                MAX(bi.date_time) as last_purchase
            FROM Bought_Items bi
            JOIN Product_Classes pc ON bi.product_id = pc.class_id
            WHERE pc.class_name = %s AND bi.date_time >= %s;
        """
        result = self.db.fetch_one(query, (product_name, start_date))
        if not result[0]:
            return None
        print(result)
            
        return ShoppingStats(
            total_spent=float(result[0]),
            item_count=float(result[1]),
            avg_price=float(result[0]) / float(result[1]),
            first_purchase=result[2],
            last_purchase=result[3]
        )

    def get_shop_spending(self, shop_id: int, time_value: int, time_unit: TimeFrame) -> ShoppingStats:
        """Get spending statistics for a specific shop"""
        start_date = self._parse_timeframe(time_value, time_unit)
        query = """
            SELECT 
                SUM(amount * price) / 10000 as total_spent,
                COUNT(*) as visit_count,
                MIN(date_time) as first_visit,
                MAX(date_time) as last_visit
            FROM Bought_Items
            WHERE shop_id = %s AND date_time >= %s;
        """
        result = self.db.fetch_one(query, (shop_id, start_date))
        if not result[0]:
            return None
            
        return ShoppingStats(
            total_spent=float(result[0]),
            item_count=float(result[1]),
            avg_price=float(result[0]) / float(result[1]),
            first_purchase=result[2],
            last_purchase=result[3]
        )

    def get_most_visited_shop(self, time_value: int, time_unit: TimeFrame) -> Tuple[int, str, int]:
        """Get the most frequently visited shop in the time period"""
        start_date = self._parse_timeframe(time_value, time_unit)
        query = """
            SELECT 
                bi.shop_id,
                s.shop_name,
                COUNT(*) as visit_count
            FROM Bought_Items bi
            JOIN Shops s ON bi.shop_id = s.shop_id
            WHERE bi.date_time >= %s
            GROUP BY bi.shop_id, s.shop_name
            ORDER BY visit_count DESC
            LIMIT 1;
        """
        result = self.db.fetch_one(query, (start_date,))
        return (result[0], result[1], result[2]) if result else None

    def get_most_expensive_product(self, time_value: int, time_unit: TimeFrame) -> Dict:
        """Get the product with the highest total cost in the time period"""
        start_date = self._parse_timeframe(time_value, time_unit)
        query = """
            SELECT 
                pc.class_name,
                SUM(bi.amount * bi.price) / 10000 as total_cost,
                SUM(bi.amount) as total_quantity,
                COUNT(*) as purchase_count
            FROM Bought_Items bi
            JOIN Product_Classes pc ON bi.product_id = pc.class_id
            WHERE bi.date_time >= %s
            GROUP BY pc.class_name
            ORDER BY total_cost DESC
            LIMIT 1;
        """
        # print(self.db.fetch_one(query, (start_date,)))
        return self.db.fetch_one(query, (start_date,))

    def get_product_price_stats(self, product_name: str) -> Dict:
        """Get price statistics for a specific product"""
        query = """
            SELECT 
                MIN(price) / 100 as min_price,
                MAX(price) / 100 as max_price,
                AVG(price) / 100 as avg_price,
                SUM(amount) / 100 as total_bought,
                COUNT(DISTINCT shop_id) as shop_count
            FROM Bought_Items bi
            JOIN Product_Classes pc ON bi.product_id = pc.class_id
            WHERE pc.class_name = %s;
        """
        return self.db.fetch_one(query, (product_name,))