import yfinance as yf
import pandas as pd

tickers = ["BP.L", "SSE.L", "CNA.L", "NG.L"] #the stocks we want to track
data = yf.download(tickers, start="2018-01-01", end="2026-01-31", group_by='ticker') #downloading the information for each stock

close = pd.DataFrame({ticker: data[ticker]['Close'] for ticker in tickers}) #within each information, extract the adjusted closing price only, and collate
closeCleaned = close.dropna()

closeCleaned.to_csv("data/ukEnergyPrices.csv")