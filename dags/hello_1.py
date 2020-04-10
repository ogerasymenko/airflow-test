from airflow.models import DAG
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta, date
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator

today = str(date.today()).replace('-', '.')

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.strptime(today, '%Y.%m.%d'),
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    dag_id='k8s-example',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval="@hourly"
)

k8s_example_task_1 = KubernetesPodOperator(
    namespace="spark-ds",
    image="ubuntu:16.04",
    cmds=["bash", "-cx"],
    arguments=["date"],
    name="k8s-example-task-1",
    task_id="k8s-example-task-1",
    startup_timeout_seconds=10,
    get_logs=True,
    dag=dag,
    in_cluster=True,
    do_xcom_push=False,
    is_delete_operator_pod=False
)

k8s_example_task_2 = KubernetesPodOperator(
    namespace="spark-ds",
    image="adoptopenjdk/openjdk11:alpine-jre",
    cmds=["java", "--version"],
    name="k8s-example-task-2",
    task_id="k8s-example-task-2",
    startup_timeout_seconds=10,
    get_logs=True,
    dag=dag,
    in_cluster=True,
    do_xcom_push=False,
    is_delete_operator_pod=False
)

k8s_example_task_2.set_upstream(k8s_example_task_1)
