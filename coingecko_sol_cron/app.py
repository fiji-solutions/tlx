import os

import requests
import boto3
import uuid
from datetime import datetime
import time

dynamodb = boto3.client('dynamodb')

def put_item_to_dynamodb(table_name, item):
    try:
        response = dynamodb.put_item(
            TableName=table_name,
            Item={
                'CompositeKey': {'S': item['CompositeKey']},
                'CoinName': {'S': item['CoinName']},
                'IndexName': {'S': item['IndexName']},
                'Liquidity': {'N': str(item['Liquidity'])},
                'MarketCap': {'N': str(item['MarketCap'])},
                'Price': {'N': str(item['Price'])},
                'Timestamp': {'S': item['Timestamp']},
                'UniqueId': {'S': item['UniqueId']},
                'Volume24h': {'N': str(item['Volume24h'])},
            }
        )
    except Exception as e:
        print(f"Error inserting item: {e}")

def put_coins_to_dynamodb(table_name, coins):
    for index, coin in enumerate(coins, start=1):
        item = {
            'id': {'S': coin['id']},
            'image': {'S': coin['image']},
            'order': {'N': str(401)}
        }
        try:
            dynamodb.put_item(TableName=table_name, Item=item)
        except Exception as e:
            print(f"Error inserting coin: {e}")

def fetch_coins_in_solana_ecosystem():
    API_KEY = "CG-in4nCVxz1tVBaxUBYMhRN5wz"
    headers = {"x-cg-demo-api-key": API_KEY}

    solana_category_id = "solana-ecosystem"
    coins_url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "category": solana_category_id,
        "order": "market_cap_desc",
        "per_page": 200,
        "page": 1,
        "sparkline": "false"
    }

    response1 = requests.get(coins_url, headers=headers, params=params)
    params["page"] = 2
    response2 = requests.get(coins_url, headers=headers, params=params)

    solana_coins1 = response1.json()
    solana_coins2 = response2.json()

    return solana_coins1 + solana_coins2

def fetch_and_store_coin_history(coins, table_name):
    API_KEY = "CG-in4nCVxz1tVBaxUBYMhRN5wz"
    headers = {"x-cg-demo-api-key": API_KEY}
    history_url = "https://api.coingecko.com/api/v3/coins/COIN_ID/history"
    today = datetime.utcnow().strftime("%d-%m-%Y")

    for index, coin in enumerate(coins):
        if index > 0 and index % 20 == 0:
            time.sleep(60)

        params = {"date": today, "localization": "false"}
        url = history_url.replace("COIN_ID", coin["id"])
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            market_data = data.get('market_data', {})

            item = {
                "CompositeKey": f"{coin['id']}#{today}",
                "CoinName": coin["id"],
                "IndexName": "coingecko",
                "Liquidity": market_data.get('total_volume', {}).get('usd', 0),
                "MarketCap": market_data.get('market_cap', {}).get('usd', 0),
                "Price": market_data.get('current_price', {}).get('usd', 0),
                "Timestamp": datetime.strptime(today, "%d-%m-%Y").strftime("%Y-%m-%d %H:%M:%S+00:00"),
                "UniqueId": str(uuid.uuid4()),
                "Volume24h": market_data.get('total_volume', {}).get('usd', 0)
            }
            put_item_to_dynamodb(table_name, item)
        else:
            print(f"Error fetching data for {coin['id']} on {today}")

def lambda_handler(event, context):
    coins = fetch_coins_in_solana_ecosystem()

    # Store coin details in DynamoDB
    put_coins_to_dynamodb(os.environ["table4"], coins)

    # Fetch and store coin history in DynamoDB
    fetch_and_store_coin_history(coins, os.environ["table3"])
