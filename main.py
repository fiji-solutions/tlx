from coins_enum import TlxCoins
from granularity_enum import Granularity
from utils import get_tlx_data, get_data_df, get_volatility, get_sharpe_ratio, get_sortino_ratio, \
    get_omega_ratio

data = get_tlx_data(TlxCoins.BTC1L, Granularity.DAYS, 1, "2024-01-01")
df = get_data_df(data, int("1000"))

print(df.to_dict(orient='records'))
print(get_volatility(df))
print(get_sharpe_ratio(df))
print(get_sortino_ratio(df))
print(get_omega_ratio(df))
