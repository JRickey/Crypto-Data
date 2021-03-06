# -*- coding: utf-8 -*-
"""Crypto_Regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fPHl6HIkcUZJ99m3EBDkMpQoYTDoHlbt

**NOT FINANCIAL ADVICE. ANY PARAMETERS OR FINANCIAL ANALYSIS CONTAINED IN THIS NOTEBOOK IS NOT INTENDED TO PROVIDE INFORMATION RELATED TO BUYING OR SELLING CRYPTOCURRENCIES IN ANY WAY. THIS NOTEBOOK IS FOR EDUCATIONAL PURPOSES ONLY. I AM NOT RESPONSIBLE FOR ANY TRADING LOSSES YOU MIGHT INCUR BY NOT FOLLOWING THE INSTRUCTIONS ABOVE**

#Importing modules
"""

import pandas as pd
import numpy as np 

from datetime import datetime as dt

import statsmodels.api as sm
from statsmodels.iolib.summary2 import summary_col

"""#CAPM Regression"""

exchangePairMap = {
    "BTCUSD":"BITSTAMP",
    "ETHUSD":"BITSTAMP",
    "TOTAL":"CRYPTOCAP",
    "SOLUSD":"FTX",
    "BNBUSD":"BINANCE"
}

def pullData(pair, timeframe="1D"):
  baseurl = "https://raw.githubusercontent.com/JRickey/Crypto-Data/main/"
  url = f"{baseurl}{exchangePairMap[pair]}_{pair}_{timeframe}.csv"
  df = pd.read_csv(url)
  df['date'] = pd.to_datetime(df['time'],unit='s')
  df.set_index("date", inplace=True)
  df["returns"] = df.close.pct_change()
  df = df[["returns"]]
  df.dropna(inplace=True)
  df = df.tail(365)
  return df

BTC = pullData("BTCUSD")
ETH = pullData("ETHUSD")
SOL = pullData("SOLUSD")
BNB = pullData("BNBUSD")
MCAP = pullData("TOTAL")

combined = pd.DataFrame(index = BTC.index)
combined["BTC"] = BTC
combined["ETH"] = ETH
combined["SOL"] = SOL
combined["BNB"] = BNB

for token in combined:
  exog = MCAP
  exog = sm.add_constant(exog, prepend=True)
  mod = sm.OLS(combined[token],exog)
  res = mod.fit()
  print(res.summary())

"""#Minimum Variance Portfolio"""

combined = pd.DataFrame(index = BTC.index)
combined["BTC"] = BTC
combined["ETH"] = ETH
combined["SOL"] = SOL
combined["BNB"] = BNB

mean_returns = combined.mean()
cov_matrix = combined.cov()


mvp = []

onesvec = np.array([1,1,1,1]).reshape(4,1)

w = np.linalg.inv(cov_matrix) @ onesvec
w = w/w.sum()

for i in w:
  mvp.append(i[0])

mvp = pd.Series(mvp, index = mean_returns.index)
print(mvp)

"""#Sharpe Ratio Portfolio"""

shPort = np.linalg.inv(cov_matrix) @ mean_returns
shPort = pd.Series(shPort/shPort.sum(),index=mean_returns.index)

print(shPort)

"""#Sortino Ratio Portfolio"""

V = combined[(combined < 0).all(1)].cov()

soPort = np.linalg.inv(V) @ mean_returns
soPort = pd.Series(soPort/soPort.sum(),index=mean_returns.index)

print(soPort)