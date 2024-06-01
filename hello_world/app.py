import json
import numpy as np
from common.utils import get_tlx_data, get_data_df, get_volatility, get_sharpe_ratio, get_sortino_ratio, get_omega_ratio


def lambda_handler(event, context):
    data = get_tlx_data(event["queryStringParameters"]["coin"], event["queryStringParameters"]["granularity"], event["queryStringParameters"]["granularityUnit"], event["queryStringParameters"]["fromDate"])
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
