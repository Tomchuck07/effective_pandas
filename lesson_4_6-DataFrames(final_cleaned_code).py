# CREATING AND UPDATING COLUMNS
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

