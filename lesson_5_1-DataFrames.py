import pandas as pd
# RESHAPING DATAFRAMES WITH DUMMIES

# Dummy Columns

url = 'https://github.com/mattharrison/datasets/raw/master/data/'\
       '2020-jetbrains-python-survey.csv'
jb = pd.read_csv(url, dtype_backend='pyarrow')

jb.filter(like='job.role')

import pyarrow as pa

string_pa=pd.ArrowDtype(pa.string())

job=(jb
    .filter(regex=r'job.role.*t')
    .where(jb.isna(), '1')
    .fillna('0')
    .astype('bool[pyarrow]')
    .idxmax(axis=1)
    .astype(string_pa)
    .str.replace('job.role.', '', regex=False)
)

dum = pd.get_dummies(job)

# Undoing Dummy Columns

dum.idxmax(axis='columns')

# Exercises
# With a dataset of your choice:

url = 'https://github.com/mattharrison/datasets/raw/master/data/'\
     'siena2018-pres.csv'

df = pd.read_csv(url, dtype_backend='pyarrow', engine='pyarrow', index_col=0)

# 1. Create dummy columns derived from a string column.

cols = pd.get_dummies(df.Party)

# 2. Undo the dummy columns.

cols.idxmax(axis=1)