import pandas as pd


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

