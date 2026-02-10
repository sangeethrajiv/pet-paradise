import requests
import json

# Configuration
API_URL = "http://127.0.0.1:8000/api/products/"
DATA_FILE = "test_products.json"

def upload_products():
    try:
        with open(DATA_FILE, "r") as f:
            products = json.load(f)
        
        print(f"Starting upload of {len(products)} products...")
        
        for product in products:
            response = requests.post(API_URL, json=product)
            if response.status_code == 201:
                print(f"Successfully added: {product['title']}")
            else:
                print(f"Failed to add {product['title']}: {response.status_code} - {response.text}")
                
        print("Upload process completed.")
        
    except FileNotFoundError:
        print(f"Error: {DATA_FILE} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    upload_products()
