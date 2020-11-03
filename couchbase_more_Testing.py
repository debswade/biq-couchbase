from couchbase.cluster import Cluster, ClusterOptions, PasswordAuthenticator, Bucket
from config import dbuser, dbpass, dbbucket
from couchbase import enable_logging

cluster = Cluster('couchbase://localhost', ClusterOptions(PasswordAuthenticator(dbuser, dbpass)))
enable_logging()
bucket = cluster.bucket(dbbucket)
rv = bucket.get("alert!00007e32-ad47-4bd4-ba64-f8dbcb10033d")
print(rv.content)