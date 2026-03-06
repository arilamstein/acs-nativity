"""
Functions for downloading, normalizing, and assembling ACS 1-year nativity data
into a consistent time series suitable for analysis and visualization.
"""

from censusdis.multiyear import download_multiyear
from censusdis.datasets import ACS1
import pandas as pd
from typing import Any


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    The earlier table (B05002) has columns that are not present in the newer
    table (B05012). The newer table also hyphenates "Foreign-born".
    Normalize column names so the tables can be concatenated.
    """
    df = df.rename(columns={"Foreign born": "Foreign-born", "NAME": "Name"})

    df = df[["Name", "Year", "Total", "Native", "Foreign-born"]]

    return df


def get_nativity_timeseries(*, end_year: int = 2024, **kwargs: Any) -> pd.DataFrame:
    """
    Retrieve a continuous ACS 1-year nativity time series from 2005 through `end_year`.

    This function stitches together ACS table B05002 (used from 2005–2008) and
    ACS table B05012 (used from 2009–`end_year`, excluding 2020 when no 1-year ACS
    was released) into a single, normalized DataFrame. It also adds a derived
    column, "Percent Foreign-born", for convenience.

    Additional keyword arguments are passed directly to
    `censusdis.download_multiyear`, allowing callers to specify geography or
    other censusdis options. Supported geography patterns mirror those in the
    censusdis documentation.

    Args:
        end_year (int): Last ACS 1-year vintage to include. Defaults to 2024.
        **kwargs: Keyword arguments forwarded to `download_multiyear`, typically
            specifying geography.

    Returns:
        pd.DataFrame: A DataFrame with nativity counts for each year, including
        "Total", "Native", "Foreign-born", and the derived
        "Percent Foreign-born".

    Examples:
        Nationwide:
            df = get_nativity_timeseries(us="*")

        State:
            from censusdis.states import MN
            df = get_nativity_timeseries(state=MN)

        County:
            from censusdis.states import NY
            from censusdis.counties.new_york import NASSAU
            df = get_nativity_timeseries(state=NY, county=NASSAU)

        City:
            from censusdis.states import IL
            from censusdis.places.illinois import CHICAGO_CITY
            df = get_nativity_timeseries(state=IL, place=CHICAGO_CITY)

        Metropolitan Statistical Area (MSA):
            from censusdis.msa_msa import EL_PASO_TX_METRO_AREA
            df = get_nativity_timeseries(
                metropolitan_statistical_area_micropolitan_statistical_area=
                    EL_PASO_TX_METRO_AREA
            )
    """

    if end_year < 2005:
        raise ValueError("end_year must be >= 2005 for ACS 1-year nativity data.")

    # 2005–2008: B05002
    df1 = download_multiyear(
        dataset=ACS1,
        vintages=[y for y in range(2005, min(end_year, 2008) + 1)],
        group="B05002",
        drop_cols=False,
        **kwargs,
    )
    df1 = _normalize_columns(df1)

    # 2009–end_year (excluding 2020): B05012
    if end_year >= 2009:
        vintages = [y for y in range(2009, end_year + 1) if y != 2020]
        df2 = download_multiyear(
            dataset=ACS1,
            vintages=vintages,
            group="B05012",
            drop_cols=False,
            **kwargs,
        )
        df2 = _normalize_columns(df2)
        df = pd.concat([df1, df2], ignore_index=True)
    else:
        df = df1

    df["Percent Foreign-born"] = df["Foreign-born"] / df["Total"] * 100
    return df
