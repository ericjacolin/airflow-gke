from airflow.decorators import dag, task
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

from common.utils.task_pod_configmaps import task_pod_configmaps
from common.utils.task_pod_secrets import task_pod_secrets
from common.utils.task_pod_volumes import task_pod_volumes

from datetime import datetime

# Global env variables - will be available as environment variables in Task containers
env_vars = {
    'SENDER_EMAIL': 'eric@jacolin.net',
}
@dag(
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    catchup=False
)
def dag1():
    """
    DAG doco
    """
    # Project-based resources
    project='example1'
    # Config maps to mount as env variables in Task containers
    configmaps = task_pod_configmaps(project)
    # Secrets to mount as env variables in Task containers
    secrets = task_pod_secrets(project)
    # Volumes to mount on Task containers
    volumes = task_pod_volumes(project)

    # Pod compute resources required (usually only in remote environments)
    task1_compute_resources = {
        'request_cpu': '200m',
        'request_memory': '1Gi',
        'limit_cpu': '400m',
        'limit_memory': '3Gi'
    }

    task1 = KubernetesPodOperator(
        task_id="task1",
        name="dag1-task1",
        namespace="airflow",
        image="pandas-basic:0.0.1",
        cmds=["python"],
        arguments=[
            "/opt/airflow/dags/example1/dag1/tasks/task1.py",
            "some Task1 argument"
        ],
        env_vars=env_vars,
        env_from=configmaps,
        secrets=secrets,
        volumes=volumes['volumes'],
        volume_mounts=volumes['volume_mounts'],
        in_cluster=True,
        is_delete_operator_pod=True,
        #resources=task1_compute_resources,
        do_xcom_push=True,
    )

    task2 = KubernetesPodOperator(
        task_id="task2",
        name="dag1-task2",
        namespace="airflow",
        image="pandas-basic:0.0.1",
        cmds=["python"],
        arguments=[
            "/opt/airflow/dags/example1/dag1/tasks/task2.py",
            "{{ task_instance.xcom_pull('task1')['task1-output'] }}"
        ],
        env_vars=env_vars,
        volumes=volumes['volumes'],
        volume_mounts=volumes['volume_mounts'],
        in_cluster=True,
        is_delete_operator_pod=True,
        #resources=task1_compute_resources,
        do_xcom_push=True,
    )

    task1 >> task2

dag1 = dag1()
