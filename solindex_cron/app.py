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
            price = cols[1].text.strip()
            data.append((name, price))

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


def lambda_handler(event, context):
    urls = [
        "https://www.solindex.xyz/index/sol-essentials",
        "https://www.solindex.xyz/index/memes",
        "https://www.solindex.xyz/index/dogs",
        "https://www.solindex.xyz/index/cats"
    ]

    all_data = []
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S+00:00')

    for url in urls:
        try:
            html = fetch_data(url)
            data = parse_html(html)
            for name, price in data:
                all_data.append((name, price))
        except Exception as e:
            print(f"Error fetching data from {url}: {e}")

    store_data_in_dynamodb(all_data, timestamp)

    return {
        'statusCode': 200,
        'body': json.dumps('Data fetched and stored successfully')
    }
