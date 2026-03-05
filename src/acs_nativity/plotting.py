import plotly.express as px
import pandas as pd
from typing import Any


def _generate_timeseries_title(df: pd.DataFrame, column: str) -> str:

    allowed = ["Total", "Native", "Foreign-born", "Percent Foreign-born"]
    if column not in allowed:
        raise ValueError(f"column must be one of {allowed}")

    if df["Name"].nunique() != 1:
        raise ValueError(
            "Automatic titles require a dataframe with a single geography."
        )

    geo_name = df["Name"].iloc[0]

    if column == "Percent Foreign-born":
        label = column
    else:
        label = f"{column} Population"

    if geo_name == "United States":
        geo_name = "the United States"

    return f"{label} in {geo_name}"


def _generate_change_title(df: pd.DataFrame, column: str) -> str:
    ts_title = _generate_timeseries_title(df, column)
    return f"Change in {ts_title}"


def _generate_timeseries_y_label(column: str) -> str:
    if column == "Percent Foreign-born":
        return "Percent"
    else:
        return "Population"


def _generate_change_y_label(column: str) -> str:
    ts_label = _generate_timeseries_y_label(column)
    return f"Change in {ts_label}"


def _add_annotations(fig: Any, df: pd.DataFrame, column: str) -> None:
    administrations = [
        {"President": "Bush 2", "Start": 2005},
        {"President": "Obama 1", "Start": 2009},
        {"President": "Obama 2", "Start": 2013},
        {"President": "Trump 1", "Start": 2017},
        {"President": "Biden", "Start": 2021},
        # Add a line for Trump's second term. But do not include a name, because there is not room for it
        # on the graph.
        {"President": "", "Start": 2025},
    ]

    # Add a vertical line on the date the administration started, and write the presdient's name on the top
    max_y = df[column].max()

    for one_administration in administrations:
        fig.add_vline(
            one_administration["Start"],
            line_color="black",
            line_dash="dash",
        )
        fig.add_annotation(
            x=one_administration["Start"],
            y=max_y,
            text=one_administration["President"],
            xanchor="left",
            xshift=5,
            showarrow=False,
            yanchor="bottom",
        )


def _add_source_footer(
    fig: Any, source_text: str = "Source: American Community Survey 1-Year Estimates"
) -> None:
    fig.add_annotation(
        text=source_text,
        x=0,
        y=-0.15,
        xref="paper",
        yref="paper",
        showarrow=False,
        xanchor="left",
        yanchor="top",
        font=dict(size=12, color="gray"),
    )


def plot_nativity_timeseries(
    df: pd.DataFrame,
    column: str,
    title: str | None = None,
    y_label: str | None = None,
    add_annotations: bool = True,
    add_source: bool = True,
) -> Any:
    if title is None:
        title = _generate_timeseries_title(df, column)

    if y_label is None:
        y_label = _generate_timeseries_y_label(column)

    # Overwrite default names for x- and y-axes
    labels = {"Year": "", column: y_label}

    fig = px.line(
        df,
        x="Year",
        y=column,
        title=title,
        markers=True,
        labels=labels,
    )

    if add_annotations:
        _add_annotations(fig, df, column)

    if add_source:
        _add_source_footer(fig)

    return fig


def plot_nativity_change(
    df: pd.DataFrame,
    column: str,
    title: str | None = None,
    y_label: str | None = None,
    add_annotations: bool = True,
    add_source: bool = True,
) -> Any:
    df = df.copy()
    df[column] = df[column].diff()

    if title is None:
        title = _generate_change_title(df, column)

    if y_label is None:
        y_label = _generate_change_y_label(column)

    # Overwrite default names for x- and y-axes
    labels = {"Year": "", column: y_label}

    fig = px.bar(
        df,
        x="Year",
        y=column,
        title=title,
        labels=labels,
    )

    if add_annotations:
        _add_annotations(fig, df, column)

    if add_source:
        _add_source_footer(fig)

    return fig
