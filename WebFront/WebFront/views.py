from django.http import HttpResponse
import pandas as pd
import pymysql
# transform data to json for sending to front end when using d3
import json

def shout(request):
    conn = pymysql.connect('35.196.88.209', 'teameleven', 'dbpassword', 'SPOTIFY') 

    cur = conn.cursor()

    sql = "select * from artist LIMIT 10;"

    cur.execute(sql)
    
    artists = cur.fetchall()

    return render(request, 'home.html', context={'table' : artists})
