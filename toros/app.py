import json
from datetime import datetime
from enum import Enum

import numpy as np
import pandas as pd
import requests


class TorosCoins(Enum):
    BTC1XPOL = "0x86c3dd18baf4370495d9228b58fd959771285c55"
    BTC1XBASE = "0xd2f23773bf5e2d59f6bb925c2232f6e83f3f79e0"
    BTC1XOPT = "0x83d1fa384ec44c2769a3562ede372484f26e141b"
    BTC1XARB = "0x27d8fdb0251b48d8edd1ad7bedf553cf99abe7b0"
    BTC2XBASE = "0x9e0501537723c71250307f5b1a8ee60e167d21c9"
    BTC2XOPT = "0x32ad28356ef70adc3ec051d8aacdeeaa10135296"
    BTC2XARB = "0xe3254397f5d9c0b69917ebb49b49e103367b406f"
    BTC3XPOL = "0xdb88ab5b485b38edbeef866314f9e49d095bce39"
    BTC3XBASE = "0xcaf08bf08d0c87e2c74dd9ebec9c776037bd7e8e"
    BTC3XOPT = "0xb03818de4992388260b62259361778cf98485dfe"
    BTC3XARB = "0xad38255febd566809ae387d5be66ecd287947cb9"
    BTC4XOPT = "0x11b55966527ff030ca9c7b1c548b4be5e7eaee6d"
    BTC4XARB = "0xd49d22f2a2f05b2088fd42503409e430a8a7d827"
    BTCCVRD2XARB = "0x32c99f405069ef47cebc0db9f4fd6e9ede2244b1"

    ETH1XPOL = "0x79d2aefe6a21b26b024d9341a51f6b7897852499"
    ETH1XOPT = "0xcacb5a722a36cff6baeb359e21c098a4acbffdfa"
    ETH1XARB = "0x40d30b13666c55b1f41ee11645b5ea3ea2ca31f8"
    STETH2X = "0xa672e882acbb96486393d43e0efdab5ebebddc1d"
    ETH2XOPT = "0x9573c7b691cdcebbfa9d655181f291799dfb7cf5"
    ETH2XARB = "0x696f6d66c2da2aa4a400a4317eec8da88f7a378c"
    ETH3XPOL = "0x460b60565cb73845d56564384ab84bf84c13e47d"
    STETH3X = "0x15e2f06138aed58ca2a6afb5a1333bbc5f728f80"
    ETH3XOPT = "0x32b1d1bfd4b3b0cb9ff2dcd9dac757aa64d4cb69"
    ETH3XARB = "0xf715724abba480d4d45f4cb52bef5ce5e3513ccc"
    STETH4X = "0xba5f6a0d2ac21a3fec7a6c40facd23407aa84663"
    ETH4XARB = "0xbf4ab4224b2ac26667cd4b8a0e5134d55cb0b293"

    SOL1XARB = "0xda6d2144faec116b53715f76ca4a79925a3bb1fb"
    SOL1XXARB = "0xa6686c9c6bc90f84e3fb77c3d5417fd66bc05697"
    SOL2XOPT = "0x7d3c9c6566375d7ad6e89169ca5c01b5edc15364"
    SOL3XOPT = "0xcc7d6ed524760539311ed0cdb41d0852b4eb77eb"
    SOL2XARB = "0xe9a71f5230a41aa09f4099a41d24450e85462fe1"
    SOL3XARB = "0xcfec7a15726d4b5d183783c9033b921ba3a5090a"

    SUI2XOPT = "0x1bae4efc60269fe66ecec7252825d6a0250a02ee"
    SUI1XXARB = "0xc8f346c8045fa911eac2ffef628e0c5fcdb445bd"
    SUI2XARB = "0x1a9b3a496fe222ba84c53e215a904c555c3157c9"

    DOGE2XOPT = "0x49bdb78f48db6e0ced4d4475b6d2047539df1412"


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

