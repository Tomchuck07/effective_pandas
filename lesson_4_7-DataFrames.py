import pandas as pd
import numpy as np

# DEALING WITH MISSING AND DUPLICATED DATA

def tweak_siena_pres(df):
    def int64_to_uint8(df):
        cols = df.select_dtypes('int64')
        return df.astype({col: 'uint8[pyarrow]' for col in cols})        
    
    return(
        df
            .rename(columns={'Seq.':'Seq'})
            .rename(columns = {k:v.replace(' ','_')
                               for k,v in {'Bg': 'Background',
              'PL': 'Party leadership', 'CAb': 'Communication ability',
              'RC': 'Relations with Congress', 'CAp': 'Court appointments',
              'HE': 'Handling of economy', 'L': 'Luck',
              'AC': 'Ability to compromise', 'WR': 'Willing to take risks',
              'EAp': 'Executive appointments', 'OA': 'Overall ability',
              'Im': 'Imagination', 'DA': 'Domestic accomplishments',
              'Int': 'Integrity', 'EAb': 'Executive ability',
              'FPA': 'Foreign policy accomplishments',
              'LA': 'Leadership ability',
              'IQ': 'Intelligence', 'AM': 'Avoid crucial mistakes',
              'EV': "Experts' view", 'O': 'Overall'}.items()})
            .pipe(int64_to_uint8)
            .assign(
                Average_rank = lambda df_: df_.select_dtypes('number')
                                                .sum(axis=1).rank(method='dense').astype('uint8[pyarrow]'),
                Quartile = lambda df_: pd.qcut(df_.Average_rank, 4,
                                            labels = '1th 2th 3th 4th'.split())
            )
    )



url = 'https://github.com/mattharrison/datasets/raw/master/data/'\
     'siena2018-pres.csv'
df = pd.read_csv(url, index_col=0, dtype_backend='pyarrow')

pres = tweak_siena_pres(df)



# Missing Data

pres.isna().any()

print(pres[pres.Integrity.isna()])

pres.query('Integrity.isna()')

pres.isna().sum()
pres.isna().mean()


# Duplicates

pres.drop_duplicates(subset='Party', keep='last')
pres.drop_duplicates(subset='Party', keep=False)

(pres
    .assign(
        first_in_seq = lambda df_:
                            df_.Party != df_.Party.shift(1)
    )).query('first_in_seq')

# Exercises
# With a dataset of your choice:

from io import StringIO

csv_data = """
Student_ID,Subject,Semester,Grade,Attendance_Days,Tutor_Name,Tutor_ID,Comments
101,Math,Fall,92,28,Smith,10,Excellent
102,Science,Fall,85,30,Jones,20,Good
103,Math,Spring,78,25,Smith,10,Average
104,History,Fall,65,29,Adams,30,Needs work
105,Math,Spring,90,30,Smith,10,Excellent
106,Science,Fall,88,27, ,20,Good
107,Math,Spring,95,30,Jones, ,Excellent
108,History,Fall, ,26,Adams,30,Missing Data
109,Math,Fall,82,29,  ,10,Good
104,History,Fall,65,29,Adams,30,Needs work
"""
df_e = pd.read_csv(StringIO(csv_data), dtype_backend='pyarrow', skipinitialspace=True)

# 1. Find out which columns have missing data.

df_e.isna().any()[df_e.isna().any()]

# 2. Count the number of missing values for each column.

df_e.isna().sum()

# 3. Find the percentage of missing values for each column.

df_e.isna().mean().mul(100)

# 4. Find the rows with missing data.

df_e[df_e.isna().any(axis=1)]

# 5. Find the rows that are duplicated.

df_e[df_e.duplicated()]


