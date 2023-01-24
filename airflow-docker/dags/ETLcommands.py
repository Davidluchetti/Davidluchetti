from airflow import DAG
from datetime import datetime

with DAG('ETLcommands',start_date = datetime(2023,1,24),
        schedule_interval = ) as dag:
