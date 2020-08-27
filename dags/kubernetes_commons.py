from airflow.contrib.kubernetes.volume import Volume
from airflow.contrib.kubernetes.volume_mount import VolumeMount

# Default affinity for tasks running in k8s cluster
ds_airflow_affinity = {
    "nodeAffinity": {
        "requiredDuringSchedulingIgnoredDuringExecution": {
            "nodeSelectorTerms": [{
                    "matchExpressions": [{
                            "key": "dedicated",
                            "operator": "In",
                            "values": ["spark-ds"]
                        }]
                }]
        }
    }
}

# Default tolerations for tasks running in k8s cluster
ds_airflow_tolerations = [
    {
        "effect": "NoExecute",
        "key": "dedicated",
        "operator": "Equal",
        "value": "spark-ds"
    }
]

ds_airflow_resources = {
    'request_ephemeral_storage': '1G'
}
