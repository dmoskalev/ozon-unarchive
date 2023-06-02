import requests
import pandas as pd
import configparser
import time
from typing import List
import json

def send_request(offer_ids: List[str], client_id: str, api_key: str):
    url = "https://api-seller.ozon.ru/v2/product/list"
    headers = {
        "Client-Id": client_id,
        "Api-Key": api_key,
        "Content-Type": "application/json",
    }
    data = {
        "filter": {
            "offer_id": offer_ids,
            "visibility": "ARCHIVED",
        },
        "last_id": "",
        "limit": 100
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    time.sleep(0.1)  # 100ms pause
    return response.json()

def unarchive_products(product_ids: List[int], client_id: str, api_key: str):
    url = "https://api-seller.ozon.ru/v1/product/unarchive"
    headers = {
        "Client-Id": client_id,
        "Api-Key": api_key,
        "Content-Type": "application/json",
    }
    data = {
        "product_id": product_ids
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    time.sleep(0.1)  # 100ms pause
    return response.json()

def main():
    # Load configuration
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Get Client-Id and Api-Key from config file
    client_id = config.get('Ozon', 'Client-Id')
    api_key = config.get('Ozon', 'Api-Key')

    # Read CSV file and skip the first row
    df = pd.read_csv('autoarchive_items.csv')

    # Split dataframe into chunks of 100
    chunks = [df[i:i+100] for i in range(0, df.shape[0], 100)]

    for chunk in chunks:
        offer_ids = chunk['offer_id'].tolist()
        response = send_request(offer_ids, client_id, api_key)

        # Extract product_id from the response
        product_ids = [item['product_id'] for item in response['result']['items']]

        if product_ids:
            # Unarchive products
            unarchive_response = unarchive_products(product_ids, client_id, api_key)
            print(f"Result: {unarchive_response} for Ids: {product_ids}")

if __name__ == "__main__":
    main()
