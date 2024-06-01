import json
from datetime import datetime
from enum import Enum

import numpy as np
import pandas as pd
import requests


class TorosCoins(Enum):
    ETH = "0xf715724abba480d4d45f4cb52bef5ce5e3513ccc"


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
    returns = df['returns']
    # Calculate the cumulative distribution function (CDF)
    sorted_returns = np.sort(returns)
    cdf = np.arange(1, len(sorted_returns) + 1) / len(sorted_returns)

    # Gains above the threshold
    gains = sorted_returns[sorted_returns > threshold] - threshold
    prob_gains = 1 - cdf[sorted_returns > threshold]

    # Losses below the threshold
    losses = threshold - sorted_returns[sorted_returns <= threshold]
    prob_losses = cdf[sorted_returns <= threshold]

    # Sum of probability-weighted gains
    weighted_gains = np.sum(gains * prob_gains)

    # Sum of probability-weighted losses
    weighted_losses = np.sum(losses * prob_losses)

    # Omega Ratio
    omega = weighted_gains / weighted_losses if weighted_losses != 0 else np.inf
    return omega


def lambda_handler(event, context):
    data = get_toros_data(event["queryStringParameters"]["coin"], event["queryStringParameters"]["interval"], event["queryStringParameters"]["fromDate"])
    df = get_data_df(data, int(event["queryStringParameters"]["initialInvestment"]))


    volatility = get_volatility(df)
    sharpe_ratio = get_sharpe_ratio(df, int(event["queryStringParameters"]["riskFreeRate"]) / 100)
    sortino_ratio = get_sortino_ratio(df, int(event["queryStringParameters"]["riskFreeRate"]) / 100)
    omega_ratio = get_omega_ratio(df)


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
            "omega_ratio": omega_ratio if not np.isnan(omega_ratio) and not np.isinf(omega_ratio) else None
        }),
    }
