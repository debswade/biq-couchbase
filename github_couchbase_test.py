import couchbase
from config import dbuser, dbpass, bucket_name, dbport

# connect to a couchbase server
couchbase.
cb = couchbase.Server('localhost:8091',
                      username=dbuser,
                      password=dbpass)

newbucket = cb[bucket_name]
rows = newbucket.view("_design/customer/_view/all")
for row in rows:
    print(row)