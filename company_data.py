import requests
import json
import os

def get_company_info(ticker, CIK, concept):

    url = f"https://data.sec.gov/api/xbrl/companyconcept/{CIK}/us-gaap/{concept}.json"

    headers = {"User-Agent": "MyAppName/1.0 (myemail@example.com)"}

    files = os.listdir(ticker)

    file = os.path.join(ticker, f"{ticker}_{concept}_data.json")

    if f"{ticker}_{concept}_data.json" in files:
        print(f"Cached Data Accessible")
    else:   
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()

            with open(file, 'w') as out_file:
                json.dump(data, out_file, indent=4)

            print(f"Finance Data for {ticker} saved to {file} sucess!!")
        else: 
            print('Error')

def company_data_to_dict(ticker, concept, year):
    
    file = os.path.join(ticker, f"{ticker}_{concept}_data.json")

    with open(file, 'r') as infile:

        data = json.load(infile)

        info_list = data['units']['USD']

        for entry in info_list:
            form = entry.get('form', 'N/A')
            fy = entry.get('fy', 0)
            fp = entry.get('fp', 'N/A')

            if form == '10-Q' and int(fy) == year and len(entry) == 7:
                if fp == 'Q1':
                    Q1 = entry.get('val', 0)
                if fp == 'Q2':
                    Q2 = entry.get('val', 0)
                if fp == 'Q3':
                    Q3 = entry.get('val', 0)

            if form == '10-K' and int(fy) == year and len(entry) == 7:
                Q4 = entry.get('val', 0)

    return {concept : {year : (Q1, Q2, Q3, Q4)}}

def insert_company_data(ticker, cur, conn, data):    

    metric = list(data.keys())[0]

    cur.execute("""
        INSERT OR IGNORE INTO company_metrics 
        (metric) 
        VALUES (?)
        """, 
        (metric,)
    )

    conn.commit()

    cur.execute("SELECT id FROM stock_tickers WHERE stock_ticker = ?", (ticker,))

    ticker_id = cur.fetchone()[0]

    cur.execute("SELECT id FROM company_metrics WHERE metric = ?", (metric,))

    metric_id = cur.fetchone()[0]

    year = list(data[metric].keys())[0]

    values = data[metric][year]

    for i, item in enumerate(values, start = 1):

        cur.execute("""
                INSERT OR IGNORE INTO company_data
                (company_id, metric_id, year, quarter, value) 
                VALUES (?,?,?,?,?)
                """, 
                (ticker_id, metric_id, int(year), i, item)
            )
        
    conn.commit()
