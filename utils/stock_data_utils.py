import pandas as pd
import numpy as np
from datetime import datetime
import yfinance as yf
from sklearn.cluster import MeanShift
import plotly.express as px
from sklearn.cluster import Birch

def get_stock_data(stock_name: str, days: int=300, interval: str='d') -> pd.DataFrame:
    """Get stock data from yfinance api.

    Args:
        stock_name (str): Name of the stock whose historical data is needed.
        days (int, optional): Number of past days for which data is needed. Defaults to 300.
        interval (str, optional): Interval between data points. Defaults to 'd'.

    Returns:
        pd.DataFrame: Dataframe containing past data for 
    """
    end = datetime.today()
    begin=end-pd.DateOffset(days)
    st=begin.strftime('%Y-%m-%d') 
    ed=end.strftime('%Y-%m-%d')

    symbol = stock_name + '.NS'
    ticker = yf.Ticker(symbol)
    data_stock = ticker.history(start=st, end=ed, interval=interval) 
    
    return data_stock

def get_dates_for_backtesting(num_periods: int, days: int=200) -> list:
    """Get list of start and end dates for backtesting the buy sell strategy.

    Args:
        num_periods (int): Number of periods for which the strategy needs to be tested.
        days (int, optional): Difference between start and end dates of each period. Defaults to 200.

    Returns:
        list: List of start and end dates for each period.
    """
    dates = []
    end = datetime.today()
    for _ in range(num_periods):
        dates.append(end-pd.DateOffset(days))
        end = end-pd.DateOffset(days)
    return dates


def add_rsi(data_stock: pd.DataFrame) -> pd.DataFrame:
    """Add RSI data to historical stock data.

    Args:
        data_stock (pd.DataFrame): Dataframe containing historical stock data.

    Returns:
        pd.DataFrame: Stock data updated with RSI values.
    """
    data_stock['delta'] = data_stock['Close'].diff()
    data_stock['advance'] = data_stock['delta'][data_stock['delta']>0]
    data_stock['decline'] = -1*data_stock['delta'][-1*data_stock['delta']>0]
    data_stock = data_stock.replace(np.nan, 0)
    data_stock['advance_SMA_14'] = data_stock['advance'].rolling(window=14).mean()
    data_stock['decline_SMA_14'] = data_stock['decline'].rolling(window=14).mean()
    data_stock['rs'] = data_stock['advance_SMA_14']/data_stock['decline_SMA_14']
    data_stock['rsi'] = np.subtract([100]*len(data_stock['rs']),list(100/(1 + (data_stock['rs']))))
    data_stock = data_stock.replace(np.nan, 0)   
    return data_stock

def avg_daily_change(data: pd.DataFrame) -> np.ndarray:
    """Get the average of the stock price.

    Args:
        data (pd.DataFrame): Dataframe containing historical stock data.

    Returns:
        np.ndarray: Numpy array containing average price of stock.
    """
    avg = np.mean((data['High']-data['Low'])/2)
    return avg
        
def get_chart(stock_data: pd.DataFrame) -> None:
    """Get the line chart for closing prices of stock data.

    Args:
        stock_data (pd.DataFrame): Historical stock prices data.
    """
    fig = px.line(stock_data, x=stock_data.index, y="Close")
    fig.show()

def support_resistance(data: pd.DataFrame, period: int=30) -> tuple:
    """Get support resistance values for a stock.

    Args:
        data (pd.DataFrame): Historical stock data.
        period (int, optional): Period of days to consider values for getting support price. Defaults to 30.

    Returns:
        tuple: tuple of two lists containing sorted support and resistance values.
    """
    max_prices_win30 = []
    min_prices_win30 = []
    for i in range((len(data['Close'])-period-1)):
        max_prices_win30 = np.append(max_prices_win30, [max(data['High'][i:period+i])])
        min_prices_win30 = np.append(min_prices_win30, [min(data['Low'][i:period+i])])  
    
    max_prices_win30 = np.reshape(max_prices_win30,(-1,1))
    min_prices_win30 = np.reshape(min_prices_win30,(-1,1))
    
    clustering_max = MeanShift(bandwidth=period).fit(max_prices_win30)
    clustering_min = MeanShift(bandwidth=period).fit(min_prices_win30)
    label_sort_max = {}
    label_sort_min = {}
    labels_max = clustering_max.labels_
    labels_min = clustering_min.labels_
    for i in range(max(labels_max)+1):
        label_sort_max[i] = []
    for i in range(len(labels_max)):
        label_sort_max[labels_max[i]] = np.append(label_sort_max[labels_max[i]], max_prices_win30[i,0]) 
    label_sort_max = {k: v for k, v in label_sort_max.items()} 
    
    for i in range(max(labels_min)+1):
        label_sort_min[i] = []
    for i in range(len(labels_min)):
        label_sort_min[labels_min[i]] = np.append(label_sort_min[labels_min[i]], min_prices_win30[i,0]) 
    label_sort_min = {k: v for k, v in label_sort_min.items()}
    
    return label_sort_max, label_sort_min

