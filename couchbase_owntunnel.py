import couch
import json
from botocore.exceptions import ClientError
import config
from sshtunnel import SSHTunnelForwarder
import paramiko
import datetime
from common import base_operating_premise
from config import hostname, dbuser, secret_name


region, instanceid, basedir, session = base_operating_premise()
migdir = basedir
ec2_client = session.client('ec2')
startTime = datetime.datetime.now()
nowish = datetime.date.today()


def assign_db(db):
    sshusername = config.sshusername
    sshpkey = config.sshpkey
    dbport = config.dbport
    dbuser = config.dbuser
    dbpass = config.dbpass
    tunnel_name = config.tunnel_name
    # print(f"{ dbhost} {dbport} {tunnel_name} {sshusername} {sshpkey}")
    return dbuser,dbpass,dbport, tunnel_name, sshusername, sshpkey

def make_connection(sql_command, user, db, data=None):
    dbport, tunnel_name, sshusername, sshpkey = assign_db(db)
    dbuser = config.dbuser
    dbpass = config.dbpass

    rows = []
    dblocal = "127.0.0.1"
    with SSHTunnelForwarder(
        tunnel_name,
        ssh_username=sshusername,
        ssh_pkey=sshpkey,
        remote_bind_address=(dbhost, 3306),
        local_bind_address=(dblocal, dbport)
    ) as tunnel:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        db = pymysql.connect(host=dblocal,
                             user=dbuser,
                             passwd=dbpass,
                             port=dbport,
                             db=mysqldb,
                             cursorclass=pymysql.cursors.DictCursor)
        with db:
            rows = []
            # print(data)
            if "FOR UPDATE" in sql_command:
                # print(f"doing for update with no extra data")
                rows = reserve_and_update_rows(sql_command, db)
            else:
                rows = exec_query(sql_command, db, data=data)
        db.close()
    # print(f'Make_connection returning rows {len(rows)}')
    return rows

def exec_query(sql_command, db, data=None):
    cur = db.cursor(pymysql.cursors.DictCursor)
    if data is None:
        # print(cur.mogrify(sql_command))
        cur.execute(sql_command)
    else:
        # print(cur.mogrify(sql_command))
        cur.executemany(sql_command,data)
    rows = cur.fetchall()
    db.commit()
    if rows is not None:
        return rows

# def reserve_and_update_rows(sel_sql_command, db):
#     # print(f'USER: {user} SQL: {sql_command} DB: {db}')
#     cur = db.cursor(pymysql.cursors.DictCursor)
#     # print(f"RESERVE: executing {cur.mogrify(sel_sql_command)}")
#     cur.execute(sel_sql_command)
#     rows = cur.fetchall()
#     if len(rows) >0:
#         # print(f"rows from rds.reserve_and_update_rows {rows}")
#         migrator = instanceid
#         migrated = "WORKING"
#         uuids = [x['uuid'] for x in rows]
#         # print(f"hubs {hubs}")
#         uuidlist = ', '.join(f'"{h}"' for h in uuids)
#         # print(f"uuidlist {uuidlist}")
#         upd_sql = f'UPDATE users.nodedevices ' \
#                   f'SET migrator = "{migrator}", ' \
#                   f'migrated = "{migrated}" ' \
#                   f'where uuid in ( {uuidlist} ) ' \
#                   f'; '
#         # print(upd_sql)
#         # print(f"executing (reserve_and_update_rows) {cur.mogrify(upd_sql)}")
#         cur.execute(upd_sql)
#         db.commit()
#
#     return rows


# def query_rds(sql_command, user, db, data=None):
#     # print(data)
#     rows = make_connection(sql_command,user,db, data=data)
#     # print(f"Query_rds returning rows {len(rows)}")
#     return rows