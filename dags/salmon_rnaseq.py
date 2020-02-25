from datetime import datetime, timedelta
from os import fspath
from pathlib import Path
import shlex

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from utils import PIPELINE_BASE_DIR, clone_or_update_pipeline

default_args = {
    'owner': 'mruffalo',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'email': ['mruffalo@cs.cmu.edu'],
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
OUTDIR = Path('/hive/users/blood/workflow/cwl-airflow/data/rnaseq/10x/test1')
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

prepare_pipeline = PythonOperator(
    python_callable=clone_or_update_pipeline,
    task_id='clone_or_update_pipeline',
    op_kwargs={'pipeline_name': pipeline_name},
    dag=dag,
)

command = [
    'cwltool',
    '--parallel',
    '--outdir',
    fspath(OUTDIR),
    fspath(PIPELINE_BASE_DIR / pipeline_name / 'pipeline.cwl'),
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

prepare_pipeline >> pipeline_exec
