import plotly.express as px


def _add_annotations(fig, df):
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
    max_y = df["Foreign-born"].max()

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
    fig, source_text="Source: American Community Survey 1-Year Estimates"
):
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
    df, column, title="", y_label="Population", add_annotations=True, add_source=True
):
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
        _add_annotations(fig, df)

    if add_source:
        _add_source_footer(fig)

    return fig


def plot_nativity_change(
    df,
    column,
    title="",
    y_label="Population Change",
    add_annotations=True,
    add_source=True,
):
    df = df.copy()
    df[column] = df[column].diff()

    labels = {"Year": "", column: y_label}

    fig = px.bar(
        df,
        x="Year",
        y=column,
        title=title,
        labels=labels,
    )

    if add_annotations:
        _add_annotations(fig, df)

    if add_source:
        _add_source_footer(fig)

    return fig
