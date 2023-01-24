from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
import pandas as pandas
import requests
import json

def capture_account_data():
    url = "https://data.cityofnewyork.us/resource/rc75-m7u3.json"
    response = requests.get(url)
    df = pd.DataFrame(json.load(response.content))
    qtt = len(df.index)
    return qtt

def is_valid(ti):
    qtt = ti.scom_pull(task_ids = 'capture_account_data')
    if (qtt > 1000):
        return 'valid'
    return 'nvalid'

with DAG('ETLcommands',start_date = datetime(2023,1,24),
        schedule_interval = '30 * * * *', catchup= false) as dag:

    capture_account_data = PythonOperator(
        task_id = 'capture_account_data',
        python_callable = capture_account_data
    )

    is_valid = BranchPythonOperator(
        task_id = 'is_valid',
        python_callable = is_valid
    )

    valid = BashOperator(
        task_id = 'valid',
        bash_command = "echo 'Quantity Valid'"
    )

    notvalid = BashOperator(
        task_id = 'nvalid',
        bash_command = "echo 'Quantity Not Valid'"
    )


capture_account_data >> is_valid >> [valid, nvalid]