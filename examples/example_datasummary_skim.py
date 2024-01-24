# %%
import pandas as pd
import polars as pl

import datasummary as ds

# %% [markdown]
# Import a csv file to a polars DataFrame:

# %%
cars_df = pl.read_csv(
    "https://vincentarelbundock.github.io/Rdatasets/csv/datasets/mtcars.csv"
)


# %%
cars_stats = ds.datasummary_skim(cars_df)

# %%
print(cars_stats)

# %%
cars_stats

# %%
ds.datasummary_skim(
    cars_df, output="markdown", title="mtcars Summary Statistics", align="l"
)

# %%
ds.datasummary_skim(
    cars_df,
    stats="moments",
    output="markdown",
    title="mtcars Summary Statistics",
    align="r",
)

# %%
ds.datasummary_skim(
    cars_df, stats="full", output="markdown", title="mtcars Summary Statistics", align="r"
)

# %% [markdown]
# Works with pandas DataFrames too:

# %%
trees_df = pd.read_csv(
    "https://vincentarelbundock.github.io/Rdatasets/csv/datasets/trees.csv"
)

# %%
trees_stats = ds.datasummary_skim(trees_df)
