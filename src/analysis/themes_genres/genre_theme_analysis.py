import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import seaborn as sns
from plotly.subplots import make_subplots
import ast
import plotly.express as px
import plotly.graph_objects as go
from ipywidgets import interact, Dropdown
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.utils.constants import *


def create_comparison_df(
    west_df,
    east_df,
    threshold,
):
    comparison_df = pd.DataFrame({"Western": west_df, "Eastern": east_df}).fillna(0)

    comparison_df["relative_difference"] = (
        comparison_df["Eastern"] - comparison_df["Western"]
    ) / (comparison_df["Eastern"] + comparison_df["Western"])

    comparison_df["absolute_relative_difference"] = comparison_df[
        "relative_difference"
    ].abs()

    comparison_df["Eastern_Proportion"] = (
        comparison_df["Eastern"] / comparison_df["Eastern"].sum(axis=0) * 100
    )
    comparison_df["Western_Proportion"] = (
        comparison_df["Western"] / comparison_df["Western"].sum(axis=0) * 100
    )

    comparison_df["proportion_relative_difference"] = (
        comparison_df["Eastern_Proportion"] - comparison_df["Western_Proportion"]
    ) / (comparison_df["Eastern_Proportion"] + comparison_df["Western_Proportion"])
    comparison_df["absolute_proportion_relative_difference"] = comparison_df[
        "proportion_relative_difference"
    ].abs()

    comparison_df["total"] = comparison_df["Eastern"] + comparison_df["Western"]

    comparison_df = (
        comparison_df[
            (comparison_df["Eastern"] > threshold)
            | (comparison_df["Western"] > threshold)
        ]
        .sort_values("absolute_relative_difference", ascending=False)
        .head(20)
    )
    return comparison_df


def get_genres_yearly_count(genres_df, common_genres):
    western_genres_yearly_counts = (
        genres_df[genres_df["cold_war_side"] == "Western"]
        .explode("genres")
        .groupby("release_date")["genres"]
        .value_counts()
    ).reset_index()
    eastern_genres_yearly_counts = (
        genres_df[genres_df["cold_war_side"] == "Eastern"]
        .explode("genres")
        .groupby("release_date")["genres"]
        .value_counts()
    ).reset_index()

    eastern_genres_yearly_counts = eastern_genres_yearly_counts[
        eastern_genres_yearly_counts["genres"].isin(common_genres)
    ]
    western_genres_yearly_counts = western_genres_yearly_counts[
        western_genres_yearly_counts["genres"].isin(common_genres)
    ]

    return western_genres_yearly_counts, eastern_genres_yearly_counts


def plot_genres_over_time(side_genres_counts, side, common_genres):
    # Create the interactive line plot
    fig = px.line(
        side_genres_counts.reset_index(),
        x="release_date",
        y="count",
        color="genres",
        category_orders={"genres": common_genres},
        title=f"Genre Counts Over Time for {side} Movies",
        labels={"release_date": "Release Date", "Count": "Count", "Genre": "Genres"},
    )

    # Make all traces except War invisible by default
    fig.for_each_trace(
        lambda trace: (
            trace.update(visible="legendonly") if trace.name != "War" else None
        )
    )
    fig.show()


def plot_interactive_genre_over_time(
    western_genres_yearly_counts, eastern_genres_yearly_counts, common_genres
):
    # Interactive widget
    def interactive_plot(side_genres):
        if side_genres == "Western":
            plot_genres_over_time(
                western_genres_yearly_counts, "Western", common_genres
            )
        elif side_genres == "Eastern":
            plot_genres_over_time(
                eastern_genres_yearly_counts, "Eastern", common_genres
            )

    # Use interact with a dropdown
    return interact(
        interactive_plot,
        side_genres=Dropdown(
            options=["Western", "Eastern"], value="Western", description="Region"
        ),
    )


def plot_genres_over_period(side_genres_counts, side, bins, labels, common_genres):

    years = [bins[i + 1] - bins[i] for i in range(len(bins) - 1)]
    period_years = dict(zip(labels, years))

    # Divide counts by the number of years in the corresponding period
    side_genres_counts["years"] = side_genres_counts["period"].map(period_years)
    side_genres_counts["count"] = side_genres_counts["count"] / side_genres_counts[
        "years"
    ].astype(int)

    # Create the interactive line plot
    fig = px.bar(
        side_genres_counts.reset_index(),
        x="period",
        y="count",
        color="genres",
        title=f"Average Number of Movies per Year for Different Genres Over Different Periods for {side} Movies",
        labels={"period": "Release Date", "Count": "Count", "Genre": "Genres"},
        category_orders={"genres": common_genres},
    )
    # Make all traces except War invisible by default

    fig.for_each_trace(
        lambda trace: (
            trace.update(visible="legendonly") if trace.name != "War" else None
        )
    )

    fig.show()


