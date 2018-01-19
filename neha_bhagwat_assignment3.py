# neha_bhagwat_assignment3.py
# Author: Neha Bhagwat (SJSU ID: 012412140)
# Last updated: October 17, 2017
# Program for assignment 3 of CS256 - Section 2
#
# 
#
# To be added: Not to create the features file if it already exists.


from PIL import Image
import re
import os
import numpy
import csv
import math
import random
try:
    import pygraph
    import matplotlib
    import matplotlib.pyplot as plt
except ImportError:
    print("No Module found. Graphs will not be created.")

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

def findCentroid(cluster_elements):
    # print len(cluster_elements)
    # print(len(cluster_elements[0]))
    sum = []
    for integer in range(0,len(cluster_elements[0])-1):
        sum.append(0)
    for count in range(0,len(cluster_elements)):
        # print("in for loop 2")
        for index in range(0,len(sum)):
            sum[index] = sum[index] + int(cluster_elements[count][index])
    for index in range(0,len(sum)):
        sum[index] = sum[index]/len(cluster_elements)
    # print("Sum: " + str(sum))
    return sum

class singleLinkClustering:
    def __init__(self):
        print("Implementing Single Link Hierarchical Clustering: ")

    def find_clusters(self):
        features_file = open("features.csv", "r")
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
        while(len(elements)>2):
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
        cluster_count = 0
        for ele in elements:
            print("Cluster "+ str(cluster_count) + ": ")
            print("\n\n\n")
            for image_details in ele:
                print(image_details[49])
            cluster_count += 1
    
class kMeansClustering:
    def __init__(self):
        print("Implementing K means clustering: ")

    def find_clusters(self):
        features_file = open("features.csv", "r")
        features = features_file.read()
        list_of_features = []
        feature_list_by_image = features.split('\n')
        for count in range(0,len(feature_list_by_image)-1):
            feature_list = feature_list_by_image[count].split(",")
            list_of_features.append(feature_list[0:len(feature_list)])
        features_file.close()
        # Randomly choose 2 cluster centroids
        centroid1_index = random.randint(0,len(list_of_features)-1)
        while(True):
            centroid2_index = random.randint(0,len(list_of_features)-1)
            # Make sure that centroid 2 is not the same as centroid 1
            if centroid1_index != centroid2_index:
                break

        centroid1_distances = {}
        centroid2_distances = {}

        for count in range(0,len(list_of_features)):
            centroid1_distances.update({count:calculateDistance(list_of_features[centroid1_index][0:48],list_of_features[count][0:48])})
            centroid2_distances.update({count:calculateDistance(list_of_features[centroid2_index][0:48],list_of_features[count][0:48])})
        cluster1 = []
        cluster2 = []
        for count in range(0,len(list_of_features)):
            # print(str(centroid1_distances[count])+"\t-\t"+str(centroid2_distances[count]))
            if centroid1_distances[count] > centroid2_distances[count]:
                # print("in cluster 2")
                cluster2.append(list_of_features[count])
            else:
                # print("in cluster 1")
                cluster1.append(list_of_features[count])
        old_centroid1 = list_of_features[centroid1_index][0:48]
        old_centroid2 = list_of_features[centroid2_index][0:48]
        new_centroid1 = findCentroid(cluster1)
        new_centroid2 = findCentroid(cluster2)
        # print(new_centroid1)
        # print(new_centroid2)
        iter_count = 0
        while(new_centroid1 != old_centroid1 and new_centroid2 != old_centroid2):
            old_centroid1 = new_centroid1
            old_centroid2 = new_centroid2
            centroid1_distances = {}
            centroid2_distances = {}
            for count in range(0,len(list_of_features)):
                centroid1_distances.update({count:calculateDistance(old_centroid1,list_of_features[count][0:48])})
                centroid2_distances.update({count:calculateDistance(old_centroid2,list_of_features[count][0:48])})
            # print("Centroid 1 distances: " + str(centroid1_distances))
            # print("Centroid 2 distances: " + str(centroid2_distances))
            cluster1 = []
            cluster2 = []
            for count in range(0,len(list_of_features)):
                # print(str(centroid1_distances[count])+"\t-\t"+str(centroid2_distances[count]))
                if centroid1_distances[count] > centroid2_distances[count]:
                    # print("in cluster 2")
                    cluster2.append(list_of_features[count])
                else:
                    # print("in cluster 1")
                    cluster1.append(list_of_features[count])
            # print("new cluster 1: " + str(cluster1))
            # print("new cluster 2: " + str(cluster2))
            new_centroid1 = findCentroid(cluster1)
            new_centroid2 = findCentroid(cluster2)
            # print("new centroid 1: "+ str(new_centroid1))
            # print("new centroid 2: " +str(new_centroid2))
            # print("Iteration: " + str(iter_count))
            iter_count +=1

        print("\n\nCluster 1: ")
        for ele in cluster1:
            print(ele[49])
        print("\n\nCluster 2: ")
        for ele in cluster2:
            print(ele[49])
        
        
