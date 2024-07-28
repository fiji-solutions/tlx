import json
import os

import boto3
from boto3.dynamodb.conditions import Attr
from collections import defaultdict
from decimal import Decimal


session = boto3.Session()
dynamodb = session.resource('dynamodb')


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def fetch_coins_for_date_range(table_name, start_date, end_date):
    table = dynamodb.Table(table_name)

    response = table.scan(
        FilterExpression=Attr('Timestamp').between(f"{start_date} 00:00:00+00:00", f"{end_date} 00:00:00+00:00")
    )
    items = response['Items']
    return items


def fetch_and_process_coins(start_date, end_date, index_start, index_end, exclude_ids):
    coins_for_date_range = fetch_coins_for_date_range(os.environ["table3"], start_date, end_date)

    coins_by_date = defaultdict(list)
    for coin in coins_for_date_range:
        date_str = coin['Timestamp'].split(' ')[0]
        coins_by_date[date_str].append(coin)

    for date_str, coins in coins_by_date.items():
        filtered_coins = [coin for coin in coins if coin['CoinName'] not in exclude_ids]
        filtered_coins.sort(key=lambda x: x['MarketCap'], reverse=True)
        coins_by_date[date_str] = filtered_coins[index_start:index_end + 1]

    market_cap_sums = {}
    for date_str, coins in coins_by_date.items():
        market_cap_sum = sum(coin['MarketCap'] for coin in coins)
        market_cap_sums[date_str] = market_cap_sum

    return market_cap_sums


def lambda_handler(event, context):
    start_date = event['queryStringParameters']['start_date']
    end_date = event['queryStringParameters']['end_date']
    index_start = int(event['queryStringParameters']['index_start'])
    index_end = int(event['queryStringParameters']['index_end'])
    exclude_ids = event['queryStringParameters']['exclude_ids'].split(',')

    market_cap_sums = fetch_and_process_coins(start_date, end_date, index_start, index_end, exclude_ids)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Origin": "*",
        },
        'body': json.dumps(market_cap_sums, default=decimal_default)
    }
