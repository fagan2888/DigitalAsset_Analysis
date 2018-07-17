import mysql.connector
from sqlalchemy import create_engine
import datetime
import pandas as pd
import config

username = config.username
password = config.password

print("getting second batch...")

print("connecting...")
engine = create_engine('mysql+mysqlconnector://' + username + ':' + password + '@twitterdata.ckmmf3gk0i4d.us-east-2.rds.amazonaws.com:3306/tweets', echo=False)

print("reading...")
df = pd.read_sql('SELECT * FROM bitcoin_dec WHERE Date > "2017-12-07" and Date < "2017-12-15"', con = engine, chunksize=100000)
#df = pd.read_sql('SELECT * FROM bitcoin_dec WHERE Date < "2017-12-07"', con = engine)

'''
print("writing to csv...")
df.to_csv('twitter_bitcoin_two.csv')
'''

for chunk in df:
    print("writing chunk to csv...")
    chunkNoDuplicates = chunk.drop_duplicates()
    chunkNoDuplicates.to_csv('twitter_bitcoin_two.csv', mode='a')
