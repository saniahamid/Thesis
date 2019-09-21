# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 11:53:47 2019

@author: sania
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def read_data(file_name):
    #Create a panda dataframe to read data in the csv file
    df = pd.read_csv(file_name)
    
    #Convert the dataframe into a matrix
    data = df.as_matrix() 
    
    return(data)

# A function to translate all the origins to the centroid of those origins
def calc_centroid(data_utm,num_points):
    
    OX = np.array(data_utm[:,0])
    OY = np.array(data_utm[:,1])
    DX = np.array(data_utm[:,2])
    DY = np.array(data_utm[:,3])
    
    #Calculate the minmum and maximum of OX and OY
    min_OX = np.amin(OX)
    min_OY = np.amin(OY)
    max_OX = np.amax(OX)
    max_OY = np.amax(OY)
    
    #Calculate the centroid
    centroid_X = (min_OX + max_OX) / 2
    centroid_Y = (min_OY + max_OY) / 2       
    #plt.scatter(centroid_X, centroid_Y)    
    #plt.plot([min_OX,max_OX,max_OX,min_OX,min_OX],[min_OY,min_OY,max_OY,max_OY,min_OY],'yellow')
    
    #Change all the origin coordinates to the centroid coordinates
    for i in range(data_utm.shape[0]):
        OX[i] = centroid_X
        OY[i] = centroid_Y
        
    plot_data(OX,OY,DX,DY,num_points)
    
    final_data = np.stack((np.array(OX),np.array(OY),np.array(DX),np.array(DY)), axis = 1)
    
    return final_data

#A function to plot origin coordinates and destination coordinates
def plot_data(OX,OY,DX,DY,num_points):
    
    plt.plot([OX,DX],[OY,DY], marker='o',markevery=(1,DY.size),color='#947CB0', zorder=2,markeredgecolor='red')#label='Origin Points')
    for i, txt in enumerate(np.arange(num_points)+1):
        plt.annotate(txt ,xy = (DX[i],DY[i]))
    
    plt.grid()
    plt.figure()
    plt.show()
