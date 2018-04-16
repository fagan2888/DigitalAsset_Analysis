##############################################
# Coin analysis project
# ECON812 - Spring 2018
# Stephen Lee

##############################################
# Import
##############################################
import os

import numpy as np
import pandas as pd

##############################################
# Variables
##############################################
FOLDER = "C:\\Users\\smlee\\Downloads\\DailyCoinData\\"
FOLDER_WRITE = "C:\\Users\\smlee\\Dropbox\\ECON8812\\project"
ETH = "ethUsd_daily_2.csv"
BTC = "btcUsd_daily_2.csv"
XRP = "xrpUsd_daily.csv"
LTC = "ltcUsd_daily.csv"

##############################################
# Read Data
##############################################
os.chdir(FOLDER)

eth = pd.read_csv(FOLDER + ETH, parse_dates=["Date"], keep_date_col=True)
btc = pd.read_csv(FOLDER + BTC, parse_dates=["Date"], keep_date_col=True)
xrp = pd.read_csv(FOLDER + XRP, parse_dates=["Date"], keep_date_col=True)
ltc = pd.read_csv(FOLDER + LTC, parse_dates=["Date"], keep_date_col=True)

##############################################
# Merge Data
##############################################
coins = pd.merge(eth, btc, 'left', on='Date', suffixes=["", "_btc"])
coins = pd.merge(coins, ltc, 'left', on='Date', suffixes=['', '_ltc'])
coins = pd.merge(coins, xrp, 'left', on='Date', suffixes=['', '_xrp'])

# check they are all there
print(coins.dtypes)
print(coins['Date'])
##############################################
# Write Data
##############################################

os.chdir(FOLDER_READ)
coins.to_csv('coinData.csv')
