"""Test the data.py module."""

import pandas as pd
from acs_nativity import data
import pytest
from unittest.mock import patch

EXPECTED_COLUMNS = ["Name", "Year", "Total", "Native", "Foreign-born"]


def test_normalize_columns_2008():
    """
    Test that we normalize columns from the 2008 data as expected. Use 2008
    because it is the last year of data from the first table we download, and
    censusdis.download_multiyear uses the column names from the of the last
    year of a multi-year period.
    """
    df_2008 = pd.DataFrame(
        {
            "US": {0: "1"},
            "Total": {0: 304059728},
            "Native": {0: 266098793},
            "Born in state of residence": {0: 179132918},
            "Born in other state in the United States": {0: 82935072},
            "Northeast": {0: 19834782},
            "Midwest": {0: 22663702},
            "South": {0: 26007650},
            "West": {0: 14428938},
            "Born outside the United States": {0: 4030803},
            "Puerto Rico": {0: 1441567},
            "U.S. Island Areas": {0: 177776},
            "Born abroad of American parent(s)": {0: 2411460},
            "Foreign born": {0: 37960935},
            "Naturalized U.S. citizen": {0: 16329909},
            "Not a U.S. citizen": {0: 21631026},
            "GEO_ID": {0: "0100000US"},
            "NAME": {0: "United States"},
            "Year": {0: 2008},
        }
    )
    df_out = data._normalize_columns(df_2008)
    assert list(df_out.columns) == EXPECTED_COLUMNS


def test_normalize_columns_2024():
    """
    Test that we normalize columns from the 2024 data as expected. Use 2024
    because it is the last year of data from the second table we download, and
    censusdis.download_multiyear uses the column names from the of the last
    year of a multi-year period.
    """
    df_2024 = pd.DataFrame(
        {
            "US": {0: "1"},
            "Total": {0: 340110990},
            "Native": {0: 289876132},
            "Foreign-born": {0: 50234858},
            "GEO_ID": {0: "0100000US"},
            "NAME": {0: "United States"},
            "Year": {0: 2024},
        }
    )
    df_out = data._normalize_columns(df_2024)
    assert list(df_out.columns) == EXPECTED_COLUMNS


def test_end_year_too_low():
    """Data not available for < 2005."""
    with pytest.raises(ValueError):
        data.get_nativity_timeseries(end_year=2004, us="*")


def test_end_year_minimum():
    """Verify we get something back for 2005."""
    df = data.get_nativity_timeseries(end_year=2005, us="*")
    assert isinstance(df, pd.DataFrame)


def test_normalize_columns_applied():
    """
    API returns different spellings of "Foreign-born" which we normalize.
    Also verify that we add in the "Percent Foreign-born" column.
    """
    # Fake early-year table (B05002)
    df_old = pd.DataFrame(
        {
            "NAME": ["United States"],
            "Year": [2005],
            "Total": [100],
            "Native": [80],
            "Foreign born": [20],
        }
    )

    # Fake later-year table (B05012)
    df_new = pd.DataFrame(
        {
            "Name": ["United States"],
            "Year": [2009],
            "Total": [110],
            "Native": [85],
            "Foreign-Born": [25],
        }
    )

    # Patch download_multiyear so your function doesn't hit the network
    with patch("acs_nativity.data.download_multiyear") as mock_dl:
        mock_dl.side_effect = [df_old, df_new]

        df = data.get_nativity_timeseries(end_year=2009, us="*")

    # After normalization, the columns should be unified
    assert list(df.columns) == [
        "Name",
        "Year",
        "Total",
        "Native",
        "Foreign-born",
        "Percent Foreign-born",
    ]


def test_vintages_passed_and_2020_skipped():
    """
    Census does not provide data for 2020 1-year ACS - it 404s if you try.
    Verify that we don't ask for that.
    """
    # Fake early-year table (B05002)
    df_old = pd.DataFrame(
        {
            "Name": ["United States"],
            "Year": [2005],
            "Total": [100],
            "Native": [80],
            "Foreign-born": [20],
        }
    )

    # Fake later-year table (B05012)
    df_new = pd.DataFrame(
        {
            "Name": ["United States"],
            "Year": [2024],
            "Total": [120],
            "Native": [90],
            "Foreign-born": [30],
        }
    )

    with patch("acs_nativity.data.download_multiyear") as mock_dl:
        mock_dl.side_effect = [df_old, df_new]

        df = data.get_nativity_timeseries(end_year=2024, us="*")

    # --- Assert the vintages passed to each call ---

    # First call: early years (B05002)
    first_call = mock_dl.call_args_list[0].kwargs
    assert first_call["vintages"] == [2005, 2006, 2007, 2008]

    # Second call: later years (B05012), skipping 2020
    second_call = mock_dl.call_args_list[1].kwargs
    assert 2020 not in second_call["vintages"]
    assert second_call["vintages"][0] == 2009
    assert second_call["vintages"][-1] == 2024

    # --- And as a sanity check, the output should not contain 2020 ---
    assert 2020 not in df["Year"].unique()
