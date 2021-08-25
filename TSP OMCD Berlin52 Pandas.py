# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 17:36:57 2021

@author: amill
"""

#%%
import time 
import numpy as np #even though we are not using this at the moment, we need it later to vectorize the code and make it more efficient 
import matplotlib.pyplot as plt 
import math as math 
import random as random 
import os
import pandas as pd 


#%%
#creating columns for the dataframe 
data = {'Initial Configuration': [], 'Final Configurartion': [], 'Accepted Moves': [], 
        'Final Distance': [], 'Acceptance Ratio': [], 'Attempted Moves': [], 'Computation Time': []}

#dataframe that will be updated 
results = pd.DataFrame(data)

#%%
#file that uses OMCD to try and solve for the optimal minimal distance based off the berlin.tsp file. Filing opening data used from a stackoverflow question. 
# =============================================================================
# cwd = os.getcwd()  # Get the current working directory (cwd)
# files = os.listdir(cwd)  # Get all the files in that directory
# print("Files in %r: %s" % (cwd, files))
# =============================================================================
start = time.time()

samples = 1

for xn in range(samples):
    sample_start = time.time()
    # Open input file
    infile = open('berlin52.tsp', 'r')
    
    # Read instance header
    Name = infile.readline().strip().split()[1] # NAME
    FileType = infile.readline().strip().split()[1] # TYPE
    Comment = infile.readline().strip().split()[1] # COMMENT
    Dimension = infile.readline().strip().split()[1] # DIMENSION
    EdgeWeightType = infile.readline().strip().split()[1] # EDGE_WEIGHT_TYPE
    infile.readline()
    
    # Read node list
    nodelist = []
    N = int(Dimension)
    for i in range(0, int(Dimension)):
        x,y = infile.readline().strip().split()[1:]
        nodelist.append([float(x), float(y)])
    
    # Close input file
    infile.close()
    
    #print(nodelist)
    
    #d0 = len(nodelist)
    #d0 = math.ceil(math.log(len(nodelist))) #used this based off the advice of Professor Kuehn 
    d0 = math.ceil(len(nodelist)/2)
    
    x = []
    y = []
    for i in range(len(nodelist)):
        x.append(nodelist[i][0])
    for j in range(len(nodelist)):
        y.append(nodelist[j][1])
    
    
    #creating plot of points (places)
    plt.scatter(x, y)
    plt.show()
    
    initial_total_distance = 0
    for i in range(len(nodelist)-1):
        delta_x=(nodelist[i][0]-nodelist[i+1][0])**2
        delta_y=(nodelist[i][1]-nodelist[i+1][1])**2
        initial_total_distance += math.sqrt(delta_x + delta_y)
    delta_x = (nodelist[-1][0]-nodelist[0][0])**2
    delta_y = (nodelist[-1][1]-nodelist[0][1])**2
    initial_total_distance += math.sqrt(delta_x + delta_y)
    #print('The initial distance of the system is: ' + str(initial_total_distance))

    medium_nodelist = nodelist.copy()
    medium_total_distance = initial_total_distance
    #counting the acceptance and rejection ratio of the system 
    acceptance = 0
    rejection = 0
    number_rejections_this_round = 0 
    rejections_limit = 1000000
    
    #creating a list of indexes to randomly 
    indexes = []
    for t in range(len(nodelist)):
        indexes.append(t)
    
    d0_acceptance_value = []
    energy_change = []
    minimum_distance = [initial_total_distance]
    
    while d0>1: #changed to 1 because when we only have 1 city left to swap, nothing will swap 
        #create function which swaps around a certain portion of the the indices 
        #need to create an array of shuffle and no-shuffle indexes 
        current_nodelist = medium_nodelist.copy()
        for _ in range(d0):
            a, b = random.randint(0, len(current_nodelist)-1), random.randint(0, len(current_nodelist)-1) # pick two random indexes
            current_nodelist[b], current_nodelist[a] = current_nodelist[a], current_nodelist[b] # swap the values at those indexes
        
        current_total_distance = 0
        
        #calculating energy of this new list 
        for i in range(len(current_nodelist)-1):
            delta_x=(current_nodelist[i][0]-current_nodelist[i+1][0])**2
            delta_y=(current_nodelist[i][1]-current_nodelist[i+1][1])**2
            current_total_distance += math.sqrt(delta_x + delta_y)
        delta_x = (current_nodelist[-1][0]-current_nodelist[0][0])**2
        delta_y = (current_nodelist[-1][1]-current_nodelist[0][1])**2
        current_total_distance += math.sqrt(delta_x + delta_y)
        
        if current_total_distance <= medium_total_distance:
            energy_change.append(abs(current_total_distance - medium_total_distance))
            medium_total_distance = current_total_distance
            medium_nodelist = current_nodelist
            acceptance += 1
            minimum_distance.append(medium_total_distance)
            d0_acceptance_value.append(d0)
            #print('Success! We have optimized it further and the new shortest distance is ' + str(medium_total_distance))
            #print('This happened at value of d0 = ' + str(d0))
            
        else: 
            rejection += 1
            number_rejections_this_round += 1
            
        if number_rejections_this_round == rejections_limit:
            d0 = d0-1
            #print('To many rejections in a row, lets try lowering the number to see if that works. The new value of d0 is ' + str(d0))
            number_rejections_this_round = 0
            if d0 == 0:
                #print('d0 will not go any lower mate, gonna have to stop here.')
                break
    
    x = []
    y = []
    for i in range(len(nodelist)):
        x.append(medium_nodelist[i][0])
    for j in range(len(nodelist)):
        y.append(medium_nodelist[j][1])
    
    for i in range(0, len(x)):
        plt.plot(x[i:i+2], y[i:i+2], 'ro-')
    plt.show()
    
    plt.scatter(d0_acceptance_value, energy_change)
    plt.title('Change in energy vs value of move class when move is accepted')
    plt.ylabel("Change in Energy")
    plt.xlabel("Value of d0 when energy changes")
    plt.show()
    
    #print('The initial total distance from the coordinates given is: ' + str(initial_total_distance))
    plt.plot(minimum_distance)
    plt.show()
    print('The number of acceptances was ' + str(acceptance) + ' and the number of rejections was ' + str(rejection))
    print('so our ratio of accepted to total number of attempted moves is ' + str(acceptance*100/(acceptance + rejection)) + '%')
    #print('Our value of d0 is currently: ' + str(d0))
    #print('The optimal travel route for the current parameters are: ' + str(medium_nodelist))
    print('The final total_distance for the shortest route of this system is: ' + str(medium_total_distance))        
    end = time.time()
    sample_end = time.time()
    #adding the new data to the dataframe 
    new_row = {'Initial Configuration': nodelist, 'Final Configurartion': medium_nodelist, 'Accepted Moves': acceptance, 
            'Final Distance': medium_total_distance, 'Acceptance Ratio': acceptance*100/(acceptance + rejection), 'Attempted Moves': acceptance+rejection, 
            'Computation Time': sample_end - sample_start}
    
    #updating the dataframe with new results 
    results = results.append(new_row, ignore_index = True)
    print('Done with Sample ' + str(xn+1))

print('This program took ' + str(end-start) + ' to run.')

#%%
#creating histogram of accepted moves and
mean_final_dist = results.mean()['Final Distance']
var_final_dist = results.var()['Final Distance']
strd_dev_final_dist = math.sqrt(var_final_dist)
mean_time = results.mean()['Computation Time']
var_time = results.var()['Computation Time']
strd_dev_time = math.sqrt(var_time)
print(mean_final_dist, var_final_dist, strd_dev_final_dist)
print(mean_time, var_time, strd_dev_time)
        