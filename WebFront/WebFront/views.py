from django.http import HttpResponse
import pandas as pd
import sqlalchemy

def shout(request):
    cloud_sql_connection_name = 'propane-ground-269323:us-east1:project-sql-space'

    # The SQLAlchemy engine will help manage interactions, including automatically
    # managing a pool of connections to your database
    db = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username='Team',
            password='Projectime',
            database='The_Database',
            query={"unix_socket": "/cloudsql/{}".format(cloud_sql_connection_name)},
        ),
        # ... Specify additional properties here.
        # ...
    )

    schem = db.execute("select * from schema;")

    return HttpResponse('This page is HERE: {}'.format(schem))