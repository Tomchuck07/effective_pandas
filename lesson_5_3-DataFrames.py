# MORE AGGREGATIONS
import pandas as pd
from common import tweak_jb

url = 'https://github.com/mattharrison/datasets/raw/master/data/'\
       '2020-jetbrains-python-survey.csv'

jb = pd.read_csv(url, dtype_backend='pyarrow', engine='pyarrow')

jb2 = tweak_jb(jb)

# Aggregations while Keeping Rows

jb2.assign(country_responses = (jb2
        .groupby('country_live', observed=True)
        .age
        .transform('size')))

# Filtering Parts of Groups

(jb2
    .country_live
    .value_counts()
    .median()
)

countries_to_remove=(jb2
    .country_live
    .value_counts()
    .lt(126.5)
    .pipe(lambda ser: ser[ser])
    .index
)

jb2.query('country_live.isin(@countries_to_remove)')

(jb2
    .groupby('country_live', observed=True)
    .filter(lambda g: g.country_live.size<126.5)
)

# # Exercises

df = pd.DataFrame({
    'Team': ['A', 'A', 'A', 'B', 'B', 'B', 'B', 'C', 'C'],
    'Revenue': [100, 150, 120, 200, 210, 190, 220, 50, 60]
})

# 1. Add a new column, the sum of a numeric column grouped by a string column.

df.assign(group_rev_sum=(df
    .groupby('Team')
    .Revenue
    .transform('sum'))
    )


# 2. Filter out the rows with less than three entries when grouped by a string column.

(df
    .groupby('Team')
    .filter(lambda g: g.Revenue.size>=3)
)