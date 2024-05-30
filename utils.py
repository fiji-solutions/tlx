import numpy as np
import requests
import pandas as pd

from coins_enum import TlxCoins
from granularity_enum import Granularity


def get_tlx_data(tlxCoin: TlxCoins, granularity: Granularity, granularityUnit: int, fromDate: str):
    return requests.get("https://api.tlx.fi/functions/v1/prices/{0}?granularity={1}{2}&from={3}".format(tlxCoin.value, granularityUnit, granularity.value, fromDate)).json()


def get_data_df(data):
    df = pd.DataFrame(data)
    df['returns'] = df['price'].pct_change()
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



