# DATAFRAMES
# Database and Spreadsheet Analogues (...)

# A Simple Python Version


df_python = {
    'index':[0,1,2],
    'cols':[
        {'name':'growth',
         'data': [.5, .7, 1.2]},
        {'name':'Name',
         'data': ['Paul', 'George', 'Ringo']}
    ]
}

def get_row(df, idx):
    results = []
    value_index = df['index'].index(idx)
    for col in df['cols']:
        results.append(col['data'][value_index])
    return results

get_row(df, 1)

def get_col(df, name):
    for col in df['cols']:
        if col['name'] == name:
            return col['data']


get_col(df_python, 'Name')

# Dataframes 
import pandas as pd
import pyarrow as pa

df = pd.DataFrame({
    'growth': [.5, .7, 1.2],
    'Name': ['Paul','George', 'Ringo']}
)
print(df)

df.iloc[2]
df['Name']

type(df['Name'])
df['Name'].str.lower()
df.Name

# Construction

print(pd.DataFrame([
    {'growth':.5, 'Name':'Paul'},
    {'growth':.7, 'Name':'George'},
    {'growth':1.2, 'Name':'Ringo'}]
))

from io import StringIO

csv_file = StringIO("""growth,Name
                    .5,Paul
                    .7,George
                    1.2,Ringo""")

print(pd.read_csv(csv_file, dtype_backend='pyarrow', engine='pyarrow'))

import numpy as np

np.random.seed(42)
pd.DataFrame(np.random.randn(10,3),
             columns=['a','b','c'])

# Dataframe Axis
df.axes
df.sum(axis=0)
df.sum(axis=1)
df.sum(axis='index')
df.axes[0]
df.axes[1]

df2 = pd.DataFrame({
    'score1': [None,None],
    'score2':[85,90]}
)
df2
df2.apply(np.sum, axis=0)
df2.apply(np.sum, axis=1)

# Exercises
# 1. Create a dataframe with the names of your colleagues, their age (or an estimate), and their title.
# 2. Capitalize the values in the name column.
# 3. Sum up the values of the age column.

# 1
d1 = pd.DataFrame({
    'imie':['radek','tomek','filip','karol'],
    'wiek':[22, 24, 24, 25],
    'tytuł': ['lic', 'lic', 'lic', 'mgr']
})
# 2
d1['imie'].str.capitalize()
d1.imie.str.capitalize()

# 3
d1.wiek.sum()
