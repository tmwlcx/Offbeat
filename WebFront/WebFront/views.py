from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.db import connections
import pandas as pd #vs1.0.1
import numpy as np # vs1.19
import sys #stdlib no reqs
import pymysql # vs0.7.2
import sqlalchemy #vs1.3.13
# transform data to json for sending to front end when using d3
import json #stdlib no reqs
import os #stdlib no reqs
import random #stdlib no reqs
from collections import defaultdict
from sklearn import preprocessing, utils
from joblib import load #vs0.14.1
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from scipy.spatial import distance_matrix
from scipy.spatial.distance import euclidean

def get_distance_matrix(centers):
    centers_arr = centers.values[:,1:8]
    return distance_matrix(centers_arr, centers_arr)

def get_centers(level1_cluster_size=633, inv=False):
	assert type(level1_cluster_size) == int
	if not inv:
		query = """
			SELECT *
			FROM centroids
			ORDER BY centroid_id desc
			LIMIT {}
			""".format(level1_cluster_size)
	else:
		query = """
			SELECT *
			FROM centroids
			ORDER BY centroid_id asc
			LIMIT {}
			""".format(level1_cluster_size)
	centers = pd.read_sql(query, conn)
	return centers

def get_top_cluster(centroid_id):
    query = """
            SELECT distinct(level3) as level3
            FROM songs_labeled
            WHERE level0 = '{}'
            """.format(centroid_id)
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

def get_closest_centroid(centers, user_data):
    return np.argmin(np.linalg.norm(centers.values[:,1:9] - user_data, axis=1, ord=2))


conn = connections['default']
centers_top = get_centers()
centers_all = get_centers(10000)
centers_bottom = get_centers(3800, inv=True)
distances_top = get_distance_matrix(centers_top)
distances_all = get_distance_matrix(centers_all)

def Home(request):
	return render(request, 'index.html')

