import boto3
import os
import json
from decimal import Decimal

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

def lambda_handler(event, context):
    index = event['queryStringParameters']['index']
    start_date = event['queryStringParameters']['fromDate']
    end_date = event['queryStringParameters']['toDate']

    data = fetch_market_cap_data(index, start_date, end_date)

    json_data = [
        {
            "timestamp": item['Timestamp'],
            "marketcap": decimal_to_float(item['MarketCap'])
        } for item in data
    ]

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Origin": "*",
        },
        'body': json.dumps(json_data)
    }