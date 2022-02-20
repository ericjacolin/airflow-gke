import sys
import json

status1 = sys.argv[1]

json_xcom = {
    'status2': status1 + ' also completed'
}
with open('/airflow/xcom/return.json', 'w') as outfile:
    outfile.write(json.dumps(json_xcom))
