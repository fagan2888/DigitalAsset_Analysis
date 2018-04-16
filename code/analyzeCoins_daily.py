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
from matplotlib.backends.backend_pdf import PdfPages

import statsmodels.graphics.tsaplots as ts
import statsmodels.tsa as tsa
from statsmodels.tsa.arima_process import ArmaProcess

from statsmodels.tsa.stattools import adfuller, grangercausalitytests

from arch import arch_model

##############################################
# Variables
##############################################
FOLDER_READ = "C:\\Users\\smlee\\Dropbox\\ECON8812\\project"
pp = PdfPages('coinGraphs.pdf')

##############################################
# Read Data
##############################################

# change into correct folder
os.chdir(FOLDER_READ)

# read data
coins = pd.read_csv('coinData.csv',  parse_dates=["Date"], keep_date_col=True)

# sort date in correct order
coins.sort_index()

##############################################
# Get Log Difference of Price
##############################################

coins["dlog"] = np.log(coins["Close"]).diff().fillna(value=0)
coins["dlog_btc"] = np.log(coins["Close_btc"]).diff().fillna(value=0)
coins["dlog_xrp"] = np.log(coins["Close_xrp"]).diff().fillna(value=0)
coins["dlog_ltc"] = np.log(coins["Close_ltc"]).diff().fillna(value=0)

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

        ts.plot_acf(y, lags=lags, alpha=0.05, ax = acf_ax, zero=False)
        ts.plot_pacf(y, lags=lags, alpha=0.05, ax = pacf_ax, zero=False)
        plt.suptitle(title, fontsize=14)
        plt.tight_layout()

    return

def plotAllSeries(_series):
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
    ts_ax1.plot(coins["Date"], coins[_series], color="blue")

    ### BTC ###
    ts_ax2.set_title("BitCoin")
    ts_ax2.plot(coins["Date"], coins[_series + "_btc"], color="red")

    ### XRP ###
    ts_ax3.set_title("Ripple")
    ts_ax3.plot(coins["Date"], coins[_series + "_xrp"], color="black")

    ### LTC ###
    ts_ax4.set_title("LiteCoin")
    ts_ax4.plot(coins["Date"], coins[_series + "_ltc"], color="green")

    plt.tight_layout()
    pp.savefig()

##############################################
# Augmented Dickey-Fuller test
##############################################

regressionTypes = ['c', 'ct', 'ctt', 'nc']
maxLags = [10,20,30,40]

for _reg in regressionTypes:
    # test dlog(ether)
    dfTest = adfuller(coins['dlog'], autolag = 'AIC', regression=_reg)

    # test dlog(btc)
    dfTest_btc = adfuller(coins['dlog_btc'], autolag = 'AIC', regression=_reg)

    # test dlog(xrp)
    dfTest_xrp = adfuller(coins['dlog_xrp'], autolag = 'AIC', regression=_reg)

    # test dlog(ltc)
    dfTest_ltc = adfuller(coins['dlog_ltc'], autolag = 'AIC', regression=_reg)

    print("\n###################################")
    print("# using " + _reg + " type regression")
    print("###################################")

    print("\n*************** ETH ***************")
    print("Test Stat... " + str(dfTest[0]))
    print("pValue...... " + str(dfTest[1]))
    print("usedLag..... " + str(dfTest[2]))
    print("N Obs....... " + str(dfTest[3]))
    print("Info Crit... " + str(dfTest[5]))

    print("\n*************** BTC ***************")
    print("Test Stat... " + str(dfTest_btc[0]))
    print("pValue...... " + str(dfTest_btc[1]))
    print("usedLag..... " + str(dfTest_btc[2]))
    print("N Obs....... " + str(dfTest_btc[3]))
    print("Info Crit... " + str(dfTest_btc[5]))

    print("\n*************** XRP ***************")
    print("Test Stat... " + str(dfTest_xrp[0]))
    print("pValue...... " + str(dfTest_xrp[1]))
    print("usedLag..... " + str(dfTest_xrp[2]))
    print("N Obs....... " + str(dfTest_xrp[3]))
    print("Info Crit... " + str(dfTest_xrp[5]))

    print("\n*************** LTC ***************")
    print("Test Stat... " + str(dfTest_ltc[0]))
    print("pValue...... " + str(dfTest_ltc[1]))
    print("usedLag..... " + str(dfTest_ltc[2]))
    print("N Obs....... " + str(dfTest_ltc[3]))
    print("Info Crit... " + str(dfTest_ltc[5]))

##############################################
# Granger causality test
##############################################

# set up pairs to test
ethBtc = np.column_stack((coins['dlog'], coins['dlog_btc']))
btcEth = np.column_stack((coins['dlog_btc'], coins['dlog']))

ethXrp = np.column_stack((coins['dlog'], coins['dlog_xrp']))
xrpEth = np.column_stack((coins['dlog_xrp'], coins['dlog']))

ethLtc = np.column_stack((coins['dlog'], coins['dlog_ltc']))
ltcEth = np.column_stack((coins['dlog_ltc'], coins['dlog']))

btcXrp = np.column_stack((coins['dlog_btc'], coins['dlog_xrp']))
xrpBtc = np.column_stack((coins['dlog_xrp'], coins['dlog_btc']))

btcLtc = np.column_stack((coins['dlog_btc'], coins['dlog_ltc']))
ltcBtc = np.column_stack((coins['dlog_ltc'], coins['dlog_btc']))

# print out one of them
gc = grangercausalitytests(xrpBtc, maxlag=30, verbose=True)

##############################################
# Plot
##############################################

# Plot series
plotAllSeries("Close")
plotAllSeries("dlog")

# Plot series, acf, pacf
tsPlot(coins["Date"], coins["Close"], lags=25, title="Ether")
tsPlot(coins["Date"], coins["dlog"], lags=25, title="Ether")

# close multipanel plot and display
pp.close()
plt.show()
