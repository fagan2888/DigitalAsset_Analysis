import mysql.connector
from sqlalchemy import create_engine
import datetime
import pandas as pd
import config

username = config.username
password = config.password

print("getting all...")

print("connecting...")
engine = create_engine('mysql+mysqlconnector://' + username + ':' + password + '@twitterdata.ckmmf3gk0i4d.us-east-2.rds.amazonaws.com:3306/tweets', echo=False)

print("reading one...")
dfOne = pd.read_sql('SELECT * FROM bitcoin_dec WHERE Date < "2017-12-07"', con = engine)

print("reconnecting and reading two...")
engine = create_engine('mysql+mysqlconnector://' + username + ':' + password + '@twitterdata.ckmmf3gk0i4d.us-east-2.rds.amazonaws.com:3306/tweets', echo=False)
dfTwo = pd.read_sql('SELECT * FROM bitcoin_dec WHERE Date > "2017-12-07" and Date < "2017-12-11"', con = engine)

print("reconnecting and reading three...")
engine = create_engine('mysql+mysqlconnector://' + username + ':' + password + '@twitterdata.ckmmf3gk0i4d.us-east-2.rds.amazonaws.com:3306/tweets', echo=False)
dfThree = pd.read_sql('SELECT * FROM bitcoin_dec WHERE Date > "2017-12-11" and Date < "2017-12-15"', con = engine)

df = dfOne.merge(dfTwo.merge(dfThree, how='outer'), how='outer')

print("writing to csv...")
df.to_csv('twitter_bitcoin_two.csv', chunksize=50000)
