import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objs as go


def plot_support_resistance(label_sort_max: list, 
                            label_sort_min: list, 
                            data_stock: pd.DataFrame, 
                            company: str='Company') -> None:
    """Plot support resistance data for a company.

    Args:
        label_sort_max (list): Maximum values of stock price sorted from high to low.
        label_sort_min (list): Minimum values of stock price sorted from high to low.
        data_stock (pd.DataFrame): Stock data.
        company (str, optional): name of the company to which the stock belongs. Defaults to 'Company'.
    """
    low_time = data_stock.index
    low_px = label_sort_min[0]

    high_time = data_stock.index
    high_px = label_sort_max[1]

    low_inner_time = data_stock.index
    low_inner_px = label_sort_min[1]

    high_inner_time = data_stock.index
    high_inner_px = label_sort_max[0]

    layout = get_layout(title=company)

    data=[go.Candlestick(x=data_stock.index,
                    open=data_stock['Open'],
                    high=data_stock['High'],
                    low=data_stock['Low'],
                    close=data_stock['Close'],
                    name='candlestick'), 
           go.Scatter(x=data_stock.index, 
                      y=[low_px for x in range(len(low_time))],
                      line=dict(color='firebrick', width=4),
                      name='Closest Support'),
           go.Scatter(x=data_stock.index, 
                      y=[high_px for x in range(len(high_time))],
                      line=dict(color='royalblue', width=4),
                      name='Closest Resistance'),
           go.Scatter(x=data_stock.index, 
                      y=[high_inner_px for x in range(len(high_inner_time))],
                      line=dict(color='royalblue', width=2),
                      name='Lower Resistance'),
           go.Scatter(x=data_stock.index, 
                      y=[low_inner_px for x in range(len(low_inner_time))],
                      line=dict(color='firebrick', width=2),
                      name='Upper Support')]
    figSignal = go.Figure(data=data, layout=layout)
    figSignal.show()
    return None

def get_layout(title="Company Name") -> dict:
    """Get layout of a plot.

    Args:
        title (str, optional): Title of the plot. Defaults to "Company Name".

    Returns:
        dict: Layout dict of the plotly figure.
    """
    layout = dict(
                title=title,
                xaxis=go.layout.XAxis(title=go.layout.xaxis.Title( text="Time")),
                yaxis=go.layout.YAxis(title=go.layout.yaxis.Title( text="Price INR")),
                width=1000,
                height=800,
                xaxis_rangeslider_visible=False
        )
    return layout

def get_data(data_stock: pd.DataFrame) -> list:
    """Get data of as a candlestick figure.

    Args:
        data_stock (pd.DataFrame): Stock data as a pandas dataframe.

    Returns:
        list: List containing candlestick figure.
    """
    data=[go.Candlestick(x=data_stock.index,
                    open=data_stock['Open'],
                    high=data_stock['High'],
                    low=data_stock['Low'],
                    close=data_stock['Close'],
                    name='candlestick')]
    return data

def images_for_stocks_to_buy(close_last: float, 
                            delta: float, 
                            cluster_min_prices: list, 
                            cluster_max_prices: list, 
                            data_stock: pd.DataFrame, 
                            company: str,
                            data: list, layout: dict, end: str):
    """Generate images for stocks which can be bought.

    Args:
        close_last (float): Last closing price of the stock.
        delta (float):Delta window for considering the min/max price.
        cluster_min_prices (list): List of min prices after clustering.
        cluster_max_prices (list): List of max prices after clustering.
        data_stock (pd.DataFrame): Dataframe containing stock data.
        company (str): Name of the company.
        data (list): List containing plotly figures.
        layout (dict): Layout od the plotly figure.
        end (str): End date of the data.
    """
    if cluster_min_prices[0]>(close_last-delta) and cluster_min_prices[0]<(close_last+delta):
        fig = go.Figure(data=data, layout=layout)
        figSignal = make_subplots(rows=2, cols=1, figure=fig)
        for px in cluster_max_prices[-2:]:
            figSignal.add_trace(go.Scatter(x=data_stock.index,
                                y=[px for _ in range(len(data_stock.index))],
                                line=dict(color='firebrick', width=4)),row=1, col=1)

        for px in cluster_min_prices[:2]:
            figSignal.add_trace(go.Scatter(x=data_stock.index,
                                y=[px for _ in range(len(data_stock.index))],
                                line=dict(color='royalblue', width=4)),row=1, col=1)

        figSignal.add_trace(go.Scatter(x=data_stock.index,
                                y=data_stock['rsi'],
                                line=dict(color='orange', width=4)),row=2, col=1)


        figSignal.write_image("Image_today/{}/BUY_{}_{}.png".format(company, end, close_last), engine="kaleido")

def images_for_stocks_to_sell(close_last: float, 
                            delta: float, 
                            cluster_min_prices: list, 
                            cluster_max_prices: list, 
                            data_stock: pd.DataFrame, 
                            company: str,
                            data: list, layout: dict, end: str):
    """Generate images for stocks which can be bought.

    Args:
        close_last (float): Last closing price of the stock.
        delta (float):Delta window for considering the min/max price.
        cluster_min_prices (list): List of min prices after clustering.
        cluster_max_prices (list): List of max prices after clustering.
        data_stock (pd.DataFrame): Dataframe containing stock data.
        company (str): Name of the company.
        data (list): List containing plotly figures.
        layout (dict): Layout od the plotly figure.
        end (str): End date of the data.
    """
    if cluster_max_prices[-1]>(close_last-delta) and cluster_max_prices[-1]<(close_last+delta):
        fig = go.Figure(data=data, layout=layout)
        figSignal = make_subplots(rows=2, cols=1, figure=fig)
        for px in cluster_max_prices[-2:]:
            figSignal.add_trace(go.Scatter(x=data_stock.index,
                                y=[px for _ in range(len(data_stock.index))],
                                line=dict(color='firebrick', width=4)),row=1, col=1)

        for px in cluster_min_prices[:2]:
            figSignal.add_trace(go.Scatter(x=data_stock.index,
                                y=[px for _ in range(len(data_stock.index))],
                                line=dict(color='royalblue', width=4)),row=1, col=1)

        figSignal.add_trace(go.Scatter(x=data_stock.index,
                                y=data_stock['rsi'],
                                line=dict(color='orange', width=4)),row=2, col=1)


        figSignal.write_image("Image_today/{}/SELL_{}_{}.png".format(company, end, close_last), engine="kaleido")