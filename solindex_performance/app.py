import json
import boto3
import numpy as np
import os
import pandas as pd

dynamodb = boto3.client('dynamodb')


def fetch_data_from_dynamodb(index_name, start_time, end_time):
    response = dynamodb.query(
        TableName=os.environ["table"],
        IndexName='IndexName-Timestamp-Index',
        KeyConditionExpression='#indexName = :indexName AND #ts BETWEEN :startTime AND :endTime',
        ExpressionAttributeNames={
            '#indexName': 'IndexName',
            '#ts': 'Timestamp'
        },
        ExpressionAttributeValues={
            ':indexName': {'S': index_name},
            ':startTime': {'S': start_time},
            ':endTime': {'S': end_time}
        }
    )
    return response['Items']


def parse_dynamodb_data(items):
    data = []
    for item in items:
        timestamp = item['Timestamp']['S']
        coin_name = item['CoinName']['S']
        data.append({
            'timestamp': timestamp,
            'coin': coin_name,
            'Price': float(item['Price']['N']),
            'Market Cap': float(item['MarketCap']['N']),
            'Liquidity': float(item['Liquidity']['N']),
            'Volume24h': float(item['Volume24h']['N']),
            'Price Change': float(item['PriceChange24h']['N']) if 'PriceChange24h' in item else 0
        })
    return data


def resample_data(data, granularity, granularity_unit):
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    if granularity == 'HOURS':
        df.set_index('timestamp', inplace=True)
        resampled_data = df.groupby('coin').resample(f'{granularity_unit}H').mean().reset_index()
    elif granularity == 'DAYS':
        df.set_index('timestamp', inplace=True)
        resampled_data = df.groupby('coin').resample(f'{granularity_unit}D').mean().reset_index()
    else:
        resampled_data = df

    return resampled_data


# Function to calculate the weighted allocation including price change
def calculate_allocations(data):
    weights = {}
    total_weight = 0
    for token, attributes in data.items():
        weight = (attributes["Price"] +
                  attributes["Market Cap"] +
                  attributes["Liquidity"] +
                  attributes["Volume24h"] +
                  attributes["Price Change"])
        weights[token] = weight
        total_weight += weight
    allocations = {token: (weight / total_weight) * 100 for token, weight in weights.items()}
    return allocations


# Function to simulate investing in the index and calculating performance and transactions
def simulate_investment(data_list, initial_investment):
    portfolio_value = initial_investment
    portfolio_distribution = {}
    capital_gains = 0
    detailed_results = []

    for hour, timestamp in enumerate(sorted(data_list.keys())):
        data = data_list[timestamp]
        allocations = calculate_allocations(data)

        new_portfolio_distribution = {token: (allocation / 100) * portfolio_value for token, allocation in
                                      allocations.items()}

        if hour > 0:
            hourly_gains = 0
            for token, new_value in new_portfolio_distribution.items():
                if token in portfolio_distribution:
                    old_value = portfolio_distribution[token]
                    price_change = data[token]["Price"] / data_list[previous_timestamp][token]["Price"]
                    if new_value < old_value:
                        amount_sold = old_value - new_value
                        gains = amount_sold * (price_change - 1)
                        capital_gains += gains
                        hourly_gains += gains

        portfolio_distribution = new_portfolio_distribution
        portfolio_value = sum(
            portfolio_distribution[token] * data[token]["Price"] / data_list[list(data_list.keys())[0]][token]["Price"]
            for token in data)

        detailed_results.append({
            "timestamp": timestamp,
            "portfolio_value": portfolio_value,
            "capital_gains": capital_gains
        })

        previous_timestamp = timestamp

    return detailed_results


