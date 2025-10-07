import pandas as pd

# Plotting with a Series

# The .plot Attribute
url = 'https://github.com/mattharrison/datasets/raw/master/'\
        'data/alta-noaa-1980-2019.csv'

alta_df = pd.read_csv(url, dtype_backend='pyarrow')
dates = pd.to_datetime(alta_df.DATE)
snow = (
    alta_df.SNOW
    .rename(dates)
)
snow

# Histograms
snow.plot.hist()
snow[snow>0].plot.hist(bins=20, title='Snowfall histogram (in)')

# Box Plot
snow.plot.box()

(snow
    [lambda s:(s.index.month == 1) & (s > 0)]
    .plot.box()
)

# Kernel Density Estimation Plot

(snow
    [lambda s:(s.index.month == 1) & (s > 0)]
    .plot.kde()    
)

# Line Plot
snow.plot.line()
(snow
    .tail(300)
    .plot.line()
)
(snow
    .resample('M')
    .mean()
    .plot.line()
)

# Line Plots with Multiple Aggregations

(snow
    .resample('QE')
    .quantile([.5, .9, .99])
    .unstack()
    .tail(100)
    .plot.line()
)

# Bar Plots

season2017 = snow.loc['2016-10':'2017-05']

(season2017
    .resample('M')
    .sum()
    .div(season2017.sum())
    .mul(100)
    .rename(lambda idx: idx.month_name())
    .plot.bar(title='2017 Monthly percent of snawfall')
)
(season2017
    .resample('M')
    .sum()
    .div(season2017.sum())
    .mul(100)
    .rename(lambda idx: idx.month_name())
    .plot.barh(title='2017 Monthly percent of snawfall')
)

url2 = 'https://github.com/mattharrison/datasets/raw/master/data/'\
        'vehicles.csv.zip'
df = pd.read_csv(url2, dtype_backend='pyarrow', engine='pyarrow')
make = df.make
make.value_counts().plot.bar()

top10 = make.value_counts().head(10).index
(make
    .where(make.isin(top10), 'other')
    .value_counts()
    .plot.barh()
)

# Styling
import matplotlib.pyplot as plt
import seaborn as sns
with sns.plotting_context(rc=dict(font='Roboto', palette='pastel')):    
    fig, ax = plt.subplots(dpi=600, figsize=(10,4))
    snow.plot.hist()  
    sns.despine()
    fig.savefig('snowhist.png', dpi=600, bbox_inches='tight')


# Exercises
# With a dataset of your choice:

# 1. Create a histogram from a numeric column. Change the bin size.
# 2. Create a boxplot from a numeric column.
# 3. Create a Kernel Density Estimate plot from a numeric column.
# 4. Create a line from a numeric column.
# 5. Create a bar plot from the frequency count of a categorical column.

grades = pd.Series([3, 5, 2, 6, 1, 4, 5, 3, 6, 2, 
 4, 1, 5, 6, 2, 3, 4, 6, 1, 5, 
 2, 3, 4, 6, 5, 1, 2, 3, 6, 4])

# 1
grades.plot.hist(bins=3)
# 2
grades.plot.box()
# 3
grades.plot.kde()
# 4
grades.plot.line()
# 5
(grades
    .astype('category')
    .value_counts()
    .plot.barh()
)