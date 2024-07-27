import json
import boto3
from datetime import datetime, timedelta
import numpy as np
import os

dynamodb = boto3.client('dynamodb')

def fetch_data_from_dynamodb(index_name, start_time, end_time):
    print("Table name: ", os.environ["table"])
    print("indexName: ", index_name)
    print("startTime: ", start_time)
    print("endTime: ", end_time)
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
    data = {}
    for item in items:
        timestamp = item['Timestamp']['S']
        if timestamp not in data:
            data[timestamp] = {}
        data[timestamp][item['CoinName']['S']] = {
            'Price': float(item['Price']['N']),
            'MarketCap': float(item['MarketCap']['N']),
            'Liquidity': float(item['Liquidity']['N']),
            'Volume24h': float(item['Volume24h']['N']),
            'Price Change': float(item['PriceChange24h']['N']) if "PriceChange24h" in item else 0
        }
    return data

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
    portfolio_values = []

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

            print(f"Total Capital Gains: ${capital_gains:.2f}")

        portfolio_distribution = new_portfolio_distribution
        portfolio_value = sum(
            portfolio_distribution[token] * data[token]["Price"] / data_list[list(data_list.keys())[0]][token]["Price"]
            for token in data)
        portfolio_values.append(portfolio_value)
        print(f"Portfolio value at hour {hour + 1}: ${portfolio_value:.2f}")
        previous_timestamp = timestamp

    print(f"\nTotal Capital Gains: ${capital_gains:.2f}")
    return portfolio_values, capital_gains

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
    end_date = event["queryStringParameters"]["toDate"]
    initial_investment = float(event["queryStringParameters"]["initialInvestment"])
    risk_free_rate = float(event["queryStringParameters"]["riskFreeRate"]) / 100

    # Adjust start_time and end_time
    end_time = f"{end_date} 23:59:59+00:00"
    start_time = (datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S%z') - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S%z')

    # Ensure timestamps are correctly formatted
    print(f"Start time: {start_time}, End time: {end_time}")  # Debug print

    # Fetch data from DynamoDB
    items = fetch_data_from_dynamodb(index_name, start_time, end_time)
    print(f"Fetched items: {items}")  # Debug print

    if not items:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "No data found for the given index and time range"})
        }

    data_list = parse_dynamodb_data(items)
    print(f"Parsed data: {data_list}")  # Debug print

    # Ensure there is data to process
    if not data_list:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "No valid data to process"})
        }

    # Simulate the investment
    portfolio_values, capital_gains = simulate_investment(data_list, initial_investment)

    # Ensure there are portfolio values to calculate
    if not portfolio_values:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "No portfolio values calculated"})
        }

    # Calculate performance metrics
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
            "final_portfolio_value": portfolio_values[-1],
            "total_capital_gains": capital_gains,
            **performance_metrics
        }),
    }