"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py

"""
from datetime import datetime, timedelta
from os import environ, fspath
from pathlib import Path
import shlex

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to operate!
from airflow.operators.bash_operator import BashOperator

# BaseOperator parameters
# https://airflow.apache.org/code.html#airflow.models.BaseOperator
# Could likewise define a different set of args for different purposes...
# ...such as dev_args or production_args
default_args = {
    'owner': 'mruffalo',
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

# Hardcoded parameters for first Airflow execution
DATA_DIRECTORY = Path('/hive/hubmap/data/CMU_Tools_Testing_Group/salmon-rnaseq')
FASTQ_R1 = DATA_DIRECTORY / 'L001_R1_001_r.fastq.gz'
FASTQ_R2 = DATA_DIRECTORY / 'L001_R2_001_r.fastq.gz'
THREADS = 6

# Instantiate a DAG
dag = DAG(
    'salmon_rnaseq',
    default_args=default_args,
    schedule_interval=None,
    max_active_runs=1,
)

pipeline_name = 'salmon-rnaseq'
pipeline_directory = Path(environ['AIRFLOW_HOME']) / pipeline_name

clone = BashOperator(
    task_id='git_clone',
    bash_command=f'git clone https://github.com/hubmapconsortium/{pipeline_name}',
    dag=dag,
)

command = [
    'cwltool',
    '--parallel',
    fspath(pipeline_directory / 'pipeline.cwl'),
    '--fastq_r1',
    fspath(FASTQ_R1),
    '--fastq_r2',
    fspath(FASTQ_R2),
    '--threads',
    str(THREADS),
]

command_str = ' '.join(shlex.quote(piece) for piece in command)

pipeline_exec = BashOperator(
    task_id='pipeline_exec',
    bash_command=command_str,
    dag=dag,
)

clone >> pipeline_exec
