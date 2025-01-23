from groq import Groq
import os
from dotenv import load_dotenv
import json
import jsonschema # type: ignore

load_dotenv()

def sortNames(receiptText):

    Groq_key = os.environ.get("GROQ_API_KEY")
    Gclient = Groq(
        api_key=Groq_key,
    )

    completion = Gclient.chat.completions.create(
        model="llama3-groq-70b-8192-tool-use-preview",
        messages=[
            {
                "role": "system",
                "content": """
Analyzuj tento text účtenky a vrať strukturovaná data v následujícím JSON formátu:
{
    "items": [
        {
            "name": "název produktu",
            "total_price": "celková cena v Kč",
            "unit_price": "cena za jednotku (pokud existuje, jinak null)"
        }
    ],
    "total": "celková částka účtenky",
    "store": "název obchodu"
}

Pravidla pro zpracování:
1. Ignoruj veškeré informace o prodejně, času, datu a kreditech
2. Pro položky prodávané na váhu:
   - "total_price" je celková zaplacená částka
   - "unit_price" obsahuje cenu za jednotku včetně jednotky (např. "29.90 Kč/kg")
3. Pro běžné položky:
   - "total_price" je uvedená cena
   - "unit_price" je null
4. Všechny ceny musí být ve formátu s desetinnou tečkou a jednotkou "Kč"
5. Zachovej přesné názvy produktů jak jsou uvedeny na účtence
6. Mezi produkty se může nacházet i řádek s počtem kreditů, ten ignoruj, nepiš místo něj nic, jen ho vynech

Chybové stavy:
- Pokud nelze určit cenu nebo název, danou položku přeskoč
- Pokud nelze určit celkovou částku, vrať null v "total"
- Pokud nelze určit název obchodu, vrať PRODEJNA v "store"

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
        stop=None,
    )


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
                        "unit_price": {"type": ["string", "null"]}
                    }
                }
            },
            "total": {"type": ["string", "integer"]},
            "store": {"type": "string"}
        }
    }
    try:
        textOutput = json.loads(completion.choices[0].message.content)
        jsonschema.validate(textOutput, schema)
    except jsonschema.ValidationError as e:
        print(e.message)
        textOutput = {}

    print(textOutput)
    i = json.validate(textOutput)

    return textOutput

if __name__ == "__main__":
    sortNames("")
