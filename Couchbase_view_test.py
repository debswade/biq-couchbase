from couchbase.cluster import Cluster, ClusterOptions, PasswordAuthenticator, Bucket
from couchbase_core.views.iterator import View
from config import dbuser, dbpass, dbbucket

# bucketname = 'bgch-cb-api'
cluster = Cluster('couchbase://localhost',
                  ClusterOptions(PasswordAuthenticator(dbuser, dbpass)))
print(cluster)

bucket = cluster.bucket(dbbucket)
print(bucket)


# This call gives a timeout (LCB_ERR_TIMEOUT (201)) BUT same request on curl
# curl http://localhost:8092/bgch-cb-api/_design/dev_user/_view/whitelist does not

resultset = cluster.view_query("dev_user", "whitelist", limit=1,
                               connection_timeout=600000,
                               stale=True, inclusive_end=False)

for row in resultset:
    print(row.key)