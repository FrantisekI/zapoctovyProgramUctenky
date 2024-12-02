# getImage.py
from datetime import datetime
import os

def getImage():
    """
    Gets receipt image path from user input and handles date.
    Returns tuple of (image_path, date)
    """
    # Get image path
    while True:
        image_path = input("Enter the full path to receipt image: ").strip()
        if os.path.exists(image_path):
            break
        print("File not found. Please enter a valid path.")

    # Get date input
    date_input = input("Enter receipt date (DD-MM-YYYY) or press Enter for current date: ").strip()
    
    if date_input:
        try:
            date = datetime.strptime(date_input, "%d-%m-%Y")
        except ValueError:
            print("Invalid date format. Using current date.")
            date = datetime.now()
    else:
        date = datetime.now()

    # Create images directory if it doesn't exist
    os.makedirs("images", exist_ok=True)
    
    # Copy file to images directory with timestamp
    new_filename = f"receipt_{date.strftime('%Y%m%d_%H%M%S')}{os.path.splitext(image_path)[1]}"
    new_path = os.path.join("images", new_filename)
    
    # Copy the file
    with open(image_path, 'rb') as src, open(new_path, 'wb') as dst:
        dst.write(src.read())

    return new_path, date

if __name__ == "__main__":
    # Test the function
    path, date = getImage()
    print(f"Saved image to: {path}")
    print(f"Date: {date}")