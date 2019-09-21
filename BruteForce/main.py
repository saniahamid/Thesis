# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 14:58:46 2019

@author: Sania Hamid

This codes generates the trainig data 10000 rows 30 points and a grouping for it 
"""


import functions as fn
import read_data as rd
import numpy as np

#Combination table parameters
#total number of points
n = 30
#group of points
m = 3

#file to read the points
file_name = 'data_30.csv'
#number of points to read
num_points = n

if __name__ == '__main__':
    
    f = open("matching_30_bf.txt","w+")
    
    combination_table = fn.generate_comb_table(m,n)

    
    data = rd.read_data(file_name)
#    
    #print("The combination table is:\n{}".format(combination_table))
    #print("All of data is:\n{}".format(data))
#    
    i = 0
#    
    while(i<12500):
#        
        print("In iteration number:{}".format(i))
        data_utm_temp = []
#        
        for j in range(num_points*i, num_points*i + num_points):
            
            #print(j)
            data_utm_temp.append([data[j][0], data[j][1], data[j][2], data[j][3]])
            #print(data[j][0], data[j][1], data[j][2], data[j][3])
            
        
        #convert the data_utm_temp array into a numpy array
        data_utm = np.asarray(data_utm_temp)
        
        #print(data_utm)
        #call calculate centroid
        final_data = rd.calc_centroid(data_utm,num_points)
        #print("The final data is:\n{}".format(final_data))
        line = str(final_data[0,0:2])
        for k in range(num_points):
            line += " " + str(final_data[k,2:4])
        index = line.find('[[')
        line2 = line[:index]+" output "+ line[index:]
        line3 = line2.replace('[','')
        line4 = line3.replace(']','')
        line5 = line4.strip()
        line6 = line5.replace(',','')
        line7 = line6.replace("       "," ")
        line8 = line7.replace("      "," ")
        line9 = line8.replace("     "," ")
        line10 = line9.replace("    "," ")
        line11 = line10.replace("   "," ")
        line12 = line11.replace("  "," ")
        line13 = line12.replace("  "," ")
        #print(line13)
        f.write(line13)
        
        
        #Generate distacne table
        dist_table = fn.generate_dist_table(final_data)
          
        #print("The distance table is:\n{}".format(dist_table))
        
#        #Generate order of travel for each triplet in the combination table
        order_table = fn.generate_order_travel_3(combination_table,dist_table)
        #order_table = fn.generate_order_travel_2(combination_table,dist_table)
        #print("Order Table is:\n{}".format(order_table))
        sequence = fn.generate_sequence_3(order_table, num_points)
        #sequence = fn.generate_sequence_2(order_table, num_points)
# 
        seq = str(sequence)
        seq1 = seq.replace('[[',' ')
        seq2 = seq1.replace('[','')
        seq3 = seq2.replace(']','')
        seq4 = seq3.replace(',','')

        #print(seq4)
        f.write((seq4)+"\n")
        i += 1
    f.close()
