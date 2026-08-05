# CROSS-TABULATION DEEP DIVE

import pandas as pd
from common import tweak_jb

url = 'https://github.com/mattharrison/datasets/raw/master/data/'\
       '2020-jetbrains-python-survey.csv'

jb = pd.read_csv(url, dtype_backend='pyarrow', engine='pyarrow')
jb2 = tweak_jb(jb)

# Cross-Tabulation Summaries

pd.crosstab(index=jb2.country_live, columns=jb2.age)

# Adding Margins

pd.crosstab(index=jb2.country_live, columns=jb2.age, margins=True)

# Normalizing Results

pd.crosstab(index=jb2.country_live, columns=jb2.age, normalize=True)
pd.crosstab(index=jb2.country_live, columns=jb2.age, normalize='columns')
pd.crosstab(index=jb2.country_live, columns=jb2.age, normalize='index')

# Hierarchical Columns with Cross Tabulations

(pd.crosstab(index=[jb2.country_live, jb2.age], columns=[jb2.use_python_most, jb2.python3_ver])
 .loc[['United States'], ['Data analysis', 'Web development']]
 .style.background_gradient(cmap='viridis', axis=None)
)

# Exercises
# With a dataset of your choice:

data = []

data.extend([{'Department': 'IT', 'Food': 'Pizza'}] * 50)
data.extend([{'Department': 'IT', 'Food': 'Burger'}] * 10)
data.extend([{'Department': 'IT', 'Food': 'Salad'}] * 5)

data.extend([{'Department': 'HR', 'Food': 'Pizza'}] * 5)
data.extend([{'Department': 'HR', 'Food': 'Burger'}] * 5)
data.extend([{'Department': 'HR', 'Food': 'Salad'}] * 40)

data.extend([{'Department': 'Sales', 'Food': 'Pizza'}] * 10)
data.extend([{'Department': 'Sales', 'Food': 'Steak'}] * 40)
data.extend([{'Department': 'Sales', 'Food': 'Salad'}] * 5)

df = pd.DataFrame(data).astype('category')
df = df.sample(frac=1, random_state=42).reset_index(drop=True)


# 1. Summarize the count of one categorical column against another.

pd.crosstab(index=df.Department, columns=df.Food)

# 2. Summarize the count of one categorical column against another, adding margins.

pd.crosstab(index=df.Department, columns=df.Food, margins=True)

# 3. Summarize the count of one categorical column against another in a heatmap.

(pd.crosstab(index=df.Department, columns=df.Food)
    .style.background_gradient(cmap='viridis', axis=None)
)