'''
this thing will be used to input receipts and save them to the database which will be 
read by a different script 
user will provide receipt image that it will be read and converted to record it will probably be in format 
(foodName, amount, price, date)
'''

# first it will convert get image input and save it to /images and returns path
# then it will convert image to text
# then will call database and return what types of food are there
# will do api call to a AI with json input which will read the input text and return how much of which food was bought
# will save this data to a database
from json import loads
from getImage import getImage
from imageToText import imageToText
from textAnalyzer.sort_names import sortNames
from textAnalyzer import analyzeText
from database_conn import Database
from communicator import Communicator
# from assignTicketToDb import assignTicketToDB

from datetime import datetime

def create_database():
    DB = Database()
    DB.create_tables()
    DB.create_indexes()

def main():
    DB = Database()
    communicator = Communicator(DB)
    imagePath = communicator.get_image_path()
    

    '''receiptText = """
13:29 •
Detail účtenky
313.50Kč • 2kredity • Ibod
Díky akcím jste ušetřili 71 Kč
Získané kredity
• Kupóny
Položka
NP BIO DŽEM MER 270G
GOUDA PLÁTKY 50
CHLÉB ŠUMAVA1200GR
RAJČ.CHERRY OV.500G
S. KRÁL SÝRŮ PROV.BY
MANDARINKY
0.95 x 29.90 Kč /kg
Získané kredity: 2 kredity
JABLKA ČERVENÁ
0.99 x 39.00 Kč /kg
Celkem
Získané kredity
Získané body
PRODEJNA
Praha 4, Arkády Pankrác
Na Pankráci 86, Praha 4
platební
900/0i
29.10.2024
2
2
Cena
36.90 Kč
99.90 Kč
42.90 Kč
39.90 Kč
26.90 Kč
28.40 Kč
38.60 Kč
313.50 Kč
2
KLIENT
+420 776 200 517
"""'''
    receiptText = imageToText(imagePath)
    # print("Extracted Text:")
    # print()
    # print(receiptText)
    # analyzedReceipt = [{'name': 'NP BIO DZEM MER 270G', 'total_price': 3690, 'amount': 100, 'units': 'Kč/ks', 'class': {(0, 'džem')}, 'flag': 21}, {'name': 'GOUDA PLATKY 50', 'total_price': 9990, 'amount': 100, 'units': 'Kč/ks', 'class': {(0, 'sýr')}, 'flag': 21}, {'name': 'CHLEB SUMAVA1200GR', 'total_price': 4290, 'amount': 100, 'units': 'Kč/ks', 'class': {(0, 'chleb')}, 'flag': 21}, {'name': 'RAJC.CHERRY OV.500G', 'total_price': 3990, 'amount': 100, 'units': 'Kč/ks', 'class': {(0, 'rajče')}, 'flag': 21}, {'name': 'S. KRAL SYRU PROV.BY', 'total_price': 2690, 'amount': 100, 'units': 'Kč/ks', 'class': {(0, 'sýr')}, 'flag': 21}, {'name': 'MANDARINKY', 'total_price': 2840, 'amount': 95, 'units': 'Kč/kg', 'class': {(0, 'mandarinka')}, 'flag': 21}, {'name': 'JABLKA CERVENA', 'total_price': 3860, 'amount': 99, 'units': 'Kč/kg', 'class': {(0, 'jablko')}, 'flag': 21}]
    store_info, analyzedReceipt = analyzeText(receiptText, DB)
    if store_info is None:
        print("something went wrong with analyzing receipt")
        print("receipt plain text:", receiptText)
        print("receipt analyzed:", analyzedReceipt)
        return

    store_info, analyzedReceipt = communicator.edit_receipt(store_info, analyzedReceipt)
    
    print("General Info:", store_info, "\nItems:", analyzedReceipt)
    if shop := DB.find_similar_shops(store_info[0]):
        shopId = shop[0][0]
    else:
        shopId = DB.insert_shop(store_info[0])
    for item in analyzedReceipt:
        if item['flag'] % 10 == 1:
            classId = DB.insert_product_class(next(iter(item['class']))[1])
        else:
            classId = next(iter(item['class']))[0]
            
        DB.insert_bought_item(item['amount'], item['units'], item['total_price'], 
                              datetime.strptime(store_info[1], "%d.%m.%Y"), shopId, classId)
        print(DB.find_all_products()) # comment 
    
    
    
    
    


if __name__ == "__main__":
    main()
r"C:\\Users\\zapot\\Downloads\\Telegram Desktop\\photo_2024-11-10_13-30-33.jpg"