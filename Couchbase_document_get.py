from couchbase.cluster import Cluster, ClusterOptions, Bucket
from couchbase.cluster import PasswordAuthenticator
from couchbase_core.views.iterator import View
from config import dbuser, dbpass, dbbucket as bucket_name, dbport
import os
import fnmatch

bucketname = 'bgch-cb-api'
cluster = Cluster('couchbase://localhost',
                  ClusterOptions(PasswordAuthenticator(dbuser, dbpass)))

bucket = cluster.bucket(bucketname)
collection = bucket.default_collection()
print(bucketname)
print(bucket)
print(collection)

resultset = bucket.get("alert!00007e32-ad47-4bd4-ba64-f8dbcb10033d")
content = resultset.content_as[str]

skip = 0
startkey = [ str,"adam.clark@britishgas.co.uk" ]
endkey = [ str,"alan.haslam@britishgas.co.uk"]

for row in content:
    print(row.key)
