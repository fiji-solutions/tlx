from enum import Enum
from datetime import datetime

import pandas as pd
import requests


class TlxCoins(Enum):
    ETH1L = "0xda08D59CaAdF87c59D56101670B5e023A0593B34"
    ETH2L = "0x46A0277d53274cAfbb089e9870d2448e4224dAD9"
    ETH3L = "0xC013551A4c84BBcec4f75DBb8a45a444E2E9bbe7"
    ETH4L = "0x330cA3de269282fD456dB203046d500633D68F11"
    ETH5L = "0x0b79C19c4929B2FA2CFb4c8ad7649c03cde00Efa"
    ETH7L = "0xe30371B3F0B34A69ADb876FE786E85f7c43F26CF"

    BTC1L = "0x169d4884be225b322963912Df3641948143FF92B"
    BTC2L = "0xc1422a15de4B7ED22EEedaEA2a4276De542C7a77"
    BTC3L = "0x54cC16d2c91F6fa0a30d4C22868459085A7CE4d9"
    BTC4L = "0xCb9fB365f52BF2e49f7e76b7E8dd3e068171D136"
    BTC5L = "0x8efd20F6313eB0bc61908b3eB95368BE442A149d"
    BTC7L = "0x530C6579D5b56Aa7C22d6aF3121CAdeE5413B48B"

    SOL1L = "0x09C2774DC4658D367162bE0bf8226F14bE4F52e6"
    SOL2L = "0x94cC3a994Af812628Fa50f0a4ABe1E2085618Fb8"
    SOL3L = "0xe4DA85B92aE54ebF736EB51f0E962859454662fa"
    SOL4L = "0xA2D72bEeF65dC3544446B3C710a0E1Fa1778e55d"
    SOL5L = "0xCf81EcA92Fc32F3a1EcFC1c7f5Ab6bCF59795278"

    DOGE2L = "0x803A5fb9EAfD8e34a8744DD9988296Bd453A58Ed"
    DOGE5L = "0x33F26f43a983D0eD9BF183A0b53092a9280D14E8"


class Granularity(Enum):
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"


def get_tlx_data(tlxCoin: str, granularity: str, granularityUnit: int, fromDate: str, toDate: str):
    url = "https://api.tlx.fi/functions/v1/prices/{0}?granularity={1}{2}&from={3}".format(TlxCoins[tlxCoin].value, granularityUnit, Granularity[granularity].value, fromDate)
    response = requests.get(url).json()

    date_to_threshold = datetime.strptime(toDate, "%Y-%m-%d")

    filtered_data = [
        entry for entry in response
        if datetime.fromtimestamp(int(str(int(datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00")).timestamp() * 1000))) / 1000) <= date_to_threshold
    ]

    return filtered_data


def lambda_handler(event, context):
    data = get_tlx_data(
        event["queryStringParameters"]["coin"],
        event["queryStringParameters"]["granularity"],
        event["queryStringParameters"]["granularityUnit"],
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
