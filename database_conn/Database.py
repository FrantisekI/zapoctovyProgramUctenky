import mysql.connector # type: ignore

class Database:
    def __init__(self, conn):
        self.conn = conn
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
                class_name VARCHAR(30) NOT NULL
            );              
            """)
            
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Bought_Items (
                receipt_id INT AUTO_INCREMENT PRIMARY KEY,
                amount DECIMAL(10,2),
                units VARCHAR(30),
                price DECIMAL(10,2),
                date_time DATETIME,
                shop_id INT,    -- Foreign key referencing Shops
                product_id INT, -- Foreign key referencing Products
                FOREIGN KEY (shop_id) REFERENCES Shops(shop_id),
                FOREIGN KEY (product_id) REFERENCES Product_Classes(class_id)
            );
            """)
            
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Custom_Product_Names (
                custom_product_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                product_id INT, -- Foreign key referencing Product_Classes
                FOREIGN KEY (product_id) REFERENCES Product_Classes(class_id)
            );
            """)

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Signatures (
                id_custom_name INT,
                hash_index INT,
                hash_value BIGINT,
                PRIMARY KEY (id_custom_name, hash_index),
                FOREIGN KEY (id_custom_name) REFERENCES Custom_Product_Names(custom_product_id)
            );
            """)

            print("Tables created successfully!")

        except mysql.connector.Error as err:
            print("err")
            print(f"Error: {err}")

    def create_indexes(self):
        try:
            self.cursor.execute("""
            CREATE INDEX idx_date ON Bought_Items(date_time);
            CREATE INDEX idx_bought_shop ON Bought_Items(shop_id);
            CREATE INDEX idx_bought_product ON Bought_Items(product_id);
            CREATE INDEX idx_custom_class ON Custom_Product_Names(product_id);
            CREATE INDEX idx_signature_custom ON Custom_Product_Names(id);
            """)
        except mysql.connector.Error as err:
            print("err")
            print(f"Error: {err}")

    def read_food_names(self):
        self.cursor.execute("""SELECT product_name FROM ReceiptItems GROUP BY product_name;""")
        foodNames = self.cursor.fetchall()
        return foodNames


    def add_receipt_item(self, receipt_id, user_id, product_name, quantity, unit_price, price_per_unit, total_price):
        self.cursor.execute("INSERT INTO ReceiptItems (receipt_id, user_id, product_name, quantity, unit_price, price_per_unit, total_price) VALUES (%s, %s, %s, %s, %s, %s, %s);", 
                            (receipt_id, user_id, product_name, quantity, unit_price, price_per_unit, total_price))
        self.conn.commit()
    