def plot_interactive_genre_over_period(
    genres_df,
    common_genres,
    bins=[1945, 1953, 1962, 1974, 1984, 1995],
    labels=[
        "Blocs Establishment",
        "Major tensions and crises",
        "Détente",
        "Second Cold War",
        "End of the Cold War",
    ],
):
    genres_df["period"] = pd.cut(
        genres_df["release_date"], bins, labels=labels, right=True
    )

    period_counts = (
        genres_df.explode("genres")
        .groupby(["period", "cold_war_side"], observed=False)["genres"]
        .value_counts()
        .reset_index()
    )
    period_counts = period_counts[period_counts["genres"].isin(common_genres)]
    eastern_period_counts = period_counts[
        period_counts["cold_war_side"] == "Eastern"
    ].reset_index()
    western_period_counts = period_counts[
        period_counts["cold_war_side"] == "Western"
    ].reset_index()

    # Interactive widget
    def interactive_plot(side_genres):
        if side_genres == "Western":
            plot_genres_over_period(
                western_period_counts, "Western", bins, labels, common_genres
            )
        elif side_genres == "Eastern":
            plot_genres_over_period(
                eastern_period_counts, "Eastern", bins, labels, common_genres
            )

    # Use interact with a dropdown
    return interact(
        interactive_plot,
        side_genres=Dropdown(
            options=["Western", "Eastern"], value="Western", description="Region"
        ),
    )


def plot_relative_difference(comparison_df, compared, abs=False, prop=False):
    column = "relative_difference"
    sort_column = "relative_difference"

    if prop:
        sort_column = "proportion_" + column
        column = "proportion_" + column
    if abs:
        column = "absolute_" + column

    comparison_df = comparison_df.sort_values(sort_column)
    comparison_df[column].plot(
        kind="barh",
        figsize=(10, 6),
        color=[
            COLOR_SCALE[0] if x > 0 else COLOR_SCALE[-1]
            for x in comparison_df[sort_column]
        ],
    )
    column = column.replace("_", " ").title()
    plt.title(f"{compared}: {column} Between Sides")
    plt.xlabel(f"{column}")
    plt.ylabel(f"{compared}")

    # Create custom legend
    legend_elements = [
        Patch(color=COLOR_SCALE[0], label="Eastern Side"),
        Patch(color=COLOR_SCALE[-1], label="Western Side"),
    ]
    plt.legend(handles=legend_elements, title="Side")
    plt.show()


def clean_genre_explode(movies_df):
    genres_df = movies_df[["countries", "cold_war_side", "genres", "release_date"]]

    genres_df = genres_df.explode("genres")[genres_df.explode("genres") != "\\N"]
    genres_df["genres"] = (
        genres_df["genres"]
        .str.title()
        .str.strip()
        .replace({"Sci-Fi": "Science Fiction"})
    )

    genre_counts = genres_df["genres"].value_counts().head(20)
    common_genres = genre_counts.head(12).index

    return genres_df, common_genres


def plot_distribution(df, column, log_scale=False):
    df_counts = df[column].value_counts().head(20)

    # Plot the distribution
    plt.figure(figsize=(10, 6))
    sns.barplot(x=df_counts.values, y=df_counts.index, color=DISTINCT_COLORS[1])
    plt.title(f"Distribution of {column.title()}")
    plt.xlabel("Count")
    plt.ylabel(column.title())
    if log_scale:
        plt.xscale("log")
    plt.show()


def plot_side_by_side(
    western_count,
    eastern_count,
    x_column="language",
    y_column="count",
    title="Top 20 Languages",
):
    color_scale = [
        COLOR_SCALE[-1],
        COLOR_SCALE[0],
    ]  # Default colors for Western and Eastern

    # Create subplot
    fig = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "bar"}, {"type": "bar"}]],
        subplot_titles=("in Western Bloc Movies", "in Eastern Bloc Movies"),
    )

    # Western plot
    fig.add_trace(
        go.Bar(
            x=western_count[x_column].head(20),
            y=western_count[y_column],
            hovertemplate="%{x}: %{y}<extra></extra>",
            marker_color=color_scale[0],
        ),
        row=1,
        col=1,
    )

    # Eastern plot
    fig.add_trace(
        go.Bar(
            x=eastern_count[x_column].head(20),
            y=eastern_count[y_column],
            hovertemplate="%{x}: %{y}<extra></extra>",
            marker_color=color_scale[1],
        ),
        row=1,
        col=2,
    )

    # Set log scale for y-axes
    fig.update_yaxes(type="log", row=1, col=1)
    fig.update_yaxes(type="log", row=1, col=2)

    # Rotate x-axis labels
    fig.update_xaxes(tickangle=45)

    # Set axis titles
    fig.update_xaxes(title_text=x_column.title())
    fig.update_yaxes(title_text="Number of Movies")

    # Update the layout
    fig.update_layout(
        title_text=title,
        title_x=0.5,
        title_font_weight="bold",
        showlegend=False,
        plot_bgcolor="#F2F2F2",
    )

    # Update layout for better visualization
    fig.update_layout(
        xaxis=dict(title_text=x_column.title()),
        xaxis2=dict(title_text=x_column.title()),
        yaxis=dict(title_text="Number of Movies"),
        yaxis2=dict(title_text="Number of Movies"),
    )

    # Show the plot
    fig.show()

    return fig


