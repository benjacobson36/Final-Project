import pandas as pd
import requests
import json
import os

def get_stock_data(ticker):
    API_KEY = 'PUKC7MUNAPZTTLD3'

    url = 'https://www.alphavantage.co/query'

    params = {'function' : 'TIME_SERIES_MONTHLY', 'symbol' : ticker, 'apikey' : API_KEY}

    files = os.listdir('.')

    file = f"{ticker}_data.json"

    if file in files:
        print(f"Cached Data Accessible")
    else:   
        response = requests.get(url, params = params)

        if response.status_code == 200:
            data = response.json()

            with open(file, 'w') as out_file:
                json.dump(data, out_file, indent=4)

            print(f"Data for {ticker} saved to {file} sucess!!")
        else: 
            print('Error')

def stock_data_to_dict(ticker, year):

    with open(f"{ticker}_data.json", 'r') as infile:
        data = json.load(infile)

    out_dict = {}
    for date, info in data['Monthly Time Series'].items():
        data_year = date.split('-')[0]

        if int(data_year) != year:
            continue

        open_price = float(info['1. open'])
        high = float(info['2. high'])
        low = float(info['3. low'])
        close = float(info['4. close'])
        volume = float(info['5. volume'])

        tup = (open_price, high, low, close, volume)

        out_dict[date] = tup

    return out_dict

def insert_stock_data(ticker, cur, conn, data):
    
    cur.execute("""
        INSERT OR IGNORE INTO stock_tickers 
        (stock_ticker) 
        VALUES (?)
        """, 
        (ticker,)
    )

    conn.commit()

    cur.execute("SELECT id FROM stock_tickers WHERE stock_ticker = ?", (ticker,))

    ticker_id = cur.fetchone()[0]

    for date, info in data.items():

        month = date.split('-')[1]
        year = date.split('-')[0]

        cur.execute("""
            INSERT OR IGNORE INTO stock_data 
            (ticker_id, open_price, high, low, close, volume, month, year) 
            VALUES (?,?,?,?,?,?,?,?)
            """, 
            (ticker_id, info[0], info[1], info[2], info[3], info[4], month, year)
        )

    conn.commit()





