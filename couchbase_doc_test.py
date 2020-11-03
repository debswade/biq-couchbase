from couchbase.cluster import Cluster, ClusterOptions, PasswordAuthenticator
from config import dbuser, dbpass, dbbucket as bucket_name, dbport


dockey = "alert!002074b7-bf1a-433c-b2d5-f15efc311850"

cluster = Cluster('couchbase://localhost',
                  ClusterOptions(PasswordAuthenticator(dbuser, dbpass)))

bucket = cluster.bucket(bucket_name)
collection = bucket.default_collection()

# result = collection.get(dockey)
try:
    resultset = cluster.view_query("user", "whitelist", limit=2)
except
for row in resultset: print (row.key)