def get_side_war_theme_counts(themes_df):
    eastern_war_themes = themes_df[
        (themes_df["cold_war_side"] == "Eastern")
        & (themes_df["genres"].apply(lambda x: "War" in x))
    ]
    western_war_themes = themes_df[
        (themes_df["cold_war_side"] == "Western")
        & (themes_df["genres"].apply(lambda x: "War" in x))
    ]
    western_war_themes_counts = western_war_themes["theme"].value_counts()
    eastern_war_themes_counts = eastern_war_themes["theme"].value_counts()

    # remove war from themes
    western_war_themes_counts = western_war_themes_counts[
        western_war_themes_counts.index != "War"
    ]
    eastern_war_themes_counts = eastern_war_themes_counts[
        eastern_war_themes_counts.index != "War"
    ]

    return western_war_themes_counts, eastern_war_themes_counts


def plot_theme_distribution(themes_df):
    theme_counts = themes_df["theme"].value_counts().head(20)
    # Plot the distribution
    plt.figure(figsize=(10, 6))

    sns.barplot(
        x=theme_counts.values,
        y=theme_counts.index,
    )

    plt.title("Distribution of Genres")
    plt.xlabel("Count")
    plt.ylabel("Theme")
    plt.show()


def get_vietnam_war_films(movies_df):
    return movies_df.dropna(subset=["genres", "theme", "cold_war_side"])[
        (
            movies_df.dropna(subset=["genres", "theme", "cold_war_side"])[
                "genres"
            ].apply(lambda x: "War" in x)
        )
        & (
            movies_df.dropna(subset=["genres", "theme", "cold_war_side"])[
                "cold_war_side"
            ]
            == "Western"
        )
        & (
            movies_df.dropna(subset=["genres", "theme", "cold_war_side"])[
                "theme"
            ].apply(lambda x: "Vietnam War" in x)
        )
    ]


def get_comedy_war_movies(movies_df):
    return movies_df.dropna(subset=["genres", "theme", "cold_war_side"])[
        (
            movies_df.dropna(subset=["genres", "theme", "cold_war_side"])[
                "genres"
            ].apply(lambda x: "War" in x)
        )
        & (
            movies_df.dropna(subset=["genres", "theme", "cold_war_side"])[
                "cold_war_side"
            ]
            == "Western"
        )
        & (
            movies_df.dropna(subset=["genres", "theme", "cold_war_side"])[
                "theme"
            ].apply(lambda x: "Comedy" in x)
        )
    ]


# Create Plotly figure function
def plot_genre_over_periods(
    genres_df,
    genre,
    bins=[1945, 1953, 1962, 1974, 1984, 1995],
    labels=[
        "Blocs Establishment",
        "Major tensions and crises",
        "Détente",
        "Second Cold War",
        "End of the Cold War",
    ],
):
    genres_df["period"] = pd.cut(
        genres_df["release_date"], bins, labels=labels, right=True
    )

    period_counts = (
        genres_df.explode("genres")
        .groupby(["period", "cold_war_side"], observed=False)["genres"]
        .value_counts()
        .reset_index()
    )

    df = period_counts
    years = [bins[i + 1] - bins[i] for i in range(len(bins) - 1)]
    period_years = dict(zip(labels, years))

    # Divide counts by the number of years in the corresponding period
    df["years"] = df["period"].map(period_years)
    df["count"] = df["count"] / df["years"].astype(int)

    fig = px.bar(
        df[df["genres"] == genre],
        x="period",
        y="count",
        color="cold_war_side",
        title=f"Average Number Of {genre} Movies per Year Over Different Periods",
        labels={
            "period": "Period",
            "count": "Count",
            "genres": "Genres",
            "cold_war_side": "Side",
        },
        template="plotly_white",
        barmode="group",
        color_discrete_map={
            "Western": COLOR_SCALE[-1],  # Assign "Western" to blue
            "Eastern": COLOR_SCALE[0],  # Assign "Eastern" to red
        },
    )

    fig.update_layout(
        hovermode="x unified",
        title=dict(x=0.5, xanchor="center"),
    )
    return fig


def plot_interactive_side_over_period(
    genres_df,
    common_genres,
    bins=[1945, 1953, 1962, 1974, 1984, 1995],
    labels=[
        "Blocs Establishment",
        "Major tensions and crises",
        "Détente",
        "Second Cold War",
        "End of the Cold War",
    ],
):

    # Use interact with a dropdown
    interact(
        lambda genre: plot_genre_over_periods(
            genres_df[genres_df["cold_war_side"].isin(["Western", "Eastern"])],
            genre,
        ),
        genre=Dropdown(options=common_genres, value="War", description="Genre"),
    )
