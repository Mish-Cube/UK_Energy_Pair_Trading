from statsmodels.tsa.stattools import coint
import itertools
import pandas as pd

df = pd.read_csv("data/ukEnergyPrices.csv", index_col=0, parse_dates=True)

stock_names = df.columns.tolist()
pairs = list(itertools.combinations(stock_names, 2))

for stock1, stock2 in pairs:
    score, pvalue, _ = coint(df[stock1], df[stock2])
    print(f"\n{stock1} vs {stock2}:")
    print(f"Cointegration test statistic: {score:.4f}")
    print(f"p-value: {pvalue:.4f}")

    if pvalue < 0.05:
        print("Cointegrated")
    else:
        print("Not cointegrated")