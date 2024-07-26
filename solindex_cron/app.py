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


def parse_market_cap(market_cap_str):
    if 'B' in market_cap_str:
        return Decimal(market_cap_str.replace('B', '')) * Decimal(1_000_000_000)
    elif 'M' in market_cap_str:
        return Decimal(market_cap_str.replace('M', '')) * Decimal(1_000_000)
    else:
        return Decimal(market_cap_str)


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
            market_cap = parse_market_cap(cols[2].text.strip())
            weight = Decimal(cols[3].text.strip().replace('%', ''))

            data.append((name, price, market_cap, weight))

    return data


def store_data_in_dynamodb(data, index_name, timestamp):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["table"])

    with table.batch_writer() as batch:
        for name, price, market_cap, weight in data:
            unique_id = str(uuid.uuid4())
            composite_key = f"{index_name}#{name}#{timestamp}"
            try:
                batch.put_item(
                    Item={
                        'CompositeKey': composite_key,
                        'IndexName': index_name,
                        'CoinName': name,
                        'Timestamp': timestamp,
                        'Price': price,
                        'MarketCap': market_cap,
                        'Weight': weight,
                        'UniqueId': unique_id
                    }
                )
            except ClientError as e:
                print(f"Failed to insert {name} into DynamoDB: {e.response['Error']['Message']}")


def parse_main_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.select("li.flex.justify-center")
    data = []

    for item in items:
        index_name = item.select_one("a").get("href").split("/")[-1]
        market_cap_str = item.select_one("p.font-semibold").text.strip()
        market_cap = parse_market_cap(market_cap_str)

        data.append((index_name, market_cap))

    return data


def store_main_page_data_in_dynamodb(data, timestamp):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["table2"])

    with table.batch_writer() as batch:
        for index_name, market_cap in data:
            unique_id = str(uuid.uuid4())
            composite_key = f"{index_name}#{timestamp}"
            try:
                batch.put_item(
                    Item={
                        'CompositeKey': composite_key,
                        'IndexName': index_name,
                        'Timestamp': timestamp,
                        'MarketCap': market_cap,
                        'UniqueId': unique_id
                    }
                )
            except ClientError as e:
                print(f"Failed to insert {index_name} into DynamoDB: {e.response['Error']['Message']}")


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

    try:
        main_page_html = fetch_data("https://www.solindex.xyz/")
        main_page_data = parse_main_page(main_page_html)
        store_main_page_data_in_dynamodb(main_page_data, timestamp)
    except Exception as e:
        print(f"Error fetching data from main page: {e}")

    return {
        'statusCode': 200,
        'body': json.dumps('Data fetched and stored successfully')
    }
