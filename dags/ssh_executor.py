from datetime import timedelta

import airflow
from airflow.contrib.hooks import ssh_hook
from airflow.contrib.operators import ssh_operator
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from operators.sftp_operator import HiveSFTPOperator  # Will actually import using plugins/ as base dir

sshHook = ssh_hook.SSHHook(ssh_conn_id='ssh_bridges_airflow', keepalive_interval=240)

default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(1),
    'email': ['julian@psc.edu'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
}

dag = DAG(
    dag_id='slurm_batch_job',
    description='A simple SLURM batch job DAG',
    default_args=default_args,
    # schedule_interval=timedelta(days=1),
    schedule_interval='0 0 * * *',
    dagrun_timeout=timedelta(minutes=60),
)
# ======================================================================================================================

# https://stackoverflow.com/questions/56322767/submit-and-monitor-slurm-jobs-using-apache-airflow
submit_slurm_job = """
cd ~/airflow &&
JID=$(sbatch airflow_slurm_job.sh)

echo $JID

sleep 10s # needed
ST="PENDING"
while [ "$ST" != "COMPLETED" ] ; do
    ST=$(sacct -j ${JID##* } -o State | awk 'FNR == 3 {print $1}')
    sleep 10s
    if [ "$ST" == "FAILED" ]; then
        echo 'Job final status:' $ST, exiting...
        exit 122
    fi
done

OUTPUT_FILES=$(readlink -f slurm*${JID##* }.*)
echo $ST"[HubFS]"$OUTPUT_FILES
"""

slurm_submit_task = ssh_operator.SSHOperator(
    task_id='submit_slurm_job',
    ssh_hook=sshHook,
    do_xcom_push=True,
    command=submit_slurm_job,
    dag=dag)


# ======================================================================================================================

def show_values(**context):
    value = context['task_instance'].xcom_pull(task_ids='submit_slurm_job')
    value = value.decode("utf-8")
    return value


show_values_task = PythonOperator(
    task_id='send_status_msg',
    python_callable=show_values,
    provide_context=True,
    dag=dag
)

# ======================================================================================================================

get_slurm_out_task = HiveSFTPOperator(
    task_id="get_slurm_out",
    ssh_conn_id="ssh_bridges_airflow",
    local_filepath="",
    remote_filepath="",
    operation="get",
    create_intermediate_dirs=False,
    job_id=7297385,
    dag=dag
)

# ======================================================================================================================

dag >> slurm_submit_task >> show_values_task >> get_slurm_out_task
