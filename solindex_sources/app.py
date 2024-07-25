import json
import boto3
from botocore.exceptions import ClientError
import os


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["table2"])

    try:
        response = table.scan()
        items = response.get('Items', [])
        sources = {}

        for item in items:
            source = item['Source']
            coin_name = item['CoinName']
            if source not in sources:
                sources[source] = []
            sources[source].append(coin_name)

        return {
            'statusCode': 200,
            'body': json.dumps(sources),
            'headers': {
                'Content-Type': 'application/json',
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Origin": "*",
            },
        }

    except ClientError as e:
        print(f"Failed to fetch data from DynamoDB: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to fetch data from DynamoDB'),
        }
