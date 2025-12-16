# RESHAPING BY PIVOTING AND GROUPING
import catboost as cb
import numpy as np
import pandas as pd

import collections

def get_uniq_cols(jb):
    counter = collections.defaultdict(list)
    for col in sorted(jb.columns):
        period_count = col.count('.')
        if period_count >=2:
            part_end = 2
        else:
            part_end = 1
        parts = col.split('.')[:part_end]
        counter['.'.join(parts)].append(col)

    uniq_cols = []
    for cols in counter.values():
        if len(cols) == 1:
            uniq_cols.extend(cols)
    return uniq_cols

def prep_for_ml(df):
    df_ = df.assign(
        **df.select_dtypes(['number','bool'])
            .astype('float[pyarrow]').astype(float),
        **{col: df[col].astype(str).fillna('')
            for col in df.select_dtypes(['category','string', 'object'])}
    )
    return df_

def predict_col(df, col):
    df = prep_for_ml(df)
    non_missing = df.query(f'~{col}.isna()')

    cat_idx = [i for i, typ in enumerate(df.drop(columns=[col]).dtypes)
               if str(typ) == 'object']

    y = non_missing[col]
    x = non_missing.drop(columns=[col]).values

    model = cb.CatBoostRegressor(iterations=20, cat_features=cat_idx)
    model.fit(x, y, cat_features=cat_idx)
    pred = model.predict(df.drop(columns=[col]))

    return df[col].where(~df[col].isna(), pred)

def tweak_jb(jb):
    uniq_cols = get_uniq_cols(jb)
    return (jb[uniq_cols]
                .rename(columns=lambda c: c.replace('.','_'))
                .assign(age = lambda df_: df_.age
                                    .str.slice(0,2)
                                    .replace('',np.nan)
                                    .astype('int8[pyarrow]'),
                        are_you_datascientist = lambda df_: df_.are_you_datascientist
                                    .replace({'Yes': '1', 'No': '0', '': '0', 'Other': '0'})
                                    .astype('bool[pyarrow]'),
                        company_size = lambda df_: df_.company_size
                                    .replace({'Just me': '1', '': pd.NA,
                                            'Not sure': pd.NA, 'More than 5,000': '5000',
                                            '2–10': '2', '11–50':'11','51–500': '51', '501–1,000':'501',
                                            '1,001–5,000':'1001'})
                                    .astype('int16[pyarrow]'),
                            country_live = lambda df_: df_.country_live.astype('category'),
                        employment_status = lambda df_: df_.employment_status.fillna('Other').astype('category'),
                        is_python_main = lambda df_: df_.is_python_main.astype('category'),
                        team_size = lambda df_: df_.team_size
                                    .str.split('-', expand=True).iloc[:,0]
                                    .replace('More than 40 people', '41')
                                    .where(df_.company_size!=1,'1')
                                    .replace('',pd.NA)
                                    .astype('float64[pyarrow]'),
                        years_of_coding = lambda df_: df_.years_of_coding.replace('Less than 1 year', '.5')
                                    .str.extract(r'(?P<years_of_coding>\.?\d+)')
                                    .astype('float64[pyarrow]'),
                        python_years = lambda df_: df_.python_years.replace('_', '.')
                                    .str.extract(r'(?P<python_years>\.?\d+)')
                                    .astype('float64[pyarrow]'),
                        use_python_most = lambda df_: df_.use_python_most.fillna('Unknown'),
                        python3_ver=lambda df_:df_.python3_version_most
                                    .str.replace('_', '.')
                                    .str.extract(r'(?P<python3_ver>\d\.\d)')
                                    .astype('float64[pyarrow]')
                )
                .assign(
                        team_size = lambda df_: predict_col(df_, 'team_size').astype(int)
                )
                #.drop(columns=['python2_version_most'])
                .loc[:, ['age', 'are_you_datascientist', 'company_size', 'country_live',
                'employment_status', 'first_learn_about_main_ide',
                'how_often_use_main_ide', 'ide_main', 'is_python_main', 'job_team',
                'main_purposes', 'missing_features_main_ide', 'nps_main_ide',
                'python_years', 'python3_version_most', 'several_projects', 'team_size',
                'use_python_most', 'years_of_coding', 'python3_ver']]
            )

url = 'https://github.com/mattharrison/datasets/raw/master/data/'\
       '2020-jetbrains-python-survey.csv'

jb = pd.read_csv(url, dtype_backend='pyarrow', engine='pyarrow')

jb2 = tweak_jb(jb)
jb2.columns
# A Basic Example

(jb2.pivot_table(index='country_live', columns='employment_status',
                  values=['age','years_of_coding'], aggfunc='mean'))

