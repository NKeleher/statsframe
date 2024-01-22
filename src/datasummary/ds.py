from __future__ import annotations

# Main ds imports ----
import pandas as pd
import polars as pl
import polars.selectors as cs
from great_tables import GT  # md, html
from great_tables._tbl_data import DataFrameLike  # , SeriesLike, TblData

float_cols = ["Missing (%)", "Mean", "SD", "Min", "Median", "Max"]
moments_cols = ["Mean", "Variance", "Skewness", "Kurtosis"]
full_cols = ["Missing (%)", "Mean", "SD", "Min", "Median", "Max", "Skewness", "Kurtosis"]
stats_cols = ["Unique (#)"] + float_cols


def datasummary_skim(
    data: pl.DataFrame,
    type: str = "numeric",
    output: str = "default",
    float_precision: int = 2,
    histogram: bool = False,
    title: str = "Summary Statistics",
    notes: str = None,
    align: str = "r",
) -> pl.DataFrame:
    """
    Summary Statistics.

    Generates summary statistics for a given DataFrame.

    Args:
        data (DataFrameLike): The input DataFrame. Can be pandas or polars.
        type (str, optional): The type of summary statistics to generate.
            Defaults to "numeric".
        output (str, optional): The output format for the summary statistics.
            Defaults to "default".
        float_precision (int, optional): The number of decimal places to round
            float values when formatting in table output.
            Defaults to 2.
        histogram (bool, optional): Whether to include a histogram in the output.
            Defaults to False.
        title (str, optional): The title of the summary statistics table.
            Only relevant if output is "gt". Defaults to "Summary Statistics".
        notes (str, optional): Additional notes or comments.
            Only relevant if output is "gt".
            Defaults to None.
        align (str, optional): The alignment of the table columns.
            Defaults to "r".

    Returns:
        pl.DataFrame: The summary statistics table.

    Examples:
        # Generate summary statistics for a numeric DataFrame
        summary = datasummary_skim(data)

        # Generate summary statistics for a categorical DataFrame
        summary = datasummary_skim(data, type="categorical")

        # Generate summary statistics in markdown format
        summary = datasummary_skim(data, output="markdown")
    """

    # methods depend on the data being a polars DataFrame
    df = convert_df(data)

    if type == "numeric":
        stats_tab = _get_numeric_stats(df)
    elif type == "categorical":
        stats_tab = _get_categorical_stats(df)

    align_dict = {"r": "RIGHT", "l": "LEFT", "c": "CENTER"}
    tbl_align = align_dict[align]

    output_dict = {
        "default": None,
        "markdown": "ASCII_MARKDOWN",
        "simple": "NOTHING",
        "gt": None,
    }
    tbl_formatting = output_dict[output]

    if output == "default":
        tbl_formatting = None
    elif output == "markdown":
        tbl_formatting = "ASCII_MARKDOWN"
    elif output == "simple":
        tbl_formatting = "NOTHING"

    if output == "gt":
        gt_stats = GT(stats_tab).fmt_number(columns=float_cols, decimals=2)
        return gt_stats.tab_header(
            title="Summary statistics",
            subtitle=f"Rows: {data.height}, Columns: {data.width}",
        )

    else:
        with pl.Config(
            float_precision=float_precision,
            tbl_formatting=tbl_formatting,
            tbl_cell_alignment=tbl_align,
            tbl_hide_column_names=False,
            tbl_hide_column_data_types=True,
            tbl_hide_dataframe_shape=True,
        ):
            print(stats_tab)


def _get_numeric_stats(data: pl.DataFrame, stats_cols: stats_cols) -> pl.DataFrame:
    """
    Generates summary statistics for a numeric datatypes in a DataFrame.

    Args:
        data (pl.DataFrame): The input DataFrame.

    Returns:
        pl.DataFrame: The summary statistics table.
    """
    return (
        data.select(cs.numeric().n_unique())
        .cast(pl.Float64, strict=True)
        .extend(
            data.select(
                cs.numeric()
                .null_count()
                .truediv(data.height)
                .cast(pl.Float64, strict=True)
            )
        )
        .extend(data.select(cs.numeric().mean()))
        .extend(data.select(cs.numeric().std()))
        .extend(data.select(cs.numeric().min().cast(pl.Float64, strict=True)))
        .extend(data.select(cs.numeric().median()))
        .extend(data.select(cs.numeric().max().cast(pl.Float64, strict=True)))
        .transpose(include_header=True, header_name="", column_names=stats_cols)
        .with_columns(pl.col("Unique (#)").cast(pl.Int32, strict=True))
    )


def _get_categorical_stats(data: pl.DataFrame) -> pl.DataFrame:
    """
    Generates summary statistics for a numeric datatypes in a DataFrame.

    Args:
        data (pl.DataFrame): The input DataFrame.

    Returns:
        pl.DataFrame: The summary statistics table.
    """
    raise NotImplementedError("Not implemented")


def convert_df(data: DataFrameLike) -> pl.DataFrame:
    """
    Converts a DataFrame-like object to a polars DataFrame.

    Args:
        data (DataFrameLike): The input DataFrame-like (pandas or polars DataFrame`)
            object.

    Returns:
        pl.DataFrame: The converted polars DataFrame.

    Raises:
        ValueError: If the input data is not a polars or pandas DataFrame.
    """
    if isinstance(data, pl.DataFrame):
        return data
    elif isinstance(data, pd.DataFrame):
        return pl.from_pandas(data)
    else:
        raise ValueError("Input data must be a polars or pandas DataFrame")