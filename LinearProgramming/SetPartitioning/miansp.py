# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 11:52:46 2019

@author: sania
"""

import read_datasp as rd
import numpy as np
import functionsp as fn
import pulp


#file to read the points from 'points_30.csv'
file_name = 'data_30.csv'

#number of points to read
num_points = 30 

maximum_taxis = 30
maximum_capacity = 3
points = '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30'.split()



def retrieve_distance(smallest_dist_matrix,distance_2,taxi):
    
    '''Find the diatance between each pair of points'''
    #sum = dist_table[0][int(taxi[0])] + dist_table[0][int(taxi[-1])] 
    #sum = 0
    #for k in range(len(taxi)-1):
        #sum += dist_table[int(taxi[k])][int(taxi[k+1])]
    if(len(taxi) < 3):
        distance = 700000
        
    #elif(len(taxi) == 2):
        #distance = distance_2[int(taxi[0])][int(taxi[1])]
        
    else:
        distance = smallest_dist_matrix[int(taxi[0])][int(taxi[1])][int(taxi[2])]
  
    return distance
    

if __name__ == '__main__':
    
    
    f = open("matching_30_lp_dist1_10.txt","w+")
    
    data = rd.read_data(file_name)
    i = 0 
    
    while(i<10):
        print("In iteration number:{}".format(i))
        data_utm_temp = [] 
        
        for j in range(num_points*i, num_points*i + num_points):
            data_utm_temp.append([data[j][0], data[j][1], data[j][2], data[j][3]])
            
        #convert the data_utm_temp array into a numpy array
        data_utm = np.asarray(data_utm_temp)
        
        #call calculate centroid
        #final_data = rd.calc_centroid(data_utm,num_points)
        
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
        f.write(" ")
        
        #Generate distance table
        dist_table = fn.generate_dist_table(final_data)
        
        #print("Distance table is:\n{}".format(dist_table))
        
        distance_2 = dist_table
        
        #distance_2 = fn.generate_dist_2_with_node(dist_table)
        
        smallest_dist_matrix_3 = fn.generate_smallest_dist_martix_3(dist_table)
        #smallest_dist_matrix_3 = fn.generate_smallest_dist_martix_3_with_node(dist_table)
        
        #print("The smallest distance matrix is:\n{}".format(smallest_dist_matrix))
               
        #create list of all possible combination of customers
        possible_taxis = [tuple(c) for c in pulp.allcombinations(points,maximum_capacity)]
        
        #create a binary variable to state that a table setting is used
        x = pulp.LpVariable.dicts('taxi', possible_taxis, lowBound = 0, upBound = 1, cat = pulp.LpInteger)
        
        matching_model = pulp.LpProblem("Rider Matching Model", pulp.LpMinimize)
        
        matching_model += sum([retrieve_distance(smallest_dist_matrix_3,distance_2,taxi) * x[taxi] for taxi in possible_taxis])
        
        
        #matching_model += sum([retrieve_distance(smallest_dist_matrix,taxi) * x[taxi] for taxi in possible_taxis])
        
        #specify the maximum number of taxis
        matching_model += sum([x[taxi] for taxi in possible_taxis]) <= maximum_taxis, "Maximum_number_of_taxis"
        
        #A customer must seated in one and only one taxis
        for cust in points:
            matching_model += sum([x[taxi] for taxi in possible_taxis if cust in taxi]) == 1, "Must_seat_%s"%cust
            
        matching_model.solve()
        
        print("The choosen taxis are out of a total of %s:"%len(possible_taxis))
        for taxi in possible_taxis:
            if x[taxi].value() == 1.0:
                print(taxi)
                
        for taxi in possible_taxis:
            if x[taxi].value() == 1.0:
                #print("0 ",end="")
                f.write("0 ")
                for a in range(len(taxi)):
                    #print("the customer at pos {} is:{}".format(a,taxi[a].strip('\'')))
                    #print("{} ".format(taxi[a].strip('\'')),end="")
                    f.write(taxi[a].strip('\'')+" ")
                #print("0 ",end="")
                f.write("0 ")
        f.write("\n")
            
        i += 1
    f.close()