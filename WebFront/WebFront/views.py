from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import pymysql
import sqlalchemy
# transform data to json for sending to front end when using d3
import json
import os
from django.conf import settings

def shout(request):
    
    try:
        conn = pymysql.connect('35.196.88.209', 'teameleven', 'dbpassword', 'SPOTIFY')
        cur = conn.cursor()

        sql = "select * from artist LIMIT 10;"

        cur.execute(sql)

        artists = cur.fetchall()
        conn.commit()
    except:
        pass

    return render(request, 'home.html')

def Path_to_Data(request):
    path = os.path.join(settings.BASE_DIR, r"static/test_songs_sample_1k.json")
    data = json.loads(open(path).read())
    return JsonResponse(data)