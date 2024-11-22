from stock_data import *
from database import *

def main():
    cur, conn = set_up_database('finance.db')

    create_stock_table(cur, conn)

    stocks = ['AAPL', 'TSLA', 'AMZN', 'MSFT']

    years = list(range(2011, 2023))

    for stock in stocks:
        get_stock_data(stock)
        for year in years:

            data = stock_data_to_dict(stock, year)

            insert_stock_data(stock, cur, conn, data)


if __name__ == "__main__":
    main()

# sqlite_web finance.db