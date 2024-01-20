import pandas as pd
import numpy as np

#I will load my dataset which was given by company
data=pd.read_excel('NIFTY 50.csv')
data.columns =data.columns.str.strip()

print(data.shape)

# 1.Daily Returns = (current close / previous close) - 1 

data =data.sort_values(by='Date')
data

data['Daily Returns'] = (data['Close'] / data['Close'].shift(1)) - 1
data.at[0, 'Daily Returns'] = 0


# 2. Daily Volatility = Standard Deviation (Daily Returns)

daily_volatility = data['Daily Returns'].std()
daily_volatility


#  3. Annualized Volatility = Daily Volatility * Square Root (length of data)

data_length = len(data)
annualized_volatility = daily_volatility * np.sqrt(data_length)
annualized_volatility


#  FINAL ANSWER

print(data[['Date', 'Close', 'Daily Returns']])
print(f'Daily Volatility: {daily_volatility:.6f}')
print(f'Annualized Volatility: {annualized_volatility:.6f}')
