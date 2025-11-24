# LOOPING AND AGGREGATION
import pandas as pd

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

url = 'https://github.com/mattharrison/datasets/raw/master/data/'\
        'siena2018-pres.csv'

df = pd.read_csv(url, index_col=0, dtype_backend='pyarrow')
pres = tweak_siena_pres(df)

#iteration over columns (col_name, series) tuples
for col_name, col in pres.items():
    print(col_name, type(col))
    break

#itearion over rows as namedtumple (index as first item)
for tup in pres.itertuples():
    print(tup[0], tup.President)
    break

# Aggregations

scores = pres.loc[:,'Background':'Average_rank']
scores.sum(axis=1)/len(scores.columns)


pres.select_dtypes('number').agg(['count', 'size', 'sum', lambda col: col[1]])

pres.select_dtypes('number').agg({'Luck': ['count','size'],
                                  'Overall': ['count','max']})

pres.select_dtypes('number').agg(intelligence_size = ('Intelligence', 'size'),
                                 intelligence_count = ('Intelligence', 'count'))
pres.describe()

# The .apply Method

(pres
    .select_dtypes('number')
    .pipe(lambda df_: df_.max(axis='columns')
                        -df_.min(axis='columns'))
    .rename('range')
)
(pres
    .select_dtypes('number')
    .apply(lambda row: row.max()-row.min(), axis='columns')
    .rename('range')
)

pres.select_dtypes('number').apply('sum') #axis='index'
pres.select_dtypes('number').sum() #axis='index'

# Optimizing If Then

import io
import numpy as np

billing_data = \
'''cancel_date,period_start,start_date,end_date,rev,sum_payments
12/1/2019,1/1/2020,12/15/2019,5/15/2020,999,50
,1/1/2020,12/15/2019,5/15/2020,999,50
,1/1/2020,12/15/2019,5/15/2020,999,1950
1/20/2020,1/1/2020,12/15/2019,5/15/2020,499,0
,1/1/2020,12/24/2019,5/24/2020,699,100
,1/1/2020,11/29/2019,4/29/2020,799,250
,1/1/2020,1/15/2020,4/29/2020,799,250'''

bill_df = pd.read_csv(io.StringIO(billing_data),
                        dtype_backend='pyarrow',
                        parse_dates=['cancel_date', 'period_start', 'start_date',
                                    'end_date'])

def tweak_bill202(df_):
    return (df_.assign(
                cancel_date = pd.to_datetime(df_.cancel_date.replace('<NA>',''), format = '%m/%d/%Y')
    ))

bill_df = tweak_bill202(bill_df)

def unpayed_sum_rec(vals):
    cancel_date, period_start, start_date, end_date, rev, sum_payments = vals
    if cancel_date < period_start:
        return np.nan
    if start_date < period_start and end_date > period_start:
        if rev > sum_payments:
            return rev - sum_payments
        else:
            return 0

bill_df.apply(unpayed_sum_rec, axis=1)

def calc_unbilled_case(bill_df):
    return (pd.Series(np.nan, dtype='double[pyarrow]', index = bill_df.index)
        .case_when([(bill_df.cancel_date < bill_df.period_start,
                    np.nan),
            (((bill_df.start_date < bill_df.period_start) &
            (bill_df.end_date > bill_df.period_start) &
            (bill_df.rev > bill_df.sum_payments))
                        , bill_df.rev-bill_df.sum_payments),
            (((bill_df.start_date < bill_df.period_start) &
            (bill_df.end_date > bill_df.period_start) &
            (bill_df.rev <= bill_df.sum_payments))
                    , 0)
            ])
            )


# Optimizing .apply functions

bill_100k = bill_df.sample(100_000, replace=True)


%%timeit
bill_100k.apply(unpayed_sum_rec, axis='columns')


%% timeit
calc_unbilled_case(bill_100k)

# Exercises
# With a tabular dataset of your choice:

pres_df= pres.select_dtypes('number')

# 1. Loop over each row and calculate the maximum and minimum values.

for tup in pres_df.itertuples():
    print(max(tup[1:]), min(tup[1:]))

# 2. Calculate each row and column’s maximum and minimum value using the .agg method.

    pd.concat([pres_df.agg(['max','min'], axis=1),
    pres_df.agg(['max','min'], axis=0).T])

# 3. Calculate each row and column’s maximum and minimum value using the .apply method.
    pd.concat([    
        pres_df.apply(lambda row: {'max':row.max(), 'min':row.min()}, axis='columns'),
        pres_df.apply(lambda column: {'max':column.max(), 'min':column.min()}, axis='index')])



