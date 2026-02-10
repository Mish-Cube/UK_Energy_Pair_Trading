import pandas as pd
import plotly.graph_objects as go
from statsmodels.api import OLS, add_constant

df = pd.read_csv("data/ukEnergyPrices.csv", index_col=0, parse_dates=True)

stock_a = 'SSE.L'
stock_b = 'NG.L'

X = add_constant(df[stock_b])   # for the OLS structure
model = OLS(df[stock_a], X)
results = model.fit()   # evaluate

hedge_ratio = results.params[stock_b]
intercept = results.params['const']

print(f"Hedge ratio (β): {hedge_ratio:.4f}")
print(f"Intercept: {intercept:.4f}")

spread = df[stock_a] - hedge_ratio * df[stock_b]    # this is our epsilon(t), which we have minimised the variance of

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=spread.index,
    y=spread.values,
    mode='lines',
    name='Spread',
    line=dict(color='blue')
))
fig.add_hline(
    y=spread.mean(),
    line_dash="dash",
    line_color="red",
    annotation_text="Mean"
)
fig.update_layout(
    title=f'Spread: {stock_a} - {hedge_ratio:.2f} × {stock_b}',
    xaxis_title='Date',
    yaxis_title='Spread',
    hovermode='x unified'
)
fig.show()