import pandas as pd
from datetime import datetime, timedelta
import os
import time

# compute back date - for data management
def compute_back_date(num_candles):
    # Get the current date as period1
    period1 = datetime.now()
    # pulls data from back period with adjustments to consider market holidays and etc.
    # https://www.aarp.org/money/investing/info-2023/stock-market-holidays.html
    num_candles_adjusted = num_candles + 12
    # Subtract days while skipping weekends
    while num_candles_adjusted > 0:
        period1 -= timedelta(days=1)
        if period1.weekday() < 5:  # Weekday (Monday to Friday)
            num_candles_adjusted -= 1

    # Return the computed back date
    return int(period1.timestamp())


def download_stock_data(symbol, num_candles):
    # Get current date as period2
    period2 = int(datetime.now().timestamp())

    # Construct the URL with the symbol, period1, and period2
    # period1 is end date (back)
    # period2 is start date (now)
    url = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={compute_back_date(num_candles)}&period2={period2}&interval=1d&events=history&includeAdjustedClose=true"

    # Read the CSV data from the URL into a DataFrame
    df = pd.read_csv(url)

    # Define the CSV file name using the symbol and "_daily"
    csv_name = f"{symbol}_daily.csv"

    # Save the DataFrame to a CSV file
    df.to_csv(csv_name, index=False, mode='w')

    # Wait until the file exists in the directory
    while not os.path.exists(csv_name):
        time.sleep(1)  # delay before checking again

def watchlist_download(watchlist, num_candles):
    for symbol in watchlist:
        try:
            data = download_stock_data(symbol, num_candles)
            print(f"Data downloaded successfully for {symbol}")
        except Exception as e:
            print(f"Error occurred while downloading data for {symbol}: {e}")
            continue


# # Manual Testing
# if __name__ == "__main__":
#     num_candles = 60 # Number of Candles
#     watchlist = ['AAPL', 'TSLA', 'NVDA', 'AVGO', 'AMD', 'BABA'] # Stocks to get data
#     watchlist_download(watchlist, num_candles)
    
