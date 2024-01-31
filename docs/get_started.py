# %% [markdown]
# ---
# title: Get started with `statsframe`
# ---

# %% [markdown]
"""
`statsframe` creates tables that provide descriptive statistics of numeric and
categorical data.

The goal is to provide a simple -- yet customizable -- way to summarize
data and models in Python.

`statsframe` is heavily inspired by [`modelsummary`](https://modelsummary.com/)
in R. The goal is not to replicate all that `modelsummary` does, but to provide
a way of achieving similar results in Python.

In order to achieve this, `statsframe` builds on the [`polars`](https://docs.pola.rs/)
library to produce tables that can be easily customized and exported to other formats.

## Basic Usage

As an example of `statsframe` usage, the `skim` function provides a
summary of a DataFrame (either `polars.DataFrame` or `pandas.DataFrame`).
The default summary statistics returned by `statsframe.skim_frame()` are unique values,
percentage missing, mean, standard deviation, minimum, median, and maximum.

Where possible, `statsframe` will print a table to the console and return a
polars DataFrame with the summary statistics. This allows for easy customization.
For example, the `polars.DataFrame` with statistics from `statsframe` can be
modified using the
[`Great Tables`](https://posit-dev.github.io/great-tables/reference/) package.

"""

# %%
# | label: mtcars-skim

import polars as pl
import statsframe as sf
from great_tables import GT

file_path = "https://vincentarelbundock.github.io/Rdatasets/csv/datasets/"
df = pl.read_csv(f"{file_path}/mtcars.csv").drop("rownames")

stats = sf.skim_frame(df)

# %%
(df.pipe(sf.skim_frame, output="simple"))
# %%
(df.pipe(sf.skim_frame, output="simple").pipe(GT))

# %% [markdown]
"""
We can achieve the same result above with a pandas DataFrame.
"""

# %%
# | label: trees-skim
import pandas as pd
import statsframe as sf

trees_df = pd.read_csv(f"{file_path}/trees.csv").drop(columns=["rownames"])

trees_stats = sf.skim_frame(trees_df)


# %%
corr = sf.correlation_frame(df, method="pearson")


# %%
(
    GT(corr)
    .data_color(
        domain=[-1, 1],
        palette=[
            "#636363",
            "#bdbdbd",
            "#f0f0f0",
            "#ffffff",
            "#f0f0f0",
            "#bdbdbd",
            "#636363",
        ],
        na_color="#ffffff",
    )
    .fmt_number(columns=df.columns, decimals=2)
)

# %%
