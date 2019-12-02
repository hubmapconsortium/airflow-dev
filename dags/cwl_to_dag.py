#!/usr/bin/env python3
from cwl_airflow import CWLDAG, CWLJobDispatcher, CWLJobGatherer
dag = CWLDAG(cwl_workflow="/hive/users/blood/workflow/cwl-airflow/Dockstore.cwl", dag_id="dockstore_cwl")
dag.create()
dag.add(CWLJobDispatcher(dag=dag), to='top')
dag.add(CWLJobGatherer(dag=dag), to='bottom')



#from cwl_airflow import CWLDAG, CWLJobDispatcher, CWLJobGatherer
#from datetime import timedelta

#def cwl_workflow(workflow_file):
#    dag = CWLDAG(default_args={
#        'owner': 'airflow',
#        'email': ['blood@psc.edu'],
#        'email_on_failure': False,
#        'email_on_retry': False,
#        'retries': 20,
#        'retry_exponential_backoff': True,
#        'retry_delay': timedelta(minutes=30),
#        'max_retry_delay': timedelta(minutes=60 * 4)
#    },
#        cwl_workflow=workflow_file)
#    dag.create()
#    dag.add(CWLJobDispatcher(dag=dag), to='top')
#    dag.add(CWLJobGatherer(dag=dag), to='bottom')
#
#    return dag
# 
#cwl_workflow("/hive/users/blood/workflow/cwl-airflow/Dockstore.cwl")

