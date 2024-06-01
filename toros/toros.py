import json
import numpy as np
from common.utils import get_tlx_data, get_data_df, get_volatility, get_sharpe_ratio, get_sortino_ratio, get_omega_ratio


def lambda_handler(event, context):
    return {
        "statusCode": 200,
        'headers': {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({
            "data": "hello"
        }),
    }