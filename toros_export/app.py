from datetime import datetime
from enum import Enum

import pandas as pd
import requests


class TorosCoins(Enum):
    BTC3XPOL = "0xdb88ab5b485b38edbeef866314f9e49d095bce39"
    BTC2XOPT = "0x32ad28356ef70adc3ec051d8aacdeeaa10135296"
    BTC3XOPT = "0xb03818de4992388260b62259361778cf98485dfe"
    BTC3XARB = "0xad38255febd566809ae387d5be66ecd287947cb9"

    ETH3XPOL = "0x460b60565cb73845d56564384ab84bf84c13e47d"
    ETH2XOPT = "0x9573c7b691cdcebbfa9d655181f291799dfb7cf5"
    ETH3XOPT = "0x32b1d1bfd4b3b0cb9ff2dcd9dac757aa64d4cb69"
    ETH3XARB = "0xf715724abba480d4d45f4cb52bef5ce5e3513ccc"


class Intervals(Enum):
    h = "1h"
    hhhh = "4h"
    d = "1d"
    w = "1w"


def get_toros_data(torosCoin: str, interval: int, fromDate: str):
    url = "https://api-v2.dhedge.org/graphql"
    data = {
      "query": "query GetTokenPriceCandles($address: String!, $period: String!, $interval: String) {\n  tokenPriceCandles(address: $address, period: $period, interval: $interval) {\n    timestamp\n    open\n    close\n    max\n    min\n  }\n}\n",
      "variables": {
        "address": TorosCoins[torosCoin].value,
        "period": "1y",
        "interval": interval
      },
      "operationName": "GetTokenPriceCandles"
    }
    response = requests.post(url, json=data).json()

    date_threshold = datetime.strptime(fromDate, "%Y-%m-%d")

    filtered_candles = [
        candle for candle in response["data"]["tokenPriceCandles"]
        if datetime.fromtimestamp(int(candle["timestamp"]) / 1000) >= date_threshold
    ]

    response["data"]["tokenPriceCandles"] = filtered_candles

    return [
        {
            "timestamp": datetime.fromtimestamp(int(candle["timestamp"]) / 1000).isoformat() + "Z",
            "price": float(candle["close"]) / 10**18
        }
        for candle in filtered_candles
    ]


def lambda_handler(event, context):
    data = get_toros_data(event["queryStringParameters"]["coin"], event["queryStringParameters"]["interval"], event["queryStringParameters"]["fromDate"])
    df = pd.DataFrame(data)
    print(df)

    # Convert DataFrame to CSV without a header row
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
