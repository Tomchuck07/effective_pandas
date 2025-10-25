# Math Metods in Dataframes
import pandas as pd

url = 'https://github.com/mattharrison/datasets/raw/master/data/'\
'siena2018-pres.csv' 
df = pd.read_csv(url, index_col=0, dtype_backend='pyarrow')

def tweak_siena_pres(df):
    def int64_to_uint8(df_):
        cols = df_.select_dtypes('int64')
        return (df_
                .astype({col: 'uint8[pyarrow]' for col in cols}))
    
    return (df
        .rename(columns={'Seq.':'Seq'})         #1
        .rename(columns={k:v.replace(' ', '_') for k,v in
              {'Bg': 'Background',
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
        .astype({'Party':'category'})    #2
        .pipe(int64_to_uint8)            #3
        .assign(Average_rank=lambda df_:(df_.select_dtypes('uint8')  #4
            .sum(axis=1).rank(method='dense').astype('uint8[pyarrow]')),
                Quartile=lambda df_:pd.qcut(df_.Average_rank, 4,
                    labels='1st 2nd 3rd 4th'.split())
                )   
    )

pres = tweak_siena_pres(df)

# Index Aligment

scores = pres.loc[:,'Background':'Average_rank']

s1 = scores.iloc[:3, :4]
s2 = scores.iloc[1:6, :5]
s1+s2

s3=pd.concat([scores.iloc[1:6,:5],scores.iloc[1:6,:5]+1])
print(pd.concat([s1]*2)+s3)
s3.index.duplicated().any()

# More Math

n1=(scores.Imagination.sub(scores.Imagination.min())).div(scores.Imagination.max()
                                                    -(scores.Imagination.min()))

imag = scores.Imagination

n2=(imag-imag.min())/(imag.max()-imag.min())

n1.describe()
n2.describe()

pres.dtypes

nums = pres.select_dtypes('number')

(nums.sub(nums.min()).div(nums.max().sub(nums.min()))).describe()
((nums-nums.min())/(nums.max()-nums.min())).describe()

from sklearn.base import BaseEstimator, TransformerMixin

class NormalizerTransformer(BaseEstimator, TransformerMixin):

    def __init__(self):
        self.min=None
        self.max=None
    
    def fit(self, x, y=None):
        self.min = x.min()
        self.max = x.max()
        return self
    
    def transform(self, x):
        return ((x-self.min)/(self.max-self.min))


nt = NormalizerTransformer()

print(nt.fit_transform(scores))

std = nums.std(ddof=0)

print(nums.sub(nums.mean()).div(std))
nums.sub(nums.mean()).div(std).describe()

class StandarizerTransfomer(BaseEstimator ,TransformerMixin):

    def __init__(self):
        self.mean = None
        self.std = None
    def fit(self, x, y=None):
        self.mean = x.mean()
        self.std = x.std(ddof=0)
        return self
    
    def transform(self,x):
        return (x-self.mean)/self.std

st = StandarizerTransfomer()
st.fit_transform(nums).equals(nums.sub(nums.mean()).div(std))

from sklearn.preprocessing import StandardScaler

ss = StandardScaler()

ss.set_output(transform='pandas')

nums.sub(nums.mean()).div(std)[:2]
st.fit_transform(nums)[:2]
ss.fit_transform(nums)[:2]

# PCA Calculations in Pandas

centered = nums - nums.mean() #1
cov = centered.cov() #2

import numpy as np

vals, vects = np.linalg.eig(cov) #3

vals/vals.sum()
vects[:2].round(2)

idxs = pd.Series(vals).argsort()

def set_columns(df_):
    df_.columns = [f'PC{i+1}' for i in range(len(df_.columns))]
    return df_

comps = (pd.DataFrame(vects, index=nums.columns) #4
         .iloc[:,idxs[::-1]]
         .pipe(set_columns)
)

pcas = centered.dot(comps)



import numpy as np

centered = nums - nums.mean() #1

vals, vecs = np.linalg.eig(centered.cov()) #2,3

variance_explained = pd.Series(sorted(vals, reverse=True),
                               index=[f'PC{i+1}' for i in range(len(nums.columns))])

idxs = pd.Series(vals).argsort()

def set_columns(df_):
    df_.columns = [f'PC{i+1}' for i in range(len(nums.columns))]
    return df_

pc_loadings = (pd.DataFrame(vecs, index=(nums.columns)).iloc[:, idxs[::-1]]
                                .pipe(set_columns))    

pcas_2 = centered.dot(pc_loadings)

from sklearn.decomposition import PCA
from sklearn import set_config

set_config(transform_output='pandas')

pca = PCA()
print(pca.fit_transform(nums).round(2))
print(pca.components_[:2].round(3))
print(vecs.round(3)[:2])

pd.DataFrame(pca.components_, index = [f'pca{i}' for i in range(nums.shape[1])],
             columns=nums.columns)
comps

pca.explained_variance_ratio_.round(3)

# Exercises
# With a tabular dataset of your choice:

s1 = pd.Series([7, 4, 8, 5, 7, 3, 7, 2, 5, 4])
s2 = pd.Series([7, 7, 1, 5, 9, 8, 7, 5, 8, 6])

ex_df = pd.DataFrame({'k1':s1,'k2':s2})

# 1. Create a dataframe from the data and add it to itself.

e1 = ex_df.add(ex_df)

# 2. Create a dataframe from the data and multiply it by two.

e2 = ex_df.mul(2)

# 3. Are the results from the previous exercises equivalent?
e1.equals(e2)
#TAK