from couchbase.cluster import Cluster, ClusterOptions, Bucket, PasswordAuthenticator
from couchbase_core.views.iterator import View
from config import dbuser, dbpass, dbbucket as bucket_name, dbport
import os
import fnmatch

bucketname = 'bgch-cb-api'
cluster = Cluster('couchbase://localhost',
                  ClusterOptions(PasswordAuthenticator(dbuser, dbpass)))

bucket = cluster.bucket(bucketname)
coll = bucket.default_collection()
print(bucketname)
print(bucket)
print(coll)

dockey = "alert!00007e32-ad47-4bd4-ba64-f8dbcb10033d"
dockey = "00007e32-ad47-4bd4-ba64-f8dbcb10033d"
# dockey = "_design/alert"

result = coll.get(dockey)
content = result.content_as[str]
print(content)

viewId = "whitelist"
connection_timeout = 60000
limit = 6
inclusive_end=True
skip=0
stale=False
group = True

# "http://{0}:{1}@{2}:{3}/couchBase/{4}/_design/{5}/_view/{6}?stale=false&inclusive_end=false&connection_timeout={7}"
#
# "http://{0}:{1}@{2}:{3}/couchBase/{4}/_design/{5}/_view/{6}?stale=false&inclusive_end=false&connection_timeout={7}"
#
# ?connection_timeout=60000&full_set=true&inclusive_end=true&limit=6&skip=0&stale=false
# Show Results
#
#
# view = View(bucket,"dev_user",
#             view=viewId,
#             limit=limit,
#             reduce=True,
#             connection_timeout=connection_timeout,
#             stale=True,
#             inclusive_end=True)
# for row in view:
#     print(row.key)

# resultset = cluster.view_query("customer", "all", limit=5)
# resultset = cluster.view_query("customer", "all", connection_timeout=connection_timeout, viewId=viewId ,limit=5, reduce=True, group=True, inclusive_end=False)
#
# for row in resultset: print(row.key)
# print(resultset)


#



