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
        "var": ["A", "B"],
        "A": [1.0, -0.8485281374238571],
        "B": [-0.8485281374238571, 1.0],
    }
)


def test_correlation_df(data=df):
    # Act
    result = sf.correlation_frame(data)

    # Assert
    assert_frame_equal(result, expected_df)
