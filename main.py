import pandas as pd
import asyncio
from time import sleep
from lightweight_charts import Chart
import indicators
import get_data

def get_bar_data(symbol):
    if symbol not in watchlist:
        print(f'No data for "{symbol}"')
        return pd.DataFrame()
    
    df = pd.read_csv(f'{symbol}_daily.csv')

    # Dataframe cleanup and transformation
    
    df = df.drop('Close', axis=1) # Delete the "Close" column
    df = df.rename(columns={'Adj Close': 'Close'}) # Rename the "Adj Close" column to "Close"
    df = df.tail(num_candles)

    # Indicator Data
    sma_data = indicators.sma1(df, sma1_period) #sma1
    sma_data2 = indicators.sma2(df, sma2_period) #sma2

    return df, sma_data, sma_data2

class API:
    def __init__(self):
        self.chart = None  # Changes after each callback.
        self.indicators = []

    async def on_search(self, searched_string):  
        indicators = self.chart.lines() 
        df, indicator1_data, indicator2_data = get_bar_data(searched_string)
        if df.empty:
            return
        self.chart.topbar['corner'].set(searched_string)
        self.chart.set(df)

        # Update the indicator data
        indicators[0].set(indicator1_data, name=f'SMA1 {sma1_period}')
        indicators[1].set(indicator2_data, name=f'SMA2 {sma2_period}')
        
async def main():

    api = API()
    chart = Chart(api=api, topbar=True, searchbox=True, toolbox=True)
    chart.legend(visible=True)

    chart.topbar.textbox('corner', watchlist[0])

    df, indicator1_data, indicator2_data = get_bar_data(watchlist[0])
    
    # added indicators
    indicator1 = chart.create_line()
    indicator2 = chart.create_line()
    indicator1.set(indicator1_data, name=f'SMA1 {sma1_period}') 
    indicator2.set(indicator2_data, name=f'SMA2 {sma2_period}')  
    chart.set(df)

    await chart.show_async(block=True) # Create the chart

# Watchlist Bullish SMA
def find_bullish(watchlist, sma1_period, sma2_period):
    for symbol in watchlist:
        df = pd.read_csv(f'{symbol}_daily.csv')
        sma_data = indicators.sma1(df, sma1_period).tail(1) #sma1 - slow
        sma_data2 = indicators.sma2(df, sma2_period).tail(1) #sma2 - fast

        if sma_data.iloc[0, 0] == sma_data2.iloc[0, 0]: # time match check
            if sma_data2.iloc[0, 1] > sma_data.iloc[0, 1]:
                print(f'{symbol} - is Above by {(sma_data2.iloc[0, 1] - sma_data.iloc[0, 1]).round(2)}')
            else:
                continue

if __name__ == "__main__":

    # parameters
    num_candles = 120 # Number of Candles
    watchlist = ['AAPL', 'TSLA', 'NVDA', 'AVGO', 'AMD', 'BABA'] # Stocks to get data
    sma1_period = 30 # Period for SMA1 - slow
    sma2_period = 15 # Period for SMA2 - fast

    # ------------- Download Data ------------- 
    #get_data.watchlist_download(watchlist, num_candles)
    
    # Finding Bullish stocks from SMA and print
    find_bullish(watchlist, sma1_period, sma2_period)

    asyncio.run(main())


    