from groq import Groq
import os
from dotenv import load_dotenv
import json
import jsonschema # type: ignore

load_dotenv()

def sortNames(receiptText: str) -> dict:
    print('receiptText', receiptText)
    groq_model = os.environ.get("GROQ_MODEL")
    """
    This function takes a receipt text as input, sends it to the Groq API for analysis, 
    and returns structured data in JSON format.
    Identifies what are names and prices of products.
    
    schema = {
        "type": "object",
        "required": ["items", "total", "store"],
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["name", "total_price"],
                    "properties": {
                        "name": {"type": "string"},
                        "total_price": {"type": "string"},
                        "amount": {"type": ["string", "null"]},
                        "unit_price": {"type": ["string", "null"]}
                    }
                }
            },
            "total": {"type": ["string", "integer"]},
            "store": {"type": "string"},
            "date": {"type": ["string", "null"]}
        }
    }
    """
    Groq_key = os.environ.get("GROQ_API_KEY")
    Gclient = Groq(
        api_key=Groq_key,
    )

    completion = Gclient.chat.completions.create(
    model=groq_model,
    messages=[
        {
            "role": "system",
            "content": """
# ÚČEL
Extrahuj strukturovaná data z textu účtenky do JSON formátu.

# VÝSTUPNÍ FORMÁT
{
    "items": [
        {
            "name": "název produktu",
            "total_price": "celková cena", {"type": "number", "multipleOf": 0.01}
            "amount": "množství",
            "units": "jednotka"
        }
    ],
    "total": "celková částka", {"type": "number", "multipleOf": 0.01}
    "store": "název obchodu",
    "date": "datum nákupu ve formátu DD.MM.YYYY",
}

# PRAVIDLA ZPRACOVÁNÍ

## Obecná pravidla:
- Zachovej přesně původní názvy produktů
- Všechny ceny převeď na formát s desetinnou tečkou a "Kč"
- Ignoruj informace o věrnostních bodech/kreditech
- Ignoruj marketingové texty a slevové akce
- Všechna desetinná čísla zaokrouhli na dvě desetinná místa

## Specifická pravidla pro položky:
1. Vážené zboží:
   - amount: uveď bez jednotky, ty napiš do units (např. 0.95)
   - total_price: celková zaplacená částka
   - units: cena za jednotku (např. "Kč/kg")

2. Kusové zboží:
   - amount: počet kusů jako číslo
   - total_price: celková cena za všechny kusy
   - units: jednotka (např. "Kč/ks")

# ZPRACOVÁNÍ CHYB
- Chybějící cena/název: přeskoč položku
- Chybějící celková částka: vrať null v "total"
- Chybějící název obchodu: použij "PRODEJNA"
- Chybějící datum/čas: vrať null v příslušném poli

# PŘÍKLADY SPRÁVNÉHO VÝSTUPU
{
    "items": [
        {
            "name": "Rohlík tukový",
            "total_price": 2.90,
            "amount": 1,
            "unit_price": "Kč/ks"
        },
        {
            "name": "Banány",
            "total_price": 37.90, 
            "amount": 0.95,
            "units": "Kč/kg"
        }
    ],
    "total": 40.80,
    "store": "Potraviny U Nováků",
    "date": "28.02.2025",
}
"""
            },
            {
                "role": "user",
                "content": receiptText
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        
        # if model doesn't supoort json_object, just comment this line
        response_format={"type": "json_object"}, 
        stop=None,
    )
    print(completion.choices[0].message.content)

    schema = {
        "type": "object",
        "required": ["items", "total", "store"],
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["name", "total_price"],
                    "properties": {
                        "name": {"type": "string"},
                        "total_price": {"type": "number", "multipleOf": 0.01},
                        "amount": {"type": "number", "multipleOf": 0.01},
                        "units": {"type": "string"}
                    }
                }
            },
            "total": {"type": "number", "multipleOf": 0.01},
            "store": {"type": "string"},
            "date": {"type": ["string", "null"]}
        }
    }
    try:
        textOutput = completion.choices[0].message.content
        if type(textOutput) != dict:
            start = textOutput.find('{')
            end = textOutput.rfind('}') + 1
            textOutput = json.loads(textOutput[start:end])
        i = jsonschema.validate(textOutput, schema)
            
    except jsonschema.ValidationError as e:
        print(e.message)
        return {}

    print(dict(textOutput))

    return dict(textOutput)

if __name__ == "__main__":
    sortNames("")
