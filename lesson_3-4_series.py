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



