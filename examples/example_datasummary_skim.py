# %%
import polars as pl

import datasummary as ds

# %%
df = pl.read_csv("https://vincentarelbundock.github.io/Rdatasets/csv/datasets/mtcars.csv")

# %%
stats = ds.datasummary_skim(df)

# %%
print(stats)

# %%
stats

# %%
stats = ds.datasummary_skim(
    df, output="markdown", title="mtcars Summary Statistics", align="l"
)

# %%
