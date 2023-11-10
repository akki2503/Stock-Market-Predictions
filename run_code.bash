#!/bin/bash
source ./stock_market_pred_venv/bin/activate
git pull
git checkout feature/buy_sell_csv
python price_action_analysis.py
git add buy_sell.csv
git commit -m "updated buy sell csv"
git push
