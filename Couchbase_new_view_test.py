
from couchbase.cluster import Cluster, ClusterOptions, PasswordAuthenticator, Bucket
from couchbase_core.views.iterator import View
from config import dbuser, dbpass, dbbucket

cluster = Cluster('couchbase://localhost',
                  ClusterOptions(PasswordAuthenticator(dbuser, dbpass)))
print(cluster)

def get_total_docs(cluster, cbbucket):
    i = 0
    result = q_alldocs(cluster, cbbucket)
    for doc in result:
        i += 1
    print('%s total documents' % (i))

def create_empty_doc(cluster, cbbucket):
    bucket, collection = cbconnect_collection(cluster, cbbucket)
    new_uuid = str(uuid.uuid4())
    collection.upsert(new_uuid, {})
    return(new_uuid)


def go():
    get_total_docs(cluster, dbbucket)

go()
# create_empty_doc(cluster, dbbucket)
# get_total_docs(cluster, dbbucket)


# cluster.get("")
#
# results=cluster.query(design="customer", view="all")

# for row in cluster.query('design', 'view'):
#     print (row)
