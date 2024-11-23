import json
from datetime import datetime
import numpy as np
import pandas as pd
import requests


def get_btc_data(from_date: str, to_date: str, asset: str):
    base_asset, leverage = asset.split('-')
    leverage = int(leverage)

    url = f"https://api.catalytics.pro/v1/coingecko/{base_asset}/open"
    response = requests.get(url).json()

    date_to_threshold = datetime.strptime(to_date, "%Y-%m-%d")

    filtered_data = [
        {"timestamp": entry["date"], "price": entry["price"]}
        for entry in response
        if datetime.strptime(entry["date"], "%Y-%m-%d") >= datetime.strptime(from_date, "%Y-%m-%d")
        and datetime.strptime(entry["date"], "%Y-%m-%d") <= date_to_threshold
    ]

    if leverage > 1:
        base_price = filtered_data[0]["price"]
        for entry in filtered_data:
            entry["price"] = base_price + leverage * (entry["price"] - base_price)

    return filtered_data


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
    data = get_btc_data(
        event["queryStringParameters"]["fromDate"],
        event["queryStringParameters"]["toDate"],
        event["queryStringParameters"]["asset"]
    )
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
