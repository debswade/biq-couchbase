import requests
import sys
# import statsd
# statsd = statsd.StatsClient('localhost', 8125)


username = 'Administrator'
password = '0crownsforCouchbase'
host = 'localhost'
port = 8091
bucket = 'bgch-cb-api'
design = 'customer'
view = 'all'
connection_timeout = 60000

try:
    r = requests.get("http://{0}:{1}@{2}:{3}/couchBase/{4}/_design/{5}/_view/{6}?stale=false&inclusive_end=false&connection_timeout={7}".format(
        username,
        password,
        host,
        port,
        bucket,
        design,
        view,
        connection_timeout
      )
    )
except requests.exceptions.RequestException as e:
    print("Couchbase not responding or network issue")
    # statsd.gauge('total_clipins_from_couchbase', 0)
    sys.exit(1)

total_clipins = r.json()['total_rows']
print(total_clipins)
print("Sent total clipins to statsd", total_clipins)
# statsd.gauge('total_clipins_from_couchbase', total_clipins)