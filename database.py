import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
def connect():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_DATABASE')
    )

def create_tables():
    # Connect to MySQL server
    conn = connect()

    try:
        cursor = conn.cursor()
        
        # Create Users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Create Receipts table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Receipts (
            receipt_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_price DECIMAL(10,2),
            store_name VARCHAR(100),
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        );
        """)

        # Create ReceiptItems table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ReceiptItems (
            item_id INT AUTO_INCREMENT PRIMARY KEY,
            receipt_id INT,
            user_id INT,
            product_name VARCHAR(100) NOT NULL,
            quantity DECIMAL(10,3),
            unit_price DECIMAL(10,2),
            price_per_unit VARCHAR(50),
            total_price DECIMAL(10,2),
            FOREIGN KEY (receipt_id) REFERENCES Receipts(receipt_id),
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        );
        """)

        print("Tables created successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        conn.commit()
        cursor.close()
        conn.close()

def readFoodNames(user_id = 1):
    conn = connect()

    cursor = conn.cursor()

    cursor.execute("SELECT product_name FROM ReceiptItems \
                   WHERE user_id = %s GROUP BY product_name", (user_id,))
    foodNames = cursor.fetchall()
    cursor.close()
    conn.close()
    return foodNames

def create_user(username, email):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Users (username, email) VALUES (%s, %s)", (username, email))
    conn.commit()
    cursor.close()
    conn.close()

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


