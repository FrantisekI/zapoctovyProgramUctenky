import mysql.connector # type: ignore
from dotenv import load_dotenv
import os
load_dotenv()

class Database:
    def __init__(self, conn=None):
        if conn is None:
            conn = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_DATABASE')
            )
        self.conn = conn
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()
        print("Database connection closed.")
        
    def close(self):
        self.conn.close()
        print("Database connection closed. via close()")

    def create_tables(self):
        try:
            # Create Users table
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Config (
                config_key VARCHAR(255) PRIMARY KEY, -- Unique identifier for each setting
                config_value VARCHAR(255) NOT NULL  -- Value of the setting
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
                bought_id INT AUTO_INCREMENT PRIMARY KEY,
                amount DECIMAL(10,2),
                units VARCHAR(30),
                price DECIMAL(10,2),
                date_time DATETIME,
                shop_id INT,    -- Foreign key referencing Shops
                product_id INT, -- Foreign key referencing Products
                FOREIGN KEY (shop_id) REFERENCES Shops(shop_id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES Product_Classes(class_id) 
                ON DELETE CASCADE
            );
            """)
            
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Custom_Product_Names (
                custom_product_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                product_id INT, -- Foreign key referencing Product_Classes
                FOREIGN KEY (product_id) REFERENCES Product_Classes(class_id) 
                ON DELETE CASCADE
            );
            """)

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Signatures (
                id_custom_name INT,
                hash_index INT,
                hash_value BIGINT,
                PRIMARY KEY (id_custom_name, hash_index),
                FOREIGN KEY (id_custom_name) REFERENCES Custom_Product_Names(custom_product_id) 
                ON DELETE CASCADE
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


    ##### Insert FUNCTIONS #####
    def insert_config(self, key: str, value: str):
        
        self.cursor.execute("""
        INSERT INTO Config (config_key, config_value)
        VALUES (%s, %s);
        """, (key, value))
        self.conn.commit()
    
    def insert_shop(self, shop_name: str) -> int:
        self.cursor.execute("""
        INSERT INTO Shops (shop_name)
        VALUES (%s);
        """, (shop_name,))
        self.conn.commit()
        
        self.cursor.execute("SELECT LAST_INSERT_ID();")
        shop_id = self.cursor.fetchone()[0]
        return shop_id
    
    def insert_product_class(self, class_name: str) -> int:
        self.cursor.execute("""
        INSERT INTO Product_Classes (class_name)
        VALUES (%s);
        """, (class_name,))
        self.conn.commit()
        
        self.cursor.execute("SELECT LAST_INSERT_ID();")
        class_id = self.cursor.fetchone()[0]
        return class_id
    
    def insert_bought_item(self, amount: float, units: str, price: float, date_time, shop_id: int, product_id: int) -> int:
        amount = round(amount, 2)
        price = round(price, 2)
        self.cursor.execute("""
        INSERT INTO Bought_Items (amount, units, price, date_time, shop_id, product_id)
        VALUES (%s, %s, %s, %s, %s, %s);
        """, (amount, units, price, date_time, shop_id, product_id))
        self.conn.commit()
        
        self.cursor.execute("SELECT LAST_INSERT_ID();")
        bought_id = self.cursor.fetchone()[0]
        return bought_id
    
    def insert_custom_product_name(self, name: str, product_id: int) -> int:
        self.cursor.execute("""
        INSERT INTO Custom_Product_Names (name, product_id)
        VALUES (%s, %s);
        """, (name, product_id))
        self.conn.commit()
        
        self.cursor.execute("SELECT LAST_INSERT_ID();")
        custom_product_id = self.cursor.fetchone()[0]
        return custom_product_id
    
    def insert_signature(self, id_custom_name: int, hash_index: int, hash_value: int):
        self.cursor.execute("""
        INSERT INTO Signatures (id_custom_name, hash_index, hash_value)
        VALUES (%s, %s, %s);
        """, (id_custom_name, hash_index, hash_value))
        self.conn.commit()
        
    ##### Delete Functions #####
    
    def delete_config(self, key):
        self.cursor.execute("""
        DELETE FROM Config WHERE config_key = %s;
        """, (key,))
        self.conn.commit()
        
    def delete_shop_cascade(self, shop_id: int):
        self.cursor.execute("""
        DELETE FROM Shops WHERE shop_id = %s;
        """, (shop_id,))
        self.conn.commit()
        
    def delete_product_class_cascade(self, class_id: int):
        self.cursor.execute("""
        DELETE FROM Product_Classes WHERE class_id = %s;
        """, (class_id,))
        self.conn.commit()
        
    def delete_bought_item(self, bought_id: int):
        self.cursor.execute("""
        DELETE FROM Bought_Items WHERE bought_id = %s;
        """, (bought_id,))
        self.conn.commit()
        
    def delete_custom_product_name_cascade(self, custom_product_id: int):
        self.cursor.execute("""
        DELETE FROM Custom_Product_Names WHERE custom_product_id = %s;
        """, (custom_product_id,))
        self.conn.commit()
        
    def delete_signature(self, id_custom_name: int, hash_index: int):
        self.cursor.execute("""
        DELETE FROM Signatures WHERE id_custom_name = %s AND hash_index = %s;
        """, (id_custom_name, hash_index))
        self.conn.commit()
        
        
    ##### Select One Functions #####
    
    def select_one_config(self, key: str) -> str:
        self.cursor.execute("""
        SELECT config_value FROM Config WHERE config_key = %s;
        """, (key,))
        return self.cursor.fetchone()[0]
    
    def select_one_shop(self, shop_id: int) -> str:
        self.cursor.execute("""
        SELECT shop_name FROM Shops WHERE shop_id = %s;
        """, (shop_id,))
        return self.cursor.fetchone()[0]
    
    def select_one_product_class(self, class_id: int) -> str:
        self.cursor.execute("""
        SELECT class_name FROM Product_Classes WHERE class_id = %s;
        """, (class_id,))
        return self.cursor.fetchone()[0]
    
    def select_one_bought_item(self, bought_id: int) -> tuple:
        self.cursor.execute("""
        SELECT amount, units, price, date_time, shop_id, product_id
        FROM Bought_Items WHERE bought_id = %s;
        """, (bought_id,))
        return self.cursor.fetchone()
    
    def select_one_custom_product_name(self, custom_product_id: int) -> str:
        self.cursor.execute("""
        SELECT name FROM Custom_Product_Names WHERE custom_product_id = %s;
        """, (custom_product_id,))
        return self.cursor.fetchone()[0]
    
    def select_one_signature(self, id_custom_name: int, hash_index: int) -> int:
        self.cursor.execute("""
        SELECT hash_value FROM Signatures WHERE id_custom_name = %s AND hash_index = %s;
        """, (id_custom_name, hash_index))
        return self.cursor.fetchone()[0]