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


