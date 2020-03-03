from django.http import HttpResponse
import pandas as pd
import pymysql
# transform data to json for sending to front end when using d3
import json

def shout(request):
    
    # The SQLAlchemy engine will help manage interactions, including automatically
    # managing a pool of connections to your database
    conn = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username='teameleven',
            password='dbpassword',
            database='SPOTIFY',
            query={"unix_socket": "/cloudsql/{}".format('propane-ground-269323:us-east1:spotify-instance')},
        ),
        # ... Specify additional properties here.
        # ...
    )
    #conn = pymysql.connect('35.196.88.209', 'teameleven', 'dbpassword', 'SPOTIFY') 

    cur = conn.cursor()

    sql = "select * from artist LIMIT 10;"

    cur.execute(sql)
    
    artists = cur.fetchall()
    conn.commit()

    return render(request, 'home.html', context={'table' : artists})
