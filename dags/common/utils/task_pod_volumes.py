from airflow.kubernetes.volume import Volume
from airflow.kubernetes.volume_mount import VolumeMount

def task_pod_volumes(project):
    """
    doco
    """

    volume_config_dag = {
        'hostPath':
            {
                'path': '/hosthome/projects/airflow-gke/dags',
                'type': 'Directory'
            }
    }
    volume_dag = Volume(name='dag', configs=volume_config_dag)

    volume_config_data = {
        'hostPath':
            {
                'path': '/hosthome/storage-buckets/airflow/' + project,
                'type': 'Directory'
            }
    }
    volume_data = Volume(name='data', configs=volume_config_data)

    volume_mount_dag = VolumeMount('dag',
                                mount_path='/opt/airflow/dags',
                                sub_path=None,
                                read_only=True)
    volume_mount_data = VolumeMount('data',
                                mount_path='/opt/data',
                                sub_path=None,
                                read_only=False)

    return {
        'volumes': [volume_dag, volume_data],
        'volume_mounts': [volume_mount_dag, volume_mount_data]
    }
