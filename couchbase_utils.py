from couchbase.n1ql import N1QLQuery
from couchbase.bucket import Bucket
from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
from couchbase.exceptions import CouchbaseError
from config import dbuser, dbpass, dbbucket as bucket_name, dbport, dbapiport
import requests
import json

class CouchbaseSchemaWorker(object):

    def __init__(self,
                 db_type='couchbase',
                 db_host='127.0.0.1',
                 db_username=dbuser,
                 db_password=dbpass,
                 db_port=dbport,
                 db_api_port=dbapiport
                 ):
        self.db_type = db_type
        self.db_host = db_host
        self.db_username = db_username
        self.db_password = db_password
        self.db_port = db_port
        self.db_api_port = db_api_port
        self.record_types = [ ]

    def couchbase_cluster_connect(self):
        connection_str = 'couchbase://' + self.db_host
        try:
            # self.db_username = 'nobody'
            self.cluster = Cluster(connection_str)
            authenticator = PasswordAuthenticator(self.db_username,self.db_password)
            self.cluster.authenticate(authenticator)
        except CouchbaseError as err:
            print("Problem connecting to couchbase ({})".format(err))

    def couchbase_rest_find_buckets(self):
        base_url = 'http://' + self.db_host + ':' + self.db_api_port
        query = '/pools/default/buckets'
        request_url = base_url + query
        # print(request_url)
        try:
            response = requests.get(request_url,auth=(self.db_username,self.db_password))
            response_json = response.json()
            # print(type(response_json))
            self.buckets = [ rec[ 'name' ] for rec in response_json ]
            # print(self.buckets)
        except Exception as err:
            print("Problem reading bucket list from couchbase api ({})".format(err))

    def couchbase_describe_buckets(self):
        for bucket in self.buckets:
            self.couchbase_describe_bucket(bucket)

    def couchbase_describe_bucket(self,bucket):
        bkt = self.cluster.open_bucket(bucket)
        query_str = "SELECT * FROM `{}`".format(bucket)
        query = N1QLQuery(query_str)
        query.timeout = 300
        rows = bkt.n1ql_query(query)
        print(type(rows))
        for row in rows:
            # print(row)
            self.analyse_record(row,bucket)

    def analyse_record(self,record,bucket):
        value_dict = record[ bucket ]
        fields = [ field for field in value_dict ]
        fields_set = set(fields)
        # print(fields_set)
        self.add_record_type(fields_set,bucket)

    def add_record_type(self,fields_set,bucket):
        match_flag = False
        bucket_match_flag = False
        if not self.record_types:
            # print("should only happen once")
            self.record_types.append({bucket: fields_set})
        else:
            for saved_record_type in self.record_types:
                if bucket in saved_record_type:
                    # print("Already seen: {}".format(bucket))
                    bucket_match_flag = True
            if not bucket_match_flag:
                self.record_types.append({bucket: fields_set})
            else:
                bucket_record_types = [ record[ bucket ] for record in self.record_types if bucket in record ]
                for record_type_set in bucket_record_types:
                    if record_type_set == fields_set:
                        match_flag = True
                        break
                if not match_flag:
                    self.record_types.append({bucket: fields_set})

    def create_bucket_dict(self,bucket):
        # bucket = 'beer-sample'
        this_record_type = [ list(record_type[ bucket ]) for record_type in self.record_types if bucket in record_type ]
        bucket_dict = {'bucket_name': bucket,'record_types': this_record_type}
        return bucket_dict

    def create_schema_dict(self):
        bucket_dicts = [ ]
        for bucket in self.buckets:
            bucket_dicts.append(self.create_bucket_dict(bucket))
        self.schema_dict = {"buckets": bucket_dicts}

    def create_schema_json(self):
        schema_json = json.dumps(self.schema_dict,indent=1,sort_keys=True)
        print(schema_json)
        return schema_json


if __name__ == "__main__":
    schema_worker = CouchbaseSchemaWorker()
    schema_worker.couchbase_cluster_connect()
    schema_worker.couchbase_rest_find_buckets()
    schema_worker.couchbase_describe_buckets()
    # print(schema_worker.record_types)
    schema_worker.create_schema_dict()
    schema_worker.create_schema_json()