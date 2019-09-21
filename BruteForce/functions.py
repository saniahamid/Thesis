# -*- coding: utf-8 -*-
"""
Created on Tue May 28 13:15:34 2019

@author: sania

This code helps generate a Combination Table for nCr points.

"""
from itertools import combinations
from itertools import permutations
import numpy as np
from math import sqrt

#A  function to generate combination of mCn points
def generate_comb_table(m, n):
    
    #An array of total number of points
    a = np.array(range(1,n+1))

    #Combination of m points from total number of points
    comb = combinations(a,m)

    #A counter to keep track of number of combinations generated
    count = 0
    
    #A numpy array to store the combinations generated, the final dimension will be (n,m)
    comb_table = np.empty((0,m), int)

    #Appedning the combinations generated in comb_table
    for i in list(comb):
        #increasing the counter
        count += 1
        #converting each combination into an array
        b = [a for a in i]
        #appending each array of combination to the comb_table array
        comb_table = np.append(comb_table, np.array([b]), axis=0)
        
    #Printing the total number of combinations generated    
    #print("total number of combinations are: {}".format(count))
    return comb_table

#A function to generate disctance between pair of points
def generate_dist_table(final_data):
    
    #totla number of destination points + source points
    num_points = final_data.shape[0]+1
    
    #a table that contain the distance between a pair of points
    distance_table = np.empty([num_points,num_points])
    
    #set of points which contains the coordinates for the source point and the destination points
    #adding source coordinates to poiunts
    points = [[final_data[0][0],final_data[0][1]]]
    
    #adding destination coordinates to points
    for i in (final_data[:,2:4]):
        points.append([i[0],i[1]])
   
    #filling in the matrix using the distance formula
    for i in range(num_points):
        for j in range(num_points):
            distance_table[i][j] = int(sqrt( (points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2))
   
    return distance_table

#A function to generate the order of travle for each triplet in the combination table
def generate_order_travel_3(combination_table,dist_table):
    
    #an  array to store the final permutation sequence with the distance
    sequence_temp = []
    
    #find the permutation of each triplet in the combination, find the distance travelled for that sequence and select the sequence with the least sequence
    for i in combination_table:
        #permutatin of the triplet
        perm = permutations(i)
        
        #an array that stores unique permutation i.e. out of the 6 permutations store only 3. 3 2 1 is same as 1 2 3
        perm_3 = []
        k = 0
        
        #populate the perm_3 array
        for j in perm:
            if(k<=2):
                perm_3.append(list(j))
                k += 1
        
        #an array to store the totall distance travelled from (source->dest1->dest2->dest3->source)
        dist_sum_arr = []
        
        #add the source at the end and the begining for each trplet in the permutaion i.e. eg. [0, 2, 1, 3, 0]
        for t in perm_3:
            t.insert(0,0)
            t.insert(len(t),0)
            
            #the total distance of the path travelled
            dist_sum = 0
            
            #fetch the distance between two points from the distance table and add to find the total distance
            for p in range(len(t)-1):
                dist_sum += dist_table[t[p]][t[p+1]]
            
            #append the total distance for each permutation
            dist_sum_arr.append(dist_sum)
        
        #zip the distance and the permutation sequence and find the sequence with the least travel distance 
        aa = min(zip(perm_3,dist_sum_arr),key=lambda x:x[1])
        
        #convert the zip object into and np array
        aa = np.asarray(aa)

        #create a column array to store the path sequence(permutation) with the distance travelled for each triplet in the combination table eg. [1 2 3 list([0, 2, 1, 3, 0]) 9851.0]
        sequence_temp.append(aa)
    
    #combine the combination_table and the sequence of travel 
    combination_table = np.column_stack((combination_table,sequence_temp))

    return(combination_table)
    
#A function to generate the order of travle for each triplet in the combination table
def generate_order_travel_2(combination_table,dist_table):
    
    #an  array to store the final permutation sequence with the distance
    sequence_temp = []
    
    #find the permutation of each triplet in the combination, find the distance travelled for that sequence and select the sequence with the least sequence
    for i in combination_table:
        #permutatin of the triplet
        perm = permutations(i)
        
        #an array that stores unique permutation i.e. out of the 2 permutations store only 1. 2 1 is same as 1 2 ##### m!/2 - 1 #######
        perm_2 = []
        k = 0
        
        #populate the perm_3 array
        for j in perm:
            if(k<=0):
                perm_2.append(list(j))
                k += 1
        #print("Perm 2 is:{}".format(perm_2))
        
        #an array to store the totall distance travelled from (source->dest1->dest2->dest3->source)
        dist_sum_arr = []
        
        #add the source at the end and the begining for each trplet in the permutaion i.e. eg. [0, 2, 1, 0]
        for t in perm_2:
            t.insert(0,0)
            t.insert(len(t),0)
            #print("T in now:{}".format(t))
            
            #the total distance of the path travelled
            dist_sum = 0
            
            #fetch the distance between two points from the distance table and add to find the total distance
            for p in range(len(t)-1):
                dist_sum += dist_table[t[p]][t[p+1]]
            
            #append the total distance for each permutation
            dist_sum_arr.append(dist_sum)
        
        #zip the distance and the permutation sequence and find the sequence with the least travel distance 
        aa = min(zip(perm_2,dist_sum_arr),key=lambda x:x[1])
    
        #convert the zip object into and np array
        aa = np.asarray(aa)

#        #create a column array to store the path sequence(permutation) with the distance travelled for each triplet in the combination table eg. [1 2 3 list([0, 2, 1, 3, 0]) 9851.0]
        sequence_temp.append(aa)
    
    #combine the combination_table and the sequence of travel 
    combination_table = np.column_stack((combination_table,sequence_temp))

    return(combination_table)

#A function to generate the sequence 2   
def generate_sequence_3(order_table, num_points):
    sequence = []
    arr_ones = np.ones(order_table.shape[0])
    order_table = np.column_stack((order_table,arr_ones))   
    count = 1    
    while count <= num_points/3:
        order_table_2 = []
        for i in order_table:
            if(i[5] == 1):
                order_table_2.append(i)
        order_table_2 = np.asarray(order_table_2)
        min_dist = np.amin(order_table_2[:,4])
        #print("The minimum distance is:{}".format(min_dist))
        index = np.where(order_table_2[:,4] == np.amin(order_table_2[:,4]))
        a = order_table_2[index][0][0]
        b = order_table_2[index][0][1]
        c = order_table_2[index][0][2]
        sequence.append(order_table_2[index][0][3])
        
        list1 = [a,b,c]
        for  j in order_table:
            arr = j[0:3]
            result = any(elem in arr for elem in list1)
            if(result):
                j[5] = 0        
        count+=1
    return sequence
    
#A function to generate the sequence 3  
def generate_sequence_2(order_table, num_points):
    sequence = []
    arr_ones = np.ones(order_table.shape[0])
    order_table = np.column_stack((order_table,arr_ones))
    #print("Order table is now:\n{}".format(order_table))
    count = 1    
    while count <= num_points/2:
        order_table_2 = []
        for i in order_table:
            if(i[4] == 1):
                order_table_2.append(i)
        order_table_2 = np.asarray(order_table_2)
        min_dist = np.amin(order_table_2[:,3])
        #print("The minimum distance is:{}".format(min_dist))
        index = np.where(order_table_2[:,3] == np.amin(order_table_2[:,3]))
        a = order_table_2[index][0][0]
        b = order_table_2[index][0][1]
        #c = order_table_2[index][0][2]
        #print("a is:{}".format(a))
        #print("b is:{}".format(b))
        #print("c is:{}".format(c))
        #print("d is:{}".format(order_table_2[index][0][2]))
        sequence.append(order_table_2[index][0][2])
        
        list1 = [a,b]
        for  j in order_table:
            #print("Print j is:{}".format(j[0:2]))
            arr = j[0:2]
            result = any(elem in arr for elem in list1)
            if(result):
                j[4] = 0        
        count+=1
    return sequence

 
        
#parameters
#n = 12
#m = 3 
 
#if __name__ == '__main__':
    
    #Calling generate_comb_table() to generate the combination table
    #combination_table = generate_comb_table(m,n)
    
    #Printing the combination table
    #print("In original file.")
    #print(combination_table)