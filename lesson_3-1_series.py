import pandas as pd
import numpy as np

series = {
    'year':[1978,1999,2008,2013],
    'champion':['milan','udienese', 'juventus', 'roma'],
    'name':'team'
}

def get(series, year):
    ins_inx = series['year'].index(year)
    return series['champion'][ins_inx]


get(series, 2013)

#why do we prefer to use pandas instead

profit = pd.Series([205,199,10,-30], name = 'money')
profit

rev = pd.Series([205,199,10,-30], name = 'money', dtype='int64[pyarrow]')
rev

rev.index

class Foo:
    pass

sW_objVls = pd.Series(
    ['John','Weronika',13,Foo()],
    index = ['man','women','day','function'],
    name = 'example')

sW_objVls




ex2=  pd.Series([23,21,np.nan,23,43,2.5,23])
ex2.size
print(ex2.count())

sW_objVls[2]