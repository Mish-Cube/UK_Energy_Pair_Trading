from statsmodels.tsa.stattools import adfuller
import pandas as pd

df = pd.read_csv("data/ukEnergyPrices.csv", index_col=0, parse_dates=True)


def test_stationarity(price_series, name, i):  # define a function because it's nicer
    result = adfuller(price_series)

    print(f"\n{name}:")
    print(f"ADF Statistic: {result[0]:.4f}")
    print(f"p-value: {result[1]:.4f}")
    print(f"Critical values: {result[4]}")

    if result[1] > 0.05:
        print("do not reject I(≥" + str(i+1) + "), possibly I(" + str(i+1) + ")")
    else:
        print("reject I(" + str(i+1) + "), likely I(" + str(i) + ")")

    return result[1]


for stock_name in df:
    test_stationarity(df[stock_name], stock_name, 0)
dfdiff = df.diff().dropna()
for stock_name in dfdiff:
    test_stationarity(dfdiff[stock_name], stock_name, 1)