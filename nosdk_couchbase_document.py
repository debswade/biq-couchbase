import requests
import sys
from config import dbuser, dbpass, dbbucket

host = 'localhost'
port = 8091
connection_timeout = 60000

design = 'customer'
view = 'all'

request_build = f"http://{dbuser}:{dbpass}@{host}:{port}" \
                f"/couchBase/" \
                f"{dbbucket}/_design/{design}/" \
                f"_view/{view}" \
                f"?stale=false" \
                f"&inclusive_end=false" \
                f"&connection_timeout={connection_timeout}"

try:
    r = requests.get(request_build.format(
      )
    )
    print(r.json())
except requests.exceptions.RequestException as e:
    print("Couchbase not responding or network issue")
    sys.exit(1)

total_clipins = r.json()['total_rows']
print(total_clipins)
