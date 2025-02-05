import requests # type: ignore
import json
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

def imageToText(image_path: str) -> str:
    """
    Convert image to text using OCR.space API
    
    Args:
        image_path: Path to the image file
        
    Returns:
        str: Extracted text from the image
    """
    # API Configuration
    API_KEY =  os.getenv('OCR_API_KEY')
    API_URL = 'https://api.ocr.space/parse/image'
    
    try:
        with open(image_path, 'rb') as image_file:
            payload = {
                'apikey': API_KEY,
                'language': 'cze',  
                'isOverlayRequired': False,
                'detectOrientation': True,
            }
            
            files = {
                'file': image_file
            }

            response = requests.post(API_URL, files=files, data=payload)
            response.raise_for_status()  
            result = response.json()
            
            if result['OCRExitCode'] == 1:
                text = ' '.join([page['ParsedText'] for page in result['ParsedResults']])
                return text.strip()
            else:
                error_message = result.get('ErrorMessage', 'Unknown error occurred')
                raise Exception(f"OCR API Error: {error_message}")
                
    except Exception as e:
        print(f"Error processing image: {e}")
        return ""

if __name__ == "__main__":
    sample_path = input("Enter image path: ").strip()
    if os.path.exists(sample_path):
        text = imageToText(sample_path)
        print("Extracted text:")
        print(text)
    else:
        print("File not found")