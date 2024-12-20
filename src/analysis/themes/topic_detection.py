import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plots_template import *
import spacy
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from pyLDAvis import gensim_models
import warnings
import pickle
from src.utils.constants import *
from src.utils.helpers import *

warnings.filterwarnings("ignore")

BEGIN_COLD_WAR = (1947, 1953)
CRISIS = (1954, 1962)
DETENT = (1963, 1974)
SECOND_COLD_WAR = (1975, 1984)
END = (1985, 1991)

THEME_PERIODS = [
    "Begin (47-53)",
    "Crisis (54-62)",
    "Detent (63-74)",
    "Second CW (75-84)",
    "End (85-91)",
]

THEME_TOPICS = {
    0: "Romance & Social Dramas",
    1: "War & Spy Dramas",
    2: "Crime & Moral Thrillers",
    3: "Political Dramas",
}

THEME_TOPIC_COLORS = {
    THEME_TOPICS[0]: DISTINCT_COLORS[0],
    THEME_TOPICS[1]: DISTINCT_COLORS[1],
    THEME_TOPICS[2]: DISTINCT_COLORS[2],
    THEME_TOPICS[3]: DISTINCT_COLORS[3],
}

# THEME_TOPIC_COLORS = {
#     THEME_TOPICS[0]: DISTINCT_COLORS[0],
#     THEME_TOPICS[1]: DISTINCT_COLORS[2],
#     THEME_TOPICS[2]: DISTINCT_COLORS[4],
#     THEME_TOPICS[3]: DISTINCT_COLORS[9]
# }


def create_theme(df):
    new_df = df[["theme", "cold_war_side", "title", "release_date"]]
    # get only Western and Eastern movies
    new_df = new_df[
        (new_df["cold_war_side"] == "Western") | (new_df["cold_war_side"] == "Eastern")
    ]
    new_df = new_df.rename(columns={"cold_war_side": "movie_side"})
    new_df = new_df.drop_duplicates(subset=["theme"])
    # be sure theme is a list
    new_df["theme"] = new_df["theme"].apply(lambda x: x if isinstance(x, list) else [x])
    # be sure all elements of the list are strings
    new_df["theme"] = new_df["theme"].apply(lambda x: [str(i) for i in x])
    # use lower case for theme for each element of the list
    new_df["theme"] = new_df["theme"].apply(lambda x: [i.lower() for i in x])
    return new_df


# Preprocess the text
def preprocess(string_list, nlp, words_to_remove):
    docs = [nlp(s) for s in string_list]
    tokens = []
    for doc in docs:
        tokens.extend(
            [
                token.lemma_
                for token in doc
                if not token.is_stop
                and not token.is_punct
                and token.lemma_ not in words_to_remove
            ]
        )
    return tokens


def topic_detection(df, nb_topics, nb_passes):
    # Create a dictionary and corpus for Gensim
    dictionary = corpora.Dictionary(df)
    corpus = [dictionary.doc2bow(text) for text in df]

    # Train LDA model
    lda_model = LdaModel(
        corpus, num_topics=nb_topics, id2word=dictionary, passes=nb_passes
    )

    # Print the topics
    for idx, topic in lda_model.print_topics(-1):
        print(f"Topic: {idx}\nWords: {topic}\n")

    return lda_model, corpus, dictionary


# Assign topics to characters
def get_dominant_topic(lda_model, corpus):
    topics = []
    for row in corpus:
        row = lda_model[row]
        max_topic, max_val = 0, 0
        for topic_num, prop_topic in row:
            if prop_topic > max_val:
                max_val = prop_topic
                max_topic = topic_num
        topics.append(max_topic)
    return topics


def create_theme_topics(theme_df):
    nlp = spacy.load("en_core_web_sm")
    words_to_remove = {"theme", "soviet", "ii", "vs", "vs.", " "}
    theme_df["processed_repres"] = theme_df["theme"].apply(
        preprocess, args=(nlp, words_to_remove)
    )
    theme_topic = topic_detection(theme_df["processed_repres"], 5, 15)
    pickle.dump(
        theme_topic,
        open(
            DATA_FOLDER + "theme_topic3.pkl",
            "wb",
        ),
    )
    return theme_topic


