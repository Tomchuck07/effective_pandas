import pandas as pd
import numpy as np
import pyarrow as pa

# csv import

url = 'https://github.com/mattharrison/datasets/raw/master/data/' \
'vehicles.csv.zip'
df = pd.read_csv(url, dtype_backend = 'pyarrow', engine = 'pyarrow')

city_mpg = df.city08
highway_mpg = df.highway08

city_mpg
highway_mpg

len(dir(city_mpg))


# operators (&dunder methods)

2+4
(2).__add__(4)

(city_mpg)+(highway_mpg)/2

s1 = pd.Series([10, 20, 30], index = [1,2,2])
s2 = pd.Series([35, 44, 53], index = [2,2,4], name = 's2')

s1
s2

s1.add(s2, fill_value=0)

s2 + 5

s1+s2
s1.add(s2)

s1.add(s2, fill_value=0)

((city_mpg+highway_mpg)/2)
city_mpg.add(highway_mpg).div(2)

exmp = pd.Series([13, 24, 25, 11])
exmp+exmp
exmp+10
exmp2 = pd.Series([1, 2, 5, 7])
exmp.add(exmp2)

# Aggregate methods

city_mpg.mean()
city_mpg.is_unique
city_mpg.is_monotonic_increasing

city_mpg.quantile()
city_mpg.quantile(.9)

city_mpg.quantile([.1,.5,.9])

(city_mpg
 .gt(20)
 .sum())

(city_mpg
 .gt(20)
 .astype('int64[pyarrow]')
 .mul(100)
 .mean())

# .agg() and aggregation strings

city_mpg.agg('mean')


def second_to_last(s):
    return s.iloc[-2]

city_mpg.agg(['mean', np.var, max, second_to_last])
# # exercices
# Find the count of non-missing values of a series.
# Find the number of entries of a series.
# Find the number of unique entries of a series.
# Find the mean value of a series.
# Find the maximum value of a series.
# Use the .agg method to find all of the above.

# 1
ex = pd.Series([1, 2, 3, 3, 3, None, 5, 6, 9, 5])
ex.count()

# 2
ex.size

# 3
ex.nunique()

# 4
ex.mean()

# 5
ex.max()

# 6
ex.agg(['count', 'size', 'nunique', 'mean', 'max'])


# CONVERSION METHODS

# Type conversion

city_mpg.astype('int16[pyarrow]')
city_mpg.astype('int8[pyarrow]')

np.iinfo('int64')
np.iinfo('uint8')
np.finfo('float32')

# Memory usage

city_mpg.nbytes
city_mpg.astype('int16[pyarrow]').nbytes

make = df.make
make.nbytes
make.memory_usage()
make.memory_usage(deep=True)

make.astype(str).memory_usage()
make.astype(str).memory_usage(deep=True)

# String and category types

make.astype('category').memory_usage(deep=True)

city_mpg.astype('category').cat.as_ordered()

# Ordered categories

values = pd.Series(sorted(set(city_mpg)))
city_type = pd.CategoricalDtype(categories=values, ordered=True)
city_mpg.astype(city_type)

# Converting to other types

city_mpg.to_frame()

# Exercises
# With a dataset of your choice:

s = pd.Series([2, 7, 3, 11])
s.dtype

# 1. Convert a numeric column to a smaller type.

s1 = s.astype('int8[pyarrow]')
s1.dtype

# 2. Calculate the memory savings by converting to smaller numeric types.

s.nbytes
s1.nbytes

# 3. What is the proper type to cast into String types?

prop_type = pd.ArrowDtype(pa.string())

s3 = pd.Series(['one', 'two','three'])
s3.dtype
s3.astype(prop_type)

# 4. Convert a string column into a categorical type.

num_cat = pd.CategoricalDtype(categories=s3, ordered = True)
s4 = pd.Series(['three', 'one', 'three', 'two', 'three', 'two', 'one'])
s4
s4.astype(num_cat).sort_values()

# 5. Calculate the memory savings (or losses) by converting to a categorical type.

s4.memory_usage(deep=True)
s4.astype(num_cat).memory_usage(deep=True)