def get_cluster_max_prices(data: pd.DataFrame, period: int=5) -> list:
    """Get the max prices after clustering.

    Args:
        data (pd.DataFrame): Historical stock price.
        period (int, optional): Window period for gathering prices. Defaults to 5.

    Returns:
        list: List of max prices after clustering.
    """
    max_prices_win30 = np.asarray([max(data['High'][i:period+i]) for i in range(len(data['Close'])-period-1)])
    max_prices_win30 = np.reshape(max_prices_win30,(-1,1))
    brc = Birch(n_clusters=5)
    brc.fit(max_prices_win30)
    clustering_max = brc.predict(max_prices_win30)

    label_sort_max = {}
    labels_max = clustering_max
    for i in range(max(labels_max)+1):
        label_sort_max[i] = []
    for i in range(len(labels_max)):
        label_sort_max[labels_max[i]] = np.append(label_sort_max[labels_max[i]], max_prices_win30[i,0]) 
    label_sort_max = {k: v for k, v in label_sort_max.items()} 

    c = []
    for key in list(label_sort_max.keys()):
        items = label_sort_max[key]
        unique, frequency = np.unique(items, return_counts=True)
        e = sorted(np.array(unique)[np.array(frequency)>4])
        for price in e:
            c.append([price, list(data.index)[np.argwhere(list(data['High'])==price)[0][0]]])        
    c = np.array(sorted(c))
    clustering = MeanShift(bandwidth=10).fit(c[:,0].reshape(-1,1))
    labels_dmax = clustering.labels_

    label_sort_max = {}
    c_new = []
    labels_max = labels_dmax
    for i in range(max(labels_max)+1):
        label_sort_max[i] = []
    for i in range(len(labels_max)):
        label_sort_max[labels_max[i]] = np.append(label_sort_max[labels_max[i]], c[i,0]) 
    c_new = np.array(sorted([max(v) for k, v in label_sort_max.items()]))
    
    return c_new

def get_cluster_min_prices(data: pd.DataFrame, period: int=5) -> list:
    """Get the min prices after clustering.

    Args:
        data (pd.DataFrame): Historical stock price.
        period (int, optional): Window period for gathering prices. Defaults to 5.

    Returns:
        list: List of min prices after clustering.
    """
    min_prices_win30 = np.asarray([max(data['Low'][i:period+i]) for i in range(len(data['Close'])-period-1)])
    min_prices_win30 = np.reshape(min_prices_win30,(-1,1))
    brc = Birch(n_clusters=5)
    brc.fit(min_prices_win30)
    Birch(n_clusters=5)
    clustering_min = brc.predict(min_prices_win30) 

    label_sort_min = {}
    labels_min = clustering_min
    for i in range(max(labels_min)+1):
        label_sort_min[i] = []
    for i in range(len(labels_min)):
        label_sort_min[labels_min[i]] = np.append(label_sort_min[labels_min[i]], min_prices_win30[i,0]) 
    label_sort_min = {k: v for k, v in label_sort_min.items()}

    d = []
    for key in list(label_sort_min.keys()):
        items = label_sort_min[key]
        unique, frequency = np.unique(items, return_counts=True)
        e = sorted(np.array(unique)[np.array(frequency)>4])
        for price in e:
            d.append([price, list(data.index)[np.argwhere(list(data['Low'])==price)[0][0]]])
    d = np.array(sorted(d))
    clustering = MeanShift(bandwidth=10).fit(d[:,0].reshape(-1,1))
    labels_dmin = clustering.labels_

    label_sort_min = {}
    d_new = []
    labels_min = labels_dmin
    for i in range(max(labels_min)+1):
        label_sort_min[i] = []
    for i in range(len(labels_min)):
        label_sort_min[labels_min[i]] = np.append(label_sort_min[labels_min[i]], d[i,0]) 
    d_new = np.array(sorted([min(v) for k, v in label_sort_min.items()]))
    return d_new
