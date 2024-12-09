from stock_data import *
from database import *
from company_data import *
from macro_data import *

def main():

    cur, conn = set_up_database('finance.db')

    create_stock_table(cur, conn) # 12 * 9 * 4 = 432

    create_company_table(cur, conn) # 4 * 9 * 5 * 4 = 720

    create_macro_table(cur, conn) # 4 * 9 * 4 = 144

    companies_dict = {
        'TSLA' : 'CIK0001318605',
        'AAPL' : 'CIK0000320193',
        'AMZN' : 'CIK0001018724',
        'MSFT' : 'CIK0000789019'
    }

    finance_metrics = [
        "AccountsPayableCurrent",
        "AccountsReceivableNetCurrent",
        "CashAndCashEquivalentsAtCarryingValue",
        "InventoryNet",
        "Assets"
    ]

    macro_metrics = ['GDP', 'FEDFUNDS', 'CPIAUCSL', 'UNRATE']

    years = list(range(2014, 2023))

    cur.execute("SELECT COUNT(*) FROM stock_data")
    stock_data_count = cur.fetchone()[0]
    ticker_index = stock_data_count // (len(years) * 12)

    cur.execute("SELECT COUNT(*) FROM company_data")
    company_data_count = cur.fetchone()[0]
    finance_metric_index = company_data_count // (len(years) * 12)

    cur.execute("SELECT COUNT(*) FROM macro_data")
    macro_data_count = cur.fetchone()[0]
    macro_index = macro_data_count // (len(years) * 4)

    cur.execute("SELECT ticker_id, year FROM stock_data ORDER BY ticker_id DESC, year DESC LIMIT 1")
    data_check = cur.fetchone()

    if stock_data_count <= 100 and company_data_count <= 100 or macro_data_count <= 100:

        if data_check:
            stock_ticker, year_insert = data_check

        else:
            stock_ticker, year_insert = None, None

        if stock_ticker and year_insert:
            if year_insert == max(years):
                year_insert = min(years)
                stock_ticker = list(companies_dict.items())[ticker_index][0]
                finance_metric = finance_metrics[finance_metric_index]
                macro_data = macro_metrics[macro_index]
            else:
                year_insert += 1
                stock_ticker = list(companies_dict.items())[ticker_index][0]
                finance_metric = finance_metrics[finance_metric_index]
                macro_data = macro_metrics[macro_index]
        else:
            year_insert = min(years)
            stock_ticker = list(companies_dict.items())[ticker_index][0]
            finance_metric = finance_metrics[finance_metric_index]
            macro_data = macro_metrics[macro_index]
        
        get_stock_data(stock_ticker)
        
        stock_data = stock_data_to_dict(stock_ticker, year_insert)

        insert_stock_data(stock_ticker, cur, conn, stock_data)

        get_company_info(stock_ticker, companies_dict[stock_ticker], finance_metric)
                
        company_data = company_data_to_dict(stock_ticker, finance_metric, year_insert)

        insert_company_data(stock_ticker, cur, conn, company_data)

        get_macro_data(macro_data)

        macro_data = macro_data_to_dict(macro_data, year_insert)

        insert_macro_data(cur, conn, macro_data)

    else:

        for stock in list(companies_dict.keys()):

            get_stock_data(stock)

            for year in years:

                stock_data = stock_data_to_dict(stock, year)

                insert_stock_data(stock, cur, conn, stock_data)

        for company, cik in companies_dict.items():

            for metric in finance_metrics:

                get_company_info(company, cik, metric)
                
                for year in years:

                    company_data = company_data_to_dict(company, metric, year)

                    insert_company_data(company, cur, conn, company_data)

        for metric in macro_metrics:

            get_macro_data(metric)

            for year in years:

                macro_data = macro_data_to_dict(metric, year)

                insert_macro_data(cur, conn, macro_data)

if __name__ == "__main__":
    main()

# sqlite_web finance.db