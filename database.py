import sqlite3
import os

def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn

def create_stock_table(cur, conn):
    cur.execute("""
            CREATE TABLE IF NOT EXISTS stock_tickers (
                id INTEGER PRIMARY KEY,
                stock_ticker TEXT UNIQUE
            )
    """)
                
    cur.execute("""
            CREATE TABLE IF NOT EXISTS stock_data (
                id INTEGER PRIMARY KEY,
                ticker_id INTEGER,
                open_price REAL, 
                high REAL,
                low REAL, 
                close REAL,
                volume REAL,
                month INTEGER,
                year INTEGER,
                FOREIGN KEY (ticker_id) REFERENCES stock_tickers (id),
                UNIQUE (ticker_id, month, year)
            )
    """)

    conn.commit()

def create_company_table(cur, conn):
    cur.execute("""
            CREATE TABLE IF NOT EXISTS company_metrics (
                id INTEGER PRIMARY KEY,
                metric TEXT UNIQUE
            )
    """)

    cur.execute("""
            CREATE TABLE IF NOT EXISTS company_data (
                id INTEGER PRIMARY KEY,
                company_id INTEGER,
                metric_id INTEGER,
                year INTEGER,
                quarter INTEGER,
                value FLOAT,
                FOREIGN KEY (company_id) REFERENCES stock_tickers (id),
                FOREIGN KEY (metric_id) REFERENCES company_metrics (id),
                UNIQUE (company_id, metric_id, year, quarter, value)
            )
    """)

    conn.commit()

def create_macro_table(cur, conn):
    cur.execute("""
            CREATE TABLE IF NOT EXISTS macro_metrics (
                id INTEGER PRIMARY KEY,
                metric TEXT UNIQUE
            )
    """)

    cur.execute("""
            CREATE TABLE IF NOT EXISTS macro_data (
                id INTEGER PRIMARY KEY,
                macro_id INTEGER,
                year INTEGER,
                quarter INTEGER,
                value FLOAT,
                FOREIGN KEY (macro_id) REFERENCES macro_metrics (id),
                UNIQUE (macro_id, year, quarter, value)
            )
    """)

    conn.commit()