import mysql.connector # type: ignore

class Database:
    def __init__(self, conn):
        self.conn = connect()
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def create_tables(self):
        try:
            # Create Users table
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Config (
                configKey VARCHAR(255) PRIMARY KEY, -- Unique identifier for each setting
                configValue VARCHAR(255) NOT NULL  -- Value of the setting
            );
            """)
            
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Shops (
                shop_id INT AUTO_INCREMENT PRIMARY KEY,
                shop_name VARCHAR(30) NOT NULL
            );
            """)
            
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Product_Classes (
                class_id INT AUTO_INCREMENT PRIMARY KEY,
                class_name VARCHAR(30) NOT NULL,
            );              
            """)
            
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Bought_Items (
                receipt_id INT AUTO_INCREMENT PRIMARY KEY,
                amount DECIMAL(10,2),
                units VARCHAR(30),
                price DECIMAL(10,2),
                date_time DATETIME,
                CREATE INDEX idx_date ON Bought_Items(date_time),
                CREATE INDEX idx_shop ON Shops(shop_id),
                CREATE INDEX idx_class ON Product_Classes(class_id),
            );
            """)
            
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Custom_Product_Names (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                CREATE INDEX idx_name ON Product_Classes(class_id),
            );
            """)

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Signatures (
                id_name INT,
                hash_index INT,
                hash_value BIGINT,
                PRIMARY KEY (id_name, hash_index),
                FOREIGN KEY (id_name) REFERENCES Custom_Product_Names(name),
            );
            """)


            print("Tables created successfully!")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            self.conn.commit()

    def readFoodNames(self, user_id = 1):
        self.cursor.execute("""SELECT product_name FROM ReceiptItems 
            WHERE user_id = %s GROUP BY product_name;""",
            (user_id,))
        foodNames = self.cursor.fetchall()
        return foodNames

    def create_user(self, username, email):
        self.cursor.execute("INSERT INTO Users (username, email) VALUES (%s, %s);", (username, email))
        self.conn.commit()

    def create_receipt(self, user_id, total_price, store_name):
        self.cursor.execute("INSERT INTO Receipts (user_id, total_price, store_name) VALUES (%s, %s, %s);", (user_id, total_price, store_name))
        self.conn.commit()

    def create_receipt_item(self, receipt_id, user_id, product_name, quantity, unit_price, price_per_unit, total_price):
        self.cursor.execute("INSERT INTO ReceiptItems (receipt_id, user_id, product_name, quantity, unit_price, price_per_unit, total_price) VALUES (%s, %s, %s, %s, %s, %s, %s);", 
                            (receipt_id, user_id, product_name, quantity, unit_price, price_per_unit, total_price))
        self.conn.commit()
