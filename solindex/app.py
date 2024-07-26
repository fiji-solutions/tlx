import boto3
import os


def fetch_market_cap_data(index_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["table2"])

    response = table.query(
        IndexName="IndexName-Timestamp-Index",
        KeyConditionExpression=boto3.dynamodb.conditions.Key('IndexName').eq(index_name)
    )

    items = response['Items']
    return items


def lambda_handler(event, context):
    index = event['queryStringParameters']['index']

    data = fetch_market_cap_data(index)

    csv_data = "timestamp,marketcap\n"
    csv_data += "\n".join([f"{item['Timestamp']},{item['MarketCap']}" for item in data])

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/csv'},
        'body': csv_data
    }
