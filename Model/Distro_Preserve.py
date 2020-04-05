# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 09:17:34 2020

@author: j68452
"""

import pandas as pd
import numpy as np
import copy
import matplotlib.pyplot as plot
import glob
import os
import json
from collections import defaultdict

disc_directory = r'C:\temp\Cluster_Compute'

tbl_id = 'song_id'
attribs = [tbl_id, 'artist_id', 'album_id', 'track_href']
features = [tbl_id, 'time_signature', 'danceability', 'energy', 'musical_key', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
# size to divide space into
Manual_Partitions = {'time_signature' : [1,2,3,4,5],
                     'musical_key' : [0,1,2,3,4,5,6,7,8,9,10,11]}

Removed_Partitions = {'mode' : [0,1]}

Data_Length_Estimate = 3000000
target_bin_size = 50


# Enter Path to target file.
Partitions = glob.glob(disc_directory+r'//Values_Only//ValsCleaned_Partition*.csv')
# Use when restarting from partial progress
Restart = True

if not Restart:
    try:
        del dim_checks
    except:
        pass
    try:
        del ceilings
    except:
        pass
    try:
        del Bins
    except:
        pass
    try:
        del Intersects
    except:
        pass
    try:
        del approx_bins
    except:
        pass
    try:
        del Dividers
    except:
        pass
    try:
        del Key_Conglomerate
    except:
        pass

def Get_Manual_Partitions_Divisions(Dictionary):
    Total_Combinations = 1
    for key, val in Dictionary.items():
        Total_Combinations *= len(val)
    return Total_Combinations

def Get_Remaining_Partitions(dim_checks, Manual_Partitions):
    Remaining_Dimensions = 0
    for key in dim_checks.keys():
        if key in Manual_Partitions.keys():
            pass
        else:
            Remaining_Dimensions +=1
    return Remaining_Dimensions

def Find_Even_Partition_Value(Manual_Partitions_Divisions, Remaining_Dimensions, Data_Length_Estimate, target_bin_size):
    Test_Val = 0
    current_test = target_bin_size + 1
    while current_test > target_bin_size:
        Test_Val += 1
        current_test = Data_Length_Estimate / (Manual_Partitions_Divisions * Test_Val**Remaining_Dimensions)
    return Test_Val - 1

def Locator(row_val, ceilings):
    address = []
    for index, vals in row_val.items():
        if index != 'song_id':
            cp = copy.deepcopy(ceilings[index])
            cp.append(vals); cp.sort()
            address.append(cp.index(vals))
            del cp
    return address

def Address_Name_Builder(Address):
    return '.'.join([str(x) for x in Address])

if 'dim_checks' not in locals():
    dim_checks = {}
    if len(Partitions) !=0:
        for part in Partitions:
            temp = pd.read_csv(part)
            temp.columns = features
            for column in features:
                if column not in (tbl_id):
                    try:
                        old_min = dim_checks[column][0]
                        old_max = dim_checks[column][1]
                    except:
                        old_min = 1000000000
                        old_max = 0
                    new_min = min(temp[column])
                    new_max = max(temp[column])
                    # Create a new record
                    dim_checks[column] = [min(old_min, new_min), max(old_max, new_max)]
                    # cast to Float for easy viewing
                    dim_checks[column][0] = float(dim_checks[column][0])
                    dim_checks[column][1] = float(dim_checks[column][1])

        print("Field Dimension Checks created")

if 'ceilings' not in locals():
    # Use Manual Partitions Dictionary to determine how many subsets these create
    Manual_Partitions_Divisions = Get_Manual_Partitions_Divisions(Manual_Partitions)
    # Use Manual Partitions dictionary to determin how many dimensions are left for subsetting
    Remaining_Dimensions = Get_Remaining_Partitions(dim_checks, Manual_Partitions)
    # Use Previous data to determine a generic partition count in each dimension that targets the target_bin_size
    subset_factor = Find_Even_Partition_Value(Manual_Partitions_Divisions, Remaining_Dimensions, Data_Length_Estimate, target_bin_size)

    ceilings = {}
    if len(dim_checks) != 0:
        for column, val in dim_checks.items():
            # Includes special handling for discrete values. Is now with respect to distribution
            if column in Manual_Partitions.keys():
                ceilings[column] = Manual_Partitions[column]
            else:
                s = subset_factor
                step_val = (val[1] - val[0]) / s
                ceilings[column] = []
                for x in range(0, s):
                    ceilings[column].append(val[0] + step_val * x)
                ceilings[column].append(val[1])

if 'Bins' not in locals():
    Bins = {}
    if len(Partitions) !=0:
        print("Creating Bins")
        for part in Partitions:
            Values = pd.read_csv(part)
            Values.columns = features

            for key, val in ceilings.items():
                Bins[key] = dict((x, 0) for x in val)

            for key, val in ceilings.items():
                for x in Values[key]:
                    cp = copy.deepcopy(ceilings[key])
                    cp.append(x); cp.sort()
                    addr = cp.index(x)
                    lower = cp[addr - 1]
                    upper = cp[addr + 1]
                    xis = ((x - upper)/ (lower - upper))
                    yis = (1 - ((x - upper)/ (lower - upper)))
                    Bins[key][lower] += xis
                    Bins[key][upper] += yis
                    del cp


    for key, val in Bins.items():
        Bins[key] = {x:y for x,y in val.items() if y!=0}

    for key, val in ceilings.items():
        ceilings[key] = [x for x in val if x in Bins[key].keys()]

if 'Intersects' not in locals():
    Intersects = {}
    print("Calculating Intersects")
    for key, val in ceilings.items():
        Intersects[key] = []
        for i in range(0, len(val)-1):
            lower = ceilings[key][i]
            upper = ceilings[key][i+1]
            lower_val = Bins[key][lower]
            upper_val = Bins[key][upper]
            Intersects[key].append((lower * lower_val/(lower_val + upper_val)) + (upper * upper_val/(lower_val + upper_val)))

if 'approx_bins' not in locals():
    approx_bins = {}
    print("Approximating new Bins")
    for key, val in Bins.items():
        total_points = sum(val.values())
        approx_bins[key] = [val1 / total_points for key1, val1 in val.items()]

if 'Dividers' not in locals():
    Dividers = {}
    print("Inserting Dividers")
    for key, val in approx_bins.items():
        divisor = 1 / len(Intersects[key])
        Dividers[key] = [ceilings[key][0], ceilings[key][-1]]
        hold = copy.deepcopy(approx_bins[key])
        remainder = 0
        for index, val1 in enumerate(hold[0:(len(hold)-1)]):
            num = int((val1 + remainder) / divisor)
            remainder = (val1 + remainder) % divisor
            #hold[index + 1] += remainder
            if num != 0:
                for parts in range(1, num+1):
                    Dividers[key].append(Intersects[key][index]/num * parts)
        Dividers[key].sort()

#Assign Points to test

Val_test_assignments_list = Values

if 'Key_Conglomerate' not in locals():
    Key_Conglomerate = {}
    print("Building Key_Congolmerate")
    for part in Partitions:
        Values = pd.read_csv(part)
        Values.columns = features
        Assignments = []
        for discard, vals in Values.iterrows():
            save = list(vals)
            Assignment = Address_Name_Builder(Locator(vals, Dividers))
            Assignments.append(Assignment)
            try:
                current_count = Key_Conglomerate[Assignment][0]
                current_vals = Key_Conglomerate[Assignment][1]
            except:
                current_count = 0
                current_vals = [0,0,0,0,0,0,0,0,0,0,0,0.0]
            Key_Conglomerate[Assignment] = [current_count+1, [(x+y*current_count)/(current_count+1) for x, y in zip(save[1:], current_vals)]]


        Values['OutValues'] = Assignments

        Values.to_csv('{}\Parsed\Test_Data_Parsed_{}'.format(os.path.dirname(part),os.path.basename(part)), index=False)


with open('Feature Dimensions.txt', 'w') as outfile:
    json.dump(dim_checks, outfile)
with open('Feature Ceilings.txt', 'w') as outfile:
    json.dump(ceilings, outfile)
with open('Feature Bins.txt', 'w') as outfile:
    json.dump(Bins, outfile)
with open('Feature Intersects.txt', 'w') as outfile:
    json.dump(Intersects, outfile)
with open('Feature Bin Estimates.txt', 'w') as outfile:
    json.dump(approx_bins, outfile)
with open('Feature Final Dividers.txt', 'w') as outfile:
    json.dump(Dividers, outfile)

#Key_Conglomerate_JSON = json.loads(json.dumps(Key_Conglomerate))
