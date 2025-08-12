import pandas as pd
import numpy as np

series = {
    'year':[1978,  1999,  2008,  2013],
    'champion':['milan', 'udienese',  'juventus',  'roma'],
    'name':'team'
}

def get(series, year):
    ins_inx = series['year'].index(year)
    return series['champion'][ins_inx]


get(series, 2013)

#why do we prefer to use pandas instead

profit = pd.Series([205, 199, 10, -30], name = 'money')
profit

rev = pd.Series([205, 199, 10, -30],  name = 'money',  dtype='int64[pyarrow]')
rev

rev.index

class Foo:
    pass

sW_objVls = pd.Series(
    ['John',  'Weronika',  13,  Foo()],
    index = ['man', 'women', 'day', 'function'],
    name = 'example')

sW_objVls




ex2=  pd.Series([23,  21,  np.nan,  23,  43,  2.5,  23])
ex2.size
print(ex2.count())


#numpy array vs padnas series

npA_songs = np.array([145, 142, 38, 13])

pdS_songs = pd.Series([145, 142, 38, 13],
                      index = ['Paul', 'John', 'George', 'Ringo'],
                      name = 'counts',
                      dtype='int64[pyarrow]')


npA_songs[1]
pdS_songs[1] #future warning, use .iloc[pos]
pdS_songs.iloc[1]

npA_songs.mean()
pdS_songs.mean()

len(set(dir(npA_songs)) & set(dir(pdS_songs)))

#cd., maski

mask = pdS_songs > pdS_songs.median() #boolean array
mask

pdS_songs[mask]
pdS_songs[pdS_songs>pdS_songs.median()]

npA_songs[npA_songs>np.median(npA_songs)]

#Categorical Data


s = pd.Series(['s', 'm', 'l'], dtype = 'category')
s.cat.ordered

s2 = pd.Series(['m', 'l', 'xs', 's', 'xxl'], dtype = 'string[pyarrow]')
sizes_type = pd.CategoricalDtype(categories=['s', 'm', 'l'], ordered = True)
s3 = s2.astype(sizes_type)
s3
s3.sort_values()
s3>'s'

s = pd.Series(['s','m','l'], dtype = 'category')
s.cat.reorder_categories(['xl', 'l', 'm', 's', 'xs'], ordered=True) #ValueError - categories differ
s.cat.categories


s.cat.add_categories(['xs','xl']).cat.reorder_categories(['xl', 'l', 'm', 's', 'xs'], ordered=True)

s3.str.upper()

#Exercises
#1. Using Jupyter, create a series with the temperature values for the last seven days. Filter out the values below the mean.
#2. Using Jupyter, create a series with your favorite colors. Use a categorical type.

#1.
temperatures = pd.Series(['23.5', '25.3', '18.1', '14.0', '26.3', '32.4', '33.1'],
                         index=['tuesday', 'wendesday', 'thursday', 'friday', 'saturday', 'sunday', 'moonday'],
                         dtype = 'double[pyarrow]',
                         name = 'celsius') 
temperatures[temperatures >= temperatures.mean()]

#2.
color_types = pd.CategoricalDtype(['blue', 'green', 'purple', 'white', 'black', 'pink', 'orange', 'red'], ordered=True)
colors = pd.Series(['red', 'blue', 'green'], dtype=color_types)
colors.sort_values()