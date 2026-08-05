# MELTING TRANSPOSING AND STACKING DATA
import pandas as pd
import io

# Melting Data

data = '''name,age,test1,test2,teacher
Adam,15,95.0,80,Ashby
Bob,16,81.0,82,Ashby
Dave,16,89.0,84,Jones
Fred,15,,88,Jones'''

scores = pd.read_csv(io.StringIO(data), dtype_backend='pyarrow')

pd.concat([scores.test1, scores.test2]).mean()

(scores
    .groupby(['name','age'])
    .apply(lambda g: pd.concat([
        g[['test1']].rename(columns={'test1':'val'})
                  .assign(var='test1'),
        g[['test2']].rename(columns={'test2':'val'})
                  .assign(var='test2') 
    ]))
    .sort_index(axis=1,ascending=False)
    .reset_index()
    .drop(columns='level_2')    
)

(scores
    .pivot_table(index=['name','age','teacher'])
    .stack(dropna=False)
    .reset_index()
    .drop(columns='teacher')
    .rename(columns={'level_3':'var', 0:'val'})
)

melted = (scores.melt(id_vars=['name','age','teacher'],
             value_vars=['test1','test2'],
             var_name='test',
             value_name='score')
)

# Un-melting Data

(melted.pivot_table(index=['name','age','teacher'],
                    columns='test',values='score')
        .reset_index()
)

(melted
    .groupby(['name','age','teacher','test'])
    .score
    .mean()
    .unstack()
    .reset_index()
)

# Pulling Out Categorical Values into Columns

melted.pivot(columns='teacher', values='score')

(scores
    .pivot(columns=['teacher'], values=['test1','test2'])
    .apply(lambda ser: ser
                        .dropna()
                        .reset_index(drop=True)
                        .astype('float16[pyarrow]'))
)

def shift_up_as_int(ser):
    
    return(ser
                .dropna()
                .reset_index(drop=True)
                .astype('int8[pyarrow]')
    )

melted.pivot(columns='teacher', values='score').apply(shift_up_as_int)

# Transposing Data
# Stacking and Unstacking

from common import tweak_jb

url = 'https://github.com/mattharrison/datasets/raw/master/data/'\
       '2020-jetbrains-python-survey.csv'

jb = pd.read_csv(url, dtype_backend='pyarrow', engine='pyarrow')

jb2 = tweak_jb(jb)

pd.crosstab(jb2.country_live, jb2.are_you_datascientist)
    
jb2.groupby(['country_live', 'are_you_datascientist'], observed=True).size().unstack()
jb2.groupby(['country_live', 'are_you_datascientist'], observed=True).size().unstack(0)
jb2.groupby(['country_live', 'are_you_datascientist'], observed=True).size().unstack('country_live')

# Stacking

