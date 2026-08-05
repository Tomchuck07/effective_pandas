# RESHAPING BY PIVOTING AND GROUPING
import pandas as pd
from common import tweak_jb

url = 'https://github.com/mattharrison/datasets/raw/master/data/'\
       '2020-jetbrains-python-survey.csv'

jb = pd.read_csv(url, dtype_backend='pyarrow', engine='pyarrow')

jb2 = tweak_jb(jb)
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

