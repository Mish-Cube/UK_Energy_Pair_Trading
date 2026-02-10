import pandas as pd
import plotly.express as px

df = pd.read_csv("data/ukEnergyPrices.csv", index_col=0, parse_dates=True)

print(df.info())
print(df.describe())
print(df.head())

fig = px.line(df, x=df.index, y=['BP.L','SSE.L','CNA.L','NG.L'], title="Big Four Energy Stock Prices")
fig.show()