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
FOLDER_READ = "C:\\Users\\smlee\\Downloads\\TxCoinData\\"
FOLDER_WRITE = "C:\\Users\\smlee\\Dropbox\\ECON8812\\project"

ETH = "ETHUSD_transactions.csv"
BTC = "BTCUSD_transactions.csv"
XRP = "XRPUSD_transactions.csv"
LTC = "LTCUSD_transactions.csv"

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

    finalPriceSeries = []
    finalAmountSeries = []

    time_orig = _df['timestamp']
    price_orig = _df['price']
    amount_orig = _df['amount']

    indexCounter = 0
    for timeSlot in _finalTimes:

        print("\n" + str(timeSlot))

        totalAmountToAve = 0
        totalWeightedPrice = 0

        while (time_orig.iloc[indexCounter] <= timeSlot):

            amount = amount_orig.iloc[indexCounter]

            if (amount == 0):
                amount = 0.000000001

            totalWeightedPrice += amount*price_orig.iloc[indexCounter]
            totalAmountToAve += amount
            indexCounter += 1


        weightedPrice = totalWeightedPrice/totalAmountToAve
        finalPriceSeries.append(weightedPrice)
        finalAmountSeries.append(amount)
        print(weightedPrice)

    print("Time series observations: " + str(len(_finalTimes)))
    print("Price series observations: " + str(len(finalPriceSeries)))
    return finalPriceSeries, finalAmountSeries

##############################################
# Read Data
##############################################
os.chdir(FOLDER_READ)

print("reading eth...")
eth = pd.read_csv(FOLDER_READ + ETH, \
                  dtype={"ID":int, "timestamp":int, "amount":float, "price":float})

print("reading xrp...")
xrp = pd.read_csv(FOLDER_READ + XRP,  \
                  dtype={"ID":int, "timestamp":int, "amount":float, "price":float})

print("reading ltc...")
ltc = pd.read_csv(FOLDER_READ + LTC, \
                  dtype={"ID":int, "timestamp":int, "amount":float, "price":float})

print("reading btc...")
btcIter = pd.read_csv(FOLDER_READ + BTC, iterator=True, chunksize=100000,dtype={"ID":int, "timestamp":int, "amount":float, "price":float})
btc = pd.concat([chunk[chunk['timestamp'] >= 1502901198] for chunk in btcIter])

##############################################
# Clean Data
##############################################

### Time

# drop first row for ethereum
# this appears to be a test transaction
# including creates a huge jump in time
eth = eth.drop([0,1])

# find limiting minimum time
minEth = min(eth['timestamp'])
minXrp = min(xrp['timestamp'])
minLtc = min(ltc['timestamp'])
minBtc = min(btc['timestamp'])
minTime = max([minEth,minXrp,minLtc,minBtc])

# find limiting maximum time
maxEth = max(eth['timestamp'])
maxXrp = max(xrp['timestamp'])
maxLtc = max(ltc['timestamp'])
maxBtc = max(btc['timestamp'])
maxTime = min(maxEth,maxXrp,maxLtc,maxBtc)

# Turns out eth is limiting factor
# But when it was first opened to trade
# it took a few hours for people to use it
# So, I'm setting the minimum time based on looking at data

print("Limiting minimum timestamp " + str(minTime))
print("Limiting maximum timestamp " + str(maxTime))

# reset each series to only count observations past that date
btc = btc[btc['timestamp'] >= minTime]
eth = eth[eth['timestamp'] >= minTime]
ltc = ltc[ltc['timestamp'] >= minTime]
xrp = xrp[xrp['timestamp'] >= minTime]

print(eth)
print(btc)
print(ltc)
print(xrp)

print("Calculating max and min time jumps for eth")
e = getTimeUnit(eth['timestamp'])

print("Calculating max and min time jumps for btc")
b = getTimeUnit(btc['timestamp'])

print("Calculating max and min time jumps for xrp")
x = getTimeUnit(xrp['timestamp'])

print("Calculating max and min time jumps for ltc")
l = getTimeUnit(ltc['timestamp'])

timeChunk = max(e[0], b[0], x[0], l[0])

print("\nThe final time bucket " + str(timeChunk))

# array for my final time buckets
finalTimeBucket = np.arange(minTime + timeChunk, maxTime, timeChunk)
print("Total observataions in finals series " + str(len(finalTimeBucket)))

### calculate new dataset

print("Starting times:")
print(min(eth['timestamp']))
print(min(xrp['timestamp']))
print(min(ltc['timestamp']))
print(min(btc['timestamp']))

print("Calculating weighted prices...")
ethPrices = getWeightedPriceAverage(eth, finalTimeBucket)
btcPrices = getWeightedPriceAverage(btc, finalTimeBucket)
ltcPrices = getWeightedPriceAverage(ltc, finalTimeBucket)
xrpPrices = getWeightedPriceAverage(xrp, finalTimeBucket)

### add and write new dataset

data = {"Time":finalTimeBucket, \
        "ETH":ethPrices[0], "Volume_Eth":ethPrices[1], \
        "BTC":btcPrices[0], "Volume_BTC":btcPrices[1], \
        "LTC":ltcPrices[0], "Volume_LTC":ltcPrices[1], \
        "XRP":xrpPrices[0], "Volume_XRP":xrpPrices[1]}

coins = pd.DataFrame(data=data)

os.chdir(FOLDER_WRITE)
coins.to_csv("coinData_hourly.csv")
