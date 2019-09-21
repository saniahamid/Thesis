# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 15:39:46 2019

@author: Zodiac
This program takes in a file or origin and destination coordinates and gives out points that have their origin in a 200X200 grid 
a set of multiples of 30 points in a grid
"""

import pandas as pd
import numpy as np
import utm
import matplotlib.pyplot as plt

file_name = 'data.csv'

df = pd.read_csv(file_name)
print(df.head(5))
data = df.as_matrix()

#train_num = 10

data_utm_temp = []

#Convert data to UTM coordinates
for i in range(data.shape[0]):
    #convert the origin latitude and longitude to utm coordinates
    origin_utm = utm.from_latlon(data[i,1],data[i,0])
    #cenvert the destination latitude and longitude to utm coordinates
    destination_utm = utm.from_latlon(data[i,3],data[i,2])
    data_utm_temp.append([origin_utm[0],origin_utm[1],destination_utm[0],destination_utm[1]])
  
#convert the data_utm_temp array into a numpy array
data_utm = np.asarray(data_utm_temp)

OX = np.array(data_utm[:,0])
OY = np.array(data_utm[:,1])
DX = np.array(data_utm[:,2])
DY = np.array(data_utm[:,3])
    

#min_OX = 539364.3002644884
#min_OY = 4476326.671394471
#max_OX = 640713.8632637523
#max_OY = 4574556.080298231



indices_1 = [i for (i,v) in enumerate(OX) if v<=582854 or v>=589963]
#print("deletin coordinates {} ".format(indices_1))
OX = np.delete(OX, indices_1)
OY = np.delete(OY, indices_1)
DX = np.delete(DX, indices_1)
DY = np.delete(DY, indices_1)

indices_2 = [i for (i,v) in enumerate(OY) if v<=4505840 or v>=4523680]
#print("deleting coordinates {} ".format(indices_2))
OX = np.delete(OX, indices_2)
OY = np.delete(OY, indices_2)
DX = np.delete(DX, indices_2)
DY = np.delete(DY, indices_2)

#Calculate the minmum and maximum of OX and OY
min_OX = np.amin(OX)
min_OY = np.amin(OY)
max_OX = np.amax(OX)
max_OY = np.amax(OY)

print("Min OX is:{}".format(min_OX))
print("Min OY is:{}".format(min_OY))
print("Max OX is:{}".format(max_OX))
print("Max OY is:{}".format(max_OY))

plt.plot([min_OX,max_OX,max_OX,min_OX,min_OX],[min_OY,min_OY,max_OY,max_OY,min_OY],'yellow')
plt.scatter(OX, OY)


utm_final_data = np.stack((np.array(OX),np.array(OY),np.array(DX),np.array(DY),np.full(OX.shape[0],-1)), axis = 1)

for i in range(36):
    plt.plot([min_OX+200*i,min_OX+200*i],[min_OY,max_OY],'red')
   
for i in range(89):
    plt.plot([min_OX,max_OX],[min_OY+200*i,min_OY+200*i],'red')

#plt.grid()
#plt.figure()
plt.show()


grid = np.empty([35*88,5])

#for i in grid:
#    i[0] = 0
#    i[1] = 1
#    i[2] = 2
#    i[3] = 3

k = 0
for i in range(88):
    for j in range(35):
        grid[k][0] = k
        grid[k][1] = min_OX + ( j * 200 )
        grid[k][2] = min_OY + ( i * 200 )
        grid[k][3] = min_OX + ( (j+1) * 200 )
        grid[k][4] = min_OY + ( (i+1) * 200 )
        k += 1
print(k)

for point in utm_final_data:
    for t in grid:
        if( point[0] >= t[1] and point[0] <= t[3]):
            if( point[1] >= t[2] and point[1] <= t[4]):
                point[4] = t[0]
                
for i in range(5):
    print(utm_final_data[i])
    plt.scatter(utm_final_data[i][0], utm_final_data[i][1], color= 'orange')
    
utm_final_data = utm_final_data[utm_final_data[:,4].argsort()]

unique, counts = np.unique(utm_final_data[:,4], return_counts = True)
a = dict(zip(unique,counts))
print(a)

points_30_more = []

for i in utm_final_data:
    if (a[i[4]]>= 30):
        points_30_more.append(i)
        
points_30_more = np.asarray(points_30_more)

ol = np.ones((points_30_more.shape[0],1))
points_30 = np.column_stack((points_30_more,ol))

unique, counts = np.unique(points_30[:,4], return_counts = True)
b = dict(zip(unique,counts))
print(b)

k = 0 
while k < points_30.shape[0]:
    c = b[points_30[k][4]]
    p = c // 30
    r = c % 30
    k += p * 30
    for j in range(k,k+r):
        points_30[j][5] = 0
    k += r 

index = np.where(points_30[:,5] == 0)
points_30 = np.delete(points_30,index,axis = 0)    

unique, counts = np.unique(points_30[:,4], return_counts = True)
c = dict(zip(unique,counts))
print(c) 
        
#dataset = pd.DataFrame()
dataset = pd.DataFrame({'OX':points_30[:,0],'OY':points_30[:,1],'DX':points_30[:,2],'DY':points_30[:,3],'Grid':points_30[:,4]})        

dataset.to_csv("data_30.csv",index=False)
    