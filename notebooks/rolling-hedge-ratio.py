import pandas as pd
import numpy as np
from statsmodels.api import OLS, add_constant
import plotly.graph_objects as go

df = pd.read_csv("data/ukEnergyPrices.csv", index_col=0, parse_dates=True)

stock_a = 'SSE.L'
stock_b = 'NG.L'

min_train_window = 252 # start after 1 year
rebalance_freq = 21  # adjust every month

results_df = pd.DataFrame(index=df.index)
results_df['price_a'] = df[stock_a]
results_df['price_b'] = df[stock_b]
results_df['hedge_ratio'] = np.nan
results_df['spread'] = np.nan

for i in range(min_train_window, len(df), rebalance_freq):  # increments as set above
    train_data = df.iloc[:i]

    X = add_constant(train_data[stock_b])   # find beta up to day i
    model = OLS(train_data[stock_a], X)
    result = model.fit()
    beta = result.params[stock_b]

    end_idx = min(i + rebalance_freq, len(df))  # fill in our results df with hedge and spread data
    results_df.loc[results_df.index[i:end_idx], 'hedge_ratio'] = beta
    results_df.loc[results_df.index[i:end_idx], 'spread'] = (
            df[stock_a].iloc[i:end_idx] - beta * df[stock_b].iloc[i:end_idx]
    ).values

results_df = results_df.dropna()    # just leave the bits where we actually traded

print(f"Walk-forward analysis complete!")
print(f"Trading period: {results_df.index[0]} to {results_df.index[-1]}")
print(f"Hedge ratio ranged from {results_df['hedge_ratio'].min():.4f} to {results_df['hedge_ratio'].max():.4f}")
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=results_df.index,
    y=results_df.hedge_ratio,
    mode='lines',
    name='Spread',
    line=dict(color='blue')
))
fig.show()