import asyncio
from groq import AsyncGroq
import os
from dotenv import load_dotenv
import json
from textAnalyzer.assign_by_database import assign_by_database
load_dotenv()

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from database_conn import Database

def find_by_AI(wordsToAssign: list[tuple[str, int]], DatabaseObject: 'Database') -> list[tuple[str, int, dict[str, str] | None, str]]:
    """
    as an input it takes list of tuples with:
    name, order
    
    tries to find they classification by calling LLM
    returns sorted list by order of tuples with:
    
    name, order, class_name, class_id, what_AI_assigned
    """
    # the tuple is (order, name)
    products = wordsToAssign
    print('products in assigned by ai', products)
    client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))
    results = asyncio.run(_classify_products(client, products))
    
    classifiedProducts = []
    for i, result in enumerate(results):
        assigned_class = assign_by_database(result['classification'], DatabaseObject)
        classifiedProducts.append((products[i][0], products[i][1], 
                                  assigned_class, result['classification']))
    print('classifiedProducts', classifiedProducts)
    return classifiedProducts

async def _classify_products(client: 'AsyncGroq', products: list[tuple[int, str]]) -> list[dict[int, str, str]]:
    """
    Basically just calls send_request_to_classify for each product in paralel
    returns list of dicts in format:
    {
        'index': index,
        'product': product, 
        'classification': product_name
    }
    """
    classification_tasks = [
        send_request_to_classify(client, product_inf) for product_inf in products
    ]
    
    result = await asyncio.gather(*classification_tasks)
    
    return sorted(result, key=lambda x: x['index'])

async def send_request_to_classify(client: 'AsyncGroq', product_info: tuple[int, str]) -> dict[int, str, str]:
    """
    Async function sends a request to classify a product to LLM
    returns dict in format:
    {
        'index': index,
        'product': product, 
        'classification': product_name
    }
    """
    global groq_model
    index, product = product_info
    
    try:
        chat_completion = await client.chat.completions.create(
            model=os.environ.get("GROQ_MODEL"),
            messages=[
                {
                    "role": "system",
                    "content": """
Jsi asistent pro klasifikaci potravin. Uživatel ti pošle název produktu z účtenky, 
který je často zkrácený, obsahuje množství nebo další specifikace. 
Tvým úkolem je vrátit pouze základní název produktu v jednotném čísle.

Například:
"RAJC.CHERRY OV.500G" -> "rajče"
"ROHLIKY CESNEK 3KS" -> "rohlík"
"GOUDA PLATKY 50%" -> "sýr"
"JABLKA GALA VB" -> "jablko"

Odpověz pouze v JSON formátu:
{
    "name": "název produktu"
}

Pokud si nejsi jistý, co produkt znamená, vrať:
{
    "name": null
}

Je lepší vrátit null než hádat.
                        """
                },
                {
                    "role": "user",
                    "content": f"Co je tento produkt: {product}?"
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
        simplified_product = json.loads(chat_completion.choices[0].message.content)
        product_name = simplified_product.get('name', None)
        
        print({
            'index': index,
            'product': product, 
            'classification': product_name
        })
        return {
            'index': index,
            'product': product, 
            'classification': product_name
        }
    except Exception as e:
        print(f"Error classifying: {str(e)} - assign_by_LLM.py")
        return {
            'index': index,
            'product': product, 
            'classification': f"Error classifying"
        }
        