def get_eastern_western_theme_topics(theme_df, theme_topic):
    # for idx, topic in theme_topic[0].print_topics(-1):
    #     print(f"Topic: {idx}\nWords: {topic}\n")

    theme_df["dominant_topic"] = get_dominant_topic(theme_topic[0], theme_topic[1])
    eastern_theme = theme_df[theme_df["movie_side"] == "Eastern"]
    western_theme = theme_df[theme_df["movie_side"] == "Western"]

    return theme_df, eastern_theme, western_theme


def get_model(topics):
    return gensim_models.prepare(topics[0], topics[1], topics[2])


def to_topic_list(series):
    # Given a Series from value_counts() indexed by topics, return a list
    # of counts for topics [0,1,2,3] in that exact order.
    return [series.get(i, 0) for i in [0, 1, 2, 3]]


def plot_normalised_distribution_topic_periods_side(eastern_df, western_df):
    eastern_percent = eastern_df.div(eastern_df.sum(axis=1), axis=0) * 100

    western_percent = western_df.div(western_df.sum(axis=1), axis=0) * 100

    # Create subplots: one for Eastern and one for Western
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=[
            "Eastern Theme Topics (Percentage)",
            "Western Theme Topics (Percentage)",
        ],
    )

    # Add stacked bars for Eastern (with legend)
    for topic in eastern_percent.columns:
        fig.add_trace(
            go.Bar(
                x=THEME_PERIODS,
                y=eastern_percent[topic],
                name=topic,
                marker_color=THEME_TOPIC_COLORS[topic],
                hovertemplate="Period: %{x}<br>Topic: "
                + topic
                + "<br>Percentage: %{y:.1f}%<extra></extra>",
            ),
            row=1,
            col=1,
        )

    # Add stacked bars for Western (no legend to avoid duplication)
    for topic in western_percent.columns:
        fig.add_trace(
            go.Bar(
                x=THEME_PERIODS,
                y=western_percent[topic],
                name=topic,
                marker_color=THEME_TOPIC_COLORS[topic],
                hovertemplate="Period: %{x}<br>Topic: "
                + topic
                + "<br>Percentage: %{y:.1f}%<extra></extra>",
                showlegend=False,
            ),
            row=1,
            col=2,
        )

    fig.update_layout(
        barmode="stack",
        title_text="Percentage Distribution of Topics in Eastern vs Western Themed Movies Over Cold War Periods",
        height=600,
        width=1200,
        legend_title_text="Topics",
        font_family="Helvetica",
        plot_bgcolor="#F2F2F2",
    )

    fig.update_xaxes(title_text="Cold War Periods", row=1, col=1)
    fig.update_yaxes(
        title_text="Percentage of Movies", ticksuffix="%", range=[0, 100], row=1, col=1
    )

    fig.update_xaxes(title_text="Cold War Periods", row=1, col=2)
    fig.update_yaxes(
        title_text="Percentage of Movies", ticksuffix="%", range=[0, 100], row=1, col=2
    )

    fig.show()

    return fig


def plot_distribution_topic_periods_side(eastern_df, western_df):
    # Create subplots: one for Eastern and one for Western
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=[
            "Eastern Theme Topics Over Periods",
            "Western Theme Topics Over Periods",
        ],
    )

    # Add stacked bars for Eastern (with legend)
    for topic in eastern_df.columns:
        fig.add_trace(
            go.Bar(
                x=THEME_PERIODS,
                y=eastern_df[topic],
                name=topic,
                marker_color=THEME_TOPIC_COLORS[topic],
                hovertemplate="Period: %{x}<br>Topic: "
                + topic
                + "<br>Count: %{y}<extra></extra>",
            ),
            row=1,
            col=1,
        )

    # Add stacked bars for Western (no legend)
    for topic in western_df.columns:
        fig.add_trace(
            go.Bar(
                x=THEME_PERIODS,
                y=western_df[topic],
                name=topic,
                marker_color=THEME_TOPIC_COLORS[topic],
                hovertemplate="Period: %{x}<br>Topic: "
                + topic
                + "<br>Count: %{y}<extra></extra>",
                showlegend=False,  # Disable legend here
            ),
            row=1,
            col=2,
        )

    fig.update_layout(
        barmode="stack",
        title_text="Distribution of Topics in Eastern vs Western Themed Movies Over Cold War Periods",
        # center the title
        # title_x=0.5,
        height=600,
        width=1200,
        legend_title_text="Topics",
    )

    fig.update_xaxes(title_text="Cold War Periods", row=1, col=1)
    fig.update_yaxes(title_text="Number of Movies", row=1, col=1)

    fig.update_xaxes(title_text="Cold War Periods", row=1, col=2)
    fig.update_yaxes(title_text="Number of Movies", row=1, col=2)

    fig.show()

    return fig


