from sortNames import sortNames
from assignByDatabase import assignByDatabase
groq_model = "llama-3.3-70b-versatile"
# groq_model = "llama-3.2-3b-preview"

def analyzeText(text: str, DatabaseObject: object):
    # sortedNamesJson = sortNames(text, groq_model)
    sortedNamesJson = {'items': [{'name': 'NP BIO DŽEM MER 270G', 'total_price': '36.90', 'unit_price': None}, {'name': 'GOUDA PLÁTKY 50', 'total_price': '99.90', 'unit_price': None}, {'name': 'CHLÉB ŠUMAVA1200GR', 'total_price': '42.90', 'unit_price': None}, {'name': 'RAJČ.CHERRY OV.500G', 'total_price': '39.90', 'unit_price': None}, {'name': 'S. KRÁL SÝRŮ PROV.BY', 'total_price': '26.90', 'unit_price': None}, {'name': 'MANDARINKY', 'total_price': '28.40', 'unit_price': '29.90 Kč/kg'}, {'name': 'JABLKA ČERVENÁ', 'total_price': '38.60', 'unit_price': '39.00 Kč/kg'}], 'total': '313.50', 'store': 'PRODEJNA'}
    if sortedNamesJson == {}:
        return
    assignedJson = assignByDatabase(sortedNamesJson, DatabaseObject)
    
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