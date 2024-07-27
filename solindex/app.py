import boto3
import os
import json
from decimal import Decimal
from datetime import datetime, timedelta

def fetch_market_cap_data(index_name, start_date, end_date):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["table2"])

    response = table.query(
        IndexName="IndexName-Timestamp-Index",
        KeyConditionExpression=boto3.dynamodb.conditions.Key('IndexName').eq(index_name) &
                               boto3.dynamodb.conditions.Key('Timestamp').between(start_date, end_date)
    )

    items = response['Items']
    return items

def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def aggregate_data(data, granularity, granularity_unit):
    aggregated_data = []
    current_time = None
    current_sum = 0
    count = 0

    for item in data:
        timestamp = datetime.strptime(item['Timestamp'], "%Y-%m-%d %H:%M:%S%z")
        marketcap = decimal_to_float(item['MarketCap'])

        if current_time is None:
            current_time = timestamp
            current_sum = marketcap
            count = 1
        else:
            time_diff = timestamp - current_time
            if granularity == 'HOURS' and time_diff < timedelta(hours=granularity_unit):
                current_sum += marketcap
                count += 1
            elif granularity == 'DAYS' and time_diff < timedelta(days=granularity_unit):
                current_sum += marketcap
                count += 1
            elif granularity == 'WEEKS' and time_diff < timedelta(weeks=granularity_unit):
                current_sum += marketcap
                count += 1
            else:
                aggregated_data.append({
                    'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S%z"),
                    'MarketCap': current_sum / count
                })
                current_time = timestamp
                current_sum = marketcap
                count = 1

    if count > 0:
        aggregated_data.append({
            'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S%z"),
            'MarketCap': current_sum / count
        })

    return aggregated_data

def lambda_handler(event, context):
    index = event['queryStringParameters']['index']
    start_date = event['queryStringParameters']['fromDate']
    end_date = event['queryStringParameters']['toDate']
    granularity = event['queryStringParameters'].get('granularity', 'HOURS')
    granularity_unit = int(event['queryStringParameters'].get('granularityUnit', 1))

    data = fetch_market_cap_data(index, start_date, end_date)

    aggregated_data = aggregate_data(data, granularity, granularity_unit)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Origin": "*",
        },
        'body': json.dumps(aggregated_data)
    }