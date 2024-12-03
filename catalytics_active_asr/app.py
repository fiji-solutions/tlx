import json


def lambda_handler(event, context):
    return {
        "statusCode": 200,
        'headers': {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps([
            # {
            #     "proposalId": "",
            #     "proposalName": "",
            # }
        ]),
    }
