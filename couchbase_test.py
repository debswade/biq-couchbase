import requests
import sys
import config


def assign_db(db):
    sshusername = config.sshusername
    sshpkey = config.sshpkey
    dbport = config.dbport
    dbuser = config.dbuser
    dbpass = config.dbpass
    tunnel_name = config.tunnel_name
    # print(f"{ dbhost} {dbport} {tunnel_name} {sshusername} {sshpkey}")
    return dbuser,dbpass,dbport,tunnel_name,sshusername,sshpkey


def go():
    dbuser,dbpass,dbport,tunnel_name,sshusername,sshpkey = assign_db("couchbase")
    host = 'localhost'
    bucket = 'bgch-cb-api'
    design = 'customer'
    view = 'all'
    connection_timeout = 60

    try:
        r = requests.get(
            "http://{0}:{1}@{2}:{3}/couchBase/{4}/_design/{5}/_view/{6}?stale=false&inclusive_end=false&connection_timeout={7}".format(
                dbuser,
                dbpass,
                host,
                dbport,
                bucket,
                design,
                view,
                connection_timeout
            )
        )
    except requests.exceptions.RequestException as e:
        print("Couchbase not responding or network issue")
        statsd.gauge('total_clipins_from_couchbase',0)
        sys.exit(1)

    total_clipins = r.json()[ 'total_rows' ]
    print(f"numrows = {len(total_clipins)}")

go()
