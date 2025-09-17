import pandas as pd
import pyarrow as pa

url = 'https://github.com/mattharrison/datasets/raw/master/data/' \
'vehicles.csv.zip'
df = pd.read_csv(url, dtype_backend = 'pyarrow', engine = 'pyarrow')

city_mpg = df.city08
highway_mpg = df.highway08
make = df.make

# STRING MANIPULATION

# Strings and Objects
make

make.astype(str) # go old school
string_pa = pd.ArrowDtype(pa.string())
make.astype(str).astype(string_pa)

# Categorical Strings
make.astype('category')

# The .str Accessor

'FoRd'.lower()
'Hello'.lower()
make.str.lower()

'Alfa Romeo'.find('A')
make.str.find('A')

# Searching
make.str.extract(r'([^a-z A-Z])')
make.str.extract(r'(?P<non_alpha>[^a-z A-Z])', expand=False).value_counts()

# Splitting
age = pd.Series(['0-10', '11-15', '11-15', '61-65', '46-50'],
                dtype=string_pa)

age.str.split('-', expand=True).iloc[:, 0].astype('int8[pyarrow]')
age.str.slice(-2).astype('int8[pyarrow]')
age.str[-2:].astype('int8[pyarrow]')

(age
 .str
 .split('-', expand=True)
 .astype('int8[pyarrow]')
 .mean(axis='columns')
)

import random

def between(row):
    return random.randint(*row.values)

%%timeit
print(age
 .str
 .split('-', expand=True)
 .astype('int8[pyarrow]')
 .apply(between, axis='columns')
)

# Removing .apply

import numpy as np

%%timeit
print(age.
str.split('-', expand=True)
.rename(columns={0: 'lower', 1: 'upper'})
.astype('int8[pyarrow]')
.assign(rand = np.random.rand(len(age))
        , age = lambda df_: (df_.lower + (df_.rand*
                            (df_.upper - df_.lower)))
                            .astype('int8[pyarrow]', errors = 'ignore')
        )
)

# Optimizing with NumPy


%%timeit
print(age
      .str.split('-', expand=True)
      .astype('int8[pyarrow]')
      .pipe(lambda df_: pd.Series(np.random.randint(df_.iloc[:,0]
                                          , df_.iloc[:,1])
            , index=df_.index))
)

age100k = (age
            .sample(100_000, replace=True, random_state=42)
            .reset_index(drop=True)
            )
age100k
age=age100k

# Optimizing .apply with Cython

%load_ext Cython


%%cython
import random
def between_cy(row):
    return random.randint(*row.values)

%%cython
import random
def between_cy3(x: np.int64, y: np.int64) -> np.int64:
    return random.randint(x,y)

%%timeit
(age100k
 .str.split('-', expand=True)
 .astype('int8[pyarrow]')
 .apply(lambda row: between_cy3(row[0], row[1]), axis=1)
)

%prun -l 10 (age100k.str.split('-', expand=True).astype('int8[pyarrow]') \
             .apply(lambda row: between_cy3(row[0], row[1]), axis=1))

%%cython
import numpy as np
import random
def between_cy4(x: np.ndarray[int],
                y: np.ndarray[int]) -> np.ndarray[int]:
    res: np.ndarray[int] = np.empty(len(x), dtype='int32')
    i: int
    for i in range(len(x)):
        res[i] = random.randint(x[i], y[i])
    return res

%%timeit
(age100k.
 str.split('-', expand=True)
 .astype('int8[pyarrow]')
 .pipe(lambda df_: between_cy4(
                            df_.iloc[:,0].to_numpy('int32'),
                            df_.iloc[:,1].to_numpy('int32')))
)


np.random.randint

%%cython
import random
import numpy as np

def between_cy5(x: np.ndarray[int],
                y: np.ndarray[int]) -> np.ndarray[int]:
    return np.random.randint(x, y)

%%timeit
(age100k.
 str.split('-', expand=True)
 .astype('int8[pyarrow]')
 .pipe(lambda df_: between_cy5(
                            df_.iloc[:,0].to_numpy('int32'),
                            df_.iloc[:,1].to_numpy('int32')))
)

# Optimizing .apply with Numba


import numba as nb
import numpy
@nb.jit(nb.int32[:](nb.int32[:], nb.int32[:]))
def between_nb(arr1, arr2):
    return numpy.random.randint(arr1, arr2)


(age100k.
 str.split('-', expand=True)
 .astype('int8[pyarrow]')
 .pipe(lambda df_: between_nb(
                            df_.iloc[:,0].to_numpy('int32'),
                            df_.iloc[:,1].to_numpy('int32')))
)

# Replacing Text

make.str.replace('A', 'Å')
make.replace('A', 'Å')
make[make=='A']

make.replace('A', 'Å', regex=True)

# Exercises
# With a dataset of your choice:

# 1. Using a string column, lowercase the values.
# 2. Using a string column, slice out the first character.
# 3. Using a string column, slice out the last three characters.
# 4. Create a series extracting the numeric values using a string column.
# 5. Using a string column, create a series extracting the non-ASCII values.
# 6. Using a string column, create a dataframe with the dummy columns for every character in the column.

# 1
make.str.lower()
# 2
make.str.slice(1)
# 3
make.str.slice(0,-3)
# 4
ex4 = pd.Series(['Alf4', 'Dodg33', 'Aud1', 'M3rcedes'])
(ex4.str.extractall(r'(?P<numbers>[0-9]+)')
        .loc[:,'numbers']
        .reset_index(drop=True)
        .astype('int8[pyarrow]')
)

# 5
s5 = pd.Series(['Bańka', 'Alfa-Romeo', 'Kładka'])
(s5.str.extractall(r'(?P<Nonascii>[^\x00-\x7F])')
        .loc[:,'Nonascii']
        .reset_index(drop=True)
)

# 6
ex4.str.get_dummies(sep = '')
