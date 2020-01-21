from datetime import datetime, timedelta
from os import fspath
from pathlib import Path
import shlex

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from utils import PIPELINE_BASE_DIR, clone_or_update_pipeline

default_args = {
    # TODO: Should these defaults be factored out and used across DAGs?
    'owner': 'mccalluc', # TODO: What does this imply?
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    # TODO: email not necessary if I don't want email?
    # 'email': ['mruffalo@cs.cmu.edu'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # Commented out in original:
    ## 'queue': 'bash_queue',
    ## 'pool': 'backfill',
    ## 'priority_weight': 10,
    ## 'end_date': datetime(2016, 1, 1),
}

# Hardcoded parameters for first Airflow execution
# DATA_DIRECTORY = Path('/hive/hubmap/data/????')
THREADS = 6

# Instantiate a DAG
dag = DAG(
    'portal_container_h5ad_to_arrow',
    default_args=default_args,
    schedule_interval=None,
    max_active_runs=1,
)

pipeline_name = 'portal-container-h5ad-to-arrow'

prepare_pipeline = PythonOperator(
    python_callable=clone_or_update_pipeline,
    task_id='clone_or_update_pipeline',
    op_kwargs={'pipeline_name': pipeline_name},
    dag=dag,
)

command = [
    'cwltool',
    '--parallel',
    fspath(PIPELINE_BASE_DIR / pipeline_name / 'workflow.cwl'),
    # TODO: How are inputs specified?
    '--threads',
    str(THREADS),
]

command_str = ' '.join(shlex.quote(piece) for piece in command)

pipeline_exec = BashOperator(
    task_id='pipeline_exec',
    bash_command=command_str,
    dag=dag,
)

prepare_pipeline >> pipeline_exec
