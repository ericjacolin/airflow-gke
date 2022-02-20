from fs import open_fs
import pandas as pd
import numpy as np
import json

prefix = '/opt/data'
input_file = open_fs(prefix).open('/input/input.csv', mode='r')
open_fs(prefix).create('/output/output.csv', wipe=True)
output_file = open_fs(prefix).open('/output/output.csv', mode='w')
df = pd.read_csv(input_file)
#df.head()
df = df.apply(np.sqrt)
df.to_csv(output_file)

json_xcom = {
    'status1': 'completed'
}
with open('/airflow/xcom/return.json', 'w') as outfile:
    outfile.write(json.dumps(json_xcom))
