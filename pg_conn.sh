#!/bin/bash
db=postgresql
dbdriver=psycopg2
dbuser=blood
passwd=`cat $AIRFLOW_HOME/.pgpwd`
host=127.0.0.1
port=5432
dbname=cwl_airflow
conn_string="${db}+${dbdriver}://${dbuser}:${passwd}@${host}:${port}/${dbname}"
#cmd = `postgresql+psycopg2://airflow:airflow@127.0.0.1:5432/airflow
echo $conn_string

