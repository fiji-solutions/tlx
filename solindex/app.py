import boto3
import os
import json
from decimal import Decimal


def fetch_market_cap_data(index_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["table2"])

    response = table.query(
        IndexName="IndexName-Timestamp-Index",
        KeyConditionExpression=boto3.dynamodb.conditions.Key('IndexName').eq(index_name)
    )

    items = response['Items']
    return items


def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def lambda_handler(event, context):
    index = event['queryStringParameters']['index']

    data = fetch_market_cap_data(index)

    json_data = [
        {
            "timestamp": item['Timestamp'],
            "marketcap": decimal_to_float(item['MarketCap'])
        } for item in data
    ]

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(json_data)
    }