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
import matplotlib.pyplot as plt

import statsmodels.graphics.tsaplots as ts
import statsmodels.tsa as tsa
from statsmodels.tsa.arima_process import ArmaProcess

from arch import arch_model

##############################################
# Variables
##############################################
FOLDER_READ = "C:\\Users\\smlee\\Dropbox\\ECON8812\\project"

##############################################
# Read Data
##############################################
os.chdir(FOLDER_READ)
coins = pd.read_csv('coinData.csv',  parse_dates=["Date"], keep_date_col=True)

##############################################
# Functions
##############################################

def tsPlot(t, y, lags, title, figsize=(10,8), style="bmh"):
    '''
       Graphs:
            - Series
            - ACF
            - PACF
    '''
    if not isinstance(y, pd.Series):
        y = pd.Series(y)

    with plt.style.context(style):

        # Layout info
        layout = (2,2)

        # Set up axis info
        fig = plt.figure(figsize=figsize)
        ts_ax = plt.subplot2grid(layout, (0,0), colspan=2)
        acf_ax = plt.subplot2grid(layout, (1,0))
        pacf_ax = plt.subplot2grid(layout, (1,1))

        # Plot
        ts_ax.plot(t, y, color="blue")

        ts.plot_acf(y, lags=10, alpha=0.05, ax = acf_ax)
        ts.plot_pacf(y, lags=10, alpha=0.05, ax = pacf_ax)
        plt.suptitle(title, fontsize=14)
        plt.tight_layout()

    return


##############################################
# Describe Data
##############################################

print(coins.describe())

##############################################
# Plot Data
##############################################

tsPlot(coins["Date"], coins["Close"], lags=25, title="Ether")
tsPlot(coins["Date"], coins["Close_btc"], lags=25, title="BitCoin")
tsPlot(coins["Date"], coins["Close_xrp"], lags=25, title="Ripple")
tsPlot(coins["Date"], coins["Close_ltc"], lags=25, title="LiteCoin")

##############################################
# Plot All Data
##############################################
# Layout info
layout = (4,1)
figsize = (12,8)

# Set up axis info
fig = plt.figure(figsize=figsize)

ts_ax1 = plt.subplot2grid(layout, (0,0), colspan=2)
ts_ax2 = plt.subplot2grid(layout, (1,0), colspan=2)
ts_ax3 = plt.subplot2grid(layout, (2,0), colspan=2)
ts_ax4 = plt.subplot2grid(layout, (3,0), colspan=2)

### ETH ###
ts_ax1.set_title("Ether")
ts_ax1.plot(coins["Date"], coins["Close"], color="blue")

### BTC ###
ts_ax2.set_title("BitCoin")
ts_ax2.plot(coins["Date"], coins["Close_btc"], color="red")

### XRP ###
ts_ax3.set_title("Ripple")
ts_ax3.plot(coins["Date"], coins["Close_xrp"], color="black")

### LTC ###
ts_ax4.set_title("LiteCoin")
ts_ax4.plot(coins["Date"], coins["Close_ltc"], color="green")

plt.tight_layout()
plt.show()
