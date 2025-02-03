import asyncio
from groq import AsyncGroq
import os
from dotenv import load_dotenv
load_dotenv()

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from database_conn import Database

def find_by_AI(wordsToAssign: list, DatabaseObject: 'Database') -> int | None:
    """
    Synchronous wrapper for async classification
    """
    # the tuple is (order, name)
    products = [(product[4], product[0]) for product in wordsToAssign]

    client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))
    result = asyncio.run(_classify_products(client, products))
    return result

async def _classify_products(client, products):
    """
    Async helper function to classify products in parallel
    """
    classification_tasks = [
        send_request_to_classify(client, product_inf) for product_inf in products
    ]
    
    result = await asyncio.gather(*classification_tasks)
    
    return result

async def send_request_to_classify(client, product_info):
    """
    Async function to classify a single product
    """
    global groq_model
    index, product = product_info
    
    try:
        chat_completion = await client.chat.completions.create(
            model=os.environ.get("GROQ_MODEL"),
            messages=[
                {
                    "role": "system",
                    "content": """You are a food classification assistant. user will send
                        you some weird food name that he found in shop and your task is to respond
                        with something normal that we can work with e.g. from "12 red apples" you
                        respond with "apple".
                        in json format 
                        {
                            "name": "product name"
                        }
                        if you cant find out just to name column write None, it is better 
                        than to pretend you know
                        """
                },
                {
                    "role": "user",
                    "content": f"What this product: {product} might be?"
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
        print({
            'index': index,
            'product': product, 
            'classification': chat_completion.choices[0].message.content
        })
        return {
            'index': index,
            'product': product, 
            'classification': chat_completion.choices[0].message.content
        }
    except Exception as e:
        return {
            'index': index,
            'product': product, 
            'classification': f"Error classifying: {str(e)}"
        }
        
