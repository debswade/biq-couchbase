import sys
from couchbase.cluster import Cluster, ClusterOptions, PasswordAuthenticator, Bucket
from couchbase_core.views.iterator import View
from couchbase.exceptions import CouchbaseException
from couchbase.management import buckets


from config import dbuser, dbpass, dbbucket

cluster = Cluster('couchbase://localhost', ClusterOptions(PasswordAuthenticator(dbuser, dbpass)))
bucket = cluster.bucket(dbbucket)
coll = bucket.default_collection()

print(coll)

