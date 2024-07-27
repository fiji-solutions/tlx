import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
import os
from decimal import Decimal
import uuid


def extract_info(data):
    results = []
    while data:
        # Find the start of the next object
        data = data.replace("\\\"", "\"")
        start_idx = data.find('{"id":')
        if start_idx == -1:
            break

        # Find the end of the current object
        end_idx = data.find('}', start_idx)
        while data[end_idx + 1] == '}':  # in case of nested JSON objects
            end_idx = data.find('}', end_idx + 1)
        end_idx += 1

        # Extract the object string
        obj_str = data[start_idx:end_idx]

        # Remove this object from the data
        data = data[end_idx + 1:]

        # Parse the object string manually
        symbol = find_between(obj_str, '"symbol":"', '"')
        price = clean_and_convert(find_between(obj_str, '"price":', '}'))
        mcap = clean_and_convert(find_between(obj_str, '"mcap":"', '"').replace("$n", ""))
        liquidity = clean_and_convert(find_between(obj_str, '"liquidity":', ','))
        volume24h = clean_and_convert(find_between(obj_str, '"volume24h":', ','))

        # Append the parsed object to the results
        results.append((
            symbol,
            price,
            mcap,
            liquidity,
            volume24h
        ))

    return results


def clean_and_convert(value):
    if value is None:
        return None
    value = value.replace(",", "").replace("$", "")
    try:
        return Decimal(value)
    except ValueError:
        return value


def find_between(s, start, end):
    start_idx = s.find(start)
    if start_idx == -1:
        return None
    start_idx += len(start)
    end_idx = s.find(end, start_idx)
    if end_idx == -1:
        return None
    return s[start_idx:end_idx]


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
    script_rows = soup.select("script")
    data = []

    script_index = 0
    for count, script in enumerate(script_rows):
        if '\\"price\\"' in script.text:
            script_index = count
            break

    whole_string = ""
    for i in range(20):
        cleaned_string = script_rows[script_index + i].text.replace('self.__next_f.push([1,"21:', '').replace('"])', '')
        whole_string = whole_string + cleaned_string

    return extract_info(whole_string.replace("self.__next_f.push([1,\"", "").replace("\\\"", "\""))


def store_data_in_dynamodb(data, index_name, timestamp):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["table"])

    with table.batch_writer() as batch:
        for name, price, market_cap, liquidity, volume24h in data:
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
                        'Liquidity': liquidity,
                        'Volume24h': volume24h,
                        'UniqueId': unique_id
                    }
                )
            except ClientError as e:
                print(f"Failed to insert {name} into DynamoDB: {e.response['Error']['Message']}")


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
    main_page_data = []

    for url, index_name in urls.items():
        try:
            html = fetch_data(url)
            data = parse_html(html)
            store_data_in_dynamodb(data, index_name, timestamp)

            # Calculate total market cap for the index
            total_market_cap = sum([item[2] for item in data])
            main_page_data.append((index_name, total_market_cap))

        except Exception as e:
            print(f"Error fetching data from {url}: {e}")

    try:
        store_main_page_data_in_dynamodb(main_page_data, timestamp)
    except Exception as e:
        print(f"Error storing main page data in DynamoDB: {e}")

    return {
        'statusCode': 200,
        'body': json.dumps('Data fetched and stored successfully')
    }
