import sys
import numpy as np
import pandas as pd


#overflow loop
n1 = np.array([1], dtype='uint8')
n255 = np.array([255], dtype='uint8')
n255+=n1
n1+n255


#appending empty integer
demo=np.array([1,2,3], dtype='int8')
demo.dtype
demo_new=np.append(demo,[])
demo=demo_new

#integers
small_values = [2,5,4,45]
great_values = [2**31,2**63,2**100]
missing_values =[None,1,-45]

small_series = pd.Series(small_values, dtype='int8')
great_series = pd.Series(great_values)
great_series

small_series.astype('int8')
small_series

    #pyArrow

small_series_pa = pd.Series(small_values, dtype = 'int8[pyarrow]')
small_series_pa
great_series_pa= pd.Series(great_values, dtype = 'int64[pyarrow]')
great_series_pa

missing_series_numpy= pd.Series(missing_values)
missing_series_numpy

missing_series_pyarrow = pd.Series(missing_values, dtype = 'int8[pyarrow]')
missing_series_pyarrow

    #floats

float_values=[2.3,45.3, 5.8]
float_missing = [None, 23.2,-45.0]
float_rain = [1.5, 2.0, 'T', 4.2, 0.0]

float_series_numpy = pd.Series(float_missing)
float_series_numpy

float_series_pyarrow = pd.Series(float_missing, dtype='double[pyarrow]')
float_series_pyarrow

fSer_rain_numpy = pd.Series(float_rain)
fSer_rain_numpy.replace('T', '0.0').astype('float64')
fSer_rain_numpy

fSer_rain_pyarrow = pd.Series(float_rain, dtype = 'double[pyarrow]')
pd.Series(float_rain).replace('T', '0.0').astype('double[pyarrow]')
fSer_rain_pyarrow

pd.Series(float_rain).replace('T','0.0').astype('float').astype('double[pyarrow]')


%%timeit # type[ignore]
print('hi')



list_ex = [2.7,8.5,5.3,-25.3,0,8]
sys.getsizeof(list_ex)

Numpy_array
sys.getsizeof(Numpy_array)


%%timeit
Numpy_array = pd.Series(list_ex)
Numpy_array+=1

Numpy_array
pyarrow_array

%%timeit
pyarrow_array = pd.Series(list_ex, dtype='float64[pyarrow]')
pyarrow_array+=1

import pandas as pd
import pyarrow as pA

pa_string = pd.ArrowDtype(pA.string())

strings_list = ['elo', 'witomyy', 'dobrydobry']
strings_missing = ['elo', None, 'dobrydobry']

string_array = pd.Series(strings_list)
string_array_missing = pd.Series(strings_missing)

string_array_missing

pA_strings = pd.Series(strings_list, dtype='string[pyarrow]')
pA_strings_missing = pd.Series(strings_missing, dtype='string[pyarrow]')
pA_strings
pA_strings_missing

pA_strings_perfect = pd.Series(strings_list, dtype=pa_string)

pA_strings_perfect.dtype == pA_strings.dtype


#categories

months = ['january','february','march','april','may','june','july','august']
months_series = pd.Series(months, dtype = 'string')
pdmonths = pd.Series(months_series, dtype = 'category')
pdmonths


pdmonth_cat = pd.CategoricalDtype(categories=months, ordered=True)
pd.Series(months, dtype=pdmonth_cat).sort_values()


# %%