# Additional functions for performance metrics
def calculate_performance_metrics(portfolio_values, risk_free_rate):
    returns = np.diff(portfolio_values) / portfolio_values[:-1]
    volatility = returns.std()
    sharpe_ratio = (returns.mean() - risk_free_rate) / volatility if volatility != 0 else np.nan
    sortino_ratio = (returns.mean() - risk_free_rate) / returns[returns < 0].std() if returns[
                                                                                          returns < 0].std() != 0 else np.nan
    omega_ratio = omega_ratio_calculation(returns)
    simple_omega_ratio = simple_omega_ratio_calculation(returns)

    return {
        "volatility": volatility if not np.isnan(volatility) and not np.isinf(volatility) else None,
        "sharpe_ratio": sharpe_ratio if not np.isnan(sharpe_ratio) and not np.isinf(sharpe_ratio) else None,
        "sortino_ratio": sortino_ratio if not np.isnan(sortino_ratio) and not np.isinf(sortino_ratio) else None,
        "omega_ratio": omega_ratio if not np.isnan(omega_ratio) and not np.isinf(omega_ratio) else None,
        "simple_omega_ratio": simple_omega_ratio if not np.isnan(simple_omega_ratio) and not np.isinf(
            simple_omega_ratio) else None
    }


def omega_ratio_calculation(returns, threshold=0):
    sorted_returns = np.sort(returns)
    cdf = np.arange(1, len(sorted_returns) + 1) / len(sorted_returns)
    gains = sorted_returns[sorted_returns > threshold] - threshold
    prob_gains = 1 - cdf[np.searchsorted(sorted_returns, sorted_returns[sorted_returns > threshold]) - 1]
    losses = threshold - sorted_returns[sorted_returns <= threshold]
    prob_losses = cdf[np.searchsorted(sorted_returns, sorted_returns[sorted_returns <= threshold]) - 1]
    weighted_gains = np.sum(gains * prob_gains)
    weighted_losses = np.sum(losses * prob_losses)
    omega = weighted_gains / weighted_losses if weighted_losses != 0 else np.inf
    return omega


def simple_omega_ratio_calculation(returns, threshold=0):
    gains = returns[returns > threshold].sum() - threshold * len(returns[returns > threshold])
    losses = abs(returns[returns <= threshold].sum() - threshold * len(returns[returns <= threshold]))
    omega = gains / losses if losses != 0 else np.inf
    return omega


def lambda_handler(event, context):
    index_name = event["queryStringParameters"]["index"]
    start_date = event["queryStringParameters"]["fromDate"]
    end_date = event["queryStringParameters"]["toDate"]
    initial_investment = float(event["queryStringParameters"]["initialInvestment"])
    risk_free_rate = float(event["queryStringParameters"]["riskFreeRate"]) / 100
    granularity = event["queryStringParameters"]["granularity"]
    granularity_unit = int(event["queryStringParameters"]["granularityUnit"])

    # Adjust start_time and end_time
    start_time = f"{start_date} 00:00:00+00:00"
    end_time = f"{end_date} 23:59:59+00:00"

    items = fetch_data_from_dynamodb(index_name, start_time, end_time)

    data_list = parse_dynamodb_data(items)

    # Resample data based on granularity and granularity unit
    resampled_data = resample_data(data_list, granularity, granularity_unit)

    # Convert resampled data back to the required format for investment simulation
    data_dict = {}
    for record in resampled_data:
        timestamp = record.pop('timestamp')
        if timestamp not in data_dict:
            data_dict[timestamp] = {}
        data_dict[timestamp][record['coin']] = record

    # Simulate the investment
    detailed_results = simulate_investment(data_dict, initial_investment)

    # Calculate performance metrics
    portfolio_values = [result['portfolio_value'] for result in detailed_results]
    performance_metrics = calculate_performance_metrics(portfolio_values, risk_free_rate)

    return {
        "statusCode": 200,
        'headers': {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({
            "data": detailed_results,
            "final_portfolio_value": portfolio_values[-1],
            "total_capital_gains": detailed_results[-1]['capital_gains'],
            **performance_metrics
        }),
    }