class Agent:
    def __init__(self, features_file):
        print("File opened")
        self.features = features_file.read()
        
    def agent_function(self):
        print("Enter the value of k.")
        k = input()
        print("Enter the path of the image file.")
        input_image_path = raw_input()
        print("Accessing input image... \n")
        img = Image.open(input_image_path)
        img_hist = img.histogram()
        new_hist = []            
        for index in range(0, len(img_hist), 16):
            # print("Adding hist values for: "+filename)
            new_hist.append(sum(img_hist[index:index+15]))
        print("new_hist: "+str(new_hist))
        distances = {}        
        features = self.features
        # print(features)
        feature_list_by_image = features.split('\n')
        for count in range(0,len(feature_list_by_image)-1):
            feature_list = feature_list_by_image[count].split(",")
            feature_list = feature_list[0:len(feature_list)-1]
            distance = calculateDistance(feature_list[0:len(feature_list)-1],new_hist)
            distances.update({count:distance})
        # print(distances)
        sorted_distances = sorted(distances.items(), key=lambda x:x[1])
        class0 = 0
        class1 = 0
        for dict_entry in sorted_distances[0:k]:            
            if(feature_list_by_image[dict_entry[0]][48]==0):
                class0+=1
            else:
                class1+=1
        if class0>class1:
            return 0
        else:
            return 1

            
