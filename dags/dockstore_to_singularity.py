"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py

"""

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

# BaseOperator parameters
# https://airflow.apache.org/code.html#airflow.models.BaseOperator
# Could likewise define a different set of args for different purposes...
# ...such as dev_args or production_args
default_args = {
    'owner': 'blood',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'email': ['blood@psc.edu'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

# Instantiate a DAG
dag = DAG(
    'dockstore_singularity',
    default_args=default_args,
    schedule_interval=None,
    max_active_runs=1)

t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag)

t2 = BashOperator(
    task_id='rm',
    bash_command='if [ -f ~/helloworld.txt ]; then rm ~/helloworld.txt; fi; if [ -f ~/dockstore-tool-helloworld_1.0.2.sif ]; then rm ~/dockstore-tool-helloworld_1.0.2.sif; fi',
    dag=dag)

t3 = BashOperator(
    task_id='singularity_pull',
    bash_command='singularity pull ~/dockstore-tool-helloworld_1.0.2.sif docker://quay.io/ga4gh-dream/dockstore-tool-helloworld:1.0.2',
    dag=dag)

t4 = BashOperator(
    task_id='singularity_exec',
    bash_command='singularity exec ~/dockstore-tool-helloworld_1.0.2.sif hello_world ~/template.txt ~/words.txt; mv helloworld.txt ~/',
    dag=dag)

t5 = BashOperator(
    task_id='cat',
    bash_command='cat ~/helloworld.txt',
    dag=dag)

t1 >> t2 >> t3 >> t4 >> t5
