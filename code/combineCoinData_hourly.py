##############################################
# Coin analysis project
# ECON812 - Spring 2018
# Stephen Lee
#
# Make dataset with observataion each hour
# instead of every hour and a half (ish)

##############################################
# Import
##############################################
import os

import numpy as np
import pandas as pd

##############################################
# Variables
##############################################
FOLDER_READ = "C:\\Users\\smlee\\Downloads\\CoinData\\TxLevelCoinData\\"
FOLDER_WRITE = "C:\\Users\\smlee\\Dropbox\\Spring2018_Coursework\\ECON8812\\project\\data\\"

ETH = "ETHUSD_transactions.csv"
BTC = "BTCUSD_transactions.csv"
XRP = "XRPUSD_transactions.csv"
LTC = "LTCUSD_transactions.csv"

# set time chunk to 1 hour
timeChunk = 3600

##############################################
# Functions
##############################################
def getTimeUnit(_ts):
    # Finds the largest and smallest space between two observations
    #
    # Pre... a time series
    # Post.. returns largest and sallest gap in the time

    differencedSeries = _ts.diff().fillna(value=5)

    maxTimeJump = max(differencedSeries)
    minTimeJump = min(differencedSeries)

    return maxTimeJump, minTimeJump

def getWeightedPriceAverage(_df, _finalTimes):
    # Finds the weighted price average for all transactions
    # between time stamps given in final time
    #
    # Pre... a dataframe with series for "timestamp", "price", and "amount"
    #        and a series of final time buckets with regular periods
    # Post.. returns a series of the weighted price and amount transacted in each time jump

    # placeholders for final series
    finalPriceSeries = []
    finalAmountSeries = []

    # decompose the dataframe
    time_orig = _df['timestamp']
    price_orig = _df['price']
    amount_orig = _df['amount']

    # get time chunk for use later...
    timeChunks = _finalTimes[1] - _finalTimes[0]

    # fill each time slot with a weighted price average
    indexCounter = 0
    loopCounter = 0
    print("\nCalculating weighted price average...")
    for timeSlot in _finalTimes:

        print("Time: " + str(timeSlot))

        # find proper starting index on tx level series
        # some start way before the first time slot
        # loop through until it is within an hour of the first time bucket
        while (time_orig.iloc[indexCounter] < _finalTimes[0] - timeChunks):
            indexCounter += 1

        # reset temp variables for calculating weighted averages
        totalAmountToAve = 0
        totalWeightedPrice = 0

        # calculate weighted average while time is less than the
        # current bucket to fill
        while (time_orig.iloc[indexCounter] <= timeSlot):

            amount = amount_orig.iloc[indexCounter]

            if (amount == 0):
                amount = 0.000000001

            totalWeightedPrice += amount*price_orig.iloc[indexCounter]
            totalAmountToAve += amount
            indexCounter += 1

        # when you exit while loop, calculate weighted price
        if (totalAmountToAve > 0):
            weightedPrice = totalWeightedPrice/totalAmountToAve
            print("Price: " + str(weightedPrice))
        else:
            weightedPrice = None
            print("Missing observation")

        # add to series
        finalPriceSeries.append(weightedPrice)
        finalAmountSeries.append(amount)

    print("Time series observations: " + str(len(_finalTimes)))
    print("Price series observations: " + str(len(finalPriceSeries)))
    return finalPriceSeries, finalAmountSeries

##############################################
# Read Data
##############################################
os.chdir(FOLDER_READ)

print("reading eth...")
_eth = pd.read_csv(FOLDER_READ + ETH, \
                  dtype={"ID":int, "timestamp":int, "amount":float, "price":float})

print("reading xrp...")
_xrp = pd.read_csv(FOLDER_READ + XRP,  \
                  dtype={"ID":int, "timestamp":int, "amount":float, "price":float})

print("reading ltc...")
_ltc = pd.read_csv(FOLDER_READ + LTC, \
                  dtype={"ID":int, "timestamp":int, "amount":float, "price":float})

# due to memory issues, read this in iteratively
print("reading btc...")
btcIter = pd.read_csv(FOLDER_READ + BTC, \
                     iterator=True, chunksize=100000,dtype={"ID":int, "timestamp":int, "amount":float, "price":float})
_btc = pd.concat([chunk[chunk['timestamp'] >= 1502901198] for chunk in btcIter])

##############################################
# Clean Data
##############################################

### Time

# drop first row for ethereum
# this appears to be a test transaction
# including creates a huge jump in time
_eth = _eth.drop([0,1])

# find limiting minimum time
minEth = min(_eth['timestamp'])
minXrp = min(_xrp['timestamp'])
minLtc = min(_ltc['timestamp'])
minBtc = min(_btc['timestamp'])
minTime = max([minEth,minXrp,minLtc,minBtc])

# find limiting maximum time
maxEth = max(_eth['timestamp'])
maxXrp = max(_xrp['timestamp'])
maxLtc = max(_ltc['timestamp'])
maxBtc = max(_btc['timestamp'])
maxTime = min(maxEth,maxXrp,maxLtc,maxBtc)

print("Limiting minimum timestamp " + str(minTime))
print("Limiting maximum timestamp " + str(maxTime))
print("\nThe final time jump for each bucket is " + str(timeChunk) + " s")

# array for my final time series
finalTimeBucket = np.arange(minTime + timeChunk, maxTime, timeChunk)
print("Total observataions in finals series " + str(len(finalTimeBucket)) + "\n")

# calculate new dataset
# find new price series
ethPrices = getWeightedPriceAverage(_eth, finalTimeBucket)
btcPrices = getWeightedPriceAverage(_btc, finalTimeBucket)
ltcPrices = getWeightedPriceAverage(_ltc, finalTimeBucket)
xrpPrices = getWeightedPriceAverage(_xrp, finalTimeBucket)

# make and write new dataset
data = {"Time":finalTimeBucket, \
        "ETH":ethPrices[0], "Volume_Eth":ethPrices[1], \
        "BTC":btcPrices[0], "Volume_BTC":btcPrices[1], \
        "LTC":ltcPrices[0], "Volume_LTC":ltcPrices[1], \
        "XRP":xrpPrices[0], "Volume_XRP":xrpPrices[1]}

coins = pd.DataFrame(data=data)

os.chdir(FOLDER_WRITE)
coins.to_csv("coinData_hourly(Aug17-May18).csv")
