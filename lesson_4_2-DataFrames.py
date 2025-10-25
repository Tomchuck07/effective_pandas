import pandas as pd

# Similarities with Series and DataFrames

# Getting the Data
url = 'https://github.com/mattharrison/datasets/raw/master/data/'\
'siena2018-pres.csv' 
df = pd.read_csv(url, index_col=0, dtype_backend='pyarrow')

df.dtypes

def tweak_siena_pres(df):
    def int64_to_uint8(df_):
        cols = df_.select_dtypes('int64')
        return (df_
                .astype({col: 'uint8[pyarrow]' for col in cols}))
    
    return (df
        .rename(columns={'Seq.':'Seq'})         #1
        .rename(columns={k:v.replace(' ', '_') for k,v in
              {'Bg': 'Background',
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
        .astype({'Party':'category'})    #2
        .pipe(int64_to_uint8)            #3
        .assign(Average_rank=lambda df_:(df_.select_dtypes('uint8')  #4
            .sum(axis=1).rank(method='dense').astype('uint8[pyarrow]')),
                Quartile=lambda df_:pd.qcut(df_.Average_rank, 4,
                    labels='1st 2nd 3rd 4th'.split())
                )   
    )

tweak_siena_pres(df)


dfs = pd.DataFrame([
    {'Obs Date':'1980/01/01', 'Precip.':'0.1', 'Snowfall':1, 'T. Obs':25},
    {'Obs Date':'1980/01/02', 'Precip.':'T', 'Snowfall':0, 'T. Obs':18},
    ]
)

def tweak_snow(dfs):
    dfs=(
        dfs.rename(columns=lambda c: c.lower().replace(' ','_').replace('.',''))
        .assign(obs_date=lambda df2: pd.to_datetime(df2.obs_date),
                precip=dfs['Precip.'].replace('T','0').astype('float64[pyarrow]'))
    )
    return dfs

tweak_snow(dfs).dtypes

import matplotlib.pyplot as plt
import seaborn as sns

fix, ax = plt.subplots(figsize=(10,10), dpi=600)

g = sns.heatmap(tweak_siena_pres(df)
                .set_index('President')
                .loc[:,'Background':'Overall']
                .astype('uint8'),
                annot=True, cmap='viridis', ax=ax)

g.set_xticklabels(g.get_xticklabels(), rotation=45, fontsize=8,
                  ha='right')
_=plt.title('Presidential ranking')

# Viewing Data

pres = tweak_siena_pres(df)

print(pres.head(3))
print(pres.sample(3))

# Exercises
# With a tabular dataset of your choice:

# 1. Create a dataframe from the data.
# 2. View the first 20 rows of data.
# 3. Sample 30 rows from your data.