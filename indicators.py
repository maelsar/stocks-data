import pandas as pd

def sma1(data: pd.DataFrame, period: int):
   def avg(d: pd.DataFrame):
      return d['Close'].mean()

   result = []
   for i in range(period - 1, len(data)):
      val = avg(data.iloc[i - period + 1:i])
      result.append({'time': data.iloc[i]['Date'], f'SMA1 {period}': val})
   return pd.DataFrame(result)

def sma2(data: pd.DataFrame, period: int):
   def avg(d: pd.DataFrame):
      return d['Close'].mean()

   result = []
   for i in range(period - 1, len(data)):
      val = avg(data.iloc[i - period + 1:i])
      result.append({'time': data.iloc[i]['Date'], f'SMA2 {period}': val})
   return pd.DataFrame(result)

'''
Note: This can be refactored to take in X number of arguements and and compute for different SMA
periods in a single function
'''