def create_eastern_western_topics_periods(eastern_theme, western_theme):
    eastern_theme_begin = eastern_theme[
        eastern_theme["release_date"].apply(
            lambda x: x >= BEGIN_COLD_WAR[0] and x <= BEGIN_COLD_WAR[1]
        )
    ]
    eastern_theme_crisis = eastern_theme[
        eastern_theme["release_date"].apply(lambda x: x >= CRISIS[0] and x <= CRISIS[1])
    ]
    eastern_theme_detent = eastern_theme[
        eastern_theme["release_date"].apply(lambda x: x >= DETENT[0] and x <= DETENT[1])
    ]
    eastern_theme_second = eastern_theme[
        eastern_theme["release_date"].apply(
            lambda x: x >= SECOND_COLD_WAR[0] and x <= SECOND_COLD_WAR[1]
        )
    ]
    eastern_theme_end = eastern_theme[
        eastern_theme["release_date"].apply(lambda x: x >= END[0] and x <= END[1])
    ]

    western_theme_begin = western_theme[
        western_theme["release_date"].apply(
            lambda x: x >= BEGIN_COLD_WAR[0] and x <= BEGIN_COLD_WAR[1]
        )
    ]
    western_theme_crisis = western_theme[
        western_theme["release_date"].apply(lambda x: x >= CRISIS[0] and x <= CRISIS[1])
    ]
    western_theme_detent = western_theme[
        western_theme["release_date"].apply(lambda x: x >= DETENT[0] and x <= DETENT[1])
    ]
    western_theme_second = western_theme[
        western_theme["release_date"].apply(
            lambda x: x >= SECOND_COLD_WAR[0] and x <= SECOND_COLD_WAR[1]
        )
    ]
    western_theme_end = western_theme[
        western_theme["release_date"].apply(lambda x: x >= END[0] and x <= END[1])
    ]

    eastern_counts = {
        THEME_PERIODS[0]: to_topic_list(
            eastern_theme_begin["dominant_topic"].value_counts()
        ),
        THEME_PERIODS[1]: to_topic_list(
            eastern_theme_crisis["dominant_topic"].value_counts()
        ),
        THEME_PERIODS[2]: to_topic_list(
            eastern_theme_detent["dominant_topic"].value_counts()
        ),
        THEME_PERIODS[3]: to_topic_list(
            eastern_theme_second["dominant_topic"].value_counts()
        ),
        THEME_PERIODS[4]: to_topic_list(
            eastern_theme_end["dominant_topic"].value_counts()
        ),
    }

    western_counts = {
        THEME_PERIODS[0]: to_topic_list(
            western_theme_begin["dominant_topic"].value_counts()
        ),
        THEME_PERIODS[1]: to_topic_list(
            western_theme_crisis["dominant_topic"].value_counts()
        ),
        THEME_PERIODS[2]: to_topic_list(
            western_theme_detent["dominant_topic"].value_counts()
        ),
        THEME_PERIODS[3]: to_topic_list(
            western_theme_second["dominant_topic"].value_counts()
        ),
        THEME_PERIODS[4]: to_topic_list(
            western_theme_end["dominant_topic"].value_counts()
        ),
    }

    eastern_df = pd.DataFrame(
        eastern_counts, index=[topic for topic in THEME_TOPICS.values()]
    ).T
    western_df = pd.DataFrame(
        western_counts, index=[topic for topic in THEME_TOPICS.values()]
    ).T

    return eastern_df, western_df
