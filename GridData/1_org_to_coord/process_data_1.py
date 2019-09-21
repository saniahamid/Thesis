# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 16:21:19 2019

@author: Sania Hamid

This file takes the original taxi data and drops ['id','vendor_id', 'pickup_datetime', 'dropoff_datetime', 'passenger_count','store_and_fwd_flag', 'trip_duration'] 
"""
import pandas as pd

file_name = 'taxidata.csv'

df = pd.read_csv(file_name)
#data = df.as_matrix()

print(df.head(2))
df.drop(['id','vendor_id', 'pickup_datetime', 'dropoff_datetime', 'passenger_count','store_and_fwd_flag', 'trip_duration'], axis = 1, inplace = True)
print(list(df.columns.values))
print(df.head(2))


df.to_csv("data.csv",index=False)
