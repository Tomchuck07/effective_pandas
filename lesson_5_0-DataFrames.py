# PLOTTING WITH DATAFRAMES

import pandas as pd
import matplotlib.pyplot as plt

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
                                            labels = '1th 2th 3th 4th'.split()),
                Party = lambda df_: df_.Party.astype('category')
            )
    )

url = 'https://github.com/mattharrison/datasets/raw/master/data/'\
     'siena2018-pres.csv'

df = pd.read_csv(url, dtype_backend='pyarrow', engine='pyarrow', index_col=0)

pres = tweak_siena_pres(df)

# Lines Plots

pres.plot().legend(bbox_to_anchor=(1,1))

fig, ax = plt.subplots(dpi=600, figsize=(10,8))

colors=[]
def set_colors(df):
        for col in df.columns:
            if 'George' in col:
                colors.append('#990000')
            else:
                colors.append('#999999')
        return df
(pres
    .set_index('President')
    .loc[::2, 'Background':'Overall']
    .T
    .pipe(set_colors)
    .plot(ax=ax, rot=45, color=colors).legend(bbox_to_anchor=(1,1), ncols=1)
)

ax.set_xticks(range(21))
ax.set_xticklabels(pres.loc[:,'Background':'Overall'].columns, ha='right')
ax.set_ylabel('rank')

# Bar Plots

fig, ax = plt.subplots(dpi=600, figsize=(10,8))

(pres
    .set_index('President')
    .iloc[:,-5:-1]
    .plot.bar(rot=45, ax=ax)    
)

ax.set_xticklabels(labels=ax.get_xticklabels(), ha='right')
ax.legend(bbox_to_anchor=(1,1))

ax = (pres
        .set_index('President')
        .iloc[:,-5:-1]
        .plot.barh(figsize=(4,12))
        .legend(bbox_to_anchor=(1,1)) 
     )

# Scatter Plots

url = 'https://github.com/mattharrison/'\
  'datasets/raw/master/data/alta-noaa-1980-2019.csv'
alta = (pd.read_csv(url, parse_dates=['DATE'], dtype_backend='pyarrow')
         .loc[:, ['DATE', 'PRCP', 'SNOW', 'SNWD', 'TMAX', 'TMIN']])

alta.SNOW.corr(alta.PRCP)
(alta
    .assign(
         SNOW = lambda df_: df_.SNOW+1, 
         PRCP = lambda df_: df_.PRCP+1 
    )
    .plot.scatter(x='PRCP', y='SNOW', alpha=.7, logx=True, logy=True, c='TMAX', cmap='coolwarm')
)

#TBC on 14.12.25