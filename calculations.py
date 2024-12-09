import pandas as pd

def stock_time_series_calculations(cur, stock_metric):
    
    cur.execute(f"""
        SELECT stock_tickers.stock_ticker, stock_data.month, stock_data.year, stock_data.{stock_metric} 
        FROM stock_data 
        JOIN stock_tickers 
        ON stock_data.ticker_id = stock_tickers.id
        ORDER BY stock_tickers.stock_ticker, stock_data.year, stock_data.month
    """)

    data = cur.fetchall()

    data_dict = {
        'ticker' : [],
        'month' : [],
        'year' : [],
        stock_metric : []
    }

    for ticker, month, year, info in data:
        data_dict['ticker'].append(ticker)
        data_dict['month'].append(month)
        data_dict['year'].append(year)
        data_dict[stock_metric].append(info)

    df = pd.DataFrame(data_dict)

    df['date'] = pd.to_datetime(df[['year', 'month']].assign(day = 1))

    df['quarter'] = df['date'].dt.quarter

    df = df.sort_values(by = ['ticker', 'year', 'quarter'])

    quarterly_data = df.groupby(['ticker', 'year', 'quarter']).agg({stock_metric : 'mean', 'date' : 'first'}).reset_index()

    file_path = f"calculations_text/stock_{stock_metric}_aggregated_by_quarter.csv"

    quarterly_data.to_csv(file_path, sep = ',', index = False)

    return quarterly_data

def stock_finance_calculations(cur, finance_metric):

    cur.execute(f"""
        SELECT stock_tickers.stock_ticker AS ticker, company_metrics.metric AS metric, company_data.year, company_data.quarter, company_data.value
        FROM company_data
        JOIN stock_tickers 
        ON company_data.company_id = stock_tickers.id
        JOIN company_metrics 
        ON company_data.metric_id = company_metrics.id
        WHERE metric = ?
        ORDER BY stock_tickers.stock_ticker, company_data.year, company_data.quarter
    """, 
    (finance_metric,))

    data = cur.fetchall()

    data_dict = {
        'ticker' : [],
        'metric' : [],
        'year' : [],
        'quarter' : [],
        finance_metric : []
    }

    for ticker, metric, year, quarter, info in data:
        data_dict['ticker'].append(ticker)
        data_dict['metric'].append(metric)
        data_dict['year'].append(year)
        data_dict['quarter'].append(quarter)
        data_dict[finance_metric].append(info)

    df = pd.DataFrame(data_dict)

    median_metric = df.groupby('ticker')[finance_metric].median().reset_index()

    file_path = f"calculations_text/median_{finance_metric}_2014_2022.csv"

    median_metric.to_csv(file_path, sep = ',', index = False)

    return median_metric

def macro_data_df(cur, metric_one, metric_two): 

    cur.execute("""
        SELECT macro_metrics.metric, macro_data.year, macro_data.quarter, macro_data.value
        FROM macro_data
        JOIN macro_metrics
        ON macro_data.macro_id = macro_metrics.id
        WHERE macro_metrics.metric = ? OR macro_metrics.metric = ?
    """, (metric_one, metric_two))

    data = cur.fetchall()

    data_dict = {
        'metric' : [],
        'year' : [],
        'quarter' : [],
        'value' : []
    }

    for metric, year, quarter, value in data:
        data_dict['metric'].append(metric)
        data_dict['year'].append(year)
        data_dict['quarter'].append(quarter)
        data_dict['value'].append(value)

    df = pd.DataFrame(data_dict)

    quarter_begin_month = {1 : '01', 2 : '04', 3 : '07', 4 : '10'}

    df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['quarter'].map(quarter_begin_month) + '-01')

    df1 = df[df['metric'] == metric_one].copy()

    df2 = df[df['metric'] == metric_two].copy()

    df1[f"{metric_one}_normalized"] = (df1['value'] - df1['value'].min()) / (df1['value'].max() - df1['value'].min())

    df2[f"{metric_two}_normalized"] = (df2['value'] - df2['value'].min()) / (df2['value'].max() - df2['value'].min())

    df1.drop(['quarter', 'metric', 'year', 'value'], axis = 1, inplace = True)

    df2.drop(['quarter', 'metric', 'year', 'value'], axis = 1, inplace = True)

    merged_df = pd.merge(df1, df2, on = 'date', how = 'inner')

    path = f"calculations_text/{metric_one}_{metric_two}_normalized_2014_2022.csv"

    merged_df.to_csv(path, sep = ',', index = False)

    return merged_df

def stock_finance_pivot(cur):
    
    cur.execute("""
        SELECT stock_tickers.stock_ticker AS ticker, company_metrics.metric AS metric, company_data.year, company_data.quarter, company_data.value
        FROM company_data
        JOIN stock_tickers 
        ON company_data.company_id = stock_tickers.id
        JOIN company_metrics 
        ON company_data.metric_id = company_metrics.id
    """)

    data = cur.fetchall()

    data_dict = {
        'ticker' : [],
        'metric' : [],
        'year' : [],
        'quarter' : [],
        'value' : []
    }

    for ticker, metric, year, quarter, info in data:
        data_dict['ticker'].append(ticker)
        data_dict['metric'].append(metric)
        data_dict['year'].append(year)
        data_dict['quarter'].append(quarter)
        data_dict['value'].append(info)

    df = pd.DataFrame(data_dict)

    df = df[df['metric'] != 'Assets']

    df['value'] = df['value']/1000000000

    # df = df.pivot(index = ['ticker', 'year', 'quarter'], columns = 'metric', values = 'value').reset_index()

    path = f"calculations_text/stock_finances_pivoted.csv"

    df.to_csv(path, sep = ',', index = False)

    return df