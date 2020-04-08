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

def rec_dd():
    return defaultdict(rec_dd)

def get_closest_centroid(centers, user_data):
    return np.argmin(np.linalg.norm(centers.values[:,1:9] - user_data, axis=1, ord=2))

def get_distance_matrix(centers):
    centers_arr = centers.values[:,1:8]
    return distance_matrix(centers_arr, centers_arr)

def get_centers(level1_cluster_size=3800):
    assert type(level1_cluster_size) == int
    query = """
            SELECT *
            FROM centroids
            LIMIT {}
            """.format(level1_cluster_size)
    centers = pd.read_sql(query, conn)
    return centers

conn = pymysql.connect('35.196.88.209', 'teameleven', 'dbpassword', 'SPOTIFY')
centers = get_centers()
distances = get_distance_matrix(centers)

def get_point_data(centroid_id):
    query = """
            SELECT *
            FROM songs_labeled
            WHERE level0 = '{}'
            """.format(centroid_id)
    pt_data = pd.read_sql(query, conn)
    return pt_data

def newvis(request):
    return render(request, 'index.html')

@csrf_exempt
def Path_to_Data(request):
	data = json.loads(request.body)
	qt = load(os.path.join(settings.BASE_DIR, r"static\.pickle"))
	data = np.array(list(data["Values"].values()))
	user_data = qt.transform(data.reshape(1,-1))
	centroid = get_closest_centroid(centers, user_data)
	song = get_point_data(centroid)

	nested_data = rec_dd()

	lvl3 = get_top_cluster(song)
	srtnow = list_transform(lvl3)
	lvl1 = get_fourth_cluster(srtnow)
	maximum_points = 1000

	limiter = maximum_points // len(lvl1)

	children = get_child_cluster(srtnow)

	for disregard, song_vals in children.iterrows():
		if len(nested_data[song_vals['level3']][song_vals['level2']][song_vals['level1']][song_vals['level0']]) < limiter:
			nested_data[song_vals['level3']][song_vals['level2']][song_vals['level1']][song_vals['level0']][song_vals['song_id']] = [1, 1]
		else:
			pass


	#path = os.path.join(settings.BASE_DIR, r"static\test_songs_sample_1k.json")
	#data = json.loads(open(path).read())
	#data = json.dumps(nested_data, safe=False)
	return JsonResponse(nested_data)
