import json
import os

import boto3
from boto3.dynamodb.conditions import Attr
from collections import defaultdict

# Initialize a boto3 session with your AWS profile
session = boto3.Session()
dynamodb = session.resource('dynamodb')


def fetch_coins_for_date_range(table_name, start_date, end_date):
    table = dynamodb.Table(table_name)

    response = table.scan(
        FilterExpression=Attr('Timestamp').between(f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00")
    )
    items = response['Items']
    return items


def fetch_and_process_coins(start_date, end_date, index_start, index_end, exclude_ids):
    coins_for_date_range = fetch_coins_for_date_range(os.environ["table4"], start_date, end_date)

    # Organize data into multiple arrays, one per day
    coins_by_date = defaultdict(list)
    for coin in coins_for_date_range:
        # Extract the date part from the Timestamp
        date_str = coin['Timestamp'].split(' ')[0]
        coins_by_date[date_str].append(coin)

    # Sort each array by MarketCap and filter out excluded IDs
    for date_str, coins in coins_by_date.items():
        # Filter out coins with IDs in the exclude_ids list
        filtered_coins = [coin for coin in coins if coin['CoinName'] not in exclude_ids]
        # Sort the filtered coins by MarketCap
        filtered_coins.sort(key=lambda x: x['MarketCap'], reverse=True)
        # Filter out items outside of the specified index range
        coins_by_date[date_str] = filtered_coins[index_start:index_end + 1]

    # Calculate the sum of MarketCap for each date
    market_cap_sums = {}
    for date_str, coins in coins_by_date.items():
        market_cap_sum = sum(coin['MarketCap'] for coin in coins)
        market_cap_sums[date_str] = market_cap_sum

    return market_cap_sums


def lambda_handler(event, context):
    # Get query parameters
    start_date = event['queryStringParameters']['start_date']
    end_date = event['queryStringParameters']['end_date']
    index_start = int(event['queryStringParameters']['index_start'])
    index_end = int(event['queryStringParameters']['index_end'])
    exclude_ids = event['queryStringParameters']['exclude_ids'].split(',')

    # Process and fetch market cap sums
    market_cap_sums = fetch_and_process_coins(start_date, end_date, index_start, index_end, exclude_ids)

    # Return the market cap sums
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Origin": "*",
        },
        'body': json.dumps(market_cap_sums)
    }
