# import google finance data from quandl
import quandl
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#call a matrix of all the data for Apple and Google stocks
aaplall = quandl.get("WIKI/AAPL", start_date="2015-01-01", end_date="2020-01-01")

tslaall = quandl.get("WIKI/TSLA", start_date="2015-01-01", end_date="2020-01-01")

#create the vector for prices at CLOSE
aapl = aaplall["Close"]
tsla = tslaall["Close"]

#calculate the simple moving average for a short period
short_sma_aapl = aapl.rolling(window=20).mean()
#calculate the simple moving average for a long period
long_sma_aapl = aapl.rolling(window=100).mean()

#sma for tesla as well
short_sma_tsla = tsla.rolling(window=20).mean()
long_sma_tsla = tsla.rolling(window=100).mean()

#Crossover Trading Strategy (using two SMA):
# when the shorter-term MA crosses above the longer-term MA, it is a BUY signal
# when the longer-term MA crosses above the shorter-term MA, it is a SELL signal

#Create Signal for Apple
signals1 = pd.DataFrame(index=aaplall.index)
signals1['signal'] = 0.0
signals1['signal'][20:] = np.where(short_sma_aapl[20:] > long_sma_aapl[20:], 1.0, 0.0)
signals1['positions'] = signals1['signal'].diff()

#Create Signal for Tesla
signals2 = pd.DataFrame(index=tslaall.index)
signals2['signal'] = 0.0
signals2['signal'][20:] = np.where(short_sma_tsla[20:]>long_sma_tsla[20:], 1.0, 0.0)
signals2['positions'] = signals2['signal'].diff()

#create a plot of the data
fig, ax = plt.subplots(figsize=(16,9))

#plot apple data
ax.plot(aapl.index, aapl, label='AAPL')
ax.plot(short_sma_aapl.index, short_sma_aapl, label='20 days SMA')
ax.plot(long_sma_aapl.index, long_sma_aapl, label='100 days SMA')

#plot tesla data
ax.plot(tsla.index, tsla, label='TSLA')
ax.plot(short_sma_tsla.index, short_sma_tsla, label='20 days SMA')
ax.plot(long_sma_tsla.index, long_sma_tsla, label='100 days SMA')

#Plot the Buy Signals
ax.plot(signals1.loc[signals1.positions == 1.0].index,
        short_sma_aapl[signals1.positions == 1.0],
        '^', markersize=15,color='g')
ax.plot(signals2.loc[signals2.positions == 1.0].index,
        short_sma_tsla[signals2.positions == 1.0],
        '^', markersize=15,color='g')

#Plot the Sell Signals
ax.plot(signals1.loc[signals1.positions == -1.0].index,
        short_sma_aapl[signals1.positions == -1.0],
        'v', markersize=15,color='r')
ax.plot(signals2.loc[signals2.positions == -1.0].index,
        short_sma_tsla[signals2.positions == -1.0],
        'v', markersize=15,color='r')

#label the graph
ax.set_xlabel('Date')
ax.set_ylabel('Closing Price ($)')
ax.legend()

#show the graph
plt.show()