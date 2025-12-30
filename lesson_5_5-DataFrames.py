# MELTING TRANSPOSING AND STACKING DATA
import pandas as pd
import io

# Melting Data

data = '''name,age,test1,test2,teacher
Adam,15,95.0,80,Ashby
Bob,16,81.0,82,Ashby
Dave,16,89.0,84,Jones
Fred,15,,88,Jones'''

scores = pd.read_csv(io.StringIO(data), dtype_backend='pyarrow')

scores.iloc[:,2:4].mean()

scores.melt(id_vars=['name', 'age'], value_vars=['test1','test2'])

pd.concat([scores.test1, scores.test2]).mean()

(scores
    .melt(id_vars=['name', 'age'], value_vars=['test1', 'test2'])
    .value.mean()
)

melted = scores.melt(id_vars=['name', 'age','teacher'], value_vars=['test1', 'test2'],
            var_name='test', value_name='score')

# Un-melting Data

melted.pivot_table(
    index=['name','age','teacher'],
    columns=['test'],
    values='score'
).reset_index()

(melted
    .groupby(['name','age','teacher','test'])
    .score
    .mean()
    .unstack()
    .reset_index()
)


# Pulling Out Categorical Values into Columns
#tbc