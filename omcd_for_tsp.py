# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 17:07:20 2021

@author: amill
"""
#attempt at using OMCD for travelling salesman problem 

import time 
start = time.time()
import numpy as np 
import matplotlib.pyplot as plt 
import math as math 
import random as random 

#coords_list = [(6, 9), (10, 4), (11, 6), (5, 12), (1, 1), (4, 2), (5, 2), (6, 4), (4, 4), (3, 6), (1, 5), (2, 3), (7, 2), (12, 14), (1, 13), (9, 11), (13, 9)]
coords_list = [(1, 1), (4, 2), (5, 2), (6, 4), (4, 4), (3, 6), 
               (1, 5), (2, 3)]

d0 = len(coords_list)

x = []
y = []
for i in range(len(coords_list)):
    x.append(coords_list[i][0])
for j in range(len(coords_list)):
    y.append(coords_list[j][1])


#creating plot of points (places)
plt.scatter(x, y)
plt.show()

initial_total_distance = 0
for i in range(len(coords_list)-1):
    delta_x=(coords_list[i][0]-coords_list[i+1][0])**2
    delta_y=(coords_list[i][1]-coords_list[i+1][1])**2
    initial_total_distance += math.sqrt(delta_x + delta_y)

print('The initial distance of the system is: ' + str(initial_total_distance))

medium_coords_list = coords_list.copy()
medium_total_distance = initial_total_distance
#counting the acceptance and rejection ratio of the system 
acceptance = 0
rejection = 0
number_rejections_this_round = 0 
rejections_limit = 100000

#creating a list of indexes to randomly 
indexes = []
for t in range(len(coords_list)):
    indexes.append(t)
    
minimum_distance = [initial_total_distance]

while d0>0:
    #create function which swaps around a certain portion of the the indices 
    #need to create an array of shuffle and no-shuffle indexes 
    current_coords_list = medium_coords_list
    for _ in range(d0):
        a, b = random.randint(0, len(current_coords_list)-1), random.randint(0, len(current_coords_list)-1) # pick two random indexes
        current_coords_list[b], current_coords_list[a] = current_coords_list[a], current_coords_list[b] # swap the values at those indexes
    
    current_total_distance = 0
    
    #calculating energy of this new list 
    for i in range(len(current_coords_list)-1):
        delta_x=(current_coords_list[i][0]-current_coords_list[i+1][0])**2
        delta_y=(current_coords_list[i][1]-current_coords_list[i+1][1])**2
        current_total_distance += math.sqrt(delta_x + delta_y)
    
    if current_total_distance <= medium_total_distance:
        medium_total_distance = current_total_distance
        medium_coords_list = current_coords_list
        acceptance += 1
        minimum_distance.append(medium_total_distance)
        
    else: 
        rejection += 1
        number_rejections_this_round += 1
        
    if number_rejections_this_round == rejections_limit:
        d0 = d0-1
        print('To many rejections in a row, lets try lowering the number to see if that works. The new value of d0 is ' + str(d0))
        number_rejections_this_round = 0
        if d0 == 0:
            print('d0 will not go any lower mate, gonna have to stop here.')
            break

x = []
y = []
for i in range(len(coords_list)):
    x.append(medium_coords_list[i][0])
for j in range(len(coords_list)):
    y.append(medium_coords_list[j][1])

for i in range(0, len(x)):
    plt.plot(x[i:i+2], y[i:i+2], 'ro-')
plt.show()

print('The initial total distance from the coordinates given is: ' + str(initial_total_distance))
print('The final total_distance for the shortest route of this system is: ' + str(medium_total_distance))        
print('The optimal travel route for the current parameters are: ' + str(medium_coords_list))
plt.plot(minimum_distance)
plt.show()
print('The number of acceptances was ' + str(acceptance) + ' and the number of rejections was ' + str(rejection))
print('so our ratio of accepted to total number of attempted moves is ' + str(acceptance*100/(acceptance + rejection)) + '%')
print('Our value of d0 is currently: ' + str(d0))
end = time.time()
print('This program took ' + str(end-start) + ' to run.')
