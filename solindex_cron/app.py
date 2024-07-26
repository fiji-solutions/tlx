import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
import os
from decimal import Decimal
import uuid


def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.select("table tbody tr")
    data = []

    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 1:
            name = cols[0].text.strip()
            price = Decimal(cols[1].text.strip().replace('$', '').replace('₀', '0').replace('₁', '1')
                            .replace('₂', '2').replace('₃', '3').replace('₄', '4').replace('₅', '5')
                            .replace('₆', '6').replace('₇', '7').replace('₈', '8').replace('₉', '9'))
            market_cap = cols[2].text.strip().replace('B', '000000000').replace('M', '000000')
            market_cap = int(float(market_cap))
            weight = Decimal(cols[3].text.strip().replace('%', ''))

            data.append((name, price, market_cap, weight))

    return data


def store_data_in_dynamodb(data, index_name, timestamp):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["table"])

    with table.batch_writer() as batch:
        for name, price, market_cap, weight in data:
            unique_id = str(uuid.uuid4())
            try:
                batch.put_item(
                    Item={
                        'IndexName': index_name,
                        'CoinName': name,
                        'Timestamp': timestamp,
                        'Price': price,
                        'MarketCap': market_cap,
                        'Weight': float(weight),
                        'UniqueId': unique_id  # Ensure uniqueness
                    }
                )
            except ClientError as e:
                print(f"Failed to insert {name} into DynamoDB: {e.response['Error']['Message']}")


def lambda_handler(event, context):
    urls = {
        "https://www.solindex.xyz/index/sol-essentials": "sol-essentials",
        "https://www.solindex.xyz/index/memes": "memes",
        "https://www.solindex.xyz/index/dogs": "dogs",
        "https://www.solindex.xyz/index/cats": "cats"
    }

    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S+00:00')

    for url, index_name in urls.items():
        try:
            html = fetch_data(url)
            data = parse_html(html)
            store_data_in_dynamodb(data, index_name, timestamp)
        except Exception as e:
            print(f"Error fetching data from {url}: {e}")

    return {
        'statusCode': 200,
        'body': json.dumps('Data fetched and stored successfully')
    }
