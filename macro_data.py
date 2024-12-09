import requests
import json
import os

def get_macro_data(macro_indicator):

    url = 'https://api.stlouisfed.org/fred/series/observations'

    params = {
        'series_id': macro_indicator,
        'observation_start': '2000-01-01',
        'observation_end': '2023-12-31',
        'frequency': 'q',
        'api_key': '2259a8645eeca1a53effd291204423f7', 
        'file_type': 'json'
    }

    files = os.listdir('macro_data')

    file = os.path.join('macro_data', f"{macro_indicator}_data.json")

    if f"{macro_indicator}_data.json" in files:
        print(f"Cached Data Accessible")
    else:   
        response = requests.get(url, params = params)
        if response.status_code == 200:
            data = response.json()

            with open(file, 'w') as out_file:
                json.dump(data, out_file, indent=4)

            print(f"Macro Data for {macro_indicator} saved to {file} sucess!!")
        else: 
            print('Error')

def macro_data_to_dict(macro_indicator, year):

    file = os.path.join('macro_data', f"{macro_indicator}_data.json")

    with open(file, 'r') as infile:
        data = json.load(infile)

        for item in data['observations']:

            date_split = item['date'].split('-')

            item_year = int(date_split[0])

            item_month = date_split[1]

            if item_year == year:
                if item_month == '01':
                    Q1 = float(item['value'])
                elif item_month == '04':
                    Q2 = float(item['value'])
                elif item_month == '07':
                    Q3 = float(item['value'])
                elif item_month == '10':
                    Q4 = float(item['value'])
            
    return {macro_indicator : {year : (Q1, Q2, Q3, Q4)}}

def insert_macro_data(cur, conn, data):    

    macro_metric = list(data.keys())[0]

    cur.execute("""
        INSERT OR IGNORE INTO macro_metrics 
        (metric) 
        VALUES (?)
        """, 
        (macro_metric,)
    )

    conn.commit()

    cur.execute("SELECT id FROM macro_metrics WHERE metric = ?", (macro_metric,))

    macro_id = cur.fetchone()[0]

    year = list(data[macro_metric].keys())[0]

    values = data[macro_metric][year]

    for i, item in enumerate(values, start = 1):

        cur.execute("""
                INSERT OR IGNORE INTO macro_data
                (macro_id, year, quarter, value) 
                VALUES (?,?,?,?)
                """, 
                (macro_id, int(year), i, item)
            )
        
    conn.commit()
