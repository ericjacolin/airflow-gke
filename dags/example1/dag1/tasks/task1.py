from fs import open_fs
import pandas as pd
import numpy as np
import json
import sys
import os
from pathlib import Path
import mysql.connector
import sqlalchemy

# Read an input file, write to an output file in the mounted data folder
prefix = '/opt/data'
input_file = open_fs(prefix).open('/input/input.csv', mode='r')
open_fs(prefix).create('/output/output.csv', wipe=True)
output_file = open_fs(prefix).open('/output/output.csv', mode='w')
df = pd.read_csv(input_file)
#df.head()
df = df.apply(np.sqrt)
df.to_csv(output_file)

# Pulling arguments from the DAG KubernetesPodOperator "arguments" parameter
arg1 = sys.argv[1]

# Write to Xcom output
xcom = {
    'status-task1': 'completed',
    'email': os.environ.get('SENDER_EMAIL'),
    'dummy-config-key': os.environ.get('dummy-key'),
    'dummy-secret': os.environ.get('BIG_SECRET'),
    'task1-output': 'some output of task1',
    'arg1': arg1
}
Path('/airflow/xcom/return.json').write_text(json.dumps(xcom))

# Read from a DB, write to a file
db_conn = sqlalchemy.create_engine(
        'mysql+mysqlconnector://airflow_test:airflow_test@10.0.2.2:3306/airflow_test',
        pool_recycle=1,
        pool_timeout=57600
    ).connect()

df = pd.read_sql(
    "SELECT * FROM author",
    con=db_conn
)
#df.head()
open_fs(prefix).create('/output/output2.csv', wipe=True)
output_file = open_fs(prefix).open('/output/output2.csv', mode='w')
df.to_csv(output_file)
db_conn.close()
