from datetime import datetime
from enum import Enum

import pandas as pd
import requests


class TorosCoins(Enum):
    BTC3XPOL = "0xdb88ab5b485b38edbeef866314f9e49d095bce39"
    BTC2XOPT = "0x32ad28356ef70adc3ec051d8aacdeeaa10135296"
    BTC3XOPT = "0xb03818de4992388260b62259361778cf98485dfe"
    BTC4XOPT = "0x11b55966527ff030ca9c7b1c548b4be5e7eaee6d"
    BTC2XARB = "0xe3254397f5d9c0b69917ebb49b49e103367b406f"
    BTC3XARB = "0xad38255febd566809ae387d5be66ecd287947cb9"

    ETH3XPOL = "0x460b60565cb73845d56564384ab84bf84c13e47d"
    ETH2XOPT = "0x9573c7b691cdcebbfa9d655181f291799dfb7cf5"
    ETH3XOPT = "0x32b1d1bfd4b3b0cb9ff2dcd9dac757aa64d4cb69"
    ETH2XARB = "0x696f6d66c2da2aa4a400a4317eec8da88f7a378c"
    ETH3XARB = "0xf715724abba480d4d45f4cb52bef5ce5e3513ccc"

    SOL2XOPT = "0x7d3c9c6566375d7ad6e89169ca5c01b5edc15364"
    SOL3XOPT = "0xcc7d6ed524760539311ed0cdb41d0852b4eb77eb"

    STETH2X = "0xa672e882acbb96486393d43e0efdab5ebebddc1d"
    STETH3X = "0x15e2f06138aed58ca2a6afb5a1333bbc5f728f80"
    STETH4X = "0xba5f6a0d2ac21a3fec7a6c40facd23407aa84663"


class Intervals(Enum):
    h = "1h"
    hhhh = "4h"
    d = "1d"
    w = "1w"


def get_toros_data(torosCoin: str, interval: int, fromDate: str, toDate: str):
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

    date_from_threshold = datetime.strptime(fromDate, "%Y-%m-%d")
    date_to_threshold = datetime.strptime(toDate, "%Y-%m-%d")

    filtered_candles = [
        candle for candle in response["data"]["tokenPriceCandles"]
        if date_from_threshold <= datetime.fromtimestamp(int(candle["timestamp"]) / 1000) <= date_to_threshold
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
    data = get_toros_data(
        event["queryStringParameters"]["coin"],
        event["queryStringParameters"]["interval"],
        event["queryStringParameters"]["fromDate"],
        event["queryStringParameters"]["toDate"]
    )
    df = pd.DataFrame(data)

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
