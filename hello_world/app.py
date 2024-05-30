import json
from enum import Enum

import numpy as np
import pandas as pd
import requests


class TlxCoins(Enum):
    ETH1L = "0xda08D59CaAdF87c59D56101670B5e023A0593B34"
    ETH2L = "0x46A0277d53274cAfbb089e9870d2448e4224dAD9"
    ETH3L = "0xC013551A4c84BBcec4f75DBb8a45a444E2E9bbe7"
    ETH4L = "0x330cA3de269282fD456dB203046d500633D68F11"
    ETH5L = "0x0b79C19c4929B2FA2CFb4c8ad7649c03cde00Efa"

    BTC1L = "0x169d4884be225b322963912Df3641948143FF92B"
    BTC2L = "0xc1422a15de4B7ED22EEedaEA2a4276De542C7a77"
    BTC3L = "0x54cC16d2c91F6fa0a30d4C22868459085A7CE4d9"
    BTC4L = "0xCb9fB365f52BF2e49f7e76b7E8dd3e068171D136"
    BTC5L = "0x8efd20F6313eB0bc61908b3eB95368BE442A149d"

    SOL1L = "0x09C2774DC4658D367162bE0bf8226F14bE4F52e6"
    SOL2L = "0x94cC3a994Af812628Fa50f0a4ABe1E2085618Fb8"
    SOL3L = "0xe4DA85B92aE54ebF736EB51f0E962859454662fa"
    SOL4L = "0xA2D72bEeF65dC3544446B3C710a0E1Fa1778e55d"
    SOL5L = "0xCf81EcA92Fc32F3a1EcFC1c7f5Ab6bCF59795278"


class Granularity(Enum):
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"


def get_tlx_data(tlxCoin: str, granularity: str, granularityUnit: int, fromDate: str):
    return requests.get("https://api.tlx.fi/functions/v1/prices/{0}?granularity={1}{2}&from={3}".format(TlxCoins[tlxCoin].value, granularityUnit, Granularity[granularity].value, fromDate)).json()


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
    data = get_tlx_data(event["queryStringParameters"]["coin"], event["queryStringParameters"]["granularity"], event["queryStringParameters"]["granularityUnit"], event["queryStringParameters"]["fromDate"])
    df = get_data_df(data, int(event["queryStringParameters"]["initial_investment"]))


    volatility = get_volatility(df)
    sharpe_ratio = get_sharpe_ratio(df)
    sortino_ratio = get_sortino_ratio(df)
    omega_ratio = get_omega_ratio(df)


    df.reset_index(inplace=True)
    df['timestamp'] = df['timestamp'].astype(str)
    df = df.replace({np.nan: None})

    return {
        "statusCode": 200,
        "body": json.dumps({
            "data": df.to_dict(orient='records'),
            "volatility": volatility,
            "sharpe_ratio": sharpe_ratio,
            "sortino_ratio": sortino_ratio,
            "omega_ratio": omega_ratio
        }),
    }
