import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
def create_tables():
    # Connect to MySQL server
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_DATABASE')
    )

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
            FOREIGN KEY (receipt_id) REFERENCES Receipts(receipt_id)
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
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_DATABASE')
    )

    cursor = conn.cursor()

    cursor.execute("SELECT product_name FROM ReceiptItems \
                   WHERE user_id = %s GROUP BY product_name", (user_id,))
    foodNames = cursor.fetchall()
    cursor.close()
    conn.close()
    return foodNames

if __name__ == "__main__":
    create_tables()
    print(readFoodNames(user_id=1))
