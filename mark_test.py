from couchbase.bucket import Bucket
bucket = Bucket("couchbase://localhost/bgch-cb-api")
data = []

data = bucket.query("customer", "all")
print(data)
# for row in data:
#         print(row)
    # customer = bucket.get(row.docid).value