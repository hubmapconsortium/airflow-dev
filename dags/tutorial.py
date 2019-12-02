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
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2015, 6, 1),
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
    'test', default_args = default_args, schedule_interval = timedelta(days = 1))

# Tasks are generated when instantiating operator objects
# By precedence they use:
# 1. explicitly passed arguments,
# 2. default_args
# 3. Operator defaults 
t1 = BashOperator(
    task_id = 'print_date',
    bash_command = 'date',
    dag = dag)

t2 = BashOperator(
    task_id = 'sleep',
    bash_command = 'sleep 5',
    retries = 3,
    dag = dag)

# Airflow leverages Jinja templating
# http://jinja.pocoo.org/docs/dev/
# This uses Airflow Macros: https://airflow.apache.org/code.html#macros
templated_command = """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7) }}"
        echo "{{ params.my_param }}"
    {% endfor %}
"""

t3 = BashOperator(
    task_id = 'templated',
    bash_command = templated_command,
    params = {'my_param': 'Parameter I passed in!'},
    dag = dag)

t1.set_downstream(t2)
t1.set_downstream(t3)

# This means that t2 will depend on t1...
# ...running successfully to run.
#t1.set_downstream(t2)

# This is equivalent to:
#t2.set_upstream(t1)

# The bit shift operator can also be
# used to chain operations:
#t1 >> t2

# And the upstream dependency with the
# bit shift operator:
#t2 << t1

# Chaining multiple dependencies becomes
# concise with the bit shift operator:
#t1 >> t2 >> t3

# A list of tasks can also be set as
# dependencies. These operations
# all have the same effect:
#t1.set_downstream([t2, t3])
#t1 >> [t2, t3]
#[t2, t3] << t1




