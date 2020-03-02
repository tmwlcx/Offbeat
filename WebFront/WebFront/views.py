from django.http import HttpResponse
import pandas as pd
import pymysql

def shout(request):
    conn = pymysql.connect('35.196.88.209', 'teameleven', 'dbpassword', 'SPOTIFY') 

    artists = conn.execute("select * from Artists LIMIT 10;")

    return render(request, 'home.html', context={'table' : artists})
