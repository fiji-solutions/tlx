import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
import os


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
            price = (cols[1].text.strip()
                     .replace('$', '')
                     .replace('₀', '0')
                     .replace('₁', '1')
                     .replace('₂', '2')
                     .replace('₃', '3')
                     .replace('₄', '4')
                     .replace('₅', '5')
                     .replace('₆', '6')
                     .replace('₇', '7')
                     .replace('₈', '8')
                     .replace('₉', '9')
                     )
            try:
                price = float(price)
                data.append((name, price))
            except ValueError:
                print(f"Skipping invalid price: {price}")

    return data


def store_data_in_dynamodb(data, timestamp):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["table"])

    with table.batch_writer() as batch:
        for name, price in data:
            try:
                batch.put_item(
                    Item={
                        'CoinName': name,
                        'Timestamp': timestamp,
                        'Price': price
                    }
                )
            except ClientError as e:
                print(f"Failed to insert {name} into DynamoDB: {e.response['Error']['Message']}")


def store_coin_source_in_dynamodb(coin_source_data):
    dynamodb = boto3.resource('dynamodb')
    coin_source_table = dynamodb.Table(os.environ["table2"])

    for name, source in coin_source_data:
        try:
            response = coin_source_table.get_item(
                Key={
                    'CoinName': name,
                    'Source': source
                }
            )
            if 'Item' not in response:
                coin_source_table.put_item(
                    Item={
                        'CoinName': name,
                        'Source': source
                    }
                )
        except ClientError as e:
            print(f"Failed to check/insert {name} from {source} into DynamoDB: {e.response['Error']['Message']}")


def lambda_handler(event, context):
    urls = {
        "https://www.solindex.xyz/index/sol-essentials": "sol-essentials",
        "https://www.solindex.xyz/index/memes": "memes",
        "https://www.solindex.xyz/index/dogs": "dogs",
        "https://www.solindex.xyz/index/cats": "cats"
    }

    all_data = set()
    coin_source_data = set()
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S+00:00')

    for url, source in urls.items():
        try:
            html = fetch_data(url)
            data = parse_html(html)
            for name, price in data:
                all_data.add((name, price))
                coin_source_data.add((name, source))
        except Exception as e:
            print(f"Error fetching data from {url}: {e}")

    store_data_in_dynamodb(list(all_data), timestamp)  # Convert set back to list
    store_coin_source_in_dynamodb(list(coin_source_data))  # Convert set back to list

    return {
        'statusCode': 200,
        'body': json.dumps('Data fetched and stored successfully')
    }
