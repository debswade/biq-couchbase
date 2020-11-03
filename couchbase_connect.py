from couchbase.cluster import Cluster, ClusterOptions
from couchbase.cluster import PasswordAuthenticator
from config import dbuser, dbpass, dbbucket as bucket_name

cluster = Cluster('couchbase://localhost', ClusterOptions(PasswordAuthenticator(dbuser, dbpass)))

bucket = cluster.bucket(bucket_name)
conn = bucket.connected
print(conn)

