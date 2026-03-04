from censusdis.multiyear import download_multiyear
from censusdis.datasets import ACS1
import pandas as pd


def _normalize_columns(df):
    """
    The earlier table (B05002) has columns that are not present in the newer
    table (B05012). The newer table also hyphenates "Foreign-born".
    Normalize column names so the tables can be concatenated.
    """
    df = df.rename(columns={"Foreign born": "Foreign-born", "NAME": "Name"})

    df = df[["Name", "Year", "Total", "Native", "Foreign-born"]]

    return df


def get_nativity_timeseries(**kwargs):
    # From 2005-8 the data we want is in table B05002
    df1 = download_multiyear(
        dataset=ACS1,
        vintages=list(range(2005, 2009)),
        group="B05002",
        drop_cols=False,
        **kwargs,
    )
    df1 = _normalize_columns(df1)

    # In later years, use B05012. Note that no ACS1 was published in 2020
    df2 = download_multiyear(
        dataset=ACS1,
        vintages=[year for year in range(2009, 2025) if year != 2020],
        group="B05012",
        drop_cols=False,
        **kwargs,
    )
    df2 = _normalize_columns(df2)

    df = pd.concat([df1, df2], ignore_index=True)

    # Add a column that will be useful for analysts, even though it's not returned by the API.
    df["Percent Foreign-born"] = df["Foreign-born"] / df["Total"] * 100

    return df
