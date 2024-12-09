import matplotlib.pyplot as plt
from calculations import *
import numpy as np

ticker_colors = {
    'AAPL': '#1f77b4',  # better blue
    'MSFT': '#ff7f0e',  # beter orange
    'AMZN': '#2ca02c',  # better green
    'TSLA': '#d62728'   # better red
}

def stock_time_series_visual(df, agg_metric):

    plt.figure(figsize = (12, 8))

    for ticker in df['ticker'].unique():

        plot_data = df[df['ticker'] == ticker]

        plt.plot(plot_data['date'], plot_data[agg_metric], label = ticker, linewidth = 4, color = ticker_colors[ticker])

    plt.title(f"Stock {agg_metric.capitalize()} Aggregated on Average By Quarter (2014 - 2022)", fontsize = 16, pad = 10, weight = 'bold')

    plt.xlabel('Date', fontsize = 14, labelpad = 10, weight = 'bold')
    
    plt.ylabel(agg_metric.capitalize(), fontsize = 14, labelpad = 14, weight = 'bold')

    plt.xticks(rotation = 45)

    plt.legend(title = 'Ticker')

    plt.xlim(df['date'].min(), df['date'].max())

    plt.savefig('visualization_figures/visual1.png', dpi = 300)

def finance_bar_chart_visual(cur, finance_metrics_dict):
    
    num_metrics = len(finance_metrics_dict)

    figure, axes = plt.subplots(1, num_metrics, figsize = (14, 8), sharey = True)

    for finance_metric, ax in zip(list(finance_metrics_dict.keys()), axes):

        metric_df = stock_finance_calculations(cur, finance_metric)

        colors = []
        for ticker in metric_df['ticker'].unique():
            colors.append(ticker_colors[ticker])

        ax.bar(metric_df['ticker'], metric_df[finance_metric]/1000000000, color = colors)

        ax.set_title(finance_metrics_dict[finance_metric], fontsize = 14, weight = 'bold')

        ax.tick_params(axis = 'y', labelleft = True)

        ax.grid(axis = 'y', linestyle = '--', alpha = 0.5, color = 'black')

        ax.set_axisbelow(True)

    figure.text(0.08, 0.5, 'Values', va = 'center', rotation = 'vertical', fontsize = 18, weight = 'bold')

    figure.text(0.5, 0.04, 'Tickers', ha = 'center', fontsize = 18, weight = 'bold')

    figure.suptitle('Comparison of Median Financial Metrics (in Billions) From 2014 - 2022', fontsize = 20, weight = 'bold')

    plt.savefig('visualization_figures/visual2.png', dpi = 300)

def macro_scatter_visual(df, metric_one, metric_two, macro_labels_dict):

    plt.figure(figsize=(12, 8))

    plt.scatter(df[f"{metric_one}_normalized"], df[f"{metric_two}_normalized"], s = 120, color = '#1f77b4', alpha = 0.8)

    slope, intercept = np.polyfit(df[f"{metric_one}_normalized"], df[f"{metric_two}_normalized"], 1)

    x = np.linspace(df[f"{metric_one}_normalized"].min(), df[f"{metric_one}_normalized"].max(), 100)

    y = (slope * x) + intercept

    plt.plot(x, y, color = '#d62728', linestyle = '--', linewidth = 4, label = 'Fit Line')

    plt.legend()

    plt.xlim(-0.05, 1.05)
    
    plt.ylim(-0.05, 1.05)

    plt.title(f"{macro_labels_dict[metric_one]} by {macro_labels_dict[metric_two]} Normalized", fontsize = 16, pad = 10, weight = 'bold')

    plt.xlabel(macro_labels_dict[metric_one], fontsize = 14, labelpad = 10, weight = 'bold')

    plt.ylabel(macro_labels_dict[metric_two], fontsize = 14, labelpad = 14, weight = 'bold')

    plt.grid(True, linestyle = '--', alpha = 0.6)

    axis = plt.gca()  

    axis.set_axisbelow(True)

    plt.savefig('visualization_figures/visual3.png', dpi = 300)

def stock_finance_box_plots_visual(df, finance_metrics_dict):

    fig, ax = plt.subplots(figsize = (10.5, 8))

    df.boxplot(column = 'value', by = 'metric', grid = False, ax = ax)

    ax.set_title('Distribution of Company Financial Metrics In Billions of US Dollars (2014 - 2022)', fontsize = 16, pad = 10, weight = 'bold')

    ax.set_xlabel('Financial Metrics', fontsize = 14, labelpad = 12, weight = 'bold')

    ax.set_ylabel('Values', fontsize = 14, labelpad = 14, weight = 'bold')

    plt.suptitle('')  

    ax.set_xticklabels([finance_metrics_dict.get(label, label) for label in df['metric'].unique()])

    labels = []
    for label in df['metric'].unique():
        labels.append(finance_metrics_dict.get(label, label))

    ax.set_xticklabels(labels)

    plt.savefig('visualization_figures/visual4.png', dpi = 300)
