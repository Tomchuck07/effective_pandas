import pandas as pd
# CATEGORICAL MANIPULATION

# Categorical Data

url = 'https://github.com/mattharrison/datasets/raw/master/' \
        'data/vehicles.csv.zip'
df = pd.read_csv(url, engine='pyarrow', dtype_backend='pyarrow')
make = df.make
make

# Frequency counts
make.value_counts()
make.shape, make.nunique()

# Benefits of Categories
cat_make = make.astype('category')
make.memory_usage(deep=True)
cat_make.memory_usage(deep=True)

%%timeit
cat_make.str.upper()
%%timeit
make.str.upper()

old_make = make.astype(str) #bez/z
%%timeit
old_make.str.upper()

# Conversion to Ordinal Categories


make_type = pd.CategoricalDtype(
                categories=sorted(make.unique()), ordered=True)

ordered_make = make.astype(make_type)
ordered_make

(make
    .astype('category')
    .cat.as_ordered()
)

ordered_make.max()
cat_make.max()

ordered_make.sort_values()

# The .cat Accessor

cat_make.cat.rename_categories(
            [c.lower() for c in cat_make.cat.categories]
)

ordered_make.cat.rename_categories(
            {c:c.lower() for c in ordered_make.cat.categories}
)

ordered_make.cat.reorder_categories(
            sorted(ordered_make.cat.categories, key=str.lower)
)

# Category Gotchas
ordered_make.head(100).value_counts()

(cat_make
    .head(100)
    .groupby(cat_make.head(100), observed=False)
    .first()
)

(make
    .head(100)
    .groupby(make.head(100))
    .first()
)

(cat_make
    .head(100)
    .groupby(cat_make.head(100), observed=True)
    .first()
)

ordered_make.iloc[0]
ordered_make.iloc[[0]]

# Generalization

def generalizetopn(ser, n=5, other='Other'):
    topn = ser.value_counts().index[:n]
    if isinstance(ser.dtype, pd.CategoricalDtype):
        ser = ser.cat.set_categories(
            topn.set_categories(list(topn)+[other]))
    return ser.where(ser.isin(topn), other)

cat_make.pipe(generalizetopn, 20, 'Rare')

def generalize_mapping(ser, mapping, default):
    seen = None
    res = ser.astype('str')
    for old, new in mapping.items():
        mask = ser.str.contains(old)
        if seen is None:
            seen = mask
        else:
            seen |= mask
        res = res.where(~mask, new)
    res = res.where(seen, default)
    return res.astype('category')

cat_make.pipe(generalize_mapping, {'Tesla':'US', 'Dodge':'US', 'Ford':'US', 'Chevrolet':'US',  'Oldsmobile': 'US', 'Plymouth': 'US', 'BMW': 'German'}, 'Other')

# With a dataset of your choice:

# 1. Convert a text column into a categorical column. How much memory did you save?
# 2. Convert a numeric column into a categorical column by binning it (pd.cut). How much memory did you save?
# 3. Use the generalize_topn function to limit the amounts of categories in your column. How much memory did you save?

# 1
langs = pd.Series([
    "angielski", "hiszpański", "niemiecki", "francuski", "włoski",
    "hiszpański", "angielski", "niemiecki", "francuski", "angielski",
    "niemiecki", "hiszpański", "angielski", "francuski", "włoski",
    "angielski", "niemiecki", "hiszpański", "włoski", "francuski",
    "angielski", "hiszpański", "niemiecki", "francuski", "angielski",
    "włoski", "niemiecki", "hiszpański", "angielski", "francuski",
    "hiszpański", "angielski", "niemiecki", "włoski", "francuski",
    "angielski", "hiszpański", "niemiecki", "francuski", "włoski",
    "angielski", "niemiecki", "hiszpański", "francuski", "włoski",
    "angielski", "niemiecki", "hiszpański", "francuski", "włoski"
])

langs.value_counts()

langs.memory_usage(deep=True)
langs.astype('category').memory_usage(deep=True)

# 2
numbers = pd.Series([
    83, 27, 59, 4, 96, 34, 71, 88, 20, 12,
    45, 78, 53, 2, 65, 99, 38, 57, 80, 25,
    14, 92, 41, 73, 60, 16, 86, 48, 33, 6,
    97, 29, 52, 70, 22, 64, 18, 84, 10, 31,
    95, 40, 26, 7, 90, 35, 55, 3, 67, 81
], dtype='int8[pyarrow]')

numbers.memory_usage(deep=True)
pd.cut(numbers, 5).memory_usage(deep=True)

# 3
langs.astype('category').memory_usage(deep=True)
langs.astype('category').pipe(generalizetopn, 2, 'Rest').memory_usage(deep=True)