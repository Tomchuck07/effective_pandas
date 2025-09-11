import pandas as pd

url = 'https://github.com/mattharrison/datasets/raw/master/data/' \
'vehicles.csv.zip'
df = pd.read_csv(url, dtype_backend = 'pyarrow', engine = 'pyarrow')

city_mpg = df.city08
highway_mpg = df.highway08
make = df.make

# INDEXING OPERATIONS

# Prepping the Data and Renaming the Index

city2 = city_mpg.rename(make.to_dict())
city2
city2.index
city2 = city_mpg.rename(make)
city2
city2.rename('citympg')

print(city2.reset_index())
city2.reset_index(drop=True)

city2.rename_axis('first').reset_index()

# The .loc Attribute

city2.loc['Subaru']
city2.loc['Fisker']

city2.loc[['Fisker']]
city2.loc[['Lamborghini', 'Ferrari']]

city2.loc['Ferrari' : 'Lamborghini']
city2.sort_index(ascending=False).loc['Lamborghini' : 'Ferrari']

city2.sort_index().loc['F':'J']

city2.loc[pd.Index(['Bugatti'])]
city2.loc[pd.Index(['Bugatti', 'Bugatti'])]

mask = city2 > 50
mask

city2.loc[mask]

cost = pd.Series([1.00, 2.25, 3.99, .99, 2.79]
                , index=['Gum', 'Cookie', 'Melon', 'Rol', 'Carrots'])

inflation = 1.1

(cost
 .multiply(inflation)
 .loc[lambda s_: s_>3]
)

mask2 = cost.multiply(inflation)>3
cost.loc[mask2]

# The .iloc Attrubute

city2.iloc[0]
city2.iloc[-1]
city2.iloc[[0, 1, -1]]
city2.iloc[0:5]
city2.iloc[-8:]

mask = city2 > 50
city2.iloc[mask]

mask = city2 > 50
city2.iloc[mask.to_numpy()]
city2.iloc[list(mask)]  

# Head and Tails

city2.head(3)
city2.tail(3)

# Sampling

city2.sample(6, random_state=42)

# Filtering Index Values

city2.filter(items=['Subaru', 'Ford'])
city2.filter(like='rd')
city2.filter(regex='(Ford)|(Subaru)')

# Reindexing

city2.reindex(['Missing', 'Ford'])

s1 = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
s2 = pd.Series([15, 25, 35], index=['b', 'c', 'd'])

city_mpg.reindex([0,0, 10, 20, 20_000_000])

s2.reindex(s1.index)

# EXERCISES
# With a dataset of your choice:

# 1. Inspect the index.
# 2. Sort the index.
# 3. Set the index to monotonically increasing integers starting from 0.
# 4. Set the index to monotonically increasing integers starting from 0, then convert these to the string version. Save this a s2.
# 5. Using s2, pull out the first five entries.
# 6. Using s2, pull out the last five entries.
# 7. Using s2, pull out one hundred entries starting at index position
# 8. Using s2, create a series with values with index entries '20', '10', and '2'.

ser = pd.Series([10, 34, 4, 34, 23, 11, 2, 3, 6, 26, 15, 23, 5, 6, 19, 20, 8, 17]
                , index=['Z', 'Y', 'X', 'W', 'V', 'U', 'T', 'S', 'R', 'Q', 'P', 'O', 'N', 'M', 'L', 'K', 'J', 'I'])

# 1
ser.index
# 2
ser.sort_index()
# 3
ser.reset_index(drop=True)
# 4
s2 = ser.reset_index(drop=True)
s2.index
s2.index = s2.index.astype('string')
s2.index
# 5
s2.head(5)
# 6
s2.tail(5)
# 7
index_pos = 4
s2.iloc[index_pos:(index_pos+10)]
# 8
s2.reindex(['20', '10', '2'])

