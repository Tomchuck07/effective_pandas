# COLUMNS TYPES, .ASSIGN() AND MEMORY USAGE
# EXERCISES
# With a tabular dataset of your choice:
# 1. Find a numeric column and change its type. Did you save memory? Did you lose precision?
# 2. Find a string column and convert it to a category. What happened to memory usage? Time a few string operations. Are they faster on the categorical column or string column?

import pandas as pd
import numpy as np

s1 = pd.Series(np.random.randint(1,255,100000))
def even(x):
    if x%2==0:
        return 'even'
    else:
        return 'not-even'

s2 = pd.Series(s1.apply(even))
df = pd.DataFrame({'col1':s1, 'col2':s2})

# 1. 
df1 = df.assign(col1=df['col1'].astype('uint8'))
df.memory_usage(deep=True)
df1.memory_usage(deep=True)

#2
df2 = df1.assign(col2=df['col2'].astype('category'))
df.memory_usage(deep=True)
df2.memory_usage(deep=True)

%%timeit
df.col2.str.upper()

%%timeit
df2.col2.str.upper()