pd.crosstab(index=jb2.country_live, columns=jb2.employment_status,
            values=jb2.age, aggfunc='mean')

(jb2
    .groupby(['country_live', 'employment_status'])
    .age
    .mean()
    .unstack()
)

# Using a Custom Aggregation Function

def per_emacs(ser):
    return ser.str.contains('Emacs').mean()*100

(jb2
    .pivot_table(index='country_live', values='ide_main', aggfunc=per_emacs)
)

pd.crosstab(
        index=jb2.country_live,
        columns=jb2.assign(iden='emacs_per').iden,
        values=jb2.ide_main,
        aggfunc=per_emacs
)

(jb2
    .groupby('country_live')
    .ide_main
    .agg(per_emacs)
)

# Multiple Aggregations

(jb2
    .pivot_table(index='country_live', values='age', aggfunc=('min', 'max'))
)

pd.crosstab(
        index=jb2.country_live, values=jb2.age,
        columns=jb2.assign(wiek='wiek').wiek,
        aggfunc=['min','max']
)

(jb2
    .groupby('country_live')
    .age
    .agg(['min','max'])
)

# Per Column Aggregations

(jb2
    .groupby('country_live')
    [jb2.select_dtypes('number').columns]
    .agg(['min','max'])
)

(jb2
    .pivot_table(index='country_live',
                 values=jb2.select_dtypes('number').columns,
                 aggfunc=('min','max'))
)


(jb2
    .pivot_table(index='country_live', aggfunc={'age':['min','max'],
                                                'team_size':'mean'})
)

(jb2
    .groupby('country_live')
    .agg({'age':['min','max'],
         'team_size':'mean'})
)

(jb2
    .groupby('country_live')
    .agg(age_min = ('age','min'),
         age_max=('age','max'),
         avg_team_size=('team_size','mean'))
)

# Grouping by Hierarchy

(jb2
    .pivot_table(index=['country_live', 'ide_main'],
                values='age',
                aggfunc=['min','max'])
)

(jb2
    .groupby(by=['country_live','ide_main'])
    [['age']]
    .agg(['min','max'])
)


(jb2
    .groupby(by=['country_live','ide_main'], observed=True)
    .agg(age_min = ('age','min'),
         age_max = ('age','max'))
)

def even_grouper(idx):
    return 'odd' if idx%2 else 'even'

jb2.pivot_table(index=even_grouper, aggfunc='size')
jb2.groupby(even_grouper).size()


# Exercises
# With a dataset of your choice:

data = {
    'Region': ['North', 'South', 'North', 'East', 'South', 'East', 'North', 'West', 'South', 'East', 'West', 'North', 'East', 'South', 'West'],
    'Category': ['A', 'B', 'A', 'C', 'B', 'A', 'B', 'C', 'A', 'C', 'B', 'A', 'B', 'C', 'A'],
    'Sales_Amount': [150.5, 200.0, 150.5, 50.2, 200.0, 180.0, 250.0, 75.0, 120.0, 60.0, 90.0, 150.5, 200.0, 250.0, 150.5],
    'Units_Sold': [10, 5, 10, 2, 5, 8, 12, 3, 4, 2, 3, 10, 5, 12, 10],
    'Customer_Rating': [4, 5, 4, 3, 5, 4, 5, 3, 4, 3, 4, 4, 5, 5, 4]
}

sales = pd.DataFrame(data)

sales['Region'] = sales['Region'].astype('category')
sales['Category'] = sales['Category'].astype('category')
sales['Customer_Rating'] = sales['Customer_Rating'].astype('int8')

# 1. Group by a categorical column and take the mean of the numeric columns.

(sales
    .groupby('Region')
    .mean(numeric_only=True)
)

# 2. Group by a categorical column and take the mean and max of the numeric columns.

(sales
    .select_dtypes('number')
    .assign(Region=sales.Region)
    .groupby('Region')
    .agg(['max','mean'])
)

# 3. Group by a categorical column and apply a custom aggregation function that calculates the mode of the numeric columns.

def top_n(ser):

    vc = ser.value_counts()
    return (vc
            [vc==vc.iloc[0]]
            .index)

(sales
    .select_dtypes('number')
    .assign(Category=sales.Category)
    .groupby('Category')
    .agg(top_n)
)



# 4. Group by two categorical columns and take the mean of the numeric columns.


(sales
    .groupby(by=['Region','Category'])
    .mean(numeric_only=True)
)

# 5. Group by binned numeric column and take the mean of the numeric columns.

binned_units_sold = pd.qcut(sales.Units_Sold, q=3)

def idx_to_bins(idx):
        return binned_units_sold[idx]

(sales
    .groupby(idx_to_bins)
    [['Sales_Amount','Customer_Rating']]
    .mean()
)

