import boto3
import os
import json
from decimal import Decimal
import csv
import io


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


def convert_to_csv(data):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["time", "open", "high", "low", "close", "volume"])  # CSV headers

    for item in data:
        timestamp = item['Timestamp']
        marketcap = decimal_to_float(item['MarketCap'])
        writer.writerow([timestamp, marketcap, marketcap, marketcap, marketcap, 0])  # Using marketcap for OHLC and 0 for volume

    return output.getvalue()


def lambda_handler(event, context):
    index = event['queryStringParameters']['index']

    data = fetch_market_cap_data(index)

    csv_data = convert_to_csv(data)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename=marketcap_data.csv'
        },
        'body': csv_data
    }