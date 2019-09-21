# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 13:46:30 2019

@author: sania
"""

import numpy as np
from math import sqrt

#A function to generate disctance between pair of points
def generate_dist_table(final_data):
    
    #totla number of destination points + source points
    num_points = final_data.shape[0]+1
    
    #a table that contain the distance between a pair of points
    distance_table = np.empty([num_points,num_points])
    
    #set of points which contains the coordinates for the source point and the destination points
    #adding source coordinates to points
    points = [[final_data[0][0],final_data[0][1]]]
    
    #adding destination coordinates to points
    for i in (final_data[:,2:4]):
        points.append([i[0],i[1]])
   
    #filling in the matrix using the distance formula
    for i in range(num_points):
        for j in range(num_points):
            distance_table[i][j] = int(sqrt( (points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2))
   
    return distance_table

def generate_dist_2_with_node(dist_table):
    
    #define a 2-D matrix
    dist_mat = np.full((31,31), np.inf)
    
    for i in range(31):
        for j in range(31):
            if(dist_mat[i][j] == np.inf):
                dist_mat[i][j] = dist_table[i][j] + dist_table[0][i] + dist_table[0][j]
                
    return dist_mat


def generate_smallest_dist_martix_3(dist_table):

    #define a 3-D matrix
    dist_mat = np.full((31,31,31), np.inf)
    
    for i in range(31):
        for j in range(31):
            for k in range(31):
                if(dist_mat[i][j][k] == np.inf):
                    #print("dist({},{})+dist({},{})={}".format(i,j,j,k, dist_table[i][j] + dist_table[j][k]))
                    #print("dist({},{})+dist({},{})={}".format(i,k,k,j, dist_table[i][k] + dist_table[k][j]))
                    #print("dist({},{})+dist({},{})={}".format(i,j,i,k, dist_table[i][j] + dist_table[i][k]))
                    #dist_mat[i][j][k] = min(dist_table[i][j] + dist_table[j][k], dist_table[i][k] + dist_table[k][j], dist_table[i][j] + dist_table[i][k])
                    #print("dist({},{})+dist({},{})={}".format(i,j,j,k, dist_table[i][j] + dist_table[j][k] + dist_table[0][i] + dist_table[0][k]))
                    #print("dist({},{})+dist({},{})={}".format(i,k,k,j, dist_table[i][k] + dist_table[k][j] + dist_table[0][i] + dist_table[0][j]))
                    #print("dist({},{})+dist({},{})={}".format(i,j,i,k, dist_table[i][j] + dist_table[i][k] + dist_table[0][j] + dist_table[0][k]))
                    a = dist_table[i][j] + dist_table[j][k]
                    b = dist_table[i][k] + dist_table[k][j]
                    c = dist_table[i][j] + dist_table[i][k]
                    dist_mat[i][j][k] = min(a,b,c)
    
    return dist_mat

def generate_smallest_dist_martix_3_with_node(dist_table):

    #define a 3-D matrix
    dist_mat = np.full((31,31,31), np.inf)
    
    for i in range(31):
        for j in range(31):
            for k in range(31):
                if(dist_mat[i][j][k] == np.inf):
                    #print("dist({},{})+dist({},{})={}".format(i,j,j,k, dist_table[i][j] + dist_table[j][k]))
                    #print("dist({},{})+dist({},{})={}".format(i,k,k,j, dist_table[i][k] + dist_table[k][j]))
                    #print("dist({},{})+dist({},{})={}".format(i,j,i,k, dist_table[i][j] + dist_table[i][k]))a = dist_table[i][j] + dist_table[j][k] + dist_table[0][i] + dist_table[0][k]
                    a = dist_table[i][j] + dist_table[j][k] + dist_table[0][i] + dist_table[0][k]
                    b = dist_table[i][k] + dist_table[k][j] + dist_table[0][i] + dist_table[0][j]
                    c = dist_table[i][j] + dist_table[i][k] + dist_table[0][j] + dist_table[0][k]
                    dist_mat[i][j][k] = min(a,b,c)
    
    return dist_mat