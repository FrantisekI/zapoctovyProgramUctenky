import mysql.connector
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
            amount INT,
            units VARCHAR(30),
            price INT,
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
        CREATE TABLE IF NOT EXISTS Bands (
            id_custom_name INT,
            band_id INT,
            band_hash BIGINT,
            PRIMARY KEY (id_custom_name, band_id, band_hash),
            INDEX (band_id, band_hash),
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
        CREATE INDEX idx_signature_custom ON Custom_Product_Names(custom_product_id);
        """)
    except mysql.connector.Error as err:
        print("err")
        print(f"Error: {err}")

def read_food_names(self):
    self.cursor.execute("""SELECT product_name FROM ReceiptItems GROUP BY product_name;""")
    foodNames = self.cursor.fetchall()
    return foodNames