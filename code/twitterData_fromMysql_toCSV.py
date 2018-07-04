import mysql.connector
from sqlalchemy import create_engine
import datetime
import pandas as pd
import config

username = config.username
password = config.password

print("connecting...")
engine = create_engine('mysql+mysqlconnector://' + username + ':' + password + '@twitterdata.ckmmf3gk0i4d.us-east-2.rds.amazonaws.com:3306/tweets', echo=False)
print("reading...")
df_aug = pd.read_sql('SELECT * FROM crypto_aug', con = engine)
df_sept = pd.read_sql('SELECT * FROM crypto_sept', con = engine)
df = df_aug.merge(df_sept, how='outer')

print("writing to csv...")
df.to_csv('twitter_crypto.csv')
