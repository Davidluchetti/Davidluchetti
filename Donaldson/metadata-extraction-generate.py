config.yml

snowflake:
  user: SVC_SECURE_AGENT_INSTANCE_SCRIPTS_DEV
  password: 3Mb8K4@X%o5#
  account: donaldson.central-us.azure
  database: EDW_DEV
  schema: EDW_LOAD_CT
  task_load_metadata_table: IICS_TMP_MTT_METADATA
  desired_taskflow_metadata_table: IICS_TMP_TSKF_METADATA
  role: EDW_DEV_OWNER
  warehouse: DEV_COMPUTE_WH
  set_table_owner: EDW_DEV_OWNER

iics:
  user: RESTASSETUPDATE_DEV
  password: nATs8HM3w@jc8Jy
  api_auth_url: https://dm1-us.informaticacloud.com/ma/api/v2/user/login
  api_root_v2: https://usw1.dm1-us.informaticacloud.com/saas/api/v2
  api_root_v3: https://usw1.dm1-us.informaticacloud.com/saas/public/core/v3
  
------------------------------------------


# This script requires that the following table exist in the target schema before execution
import sys

import snowflake.connector, requests, yaml, json, logging
from urllib.parse import urlparse
from datetime import datetime

try:
    import http.client as http_client
except ImportError:
    import httplib as http_client
#http_client.HTTPConnection.debuglevel = 1

# initialize logging
logging.basicConfig()
logging.getLogger().setLevel(logging.ERROR)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

desired_task_load_metadata_fields = {
    'MTT_NAME': 'objectName',
    'MTT_START_TIMESTAMP': 'startTime',
    'MTT_END_TIMESTAMP': 'endTime',
    'MTT_SOURCE_SUCCESS_ROWS':	'successSourceRows',
    'MTT_SOURCE_FAILURE_ROWS': 'failedSourceRows',
    'MTT_TARGET_SUCCESS_ROWS':	'successTargetRows',
    'MTT_TARGET_FAILURE_ROWS':	'failedSourceRows',
    'MTT_STATUS': 'state',
    'MTT_PARENT_TASK_FEDERATED_ID':	'parentTaskFederatedId',
    'MTT_CONSUMED_COMPUTE_UNITS':	'CONSUMED_COMPUTE_UNITS',
    'MTT_REQUESTED_COMPUTE_UNITS':	'REQUESTED_COMPUTE_UNITS',
    'MTT_RUN_TIMESTAMP': 'SYSDATE'
}

desired_taskflow_metadata_fields = {
    'TSKF_FEDERATED_ID': 'id',
    'TSKF_NAME': 'path',
    'RUN_TIMESTAMP': 'SYSDATE'
}


