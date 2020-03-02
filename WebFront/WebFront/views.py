from django.http import HttpResponse
import pandas as pd
import pymysql

def shout(request):
    db = pymysql.connections.Connection('127.0.0.1', user='TeamEleven', password='dbpassword', database='SPOTIFY')  

    artists = db.execute("select * from Artists LIMIT 10;")

    return render(request, 'home.html', context={'table' : artists})
