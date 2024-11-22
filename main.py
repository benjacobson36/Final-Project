import pandas as pd
import requests
import json

def get_stock_data(ticker):
    API_KEY = 'PUKC7MUNAPZTTLD3'

    url = 'https://www.alphavantage.co/query'

    params = {'function' : 'TIME_SERIES_MONTHLY', 'symbol' : ticker, 'apikey' : API_KEY}

    response = requests.get(url, params = params)

    if response.status_code == 200:
        data = response.json()

        file = f"{ticker}_data.json"

        with open(file, 'w') as out_file:
            json.dump(data, out_file, indent=4)

        print(f"Data for {ticker} saved to {file} sucess!!")

    else: 
        print('Error')

def stock_data_to_dict(ticker, start_year):

    with open(f"{ticker}_data.json", 'r') as infile:
        data = json.load(infile)

    out_dict = {}
    for date, info in data['Monthly Time Series'].items():
        year = date.split('-')[0]

        if int(year) < start_year:
            break

        open_price = float(info['1. open'])
        high = float(info['2. high'])
        low = float(info['3. low'])
        close = float(info['4. close'])
        volume = float(info['5. volume'])

        tup = (open_price, high, low, close, volume)

        out_dict[date] = tup

    return out_dict

def main():
    # get_stock_data('AAPL')

    stock_data_to_dict('AAPL', 2023)

if __name__ == "__main__":
    main()
