import pytest
import polars as pl
from datasummary.ds import datasummary_skim

# Define a fixture for common test data
@pytest.fixture
def data():
    return pl.DataFrame({
        "A": [1.0, 2.0, 3.0, 4.0],
        "B": [4.0, 3.0, 2.0, 1.0]
        "C": ["cat", "dog", "cat", "mouse"],
        "D": ["red", "blue", "green", "blue"]
    })

# Happy path tests with various realistic test values
@pytest.mark.parametrize("test_input, type, output, float_precision, histogram, title, notes, align, expected_columns", [
    pytest.param(data(), "numeric", "default", 2, False, "Summary Statistics", None, "r", ["A", "B"], id="numeric-default"),
    pytest.param(data(), "categorical", "markdown", 2, False, "Category Summary", None, "l", ["C", "D"], id="categorical-markdown"),
    pytest.param(data(), "numeric", "simple", 2, True, "Numeric Summary", "Some notes", "c", ["A", "B"], id="numeric-simple-histogram"),
], indirect=["test_input"])
def test_datasummary_skim_happy_path(test_input, type, output, float_precision, histogram, title, notes, align, expected_columns):
    # Act
    result = datasummary_skim(test_input, type, output, float_precision, histogram, title, notes, align)

    # Assert
    assert all(column in result.columns for column in expected_columns)

# Edge cases
@pytest.mark.parametrize("test_input, type, output, float_precision, histogram, title, notes, align", [
    pytest.param(data(), "numeric", "default", 0, False, "Summary Statistics", None, "r", id="float-precision-zero"),
    pytest.param(data(), "numeric", "default", 10, False, "Summary Statistics", None, "r", id="float-precision-ten"),
    pytest.param(data(), "numeric", "default", 2, False, "", None, "r", id="empty-title"),
], indirect=["test_input"])
def test_datasummary_skim_edge_cases(test_input, type, output, float_precision, histogram, title, notes, align):
    # Act
    result = datasummary_skim(test_input, type, output, float_precision, histogram, title, notes, align)

    # Assert
    assert result is not None

# Error cases
@pytest.mark.parametrize("test_input, type, output, float_precision, histogram, title, notes, align, expected_exception", [
    pytest.param(data(), "numeric", "unknown", 2, False, "Summary Statistics", None, "r", ValueError, id="invalid-output-format"),
    pytest.param(data(), "unknown", "default", 2, False, "Summary Statistics", None, "r", ValueError, id="invalid-type"),
    pytest.param(data(), "numeric", "default", 2, False, "Summary Statistics", None, "x", ValueError, id="invalid-align"),
], indirect=["test_input"])
def test_datasummary_skim_error_cases(test_input, type, output, float_precision, histogram, title, notes, align, expected_exception):
    # Act & Assert
    with pytest.raises(expected_exception):
        datasummary_skim(test_input, type, output, float_precision, histogram, title, notes, align)
