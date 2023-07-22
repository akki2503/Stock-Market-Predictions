
import pandas as pd
from IPython.core.display import display, HTML
import os


from utils.stock_data_utils import get_stock_data, add_rsi, get_cluster_max_prices, get_cluster_min_prices
from utils.plot_utils import get_data, get_layout, images_for_stocks_to_buy, images_for_stocks_to_sell

display(HTML("<style>.container { width:100% !important; }</style>"))

DAYS = 200
PERIOD = 5
WITHIN_SUPPORT_PERCENTAGE = 2
CSV_FILE_FOR_STOCK_INDICES = "inde_nifty100list.csv"
FOLDER_TO_SAVE_IMAGES = "buy_sell_images"

nifty_file=pd.read_csv(CSV_FILE_FOR_STOCK_INDICES, index_col=0)
os.makedirs(FOLDER_TO_SAVE_IMAGES, exist_ok=True)


buy_sell_stock = {}

for num in range(len(nifty_file)):
    company = list(nifty_file['Symbol'])[num]
    buy_sell_stock[company] = {}
    buy_sell_stock[company]["buy"] = []
    buy_sell_stock[company]["sell"] = []

for num in range(len(nifty_file)):
    try:
        print("Analysing for nifty stock:", list(nifty_file['Symbol'])[num])
        company = list(nifty_file['Symbol'])[num]
        data_stock = get_stock_data(company, days=DAYS, interval='1d')
        data_stock = add_rsi(data_stock)

        data = data_stock
        period = PERIOD
        cluster_max_prices = get_cluster_max_prices(data, period=PERIOD)
        cluster_min_prices = get_cluster_min_prices(data, period=PERIOD)
        
        layout = get_layout(title=company)
        data = get_data(data_stock)
        config = {'displayModeBar': False}

        
        close_last = data_stock["Close"][-1]
        delta = close_last*(WITHIN_SUPPORT_PERCENTAGE/100)

        os.makedirs(f"{FOLDER_TO_SAVE_IMAGES}/{company}", exist_ok=True)
        images_for_stocks_to_buy(close_last, delta, cluster_min_prices, 
                                    cluster_max_prices, data_stock, company,
                                    data, layout, "end")
        
        images_for_stocks_to_sell(close_last, delta, cluster_min_prices, 
                                    cluster_max_prices, data_stock, company,
                                    data, layout, "end")
        print("Saved Image for: ", company)

        if cluster_min_prices[0]>(close_last-delta) and cluster_min_prices[0]<(close_last+delta):
            buy_sell_stock[company]["buy"].append(close_last)
        if cluster_max_prices[-1]>(close_last-delta) and cluster_max_prices[-1]<(close_last+delta):
            buy_sell_stock[company]["sell"].append(close_last)
    except ValueError:
        print("No proper support resistance values could be found for the given period.")
        continue
        
df_buy_sell = pd.DataFrame.from_dict(buy_sell_stock, orient="index")
df_buy_sell.to_csv("buy_sell.csv")








