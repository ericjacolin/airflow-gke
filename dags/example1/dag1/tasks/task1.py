from fs import open_fs
import pandas as pd
import numpy as np
import json
import os
from pathlib import Path

prefix = '/opt/data'
input_file = open_fs(prefix).open('/input/input.csv', mode='r')
open_fs(prefix).create('/output/output.csv', wipe=True)
output_file = open_fs(prefix).open('/output/output.csv', mode='w')
df = pd.read_csv(input_file)
#df.head()
df = df.apply(np.sqrt)
df.to_csv(output_file)

# Write to Xcom
xcom = {
    'status1': 'completed ' + os.environ.get('SENDER_EMAIL') + ' ' + os.environ.get('dummy-key') + ' ' + os.environ.get('BIG_SECRET')
}
Path('/airflow/xcom/return.json').write_text(json.dumps(xcom))
