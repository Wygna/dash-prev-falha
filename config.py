import os

my_db.connect(dialect = "postgresql"
 host = os.environ['PGHOST'],
 port = os.environ['PGPORT'],
 database = os.environ['PGDATABASE'],
 username = os.environ['PGUSER'], 
 password = os.environ['PGPASSWORD'])
