from kubernetes.client import models as k8s
from airflow.kubernetes.secret import Secret

def task_pod_secrets(project):
    """
    doco
    """

    return [
        Secret('env', None, project)
    ]