## load the config
with open('./config.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)

#global icSessionId
icSessionId = ''
#the snowflake connection global
ctx = ''

sysdate = datetime.now()


def log(msg, type):
    print(f'{type}: {msg}')


def fetch_icSessionId():
    auth = {
        "@type": "login",
        "username": config.get('iics').get('user'),
        "password": config.get('iics').get('password')
    }
    resp = requests.post(config.get('iics').get('api_auth_url'), json=auth)

    if resp.status_code != 200:
        log(f"{resp} authenticating to {config.get('iics').get('api_auth_url')}", 'error')
        sys.exit(1)
    elif resp.json().get('icSessionId'):
        return resp.json().get('icSessionId')
    return False


def request_headers(url,payload=''):
    global icSessionId
    icSessionId = icSessionId if icSessionId else fetch_icSessionId()
    headers = {
        'Host': urlparse(url).hostname,
        'INFA-SESSION-ID': icSessionId, # for v3
        'icSessionId': icSessionId,  # for v2 
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Content-Length': str(len(payload)),
        'Update-Mode': 'PARTIAL'
    }
    return headers


def iics_get(url):
    resp = requests.get(url, headers=request_headers(url))
    if resp.status_code != 200:
        log(json.dumps(resp) + f' querying url', 'error')
        sys.exit(1)
    return resp.json()


def connect_snowflake():
    global ctx
    ctx = snowflake.connector.connect(
        user=config.get('snowflake').get('user'),
        password=config.get('snowflake').get('password'),
        account=config.get('snowflake').get('account'),
        #authenticator=config.get('snowflake').get('authenticator'),
        database=config.get('snowflake').get('database'),
        schema=config.get('snowflake').get('schema'),
        role=config.get('snowflake').get('role'),
        warehouse=config.get('snowflake').get('warehouse')
    )


def execute_sql(sql):
    if not ctx:
        connect_snowflake()
    try:
        cs = ctx.cursor()
        results = cs.execute(sql)
        return results
    except snowflake.connector.errors.ProgrammingError as e:
        print(sql)
        print('Error {0} ({1}): {2} ({3})'.format(e.errno, e.sqlstate, e.msg, e.sfqid))
        sys.exit(1)


# This script requires that the following table exist in the target schema before execution
def main():
    # 1. do the task load metadata extraction
    # https://usw1.dm1-us.informaticacloud.com/saas/api/v2/activity/activityLog

    task_load_metadata = iics_get(config.get('iics').get('api_root_v2') + '/activity/activityLog?rowLimit=0')
    task_load_metadata_sql = f"insert into {config.get('snowflake').get('schema')}.{config.get('snowflake').get('task_load_metadata_table')} " \
                             f"({','.join(desired_task_load_metadata_fields.keys())}) \n values "
    delim = ''
    for rec in task_load_metadata:
        rec['SYSDATE'] = sysdate
        task_load_metadata_sql += f'{delim} (' + ','.join(map(lambda p: f"'{rec.get(p, '')}'", desired_task_load_metadata_fields.values())) + f')'
        delim = ',\n'
    execute_sql(f"truncate table {config.get('snowflake').get('schema')}.{config.get('snowflake').get('task_load_metadata_table')}")
    execute_sql(task_load_metadata_sql)

    # 2. pull metadata from taskflows
    # https://usw1.dm1-us.informaticacloud.com/saas/public/core/v3/objects?q=type=='TASKFLOW'

    taskflow_metadata = iics_get(config.get('iics').get('api_root_v3') + "/objects?q=type=='TASKFLOW' and tag=='EDW_METADATA'") 
    taskflow_metadata_sql = f"insert into {config.get('snowflake').get('schema')}.{config.get('snowflake').get('desired_taskflow_metadata_table')} " \
                           f"({','.join(desired_taskflow_metadata_fields.keys())}) \n values "
    delim = ''
    for rec in taskflow_metadata.get('objects'):
        rec['SYSDATE'] = sysdate
        taskflow_metadata_sql += f'{delim} (' + ','.join(map(lambda p: f"'{rec.get(p, '')}'", desired_taskflow_metadata_fields.values())) + f')'
        delim = ',\n'
    execute_sql(f"truncate table {config.get('snowflake').get('schema')}.{config.get('snowflake').get('desired_taskflow_metadata_table')}")
    execute_sql(taskflow_metadata_sql)


def create_task_load_metadeta_table():
    table_body = 'MTT_NAME STRING,'\
                 'MTT_START_TIMESTAMP TIMESTAMP,'\
                 'MTT_END_TIMESTAMP TIMESTAMP,'\
                 'MTT_SOURCE_SUCCESS_ROWS NUMBER,'\
                 'MTT_SOURCE_FAILURE_ROWS NUMBER,'\
                 'MTT_TARGET_SUCCESS_ROWS NUMBER,'\
                 'MTT_TARGET_FAILURE_ROWS NUMBER,'\
                 'MTT_STATUS STRING,'\
                 'MTT_PARENT_TASK_FEDERATED_ID STRING,'\
                 'MTT_CONSUMED_COMPUTE_UNITS STRING,'\
                 'MTT_REQUESTED_COMPUTE_UNITS STRING,'\
                 'MTT_RUN_TIMESTAMP TIMESTAMP'

    sql = f"create table if not exists {config.get('snowflake').get('schema')}.{config.get('snowflake').get('task_load_metadata_table')} ({table_body})"
    execute_sql(sql)

    perms = f"grant ownership on table {config.get('snowflake').get('schema')}.{config.get('snowflake').get('task_load_metadata_table')} " \
            f"to role {config.get('snowflake').get('set_table_owner')} REVOKE CURRENT GRANTS"
    execute_sql(perms)


def create_taskflow_metadata_table():
    table_body = 'TSKF_FEDERATED_ID STRING,'\
                 'TSKF_NAME STRING,'\
                'RUN_TIMESTAMP TIMESTAMP'

    sql = f"create table if not exists {config.get('snowflake').get('schema')}.{config.get('snowflake').get('desired_taskflow_metadata_table')} ({table_body})"
    execute_sql(sql)

    perms = f"grant ownership on table {config.get('snowflake').get('schema')}.{config.get('snowflake').get('desired_taskflow_metadata_table')} " \
            f"to role {config.get('snowflake').get('set_table_owner')} REVOKE CURRENT GRANTS"
    execute_sql(perms)

print('running...')

create_taskflow_metadata_table()  # uncomment to create the taskflow table

create_task_load_metadeta_table() # uncomment to create the task load table

main() # comment to prevent pulling the metadata, truncating the tables and loading new data

print('Done')
