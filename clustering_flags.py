# clustering_flags.py
# Author: Neha Bhagwat
# Program to extract features for flags and cluster them using single link hierarchical clustering
# This part can be implemented using the main assignment program. But this separate
# file will make it easier to see the results for flags only.
#
#
#
from PIL import Image
import re
import os
import numpy
import csv
import math
import random


def calculateDistance(featureSet1, featureSet2):
    distance = 0
    featureSet1 = featureSet1[0:48]
    featureSet2 = featureSet2[0:48]
    if(len(featureSet1)!=len(featureSet2)):
        print("Error encountered in the training data.")
        print(len(featureSet1))
        print(len(featureSet2))
    else:
        squared_distance = float(0)
        for count in range(0, len(featureSet2)):
            squared_distance = squared_distance + math.pow((int(featureSet1[count]) - int(featureSet2[count])),2)
        distance = math.sqrt(squared_distance)
    return(distance)


print("Enter the path where the training files are located.")
folder_path = raw_input()
features_file = open("features_flags.csv", "w")

for path, subdirs, files in os.walk(folder_path):
    for filename in files:
        f = os.path.join(path, filename)
        # print(f)
        ext = os.path.splitext(filename)[1]
        new_hist = []
        if ext.lower().find("jpeg") != -1 or ext.lower().find("jpg") != -1:
            print("Accessing file " + str(filename) + "... \n")
            img = Image.open(f)
            img_hist = img.histogram()
                    
            for index in range(0, len(img_hist), 16):
                # print("Adding hist values for: "+filename)
                new_hist.append(sum(img_hist[index:index+15]))
            if filename.find('landscape')!= -1:
                # print("Found landscape: " + filename)
                new_hist.append(0)
            else:
                # print("Found headshot: " + filename)
                new_hist.append(1)
            # print(new_hist)                           
            for feature in new_hist:
                features_file.write('%d,' %  feature)
            features_file.write('%s' % f)
            features_file.write('\n')
features_file.close()


features_file = open("features_flags.csv", "r")
features = features_file.read()
list_of_features = []
feature_list_by_image = features.split('\n')

for count in range(0, len(feature_list_by_image)-1):
    feature_list = feature_list_by_image[count].split(",")
    list_of_features.append(feature_list[0:len(feature_list)])
features_file.close()


# elements = [[6], [12], [18], [24], [30], [42], [48]]
elements = []
for ele in list_of_features:
    elements.append([ele])
# print(elements)

minimum = 99999999
min_i = 0
min_j = 0
iter_count = 0
while(len(elements)>50):
    distances = []
    for i in range(0, len(elements)):
        temp = []
        # print(len(elements[i]))
        print("Working on it... ")
        for j in range(0, len(elements)):
            if len(elements[i])==1 and len(elements[j])==1:
                d = calculateDistance(elements[i][0],elements[j][0])
                if d == 0:
                    d = 9999999
                temp.append(d)
            elif len(elements[i]) == 1:
                temp_list = []
                for ele in elements[j]:
                    d = calculateDistance(ele, elements[i][0])
                    if d==0:
                        d = 9999999
                    temp_list.append(d)
                temp.append(min(temp_list))
            elif len(elements[j]) == 1:
                temp_list = []
                for ele in elements[i]:
                    d = calculateDistance(ele, elements[j][0])
                    if d == 0:
                        d = 9999999
                    temp_list.append(d)
                temp.append(min(temp_list))
            else:
                temp_list = []
                for ele in elements[i]:
                    for ele1 in elements[j]:
                        d = calculateDistance(ele, ele1)
                        temp_list.append(d)
                if min(temp_list) == 0:
                    temp.append(9999999)
                else:
                    temp.append(min(temp_list))
                                     
        distances.append(temp)
    # print("\n\n")
    # print distances
    # print len(distances[0])
    min_list = []
    for i in range(0, len(distances)):
        min_list.append(min(distances[i]))
    # print("min_list: " + str(min_list))
    # print("\n\n")
    minimum = min(min_list)
    # print(minimum)
    set_condition = 0
    for i in range(0, len(distances)):
        for j in range(0, len(distances)):
            if round(distances[i][j],2) == round(minimum,2):
                min_i = i
                min_j = j
                set_condition = 1
                break
        if set_condition == 1:
            break
                        
        # for j in range(0,i):
            # if minimum > distances[i][j] and distances[i][j]!=0:
                # print i
                # print j
                # print(str(minimum) + "\t" + str(distances[i][j]))
                # minimum = distances[i][j]
                # min_i = i
                # min_j = j
    # print("\n min_i: " + str(min_i))
    # print("\nmin_j: " + str(min_j))
    elements[min_i] = elements[min_i] + elements[min_j]
    elements = elements[0:min_j] + elements[min_j+1:]
    # print("elements[min_i]" + " " + str(elements[min_i]))
    iter_count += 1
    print("Iteration number: ")
    print(iter_count)

for ele in elements:
    print("\n\n\n")
    print ele
