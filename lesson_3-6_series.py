# Date and Time Manipulation

import pandas as pd

col = pd.Series(['2015-03-08 08:00:00+00:00',
     '2015-03-08 08:30:00+00:00',
     '2015-03-08 09:00:00+00:00',
     '2015-03-08 09:30:00+00:00',
     '2015-11-01 06:30:00+00:00',
     '2015-11-01 07:00:00+00:00',
     '2015-11-01 07:30:00+00:00',
     '2015-11-01 08:00:00+00:00',
     '2015-11-01 08:30:00+00:00',
     '2015-11-01 08:00:00+00:00',
     '2015-11-01 08:30:00+00:00',
     '2015-11-01 09:00:00+00:00',
     '2015-11-01 09:30:00+00:00',
     '2015-11-01 10:00:00+00:00'])

utc_s = pd.to_datetime(col, utc=True)
utc_s
utc_s.dt.tz_convert('America/Denver')

s = pd.Series(['2015-03-08 01:00:00-07:00',
  '2015-03-08 01:30:00-07:00',
  '2015-03-08 03:00:00-06:00',
  '2015-03-08 03:30:00-06:00',
  '2015-11-01 00:30:00-06:00',
  '2015-11-01 01:00:00-06:00',
  '2015-11-01 01:30:00-06:00',
  '2015-11-01 01:00:00-07:00',
  '2015-11-01 01:30:00-07:00',
  '2015-11-01 01:00:00-07:00',
  '2015-11-01 01:30:00-07:00',
  '2015-11-01 02:00:00-07:00',
  '2015-11-01 02:30:00-07:00',
  '2015-11-01 03:00:00-07:00'])


pd.to_datetime(s, utc=True).dt.tz_convert('America/Denver')

# Loading Local Time Data

time = pd.Series(['2015-03-08 01:00:00',
  '2015-03-08 01:30:00',
  '2015-03-08 02:00:00',
  '2015-03-08 02:30:00',
  '2015-03-08 03:00:00',
  '2015-03-08 02:00:00',
  '2015-03-08 02:30:00',
  '2015-03-08 03:00:00',
  '2015-03-08 03:30:00',
  '2015-11-01 00:30:00',
  '2015-11-01 01:00:00',
  '2015-11-01 01:30:00',
  '2015-11-01 02:00:00',
  '2015-11-01 02:30:00',
  '2015-11-01 01:00:00',
  '2015-11-01 01:30:00',
  '2015-11-01 02:00:00',
  '2015-11-01 02:30:00',
  '2015-11-01 03:00:00'])

offset = pd.Series([-7, -7, -7, -7, -7, -6, -6,
   -6, -6, -6, -6, -6, -6, -6, -7, -7, -7, -7, -7])

local = (pd.to_datetime(time)
     .groupby(offset)
     .transform(lambda s: s.dt.tz_localize(s.name)
                              .dt.tz_convert('America/Denver'))
)

offset = offset.replace({-7:'-07:00', -6:'-06:00'})

local

# Converting Local time to UTC
local.dt.tz_convert('UTC')

# Converting to Epochs

nano_sec = local.astype('int64[pyarrow]')
nano_sec

pd.to_datetime(nano_sec, unit='ns').dt.tz_localize('UTC')

(nano_sec
     .truediv(1_000_000)
     .pipe(pd.to_datetime, unit='ns')
     .dt.tz_localize('UTC')
)
(nano_sec
     .truediv(1_000_000)
     .pipe(pd.to_datetime, unit='ms')
     .dt.tz_localize('UTC')
)

# Manipulating Dates

url = 'https://github.com/mattharrison/datasets'+\
          '/raw/master/data/alta-noaa-1980-2019.csv'

alta_df = pd.read_csv(url)
alta_df

dates = (pd.to_datetime(alta_df.DATE))
         .astype('timestamp[ns][pyarrow]'))
dates

dates.dt.day_name('es_ES')

dates.dt.is_month_end
dates.dt.strftime('%d.%m.%Y')

# Date Math
