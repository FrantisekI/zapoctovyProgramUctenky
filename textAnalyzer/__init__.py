import re
if __name__ == "__main__":
    from sortNames import sortNames
    from assignByDatabase import assign_by_database
else:
    from textAnalyzer.sortNames import sortNames
    from textAnalyzer.assignByDatabase import assign_by_database

groq_model = "llama-3.3-70b-versatile"
# groq_model = "llama-3.2-3b-preview"

def analyzeText(text: str, DatabaseObject: object):
    # sortedNamesJson = sortNames(text, groq_model)
    sortedNamesJson = {'items': [{'name': 'NP BIO DŽEM MER 270G', 'total_price': 36.9, 'amount': 1, 'units': 'Kč/ks'}, {'name': 'GOUDA PLÁTKY 50', 'total_price': 99.9, 'amount': 1, 'units': 'Kč/ks'}, {'name': 'CHLÉB ŠUMAVA1200GR', 'total_price': 42.9, 'amount': 1, 'units': 'Kč/ks'}, {'name': 'RAJČ.CHERRY OV.500G', 'total_price': 39.9, 'amount': 1, 'units': 'Kč/ks'}, {'name': 'S. KRÁL SÝRŮ PROV.BY', 'total_price': 26.9, 'amount': 1, 'units': 'Kč/ks'}, {'name': 'MANDARINKY', 'total_price': 28.4, 'amount': 0.95, 'units': 'Kč/kg'}, {'name': 'JABLKA ČERVENÁ', 'total_price': 38.6, 'amount': 0.99, 'units': 'Kč/kg'}], 'total': 313.5, 'store': 'PRODEJNA', 'date': '29.10.2024'}
    products = extract_names(sortedNamesJson)
    for product in products:
        product_class = assign_by_database(product[0], DatabaseObject)
        if product_class is not None:
            print(product_class)
    # assignedJson = assign_by_database(sortedNamesJson, DatabaseObject)
    
def extract_names(text: dict) -> list[str, int, int, str]:
    products = text['items']
    pretty_products = []
    for product in products:
        name = product['name']
        total_price = int(product['total_price']*100)
        amount = int(product['amount']*100)
        units = product['units']
        
        pretty_products.append((name, total_price, amount, units))
    print(pretty_products)
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
    analyzeText(receiptText, None)