class Environment:
    def print_menu():
        print("Please enter the number corresponding to the next step you want to implement.")
        print("1. Show the training file.")
        print("2. Implement kNN on a new image.")
        print("3. Implement 3 fold cross validation and print results.")
        print("4. Implement k means clustering and print results.")
        print("5. Implement single link hierarchical clustering and print results.")
        print("6. Quit.")

    def cv_training(list_of_files):
        total_train_hist = []
        for file in list_of_files:
            img = Image.open(file)
            train_img_hist = img.histogram()
            train_hist = []  
            for index in range(0, len(train_img_hist), 16):
                # print("Adding hist values for: "+file)
                train_hist.append(sum(train_img_hist[index:index+15]))
            if file.find('landscape')!= -1:
                # print("Found landscape: " + file)
                train_hist.append(0)
            else:
                # print("Found headshot: " + file)
                train_hist.append(1)
            total_train_hist.append(train_hist)
            # print(new_hist)
        return total_train_hist

    def cv_testing(total_test_hist, total_train_hist,k):
        accurate_predictions = 0
        for image_hist in total_test_hist:
            distance_of_images = {}
            for train_hist in total_train_hist:
                dist = calculateDistance(train_hist[0:len(train_hist)-1], image_hist[0:len(image_hist)-1])
                # Add the distance with class to the dictionary distance_of_images.
                distance_of_images.update({train_hist[48]:dist})
            # Sort the dictionary according to the distances
            sorted_dict = sorted(distance_of_images.items(), key=lambda x:x[1])
            # Find predicted class
            class0 = 0
            class1 = 0
            predicted = 0
            for key,val in sorted_dict[0:k]:
                if key == 0:
                    class0 +=1
                else:
                    class1 +=1
            if class0>class1:
                predicted = 0
            else:
                predicted = 1
            
            # Compare with actual class
            # Add to correct predictions if predicted class if same as actual class
            if image_hist[48] == predicted:
                accurate_predictions = accurate_predictions + 1
            
        # Calculate accuracy
        accuracy = float(accurate_predictions * 100) / len(total_test_hist)
        return accuracy
        

    def print_training_file():
        with open("features.csv", 'rU') as f:  #opens PW file
            reader = csv.reader(f)
            features = list(list(rec) for rec in csv.reader(f, delimiter=','))
            for feature in features:
                print(feature[0:len(feature)-1])
                print("\n")
        f.close()
        
    # ********************************************************************************************************
    # Feature Extraction of training data set
    # features_file = open("features.csv", "w")
    # folder_path = "C:\\Users\\bhagw\\Desktop\\SJSU - SEM I\\Topics_in_AI\\Homework Documents\\Assignment3\\Trial1"
    print("Enter the path where the training files are located.")
    folder_path = raw_input()
    
    features_file = open("features.csv", "w")

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
    # ********************************************************************************************************

    
    features_file = open("features.csv", "r")
    menu_option = 0
    while(menu_option != 6):
        print_menu()
        menu_option = input()
        # ********************************************************************************************************
        # Menu Option to print training file was selected:
        if(menu_option == 1):
            print_training_file()

        # ********************************************************************************************************
        # Menu Option to implement kNN was selected:
        elif(menu_option == 2):
            features_file = open("features.csv", "rU")
            knn_implementation = Agent(features_file)
            predicted_class = knn_implementation.agent_function()
            if(predicted_class == 0):
                print("Image is a landscape")
            elif(predicted_class == 1):
                print("Image is a headshot")
            features_file.close()

        # ********************************************************************************************************
        # Menu option to implement 3 fold cross validation was selected:
        elif(menu_option == 3):
            # validation_folder_path = "C:\\Users\\bhagw\\Desktop\\SJSU - SEM I\\Topics_in_AI\\Homework Documents\\Assignment3\\Trial"
            print("Enter the folder path where images for 3 fold validation are located.")
            folder_path = raw_input()
            files_list = []
            for path, subdirs, files in os.walk(folder_path):
                for filename in files:
                    f = os.path.join(path, filename)
                    # print(f)
                    ext = os.path.splitext(filename)[1]
                    if ext.lower().find("jpeg") != -1 or ext.lower().find("jpg") != -1:
                        files_list.append(f)
            files_list = random.sample(files_list, len(files_list))
            bound1 = int(len(files_list)/3)
            bound2 = int((2*len(files_list))/3)
            set1 = files_list[0:bound1]
            # print(set1)
            set2 = files_list[bound1:bound2]
            # print(set2)
            set3 = files_list[bound2:len(files_list)]
            # print(set3)
            k = 1
            accuracy = []
            list_of_accuracies = []
            list_of_k = []
            for k in range(1,10,2):
                list_of_k.append(k)
                print("\nComputing accuracy for k = " + str(k) + "\n")
                # Cross validation: Fold 1
                total_train_hist = cv_training(set1 + set2)
                total_test_hist = cv_training(set3)
                accuracy1 = cv_testing(total_train_hist, total_test_hist, k)
                accuracy.append(accuracy1)
                try:
                    plt.plot(k, accuracy1, 'o')
                except:
                    print("Unexpected error.")
                print("Accuracy for fold 1: " + str(accuracy1))
                # Cross validation: Fold 2
                total_train_hist = cv_training(set2 + set3)
                total_test_hist = cv_training(set1)
                accuracy2 = cv_testing(total_train_hist, total_test_hist, k)
                accuracy.append(accuracy2)
                try:
                    plt.plot(k, accuracy2, 'o')
                except:
                    print("Unexpected error.")
                print("Accuracy for fold 2: " + str(accuracy2))
                # Cross validation: Fold 3
                total_train_hist = cv_training(set3 + set1)
                total_test_hist = cv_training(set2)
                accuracy3 = cv_testing(total_train_hist, total_test_hist, k)
                accuracy.append(accuracy3)
                try:
                    plt.plot(k, accuracy3, 'o')
                except:
                    print("Unexpected error.")
                print("Accuracy for fold 3: " + str(accuracy3))
                list_of_accuracies.append(accuracy)
                # ************************************************************************************************
                # Graph creation code
                try:
                    plt.title("Plot of K values v/s fold wise accuracy")
                    plt.xlabel("Values of K")
                    plt.ylabel("Accuracy (in %)")
                    plt.show()
                    plt.savefig(str(k) + '_graph')
                except:
                    print('Graph could not be plotted')
                # ************************************************************************************************
        # ********************************************************************************************************
        # Menu option to implement k means clustering was selected:
        elif(menu_option == 4):
            clustering_object = kMeansClustering()
            clustering_object.find_clusters()
        # ********************************************************************************************************
        # Menu option to implement single link hierarchical clustering was selected:
        elif(menu_option == 5):
            single_link_object = singleLinkClustering()
            single_link_object.find_clusters()
        # ********************************************************************************************************
        # Menu option to quit was selected:
        elif(menu_option == 6):
            print("Quitting the program...")
            break
        # ********************************************************************************************************
        else:
            print("Please enter an appropriate menu option.")
        
