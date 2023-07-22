# Stock-Market-Predictions
Generate Buy and Sell Suggestions for Nifty 50 Stocks

## 1. Introduction

- This repository aims at using the data from yahoo-finance for Nifty 50 stocks to generate buying and selling suggestions for stocks on a daily basis.
- The application uses price action based analysis to understand the resistance and support levels of the stock in past 200 days and suggests buy/sell tag based on the current price and RSI calculations.

## 2. How to create a virtual environment for running the analysis

1. `python3 -m venv stock_market_pred_venv`
2. `source stock_market_pred_venv/bin/activate`
3. `pip install -u pip`
4. `pip install -r requirements.txt`

## 3. How to run the analysis on a CSV

- To predict buy/sell calls on a list of stocks, you need a csv in the format similar to `Nifty_yahoo_sticker.csv`
- To run the predictions on a csv `python price_action_analysis.py --csv_file_path <path-to-csv-file>`

## 4. How to make sense of outputs

- After running the python script, two outputs are generate
    1. buy_sell.csv - contains buy sell recommendations for list of stocks provided as input
    2. buy_sell_images - images containing info for only the buy sell calls of the stocks mentioned in csv with support and resistance lines and past 200 days price.
