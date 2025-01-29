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
                shop_name VARCHAR(100) NOT NULL
            );
            """)
            
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS BoughtItems (
                receipt_id INT AUTO_INCREMENT PRIMARY KEY,
                amount DECIMAL(10,2),
                units VARCHAR(100),
                price DECIMAL(10,2),
                date_time DATETIME,
                CREATE INDEX idx_date ON BoughtItems(date_time),
                CREATE INDEX idx_shop ON Shops(shop_id)
            );
            """)

            self.cursor.execute("""
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
            self.conn.commit()

    def readFoodNames(self, user_id = 1):
        self.cursor.execute("SELECT product_name FROM ReceiptItems \
                            WHERE user_id = %s GROUP BY product_name", (user_id,))
        foodNames = self.cursor.fetchall()
        return foodNames

    def create_user(self, username, email):
        self.cursor.execute("INSERT INTO Users (username, email) VALUES (%s, %s)", (username, email))
        self.conn.commit()

    def create_receipt(self, user_id, total_price, store_name):
        self.cursor.execute("INSERT INTO Receipts (user_id, total_price, store_name) VALUES (%s, %s, %s)", (user_id, total_price, store_name))
        self.conn.commit()

    def create_receipt_item(self, receipt_id, user_id, product_name, quantity, unit_price, price_per_unit, total_price):
        self.cursor.execute("INSERT INTO ReceiptItems (receipt_id, user_id, product_name, quantity, unit_price, price_per_unit, total_price) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                            (receipt_id, user_id, product_name, quantity, unit_price, price_per_unit, total_price))
        self.conn.commit()
