from kubernetes.client import models as k8s

def task_pod_configmaps(project):
    """
    doco
    """

    return [
        k8s.V1EnvFromSource(config_map_ref=k8s.V1ConfigMapEnvSource(name=project)),
    ]
