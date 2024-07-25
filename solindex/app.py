import json
import boto3
from botocore.exceptions import ClientError
import os
import numpy as np
import pandas as pd
from decimal import Decimal


def get_data_df(data, initial_investment):
    for item in data:
        item['price'] = float(item['Price'])
        item.pop('Price')

    df = pd.DataFrame(data)
    df['returns'] = df['price'].pct_change()
    df['cumulative-returns'] = (1 + df['returns']).cumprod()
    df['investment-value'] = initial_investment * df['cumulative-returns']
    df['investment-value'].iloc[0] = initial_investment

    df['indexed'] = df['price'] / df['price'].iloc[0] * 100
    df['timestamp'] = pd.to_datetime(df['Timestamp'])
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

    gains = sorted_returns[sorted_returns > threshold] - threshold
    prob_gains = 1 - cdf[np.searchsorted(sorted_returns, sorted_returns[sorted_returns > threshold]) - 1]

    losses = threshold - sorted_returns[sorted_returns <= threshold]
    prob_losses = cdf[np.searchsorted(sorted_returns, sorted_returns <= threshold) - 1]

    weighted_gains = np.sum(gains * prob_gains)
    weighted_losses = np.sum(losses * prob_losses)

    omega = weighted_gains / weighted_losses if weighted_losses != 0 else np.inf
    return omega


def get_simple_omega_ratio(df, threshold=0):
    returns = df['returns'].dropna()
    gains = returns[returns > threshold].sum() - threshold * len(returns[returns > threshold])
    losses = abs(returns[returns <= threshold].sum() - threshold * len(returns[returns <= threshold]))
    omega = gains / losses if losses != 0 else np.inf
    return omega


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["table"])

    coin_name = event["queryStringParameters"]["coin"]
    from_date = event["queryStringParameters"]["fromDate"]
    to_date = event["queryStringParameters"]["toDate"]
    initial_investment = float(event["queryStringParameters"]["initialInvestment"])
    risk_free_rate = float(event["queryStringParameters"]["riskFreeRate"])

    try:
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('CoinName').eq(coin_name) &
                                  boto3.dynamodb.conditions.Key('Timestamp').between(from_date, to_date)
        )
        items = response.get('Items', [])

        if not items:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    "data": [],
                    "volatility": None,
                    "sharpe_ratio": None,
                    "sortino_ratio": None,
                    "omega_ratio": None,
                    "simple_omega_ratio": None
                }),
                'headers': {
                    'Content-Type': 'application/json',
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "*",
                    "Access-Control-Allow-Origin": "*",
                },
            }

        df = get_data_df(items, initial_investment)

        volatility = get_volatility(df)
        sharpe_ratio = get_sharpe_ratio(df, int(event["queryStringParameters"]["riskFreeRate"]) / 100)
        sortino_ratio = get_sortino_ratio(df, int(event["queryStringParameters"]["riskFreeRate"]) / 100)
        omega_ratio = get_omega_ratio(df)
        simple_omega_ratio = get_simple_omega_ratio(df)

        df.reset_index(inplace=True)
        df['timestamp'] = df['timestamp'].astype(str)
        df = df.replace({np.nan: None})

        for item in df.to_dict(orient='records'):
            item.pop('Timestamp', None)
            item.pop('CoinName', None)

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

    except ClientError as e:
        print(f"Failed to fetch data from DynamoDB: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to fetch data from DynamoDB'),
        }
