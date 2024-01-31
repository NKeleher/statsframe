import polars as pl
import statsframe as sf
from polars.testing import assert_frame_equal

df = pl.DataFrame(
    {
        "A": [1.0, 0.0, 3.0, 4.0],
        "B": [4.0, 3.0, 2.0, 1.0],
        "C": ["cat", "dog", "cat", "mouse"],
        "D": ["red", "blue", "green", "blue"],
    }
)

expected_df = pl.DataFrame(
    {
        "": ["A", "B"],
        "Unique (#)": [4, 4],
        "Missing (%)": [0.00, 0.00],
        "Mean": [2.00, 2.50],
        "SD": [1.825742, 1.290994],
        "Min": [0.00, 1.00],
        "Median": [2.00, 2.50],
        "Max": [4.00, 4.00],
    }
)


def test_skim_numeric_df(data=df):
    # Act
    result = sf.skim_frame(data)

    # Assert
    assert_frame_equal(result, expected_df)
