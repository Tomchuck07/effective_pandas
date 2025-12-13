# SORTING COLUMNS AND INDEXES
import pandas as pd

# Sorting Columns
def tweak_siena_pres(df):
    def int64_to_uint8(df):
        cols = df.select_dtypes('int64')
        return df.astype({col: 'uint8[pyarrow]' for col in cols})        
    
    return(
        df
            .rename(columns={'Seq.':'Seq'})
            .rename(columns = {k:v.replace(' ','_')
                               for k,v in {'Bg': 'Background',
              'PL': 'Party leadership', 'CAb': 'Communication ability',
              'RC': 'Relations with Congress', 'CAp': 'Court appointments',
              'HE': 'Handling of economy', 'L': 'Luck',
              'AC': 'Ability to compromise', 'WR': 'Willing to take risks',
              'EAp': 'Executive appointments', 'OA': 'Overall ability',
              'Im': 'Imagination', 'DA': 'Domestic accomplishments',
              'Int': 'Integrity', 'EAb': 'Executive ability',
              'FPA': 'Foreign policy accomplishments',
              'LA': 'Leadership ability',
              'IQ': 'Intelligence', 'AM': 'Avoid crucial mistakes',
              'EV': "Experts' view", 'O': 'Overall'}.items()})
            .pipe(int64_to_uint8)
            .assign(
                Average_rank = lambda df_: df_.select_dtypes('number')
                                                .sum(axis=1).rank(method='dense').astype('uint8[pyarrow]'),
                Quartile = lambda df_: pd.qcut(df_.Average_rank, 4,
                                            labels = '1th 2th 3th 4th'.split())
            )
    )

url = 'https://github.com/mattharrison/datasets/raw/master/data/'\
     'siena2018-pres.csv'

df = pd.read_csv(url, dtype_backend='pyarrow', index_col=0)

pres = tweak_siena_pres(df)

pres.sort_values('Party')
pres.sort_values(by=['Party','Average_rank'], ascending = [True,False])

print(pres
      .President
      .str.split()
      .apply(lambda val: val[-1]))

print(pres
      .President
      .astype(str)
      .str.split(' ')
      .str[-1])


print(pres
      .sort_values(by='President',
        key=lambda name_ser: name_ser
          .astype(str)
          .str.split()
          .str[-1])
)

# Sorting Columns Order

pres.sort_index(axis='columns')

# Setting And Sorting The Index

print(pres
      .set_index('President')
      .sort_index()
)

print(pres
      .set_index('Party')
      .sort_index()
      .loc['Democratic':'Republican']
)

# Exercises
# With a dataset of your choice:


data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace', 'Hannah'],
    'Department': ['HR', 'IT', 'IT', 'HR', 'Sales', 'Sales', 'IT', 'HR'],
    'Salary': [5000, 8000, 7500, 5200, 9000, 9200, 7800, 5100],
    'Age': [25, 30, 28, 45, 35, 40, 29, 24]
}
emp = pd.DataFrame(data, index=[10, 5, 2, 8, 1, 7, 3, 6])

# 1. Sort the index.
emp.sort_index()
# 2. Set the index to a string column, sort the index, and slice by a substring of index values.
(emp
    .set_index('Department')
    .sort_index()
    .loc['HR':'IT']
)
# 3. Sort by a single column.
emp.sort_values(by='Age')
# 4. Sort by a single column in descending order.
emp.sort_values(by='Salary',ascending=False)
# 5. Sort by two columns.
emp.sort_values(by=['Department','Name'])
# 6. Sort by the last letter of a string column.
emp.sort_values(by='Name',key=lambda name: name.str[-1])