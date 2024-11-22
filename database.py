import sqlite3
import os

def set_up_database(db_name):
    """
    Sets up a SQLite database connection and cursor.

    Parameters
    -----------------------
    db_name: str
        The name of the SQLite database.

    Returns
    -----------------------
    Tuple (Cursor, Connection):
        A tuple containing the database cursor and connection objects.
    """
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
                month TEXT,
                year TEXT,
                FOREIGN KEY (ticker_id) REFERENCES stock_tickers (id),
                UNIQUE (ticker_id, month, year)
            )
    """)

    conn.commit()