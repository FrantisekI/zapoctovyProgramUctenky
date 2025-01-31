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
from textAnalyzer.sortNames import sortNames
from database_conn import Database
# from assignTicketToDb import assignTicketToDB

def create_database():
    DB = Database()
    DB.create_tables()
    DB.create_indexes()

def main():
    # receiptPath, date = getImage()
    # print(f"Saved image to: {receiptPath}")
    # receiptText = imageToText(receiptPath)

    # print("Extracted Text:")
    # print()
    # print(receiptText)

    receiptText = """
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
"""
    
    DB = Database()
    
    


if __name__ == "__main__":
    main()
r"C:\\Users\\zapot\\Downloads\\Telegram Desktop\\photo_2024-11-10_13-30-33.jpg"