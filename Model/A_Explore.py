# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 08:09:41 2020

@author: j68452
"""

import pandas as pd
import pymysql
import copy as cp
import glob
import os
from contextlib import closing

conn = pymysql.connect('35.196.88.209', 'teameleven', 'dbpassword', 'SPOTIFY')

# The locationn to create the temp file while clustering
disc_directory = r'C:\temp\Cluster_Compute'

# artists
# song

Query_Size = 250000
target_table = 'song'
tbl_id = 'song_id'
attribs = [tbl_id, 'artist_id', 'album_id', 'track_href']
features = [tbl_id, 'time_signature', 'danceability', 'energy', 'musical_key', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
exclude = ['song_name', 'duration_ms', 'mode']
############################################################################
# Choose which step to jump to. if you have a local copy of the full result data, you can choose step 1 to save time.
step_to = 0
###########################################################################

if step_to == 0 :
    with closing(conn.cursor()) as cursor:
        sql = "SELECT count(*) FROM {}".format(target_table)
        cursor.execute(sql)
        Queries = [x[0] for x in list(cursor.fetchall())][0]

        Percentage_Ceiling = (Queries // Query_Size) * Query_Size
        Queries_Count = (Queries // Query_Size) + 1
        Queries_Total = cp.deepcopy(Queries_Count)
        Remainder = Queries % Query_Size

    with closing(conn.cursor()) as cursor:
        sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'SPOTIFY' AND TABLE_NAME = '{}'".format(target_table)
        cursor.execute(sql)
        c_names = [x[0] for x in list(cursor.fetchall())]
        for x in exclude:
            c_names.remove(x)

    if 'artist' not in locals():
        with closing(conn.cursor()) as cursor:
            # Create a new record
            sql = "SELECT * FROM artist;"
            cursor.execute(sql)
            artist = pd.DataFrame(list(cursor.fetchall()))

        with closing(conn.cursor()) as cursor:
            sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'SPOTIFY' AND TABLE_NAME = 'artist'"
            cursor.execute(sql)
            ac_names = [x[0] for x in list(cursor.fetchall())]

        artist.columns = ac_names

    enhanced_select="""song_id, artist_id, album_id, track_href, time_signature, danceability, energy, musical_key, loudness, speechiness, acousticness, instrumentalness, liveness, valence, tempo"""


    Get_Remainder_SQL = """SELECT """ + enhanced_select + """ FROM {}
                            ORDER BY {} ASC
                            LIMIT {}""".format(target_table, tbl_id, Remainder)

    while Queries_Count > 0:
        print("Beginning Partition {} of {}".format(Queries_Total - Queries_Count + 1, Queries_Total))
        if Queries_Count == 1:
            sql = Get_Remainder_SQL
        else:
            Get_Middle_SQL = """SELECT """ + enhanced_select + """ FROM (
                            SELECT * FROM {0} ORDER BY {1} ASC LIMIT {2}
                                 )T
                            ORDER BY song_id DESC
                            LIMIT {3}""".format(target_table, tbl_id, Queries_Count * Query_Size, Query_Size)
            sql = Get_Middle_SQL

        result = pd.read_sql(sql, con=conn)
        result.columns = c_names
        All_Data = disc_directory+"//Partition" + str(Queries_Count) +".csv"
        result.to_csv(All_Data, index=False)

        Queries_Count -= 1
        print("Completed Partition {} of {}".format(Queries_Total - Queries_Count, Queries_Total))


if step_to <= 1:
    Partitions = glob.glob(disc_directory+r'\\Partition*.csv')
    for part in Partitions:
        path = '{}\Cleaned_{}'.format(os.path.dirname(part), os.path.basename(part))
        with open(part, encoding='utf-8') as infile:
            mode = 'w'
            with open(path, mode, encoding='utf-8') as outfile:
                for line in infile:
                    outfile.write(line)


if step_to <= 2:
    Partitions = glob.glob(disc_directory+r'\\Cleaned_Partition*.csv')
    for part in Partitions:
        Values_Directory = '{}\\Values_Only\\Vals{}'.format(os.path.dirname(part), os.path.basename(part))
        AttribDirectory = '{}\\Attributes\\Attr{}'.format(os.path.dirname(part), os.path.basename(part))
        #Values_Directory = disc_directory+"//Values_Only//PartitionVals" + str(Queries_Count) +".csv"
        #AttribDirectory = disc_directory+"//Attributes//PartitionAttr" + str(Queries_Count) +".csv"

        result = pd.read_csv(part)
        # get song attributes not for clustering
        result_attrib = result[attribs]
        # get song values used in clustering
        result_vals = result[features]

        result_vals.to_csv(Values_Directory, index=False)
        result_attrib.to_csv(AttribDirectory, index=False)

        del result_attrib
        del result_vals


