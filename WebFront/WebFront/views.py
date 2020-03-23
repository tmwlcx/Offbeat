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
    return render(request, 'home.html')

def newvis(request):
    return render(request, 'index.html')

def Path_to_Data(request):
    path = os.path.join(settings.BASE_DIR, r"static/test_songs_sample_1k.json")
    data = json.loads(open(path).read())
    return JsonResponse(data)
