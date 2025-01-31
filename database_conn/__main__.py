import mysql.connector # type: ignore
from dotenv import load_dotenv
import os

load_dotenv()
if __name__ == "__main__":
    from Database import Database
else:
    from database_conn.Database import Database



def connect():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_DATABASE')
    )

def connectToDB():
    myDB = connect()
    return Database(myDB)

if __name__ == "__main__":
    DB = connectToDB()
    DB.create_tables()
    DB.create_indexes()
    # DB.add.config("shop_name", "Walmart")

    # create_user("John", "")
    # create_receipt(1, 100.00, "Walmart")
    # create_receipt_item(1, 1, "Apple", 2, 0.50, "each", 1.00)
    # create_receipt_item(1, 1, "Banana", 3, 0.25, "each", 0.75)


