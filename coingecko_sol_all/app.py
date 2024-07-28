import json
import os
from decimal import Decimal

import boto3

session = boto3.Session()
dynamodb = session.resource('dynamodb')


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def fetch_all_coins(table_name):
    table = dynamodb.Table(table_name)
    response = table.scan()
    items = response['Items']
    return items


def lambda_handler(event, context):
    # Define the table name
    table_name = os.environ["table4"]

    # Fetch all records from the table
    items = fetch_all_coins(table_name)

    # Order the items by the "order" field
    items_sorted = sorted(items, key=lambda x: x['order'])

    # Return the items
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Origin": "*",
        },
        'body': json.dumps(items_sorted, default=decimal_default)
    }