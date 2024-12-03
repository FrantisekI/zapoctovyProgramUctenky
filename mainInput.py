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
from textAnalyzer import sortNames
from database import readFoodNames
# from assignTicketToDb import assignTicketToDB


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
    names = """
{
  "items": [
    {
      "name": "NP BIO DŽEM MER 270G",
      "total_price": "36.90 Kč",
      "unit_price": null
    },
    {
      "name": "GOUDA PLÁTKY 50",
      "total_price": "99.90 Kč",
      "unit_price": null
    },
    {
      "name": "CHLÉB ŠUMAVA1200GR",
      "total_price": "42.90 Kč",
      "unit_price": null
    },
    {
      "name": "RAJČ.CHERRY OV.500G",
      "total_price": "39.90 Kč",
      "unit_price": null
    },
    {
      "name": "S. KRÁL SÝRŮ PROV.BY",
      "total_price": "26.90 Kč",
      "unit_price": null
    },
    {
      "name": "MANDARINKY",
      "total_price": "28.40 Kč",
      "unit_price": "0,95 x 29,90 Kč/kg"
    },
    {
      "name": "JABLKA ČERVENÁ",
      "total_price": "38.60 Kč",
      "unit_price": "0,99 x 39,00 Kč/kg"
    }
  ],
  "total": "313.50 Kč"
}
"""
    names = sortNames(receiptText)
    names = loads(names)
    print(names)

    foodNames = readFoodNames()
    print(names["total"])
    print(names["total"].split(" ")[0])
    print(foodNames)
    # foodAndPrice = readFoodNames(receiptText, foodNames)
    # assignTicketToDB(foodAndPrice, date)


if __name__ == "__main__":
    main()
r"C:\\Users\\zapot\\Downloads\\Telegram Desktop\\photo_2024-11-10_13-30-33.jpg"