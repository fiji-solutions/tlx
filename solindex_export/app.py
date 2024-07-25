import json
import boto3
from botocore.exceptions import ClientError
import os
from datetime import datetime
import pandas as pd


def get_data_from_dynamodb(coin_name, from_date, to_date):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["table"])

    try:
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('CoinName').eq(coin_name) &
                                  boto3.dynamodb.conditions.Key('Timestamp').between(from_date, to_date)
        )
        items = response.get('Items', [])
        return items

    except ClientError as e:
        print(f"Failed to fetch data from DynamoDB: {e.response['Error']['Message']}")
        return []


def lambda_handler(event, context):
    coin_name = event["queryStringParameters"]["coin"]
    from_date = event["queryStringParameters"]["fromDate"]
    to_date = event["queryStringParameters"]["toDate"]

    data = get_data_from_dynamodb(coin_name, from_date, to_date)
    if not data:
        return {
            "statusCode": 404,
            "body": json.dumps('No data found for the given criteria'),
            'headers': {
                'Content-Type': 'application/json',
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Origin": "*",
            },
        }

    df = pd.DataFrame(data)
    csv_data = df.to_csv(index=False, header=False)

    return {
        "statusCode": 200,
        'headers': {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename="data.csv"',
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Origin": "*",
        },
        "body": csv_data
    }
