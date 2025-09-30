import pandas as pd  

# Dates in The Index
 url = 'https://github.com/mattharrison/datasets'+\
        '/raw/master/data/alta-noaa-1980-2019.csv'
alta_df = pd.read_csv(url, engine='pyarrow', dtype_backend='pyarrow')
dates = pd.to_datetime(alta_df.DATE)

snow =  (alta_df 
    .SNOW
    .rename(dates)
)

snow[snow.isna()]

snow.loc['1985-09':'1985-09-20']

# Filling In Missing Data

(snow
    .loc['1985-09':'1985-09-20']
    .fillna(0)
)

snow.loc['1987-12-30':'1988-01-10']

(snow
    .loc['1987-12-30':'1988-01-10']
    .ffill()
)
(snow
    .loc['1987-12-30':'1988-01-10']
    .bfill()
)

# Interpolation

(snow
    .loc['1987-12-30':'1988-01-10']
    .interpolate()
)

winter = (snow.index.quarter == 1) | (snow.index.quarter == 4)

(snow.
         case_when([(winter & snow.isna(), snow.interpolate()),
            (~winter & snow.isna(), 0)])
).loc[['1985-09-19','1988-01-01']]

(snow
    .where(~(winter & snow.isna()), snow.interpolate())
    .where(~(~winter & snow.isna()), 0)
).loc[['1985-09-19','1988-01-01']]

# Dropping Missing Values

(snow
    .loc['1987-12-30':'1988-01-10']
    .dropna()
)

# Shifting Data
snow
snow.shift(1)
snow.shift(-1)
# Rolling Average
(snow
    .add(snow.shift(1))
    .add(snow.shift(2))
    .add(snow.shift(3))
    .add(snow.shift(4))
    .div(5)
)

snow.rolling(5).mean()

# Resampling

snow = snow.astype('float64') # line not present in book but without it i got some weird results for some  days

(snow
    .resample('2ME')
    .max()
)
(snow
    .resample('YE-MAY')
    .max()
)


(snow
   .div(snow
          .resample('QE')
          .transform('sum'))
   .mul(100)
   .fillna(0)
)

season2017 = snow.loc['2016-10':'2017-05']

(season2017.resample('ME').sum()
                .div(
                 season2017.sum()
                )
                .mul(100)
)


# Groupby Operations


def season(idx):
    year = idx.year
    month = idx.month
    if month < 10:
       return year
    else:
       return year+1
    return year.where((month<10), year+1)
    
(snow
    .groupby(season)
    .sum()
)


#sprawzdamy udzial procentowy miesiecznych opadow do opadow w sezonie


def calc_pct(s):
    return s.div(s.sum()).mul(100)

(snow
    .resample('ME')
    .sum()
    .groupby(season)
    .apply(calc_pct)
)
(snow
    .resample('ME')
    .sum()
    .resample('YE-SEP')
    .apply(calc_pct)
)

# Cumulative operations

(snow
    .loc['2016-10':'2017-09']
    .cumsum()
)
(snow
    .resample('YE-SEP')
    .transform('cumsum')
)

# EXERCISES

# With a dataset of your choice:

# 1. Convert a column with date information to a date.
# 2. Put the date information into the index for a numeric column.
# 3. Calculate the average value of the column for each month.
# 4. Calculate the average value of the column for every two months.
# 5. Calculate the percentage of the column out of the total for each month.
# 6. Calculate the average value of the column for a rolling window of size 7.
# 7. Using .loc pull out the first three months of a year.
# 8. Using .loc pull out the last four months of a year.

data = [
    '2020-01-01','2020-02-07','2020-03-16','2020-04-23','2020-05-31','2020-07-07','2020-08-14','2020-09-21','2020-10-29','2020-12-05',
    '2021-01-12','2021-02-19','2021-03-29','2021-05-05','2021-06-12','2021-07-01','2021-08-27','2021-08-31','2021-11-10','2021-12-18',
    '2022-01-25','2022-03-03','2022-04-10','2022-05-16','2022-06-25','2022-08-01','2022-09-08','2022-11-03','2022-11-23','2022-12-31'
]

# 1
dates = pd.to_datetime(data)
dates

# 2
numbers = pd.Series([
 '12.5', '0.3', '27.8', '5.6', None, '22.1', '1.7', '29.4', '14.2', '8.8',
 '25.0', '3.3', '19.7', '7.1', '11.6', None, '2.2', '16.5', '28.0', '9.9',
 '6.4', '21.2', '13.7', '4.8', '24.6', '0.9', '17.3', None, '15.0', '10.1'
], dtype='double[pyarrow]')
numbers.index = dates
numbers

# 3
numbers = numbers.interpolate()
(numbers
    .resample('ME')
    .mean()
)

# 4
(numbers
    .resample('2ME')
    .mean()
)

# 5
(numbers.
    resample('ME')
    .sum()
    .div(numbers.sum())
    .mul(100)
)

# 6
(numbers
    .rolling(7)
    .mean()
)

# 7
numbers.loc[numbers.index.month <= 3]

# 8
numbers.loc[numbers.index.month >=9]