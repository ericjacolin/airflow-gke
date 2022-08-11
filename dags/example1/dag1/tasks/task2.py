import json
import sys
import os

# Pulling xcom argument from the DAG KubernetesPodOperator "arguments" parameter
arg1 = sys.argv[1]

json_xcom = {
    'task1_output': arg1,
    'status-task2': 'also completed'
}
with open('/airflow/xcom/return.json', 'w') as outfile:
    outfile.write(json.dumps(json_xcom))
