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

classes = ['cs106', 'cs150', 'hist205', 'hist206', 'hist207']
start_dates = (pd.Series(['2015-03-08',
 '2015-03-08',
 '2015-03-09',
 '2015-03-09',
 '2015-03-11'], dtype='datetime64[ns]', index=classes)
               .astype('timestamp[ns][pyarrow]')
)

end_dates = (pd.Series(['2015-05-28 23:59:59',
'2015-06-01 3:00:00',
'2015-06-03',
'2015-06-02 14:20',
'2015-06-01'], dtype='datetime64[ns]', index=classes)
               .astype('timestamp[ns][pyarrow]')
)
end_dates

duration = (end_dates - start_dates)
duration

duration.astype('timedelta64[ns]')

(duration
     .astype('timedelta64[ns]')
     .dt.total_seconds()
)
(duration
     .astype('timedelta64[ns]')
     .dt.seconds
)
(duration
     .astype('timedelta64[ns]')
     .dt.days
)

# Exercises
# With a dataset of your choice:
# 1. Convert a column with date information to a date.
# 2. Convert a date column into UTC dates.
# 3. Convert a date column into local dates with a time zone.
# 4. Convert a date column into epoch values.
# 5. Convert an epoch number into UTC.

s0 = pd.Series(['01.05.2025', '30.03.2024', '11.11.2020'])
# 1
s1 = pd.to_datetime(s0, format='%d.%m.%Y')
s1

# 2
s2 = pd.to_datetime(s0, format='%d.%m.%Y', utc=True)
s2
# 3
s2.dt.tz_convert('Europe/Warsaw')

# 4
s4 = s1.astype('int64[pyarrow]')
s4
# 5
pd.to_datetime(s4,  unit='ns').dt.tz_localize('UTC')
