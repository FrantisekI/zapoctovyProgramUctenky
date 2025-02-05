if __name__ == "__main__":
    from sort_names import sortNames
    from assign_by_database import assign_by_database
    from assign_by_LLM import find_by_AI
else:
    from textAnalyzer.sort_names import sortNames
    from textAnalyzer.assign_by_database import assign_by_database
    from textAnalyzer.assign_by_LLM import find_by_AI
import unicodedata
from pprint import pprint

groq_model = "llama-3.3-70b-versatile"
# groq_model = "llama-3.2-3b-preview"

def analyzeText(text: str, DatabaseObject: object) -> tuple[tuple[int, str], list[dict[str, int, int, str, set[tuple[int, str]], int]]]:
    """
    as an Input it takes plain text from receipt 
    
    returns list of dictionaries with assigned classes,
    
    list of dictionaries contains:
    
    name, total_price, amount, units, class, flag
    
    flag: 10 - assigned by DB
    flag: 20 - assigned by AI
    flag: 21 - tried to assign by AI but than not found in database
    """
    sortedNamesJson = {"items": [{'name': 'NP BIO DŽEM MER 270G', 'total_price': 36.9, 'amount': 1, 'units': 'Kč/ks'}, {'name': 'GOUDA PLÁTKY 50', 'total_price': 99.9, 'amount': 1, 'units': 'Kč/ks'}, {'name': 'CHLÉB ŠUMAVA1200GR', 'total_price': 42.9, 'amount': 1, 'units': 'Kč/ks'}, {'name': 'RAJČ.CHERRY OV.500G', 'total_price': 39.9, 'amount': 1, 'units': 'Kč/ks'}, {'name': 'S. KRÁL SÝRŮ PROV.BY', 'total_price': 26.9, 'amount': 1, 'units': 'Kč/ks'}, {'name': 'MANDARINKY', 'total_price': 28.4, 'amount': 0.95, 'units': 'Kč/kg'}, {'name': 'JABLKA ČERVENÁ', 'total_price': 38.6, 'amount': 0.99, 'units': 'Kč/kg'}], 'total': 313.5, 'store': 'PRODEJNA', 'date': '29.10.2024'}
    indicator, sortedNamesJson = sortNames(text)
    if indicator != True:
        return None, sortedNamesJson
    # print(type(sortedNamesJson))
    # print(sortedNamesJson)
    otherInfo = (sortedNamesJson.get("store"), sortedNamesJson.get("date"), sortedNamesJson.get("total"))
    # print(otherInfo)
    # print(repr(sortedNamesJson))
    products = extract_names(sortedNamesJson)
    assigned_names = [0]*len(products)
    unableToAssignByDB = []
    for i, product in enumerate(products):
        product_class = assign_by_database(product[0], DatabaseObject)
        print(product_class)
        if (product_class is not None) and len(product_class) == 1:
            assigned_names[i] = {
                'name': product[0],
                'total_price': product[1],
                'amount': product[2],
                'units': product[3],
                'class': {product_class},
                'flag': 10 # 10 means that it was assigned by database, 
                # 20 means that it was assigned by AI, 
                # 21 means that it was assigned by AI but than not found in database
            }
        else:
            unableToAssignByDB.append(product)
            
    print(unableToAssignByDB)
    if unableToAssignByDB:
        toAssignByLLM = [(unableToAssignByDB[i][4], unableToAssignByDB[i][0]) for i in range(len(unableToAssignByDB))]
        print('toAssignByLLM', toAssignByLLM)
        aiClassification = find_by_AI(toAssignByLLM, DatabaseObject)
        print(aiClassification)
        
        for i, product in enumerate(unableToAssignByDB):
            print('product', product)
            if aiClassification[i][2] is not None:
                assigned_names[product[4]] = {
                    'name': product[0],
                    'total_price': product[1],
                    'amount': product[2],
                    'units': product[3],
                    'class': aiClassification[i][2],
                    'flag': 20
                }
            else:
                assigned_names[product[4]] = {
                    'name': product[0],
                    'total_price': product[1],
                    'amount': product[2],
                    'units': product[3],
                    'class': {(0, aiClassification[i][3])},
                    'flag': 21
                }
    print(assigned_names)
    return otherInfo, assigned_names
        
def extract_names(text: dict) -> list[tuple[str, int, int, str, int]]:
    """as a input it takes json with sorted names and returns list of 
    tuples with:
    
    name, total_price, amount, units and order in array"""
    products = text.get('items')
    pretty_products = []
    order = 0
    for product in products:
        name = unicodedata.normalize('NFKD', product.get('name').upper()).encode('ASCII', 'ignore').decode('ASCII')
        total_price = int(product.get('total_price', 0)*100) if product.get('total_price') is not None else 0
        amount = int(product.get('amount', 1)*100) if product.get('amount') is not None else 100
        units = product.get('units', 'ks')
        
        pretty_products.append((name, total_price, amount, units, order))
        order += 1
    print('pretty_products', pretty_products)
    return pretty_products

if __name__ == "__main__":
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
    
    # from database_conn.__init__ import Database
    # import ..database_conn.__init__ as database_conn
    # db = Database()
    # analyzeText(receiptText, db)