def get_data_df(data, initial_investment):
    df = pd.DataFrame(data)
    df['returns'] = df['price'].pct_change()
    df['cumulative-returns'] = (1 + df['returns']).cumprod()
    df['investment-value'] = initial_investment * df['cumulative-returns']
    df['investment-value'].iloc[0] = initial_investment

    df['indexed'] = df['price'] / df['price'].iloc[0] * 100
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    return df


def get_volatility(df):
    return df['returns'].std()


def get_sharpe_ratio(df, risk_free_rate=0):
    mean_return = df['returns'].mean()

    return (mean_return - risk_free_rate) / get_volatility(df)


def get_sortino_ratio(df, risk_free_rate=0):
    downside_volatility = df[df['returns'] < 0]['returns'].std()
    mean_return = df['returns'].mean()

    return (mean_return - risk_free_rate) / downside_volatility


def get_omega_ratio(df, threshold=0):
    returns = df['returns'].dropna()
    # Calculate the cumulative distribution function (CDF)
    sorted_returns = np.sort(returns)
    cdf = np.arange(1, len(sorted_returns) + 1) / len(sorted_returns)

    # Gains above the threshold
    gains = sorted_returns[sorted_returns > threshold] - threshold
    prob_gains = 1 - cdf[np.searchsorted(sorted_returns, sorted_returns[sorted_returns > threshold]) - 1]

    # Losses below the threshold
    losses = threshold - sorted_returns[sorted_returns <= threshold]
    prob_losses = cdf[np.searchsorted(sorted_returns, sorted_returns[sorted_returns <= threshold]) - 1]

    # Sum of probability-weighted gains
    weighted_gains = np.sum(gains * prob_gains)

    # Sum of probability-weighted losses
    weighted_losses = np.sum(losses * prob_losses)

    # Omega Ratio
    omega = weighted_gains / weighted_losses if weighted_losses != 0 else np.inf
    return omega


def get_simple_omega_ratio(df, threshold=0):
    returns = df['returns'].dropna()
    gains = returns[returns > threshold].sum() - threshold * len(returns[returns > threshold])
    losses = abs(returns[returns <= threshold].sum() - threshold * len(returns[returns <= threshold]))
    omega = gains / losses if losses != 0 else np.inf
    return omega



def lambda_handler(event, context):
    data = get_toros_data(event["queryStringParameters"]["coin"], event["queryStringParameters"]["interval"], event["queryStringParameters"]["fromDate"], event["queryStringParameters"]["toDate"])
    df = get_data_df(data, int(event["queryStringParameters"]["initialInvestment"]))


    volatility = get_volatility(df)
    sharpe_ratio = get_sharpe_ratio(df, int(event["queryStringParameters"]["riskFreeRate"]) / 100)
    sortino_ratio = get_sortino_ratio(df, int(event["queryStringParameters"]["riskFreeRate"]) / 100)
    omega_ratio = get_omega_ratio(df)
    simple_omega_ratio = get_simple_omega_ratio(df)


    df.reset_index(inplace=True)
    df['timestamp'] = df['timestamp'].astype(str)
    df = df.replace({np.nan: None})

    return {
        "statusCode": 200,
        'headers': {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({
            "data": df.to_dict(orient='records'),
            "volatility": volatility if not np.isnan(volatility) and not np.isinf(volatility) else None,
            "sharpe_ratio": sharpe_ratio if not np.isnan(sharpe_ratio) and not np.isinf(sharpe_ratio) else None,
            "sortino_ratio": sortino_ratio if not np.isnan(sortino_ratio) and not np.isinf(sortino_ratio) else None,
            "omega_ratio": omega_ratio if not np.isnan(omega_ratio) and not np.isinf(omega_ratio) else None,
            "simple_omega_ratio": simple_omega_ratio if not np.isnan(simple_omega_ratio) and not np.isinf(simple_omega_ratio) else None
        }),
    }
