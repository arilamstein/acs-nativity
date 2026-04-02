"""
Plotting functions for visualizing ACS nativity data, including time‑series
levels and year‑over‑year changes, with optional annotations and consistent
styling for use across analyses.
"""

import plotly.express as px
import pandas as pd
from typing import Any


def _add_numeric_hovertemplate(fig: Any, y_label: str) -> None:
    """
    Used for styling commas numbers in hover text.
    Ex.: "Total Population: 123,456,789".
    """
    fig.update_traces(
        hovertemplate=(f"Year: %{{x}}<br>{y_label}: %{{y:,.0f}}<extra></extra>")
    )


def _add_percent_hovertemplate(
    fig: Any, y_label: str, precision: int, show_percent_sign: bool
) -> None:
    """
    Format percent values in hover text.

    Examples:
    - Level percent (e.g., 12.3%): precision=1, show_percent_sign=True
    - Percentage-point change (e.g., 0.12): precision=2, show_percent_sign=False
    """
    percent_sign = "%" if show_percent_sign else ""
    fig.update_traces(
        hovertemplate=(
            "Year: %{x}<br>"
            f"{y_label}: %{{y:.{precision}f}}{percent_sign}<extra></extra>"
        )
    )


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
    """
    Plot a nativity time series for a selected column using Plotly.

    This function creates a line chart showing the values of a specified
    nativity-related column across years. It supports optional annotations
    marking the start of presidential administrations and can append a standard
    ACS data source note to the figure. The function returns a Plotly figure
    object, allowing callers to further customize or display it.

    Args:
        df: A DataFrame containing a nativity time series, typically produced by
            `get_nativity_timeseries`.
        column: The column in `df` to plot (e.g., "Foreign-born",
            "Percent Foreign-born").
        title: Optional title for the chart. If omitted, a title is generated
            automatically.
        y_label: Optional label for the y-axis. If omitted, a label is generated
            automatically.
        add_annotations: Whether to add vertical dashed lines marking the start
            of presidential administrations.
        add_source: Whether to append a standard ACS source note.

    Returns:
        A Plotly figure visualizing the selected nativity time series.

    Examples:
        Plot the nationwide foreign-born population:
            df = get_nativity_timeseries(us="*")
            fig = plot_nativity_timeseries(df, "Foreign-born")
            fig.show()

        Plot the nationwide percent foreign-born:
            df = get_nativity_timeseries(us="*")
            fig = plot_nativity_timeseries(df, "Percent Foreign-born")
            fig.show()
    """
    if title is None:
        title = _generate_timeseries_title(df, column)

    # Don't use the column name (ex. "Total") for the y-axis
    if y_label is None:
        y_label = _generate_timeseries_y_label(column)
    labels = {column: y_label}

    fig = px.line(
        df,
        x="Year",
        y=column,
        title=title,
        markers=True,
        labels=labels,
    )

    # The year is obvious and doesn't need a label on the x-axis
    # Doing it this way (instead of with the label) keeps it for the tool tip
    fig.update_xaxes(title_text="")

    if column == "Percent Foreign-born":
        _add_percent_hovertemplate(fig, y_label, precision=1, show_percent_sign=True)
    else:
        _add_numeric_hovertemplate(fig, y_label)

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
    """
    Plot year-over-year change for a selected nativity column using Plotly.

    This function computes and visualizes the annual change in a specified
    nativity-related column. It supports optional annotations marking the start
    of presidential administrations and can append a standard ACS data source
    note to the figure. The function returns a Plotly figure object, allowing
    callers to further customize or display it.

    Args:
        df: A DataFrame containing a nativity time series, typically produced by
            `get_nativity_timeseries`.
        column: The column in `df` for which to compute and plot year-over-year
            change (e.g., "Foreign-born", "Percent Foreign-born").
        title: Optional title for the chart. If omitted, a title is generated
            automatically.
        y_label: Optional label for the y-axis. If omitted, a label is generated
            automatically.
        add_annotations: Whether to add vertical dashed lines marking the start
            of presidential administrations.
        add_source: Whether to append a standard ACS source note.

    Returns:
        A Plotly figure visualizing the year-over-year change in the selected
        nativity column.

    Examples:
        Plot the nationwide year-over-year change in the foreign-born population:
            df = get_nativity_timeseries(us="*")
            fig = plot_nativity_change(df, "Foreign-born")
            fig.show()

        Plot the nationwide year-over-year change in percent foreign-born:
            df = get_nativity_timeseries(us="*")
            fig = plot_nativity_change(df, "Percent Foreign-born")
            fig.show()
    """

    df = df.copy()
    df[column] = df[column].diff()

    if title is None:
        title = _generate_change_title(df, column)

    # Don't use the column name (ex. "Total") for the y-axis
    if y_label is None:
        y_label = _generate_change_y_label(column)
    labels = {column: y_label}

    fig = px.bar(
        df,
        x="Year",
        y=column,
        title=title,
        labels=labels,
    )

    # The year is obvious and doesn't need a label on the x-axis
    # Doing it this way (instead of with the label) keeps it for the tool tip
    fig.update_xaxes(title_text="")

    if column == "Percent Foreign-born":
        _add_percent_hovertemplate(fig, y_label, precision=2, show_percent_sign=False)
    else:
        _add_numeric_hovertemplate(fig, y_label)

    if add_annotations:
        _add_annotations(fig, df, column)

    if add_source:
        _add_source_footer(fig)

    return fig
