import mysql.connector # type: ignore
from dotenv import load_dotenv
import os

load_dotenv()

from Database import Database
from createTables import create_tables



def connect():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_DATABASE')
    )


def readFoodNames():
    conn = connect()

    cursor = conn.cursor()

    cursor.execute("SELECT product_name FROM ReceiptItems")
    foodNames = cursor.fetchall()
    cursor.close()
    conn.close()
    return foodNames


def create_receipt(user_id, total_price, store_name):
    conn = connect()

    cursor = conn.cursor()

    cursor.execute("INSERT INTO Receipts (user_id, total_price, store_name) VALUES (%s, %s, %s)", (user_id, total_price, store_name))
    conn.commit()
    cursor.close()
    conn.close()

def create_receipt_item(receipt_id, user_id, product_name, quantity, unit_price, price_per_unit, total_price):
    conn =connect()

    cursor = conn.cursor()

    cursor.execute("INSERT INTO ReceiptItems (receipt_id, user_id, product_name, quantity, unit_price, price_per_unit, total_price) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                   (receipt_id, user_id, product_name, quantity, unit_price, price_per_unit, total_price))
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print(readFoodNames(user_id=1))
    # create_user("John", "")
    # create_receipt(1, 100.00, "Walmart")
    # create_receipt_item(1, 1, "Apple", 2, 0.50, "each", 1.00)
    # create_receipt_item(1, 1, "Banana", 3, 0.25, "each", 0.75)


