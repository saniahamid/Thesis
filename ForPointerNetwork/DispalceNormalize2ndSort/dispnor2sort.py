# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 13:48:26 2019

@author: sania
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


file_name = "matching_30_lp_dist1.txt"
fo = open("matching_30_lp_dist1_dnsx","w")

def displace(inputs,outputs):
    
    disp_x = inputs[0][0]
    disp_y = inputs[0][1]

    for i in range(1, inputs.shape[0]):
        
        diff_x = inputs[i][0] - disp_x
        diff_y = inputs[i][1] - disp_y
        
        for j in range(0,inputs.shape[1]):
            
            if(j % 2 == 0):
                inputs[i][j] = inputs[i][j] - (diff_x)
            else:
                inputs[i][j] = inputs[i][j] - (diff_y)
        
    return 0

def normalize2(inputs,outputs):
    
    for i in range(inputs.shape[0]):
        
        inputs_norX_temp = []
        inputs_norY_temp = []
    
        for j in range(0, inputs.shape[1]-1,2):
            inputs_norX_temp.append(inputs[i][j])
            inputs_norY_temp.append(inputs[i][j+1])
    
        inputs_norX_temp = np.asarray(inputs_norX_temp)
        inputs_norY_temp = np.asarray(inputs_norY_temp)
        
        min_X = np.amin(inputs_norX_temp)
        max_X = np.amax(inputs_norX_temp)
        min_Y = np.amin(inputs_norY_temp)
        max_Y = np.amax(inputs_norY_temp)
        
        for k in range(0, inputs.shape[1]-1, 2):
            inputs[i][k] = float("{0:.6f}".format((inputs[i][k] - min_X) / (max_X - min_X)))
            inputs[i][k+1] =float("{0:.6f}".format((inputs[i][k+1] - min_Y) / (max_Y - min_Y)))
            
    return 0

def sort(inputs,outputs):
    
    #code to sort inputs
    for i in range(inputs.shape[0]):
        
        inputs_old_x = []
        for c in range(2,inputs.shape[1]-1,2):
            inputs_old_x.append(inputs[i][c])
        inputs_old_x = np.asarray(inputs_old_x)
        
        inputs_sort_temp = []
        for k in range(2,inputs.shape[1]-1,2):
            inputs_sort_temp.append((inputs[i][k], inputs[i][k+1]))
        inputs_sort = sorted(inputs_sort_temp, key = lambda x : x[0])
        l = 0
        for m in range(2,inputs.shape[1]-1,2):
            inputs[i][m] = inputs_sort[l][0]
            inputs[i][m+1] = inputs_sort[l][1]
            l += 1
        
        inputs_x = []
        for b in range(2,inputs.shape[1]-1,2):
            inputs_x.append(inputs[i][b])
        
        inputs_x = np.asarray(inputs_x)
        out_index = [1,2,3,6,7,8,11,12,13,16,17,18,21,22,23,26,27,28,31,32,33,36,37,38,41,42,43,46,47,48]
        
        for a in out_index:
            point_x = inputs_old_x[outputs[i][a] - 2]
            index = np.where(inputs_x == point_x)
            if len(index[0]) > 1:
                outputs[i][a] = index[0][0] + 2
            else:
                outputs[i][a] = index[0] + 2
    
     
    
    #code to sort outputs
#    for i in range(inputs.shape[0]):
        OX_sort = []
        OY_sort = []
        DX_sort = []
        DY_sort = []
        
        for j in range(0, (inputs.shape[1]-2) // 2):
            OX_sort.append(inputs[i][0])
            OY_sort.append(inputs[i][1])
            
        for k in range(2, inputs.shape[1] - 1, 2):
            DX_sort.append(inputs[i][k])
            DY_sort.append(inputs[i][k+1])
            
        for l in range(1,47,5):
            temp_sort = sorted([(DX_sort[outputs[i][l]-2],outputs[i][l]), (DX_sort[outputs[i][l+1]-2],outputs[i][l+1]), (DX_sort[outputs[i][l+2]-2],outputs[i][l+2])])
            outputs[i][l] = temp_sort[0][1]
            outputs[i][l+1] = temp_sort[1][1]
            outputs[i][l+2] = temp_sort[2][1]
        
        temp_sort_data = []
        
        for m in range(1,47,5):
            temp_sort_data.append((DX_sort[outputs[i][m]-2],DX_sort[outputs[i][m+1]-2],DX_sort[outputs[i][m+2]-2],outputs[i][m],outputs[i][m+1],outputs[i][m+2]))
        temp_sort_data.sort()
        
        p = 0
        for o in range(1,47,5):
            outputs[i][o] = temp_sort_data[p][3]
            outputs[i][o+1] = temp_sort_data[p][4]
            outputs[i][o+2] = temp_sort_data[p][5]
            p += 1
                    
    return 0

def write_to_file(inputs, outputs):
     
    for i in range(inputs.shape[0]):
        
        for m in range(0,inputs.shape[1]-1,2):
            inputs[i][m] = float("{0:.6f}".format((inputs[i][m])))
            inputs[i][m+1] = float("{0:.6f}".format((inputs[i][m+1])))
        
        for j in range(inputs.shape[1]):
            line = str(inputs[i][j])+" "
            #print(line,end="")
            fo.write(line)
        fo.write("output ")
        #print("output ", end="")
        for k in range(outputs.shape[1]):
            line2 = str(outputs[i][k])+" "
            #print(line2,end="")
            fo.write(line2)
        fo.write("\n")
        
    fo.close()
    
    return 0

def display(inputs,outputs,n):
    
    for i in range(n,n+1):
        for j in range(0, inputs.shape[1] - 1 ,2):
            plt.scatter(inputs[i][j], inputs[i][j+1])
            
    for i, txt in enumerate(range(1,(inputs.shape[1]+2) // 2)):
        p = i*2
        plt.annotate(txt, (inputs[n][p], inputs[n][p+1]))
        
    plt.show()
    
    return 0

if __name__ == '__main__':
    
    with open(file_name, 'r') as file:
        recs = file.readlines()
        
        inputs = []
        outputs= []
        
        for rec in recs:
            rec = rec.rstrip(' \n')
            inp, outp = rec[:].split(' output ')
            
            inp = inp.split(' ')
            outp = outp.split(' ')
            
            temp_input = []
            for t in inp:
                temp_input.append(float(t))
            inputs.append(temp_input)
            
            temp_output = []
            for k in outp:
                temp_output.append(int(k) + 1)
            outputs.append(temp_output)
            
    inputs = np.asarray(inputs)
    outputs = np.asarray(outputs)
    
    displace(inputs,outputs)
    normalize2(inputs,outputs)
    sort(inputs,outputs)
    write_to_file(inputs,outputs)
    display(inputs,outputs,3)            
        
    fo.close()