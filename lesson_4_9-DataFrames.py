# FILTERING AND INDEXING OPERATIONS
import pandas as pd

# Renaming an Index
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

def name_to_initial(val):
    names = val.split()
    return ' '.join([f'{names[0][0]}.', *names[1:]])
    
(pres
    .set_index('President')
    .rename(name_to_initial)
)

# Resetting the Index
(pres
    .set_index('President')
    .reset_index())

# Dataframe Indexing, Filtering & Querying

lt10 = pres.Average_rank<10

pres[lt10 & (pres.Party=='Republican')]

pres.query('Average_rank<10 and Party=="Republican"')
pres.query('@lt10 and Party=="Republican"')

# Indexing by Position

pres.iloc[[1]]
pres.iloc[[0,5,10]]
pres.iloc[0:11:5]
pres.iloc[lambda df: [0,5,10]]

pres.iloc[[0,5,10], 1]
pres.iloc[[0,5,10], [1]]
pres.iloc[:,[1,2]]
pres.iloc[:, 1:3]

# Indexing by Name
pres.loc[1:5]
pres.loc['1':'5']
pres.iloc[1:5]

pres.set_index('Party').loc['Whig']
pres.set_index('Party').loc[['Whig']]

pres.set_index('Party').loc['Federalist']
pres.set_index('Party').loc[['Federalist']]

(pres
    .set_index('Party')
    .sort_index()
    .loc['Democratic':'Independent']
)

(pres
    .set_index('President')
    .sort_index()
    .loc['C':'Thomas Jefferson', 'Party':'Integrity']
)

pres.dtypes

import pyarrow as pa
string_pa = pd.ArrowDtype(pa.string())

(pres
    .assign(Party = pres.Party.astype(string_pa))
    .set_index('Party')
    .sort_index()
    .loc['D':'J']
)

(pres
    .set_index('President')
    .sort_index()
    .sort_index(axis=1)
    .loc['C':'Thomas Jefferson','B':'D']
)

# Filtering with Functions and .loc

pres.loc[lt10, lambda df_: df_.columns[:3]]

# .query vs .loc
# -> "[...]Learn them both"

# Exercises
# With a dataset of your choice:

# Pull out the first two rows by name.
(pres
    .set_index('President')
    .loc[['George Washington', 'John Adams']]
)
# Pull out the first two rows by position.
pres.iloc[:2]
# Pull out the last two columns by name.
pres.loc[:, ['Average_rank', 'Quartile']]
# Pull out the last two columns by position.
pres.iloc[:,-2:]