@csrf_exempt
def Path_to_Data(request):


	data = json.loads(request.body)
	qt = load(os.path.join(settings.BASE_DIR, r"static/qt.pickle"))

	# A distance scaler for how far to pull points
	wildness = int(data['how_offbeat'])
	# The Users cluster center
	data = np.array(list(data["Values"].values()))
	user_data = qt.transform(data.reshape(1,-1))
	centroid = get_closest_centroid(centers_bottom, user_data)
	song = get_point_data(centroid)

	lvl3 = get_top_cluster(song)
	#lvl3 = get_top_cluster(258)
	lvl3_int = int(lvl3['level3'].tolist()[0])
	top_starts = 7591
	maximum_points = 1000
	max_top_levels = 6
	limiter = 10
	scaling_factor = np.max(distances_all)

	# Take a slice of the distance matrix for top level clusters only
	useful_distances = distances_top[(lvl3_int-top_starts):(lvl3_int-top_starts+1),(lvl3_int-top_starts):]
	# Do a skip step across the useful distances, sized based on the wildness the user chose
	indices = np.argsort(useful_distances)[:,1:(wildness*60):int((wildness*60)/max_top_levels)].flatten().tolist()
	indices = [x + top_starts for x in indices]
	# Add the focus level 3
	indices.append(lvl3.values.flatten().tolist()[0])
	# Flatten the indices of the centers into a text string for SQL querying
	indices_text = ', '.join(["'" +str(x) + "'" for x in indices])
	# return all the level 3 centroids
	All_Level_3_Centers = get_centroid_values(indices_text)

	children = get_child_cluster(indices_text)
	set_vals = collapse_columns(children)
	centers = get_centroid_values(', '.join(["'" +str(x) + "'" for x in set_vals]))

	top_level_node_holder = []

	for val in All_Level_3_Centers['centroid_id']:
		nested_data = {}
		nested_data["name"] = int(val)
		curr_cluster = np.array([int(x) for x in qt.inverse_transform(np.array(All_Level_3_Centers[All_Level_3_Centers["centroid_id"]==int(nested_data["name"])].values.flatten().tolist()[1:]).reshape(1,-1)).reshape(-1,1)])
		orig_cluster = np.array(centers_all[centers_all["centroid_id"]==lvl3_int]).flatten()[1:9]
		distance = orig_cluster - curr_cluster
		dist_indexes = list(np.argsort(np.abs(distance)).reshape(1,-1).flatten())[0:3]
		names = [feature_Order[i] for i in dist_indexes]
		distances = [distance[i] for i in dist_indexes]
		nested_data["features"] = {k : v for k, v in zip(names, distances)}
		nested_data["children"] = []

		# adds Level 2s to the active level3 value dictionary
		for val1 in set(children[children['level3']==val]['level2']):
			temp = {}
			temp['name'] = int(val1)
			curr_cluster = np.array([int(x) for x in qt.inverse_transform(np.array(centers[centers["centroid_id"]==int(temp["name"])].values.flatten().tolist()[1:]).reshape(1,-1)).reshape(-1,1)])
			orig_cluster = np.array(centers_all[centers_all["centroid_id"]==lvl3_int]).flatten()[1:9]
			distance = orig_cluster - curr_cluster
			dist_indexes = list(np.argsort(np.abs(distance)).reshape(1,-1).flatten())[0:3]
			names = [feature_Order[i] for i in dist_indexes]
			distances = [distance[i] for i in dist_indexes]
			temp["features"] = {k : v for k, v in zip(names, distances)}
			temp['children'] = []
			nested_data["children"].append(temp)


		# Creates unique level1 and level2 combinations data frame
		next_level = children[children['level3']==val][['level1', 'level2']]
		next_level.drop_duplicates(inplace=True)

		for discard, song_vals1 in next_level.iterrows():
			temp = {}
			temp['name'] = int(song_vals1['level1'])
			curr_cluster = np.array([int(x) for x in qt.inverse_transform(np.array(centers[centers["centroid_id"]==int(temp["name"])].values.flatten().tolist()[1:]).reshape(1,-1)).reshape(-1,1)])
			orig_cluster = np.array(centers_all[centers_all["centroid_id"]==lvl3_int]).flatten()[1:9]
			distance = orig_cluster - curr_cluster
			dist_indexes = list(np.argsort(np.abs(distance)).reshape(1,-1).flatten())[0:3]
			names = [feature_Order[i] for i in dist_indexes]
			distances = [distance[i] for i in dist_indexes]
			temp["features"] = {k : v for k, v in zip(names, distances)}
			temp['children'] = []
			for dict1 in nested_data["children"]:
				if dict1["name"] == song_vals1['level2']:
					dict1["children"].append(temp)

		next_level = children[children['level3']==val][['level0', 'level1']]
		next_level.drop_duplicates(inplace=True)

		for discard, song_vals1 in next_level.iterrows():
			temp = {}
			temp['name'] = int(song_vals1['level0'])
			curr_cluster = np.array([int(x) for x in qt.inverse_transform(np.array(centers[centers["centroid_id"]==int(temp["name"])].values.flatten().tolist()[1:]).reshape(1,-1)).reshape(-1,1)])
			orig_cluster = np.array(centers_all[centers_all["centroid_id"]==lvl3_int]).flatten()[1:9]
			distance = orig_cluster - curr_cluster
			dist_indexes = list(np.argsort(np.abs(distance)).reshape(1,-1).flatten())[0:3]
			names = [feature_Order[i] for i in dist_indexes]
			distances = [distance[i] for i in dist_indexes]
			temp["features"] = {k : v for k, v in zip(names, distances)}
			temp['children'] = []
			for dict1 in nested_data["children"]:
				for dict2 in dict1["children"]:
					if dict2["name"] == song_vals1['level1']:
						dict2["children"].append(temp)

		next_level = utils.shuffle(children[children['level3']==val][['song_id', 'level0']])
		next_level.drop_duplicates(inplace=True)

		for discard, song_vals1 in next_level.iterrows():
			temp = {}
			temp['name'] = song_vals1['song_id']
			for dict1 in nested_data["children"]:
				for dict2 in dict1["children"]:
					for dict3 in dict2["children"]:
						if dict3["name"] == song_vals1['level0']:
							if len(dict3["children"]) < limiter:
								curr_cluster = np.array(centers_all[centers_all["centroid_id"]==int(song_vals1['level0'])]).flatten()[1:9]
								orig_cluster = np.array(centers_all[centers_all["centroid_id"]==lvl3_int]).flatten()[1:9]
								distance = euclidean(orig_cluster.flatten(), curr_cluster) / scaling_factor
								temp['similarity'] = distance
								dict3["children"].append(temp)

		top_level_node_holder.append(nested_data)

		nested_data = {"name" : "clusters", "children": top_level_node_holder}
	return JsonResponse(nested_data)
