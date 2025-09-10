import pandas as pd

url = 'https://github.com/mattharrison/datasets/raw/master/data/' \
'vehicles.csv.zip'
df = pd.read_csv(url, dtype_backend = 'pyarrow', engine = 'pyarrow')

city_mpg = df.city08
highway_mpg = df.highway08

# MANIPULATION METHODS

# .apply and .where

def gt20(val):
    return val > 20

%%timeit
city_mpg.apply(gt20)

%%timeit
city_mpg.gt(20)

make = df.make
make.value_counts()

top5 = make.value_counts().index[:5]
top10 = make.value_counts().index[:10]


def generalize_top5(val):
    if val in top5:
        return val
    else:
        return 'other'

%%timeit
make.apply(generalize_top5)

%%timeit
make.where(make.isin(top5), 'Other')

make.mask(~make.isin(top5), 'Other')

# Apply with numpy function

import numpy as np
import math

%%timeit
np.log(city_mpg)

%%timeit
city_mpg.apply(math.log)

%%timeit
city_mpg.apply(np.log)


# If Else with Pandas

vc = make.value_counts()
top5 = vc.index[:5]
top10 = vc.index[:10]

def generalize(val):
    if val in top5:
        return val
    elif val in top10:
        return 'top10'
    else:
        return "Other"

make.apply(generalize)

make.case_when(caselist=[(make.isin(top5), make),
                (make.isin(top10), 'top10'),
                (pd.Series(True, index=make.index), 'Other')])

(make
 .where(make.isin(top5), 'Top10')
 .where(make.isin(top10), 'Other')
)

# Missing data

cyl = df.cylinders

(cyl
 .isna()
 .sum()
)

missing = cyl.isna()
make.loc[missing]

# Filling in missing data

cyl.loc[cyl.isna()]
cyl.fillna(0)[7136:7141]

# Interpolating data

s = pd.Series([2, 4, 4, 5, None, 8, 3, 6], dtype='int8[pyarrow]')
s
s.astype('float[pyarrow]').interpolate()

# Clipping Data

city_mpg.loc[:447]

(city_mpg
 .loc[:447]
 .clip(lower=city_mpg.quantile(0.05),
       upper=city_mpg.quantile(0.95))
)

# Sorting Values

city_mpg.sort_values()
(city_mpg.sort_values() + highway_mpg)/2 

# Sorting the Index

city_mpg.sort_values().sort_index()

# Dropping Duplicates

city_mpg.drop_duplicates()

# Ranking Data

city_mpg.rank()
city_mpg.rank(method='min')
city_mpg.rank(method='dense')

# Repalcing Data

make
make.replace('Subaru', 'スバル')
make.replace(to_replace=['Dodge', 'Subaru'], value=['Doge', 'スバル'])
make.replace(r'(Fer)ra(r.*)'
             , value=r'\2-other-\1'
             , regex=True)

# Binning Data

pd.cut(city_mpg, 10)
pd.cut(city_mpg, [0, 10, 20, 40, 70, 150])
pd.qcut(city_mpg, 10)
pd.qcut(city_mpg, 10, labels=list(range(1,11)))

# EXERCISES

# 1.Create a series from a numeric column that has the value of 'high' if it is equal to or above the mean and 'low' if it is below the mean using .apply.
# 2. Create a series from a numeric column that has the value of 'high' if it is equal to or above the mean and 'low' if it is below the mean using .case_when.
# 3. Time the differences between the previous two solutions to see which is faster.
# 4. Replace the missing values of a numeric series with the median value.
# 5. Clip the values of a numeric series between to 10th and 90th percentiles.
# 6. Using a categorical column, replace any value that is not in the top 5 most frequent values with 'Other'.
# 7. Using a categorical column, replace any value that is not in the top 10 most frequent values with 'Other'.
# 8. Make a function that takes a categorical series and a number (n) and returns a replace series that replaces any value not in the top n most frequent values with 'Other'.
# 9. Using a numeric column, bin it into 10 groups with the same width.
# 10. Using a numeric column, bin it into 10 groups that have equal-sized bins.

# 1
s1 = pd.Series([7, 18, 3, 4, 19, None, 6, 7, 14, 1, 16, None, 9, 3, 15, 18, 4, 14]
               , dtype='int8[pyarrow]')

def relMean(val):
    if val >= s1.mean():
        return 'high'
    return 'low'

%%timeit
s1.apply(relMean)

# 2
%%timeit
s1.case_when(caselist=[
                    (s1>=s1.mean(), 'high'), 
                    (s1<s1.mean(), 'low')]
            )

# 3
# Anwser: 2.11ms vs 1.08ms 

# 4
s1.astype('double').fillna(s1.median())

# 5
s1.clip(s1.quantile(0.1), s1.quantile(0.9))

# 6
grades = pd.Series([
    'A','B+','C-','D','F','B','A-','C','B-','A+',
    'C+','D-','B','A','C','F','B+','D','A-','C+',
    'B','A','C-','D+','F','B-','A+','C','B+','D',
    'A','C+','B-','D-','F','A-','C','B','A+','D+',
    'C','B+','A','D-','F','B','C+','A-','B','C-'
], dtype='category')
grades = grades.cat.add_categories(['Other'])


top5 = grades.value_counts().index[:5]
grades.where(grades.isin(top5), 'Other')

# 7
top10 = grades.value_counts().index[:10]
grades.where(grades.isin(top10), 'Other')

# 8

def f8(ser, n):
    topn = ser.value_counts().index[:n]
    boolser = ser.isin(topn)
    return ser.where(boolser, 'Other')

f8(grades, 4)

# 9
pd.cut(s1, 10)

# 10
pd.qcut(s1, 10)

