from database import *
from calculations import *
from visualization_code import *

def main():

    cur, conn = set_up_database('finance.db')

    stock_data = stock_time_series_calculations(cur, 'close')

    stock_time_series_visual(stock_data, 'close')

    finance_metrics_visuals_dict = {
        "AccountsPayableCurrent" : 'Accounts Payable',
        "AccountsReceivableNetCurrent" : 'Accounts Receivable',
        "CashAndCashEquivalentsAtCarryingValue" : 'Cash',
        "InventoryNet" : 'Inventory'
    }

    finance_bar_chart_visual(cur, finance_metrics_visuals_dict)

    macro_metrics_dict = {
        'GDP': 'Gross Domestic Product',
        'FEDFUNDS': 'Federal Funds Rate',
        'CPIAUCSL': 'Consumer Price Index',
        'UNRATE': 'Unemployment Rate'
    }

    macro_data = macro_data_df(cur, 'GDP', 'CPIAUCSL')

    macro_scatter_visual(macro_data, 'GDP', 'CPIAUCSL', macro_metrics_dict)

    melted_finance_df = stock_finance_pivot(cur)

    stock_finance_box_plots_visual(melted_finance_df, finance_metrics_visuals_dict)

if __name__ == "__main__":
    main()