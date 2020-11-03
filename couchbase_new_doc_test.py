import couchbase
from couchbase.bucket import Bucket
from config import dbuser, dbpass, dbbucket as cb_bucket
import couchbase.exceptions

localhost = "localhost"
def fetch_doc(key):

    cb = Bucket('couchbase://' + localhost + '/' + cb_bucket)
    doc = cb.get(key)
    return doc

def go():
    dockey = "alert!00007e32-ad47-4bd4-ba64-f8dbcb10033d"
    results = fetch_doc(dockey)


go()