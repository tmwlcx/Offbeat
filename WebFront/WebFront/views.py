from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import numpy as np
import sys
import pymysql
import sqlalchemy
# transform data to json for sending to front end when using d3
import json
import os
import random
from collections import defaultdict
from sklearn import preprocessing
from joblib import load
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from scipy.spatial import distance_matrix

def get_centers(level1_cluster_size=3800):
    assert type(level1_cluster_size) == int
    query = """
            SELECT *
            FROM centroids
            LIMIT {}
            """.format(level1_cluster_size)
    centers = pd.read_sql(query, conn)
    return centers

def get_distance_matrix(centers):
    centers_arr = centers.values[:,1:8]
    return distance_matrix(centers_arr, centers_arr)

conn = pymysql.connect('35.196.88.209', 'teameleven', 'dbpassword', 'SPOTIFY')
centers = get_centers()
distances = get_distance_matrix(centers)

def get_top_cluster(centroid_id):
    query = """
            SELECT distinct(level3) as level3
            FROM songs_labeled
            WHERE level0 = '{}'
            """.format(centroid_id)
    pt_data = pd.read_sql(query, conn)
    return pt_data

def get_fourth_cluster(string_list):
    query = """
            SELECT distinct(level0)
            FROM songs_labeled
            WHERE level3 IN ({})
            """.format(string_list)
    pt_data = pd.read_sql(query, conn)
    return pt_data

def get_child_cluster(string_list):
    query = """
            SELECT *
            FROM songs_labeled
            WHERE level3 IN ({})
            """.format(string_list)
    pt_data = pd.read_sql(query, conn)
    return pt_data

def list_transform(single_column_frame):
    string_list = single_column_frame[single_column_frame.columns[0]].tolist()
    string_list = ', '.join(["'" +str(x) + "'" for x in string_list])
    return string_list


def get_closest_centroid(centers, user_data):
    return np.argmin(np.linalg.norm(centers.values[:,1:9] - user_data, axis=1, ord=2))


def get_centroid_values(list_of_vals):
    query = """
            SELECT *
            FROM centroids
            WHERE centroid_id IN ({})
            """.format(list_of_vals)
    frame = pd.read_sql(query, conn)
    return frame

def get_point_data(centroid_id):
    query = """
            SELECT *
            FROM songs_labeled
            WHERE level0 = '{}'
            """.format(centroid_id)
    pt_data = pd.read_sql(query, conn)
    return pt_data

def collapse_columns(dataframe):
    Important_Set = set(list(dataframe['level0']))
    for x in list(dataframe['level1']):
        Important_Set.add(x)
    for x in list(dataframe['level2']):
        Important_Set.add(x)
    for x in list(dataframe['level3']):
        Important_Set.add(x)
    return Important_Set

def list_transform(single_column_frame):
    string_list = single_column_frame[single_column_frame.columns[0]].tolist()
    string_list = ', '.join(["'" +str(x) + "'" for x in string_list])
    return string_list

def Home(request):
	return render(request, 'index.html')

@csrf_exempt
def Path_to_Data(request):
	data = json.loads(request.body)
	qt = load(os.path.join(settings.BASE_DIR, r"static\.pickle"))
	data = np.array(list(data["Values"].values()))
	user_data = qt.transform(data.reshape(1,-1))
	centroid = get_closest_centroid(centers, user_data)
	song = get_point_data(centroid)


	lvl3 = get_top_cluster(song)
	srtnow = list_transform(lvl3)
	lvl1 = get_fourth_cluster(srtnow)
	maximum_points = 1000

	limiter = maximum_points // len(lvl1)

	children = get_child_cluster(srtnow)

	set_vals = collapse_columns(children)

	centers = get_centroid_values(', '.join(["'" +str(x) + "'" for x in set_vals]))

	nested_data = {}
	nested_data["Id"] = int(lvl3.iloc[0:1, 0:1].values[0][0])
	nested_data["features"] = qt.inverse_transform(centers[centers["centroid_id"]==int(nested_data["Id"])].values.tolist()[0][1:])
	nested_data["Children"] = []
	for val in set(children['level2']):
		temp = {}
		temp['Id'] = int(val)
		temp["features"] = qt.inverse_transform(centers[centers["centroid_id"]==int(temp["Id"])].values.tolist()[0][1:])
		temp['Children'] = []
		nested_data["Children"].append(temp)

	next_level = children[['level1', 'level2']]
	next_level.drop_duplicates(inplace=True)

	for discard, song_vals1 in next_level.iterrows():
		temp = {}
		temp['Id'] = int(song_vals1['level1'])
		temp["features"] = qt.inverse_transform(centers[centers["centroid_id"]==int(temp["Id"])].values.tolist()[0][1:])
		temp['Children'] = []
		for dict1 in nested_data["Children"]:
			if dict1["Id"] == song_vals1['level2']:
				dict1["Children"].append(temp)

	next_level = children[['level0', 'level1']]
	next_level.drop_duplicates(inplace=True)

	for discard, song_vals1 in next_level.iterrows():
		temp = {}
		temp['Id'] = int(song_vals1['level0'])
		temp["features"] = qt.inverse_transform(centers[centers["centroid_id"]==int(temp["Id"])].values.tolist()[0][1:])
		temp['Children'] = []
		for dict1 in nested_data["Children"]:
			for dict2 in dict1["Children"]:
				if dict2["Id"] == song_vals1['level1']:
					dict2["Children"].append(temp)

	next_level = children[['song_id', 'level0']]
	next_level.drop_duplicates(inplace=True)

	for discard, song_vals1 in next_level.iterrows():
		temp = {}
		temp['Id'] = song_vals1['song_id']
		for dict1 in nested_data["Children"]:
			for dict2 in dict1["Children"]:
				for dict3 in dict2["Children"]:
					if dict3["Id"] == song_vals1['level0']:
						dict3["Children"].append(temp)

	#path = os.path.join(settings.BASE_DIR, r"static\test_songs_sample_1k.json")
	#data = json.loads(open(path).read())
	#data = json.dumps(nested_data, safe=False)
	return JsonResponse(nested_data)
