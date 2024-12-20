import pandas as pd
import numpy as np
import plotly.express as px
from empath import Empath

LEXICON = Empath()

# Select lexical categories of interest for our study
CAT = ['politics', 'leader', 'military', 'heroic', 'law', 'affection', 'help', 'pride', 'family', 
       'love', 'power', 'deception', 'friends', 'sadness', 'disappointment', 'shame']

# Define groups of similar categories
TOPIC_GROUPS = {
    'love & affection': ['love', 'affection', 'family'],
    'support & solidarity': ['help', 'friends'],
    'politics & power': ['politics', 'leader', 'military', 'power'],
    'deception': ['deception', 'sadness', 'disappointment', 'shame']
}

def semantical_analysis(text, categories):
    """
    Perform a semantical analysis of a text using the Empath lexicon

    Parameters
    text : str, the text to analyze
    categories : list[str], the lexical categories to consider

    Returns
    dict[str, float], the analysis results (only the categories with non-zero values)
    """
    analysis = LEXICON.analyze(text, categories=categories, normalize=True)
    none_condition = not text or max(analysis.values()) == 0
    return None if none_condition else {k: v for k, v in analysis.items() if v != 0}

def map_topic_to_group(topic, groups):
    """
    Map a topic to a group of similar topics
    """
    for group, topics in groups.items():
        if topic in topics:
            return group
    return topic  

def get_empath_evolution(df, empath_column, period=None, year_column='release_date'):
    """
    Create a DataFrame to track the evolution of empath topics across years
    """
    empath_topics = set()
    for entry in df[empath_column]:
        empath_topics.update(entry.keys())

    empath_evolution = {topic: [] for topic in empath_topics}
    empath_evolution['year'] = []

    if period is not None:
        years = [y for y in sorted(df[year_column].unique()) if period[0] <= y <= period[1]]
    else:

        years = [y for y in sorted(df[year_column].unique()) if y <= 1991]

    for year in years:
        year_data = df[df['release_date'] == year][empath_column]
        aggregated = {topic: 0 for topic in empath_topics}
        count = len(year_data)

        for row in year_data:
            for topic, value in row.items():
                aggregated[topic] += value

        if count > 0:
            for topic in aggregated:
                aggregated[topic] /= count

        for topic, value in aggregated.items():
            empath_evolution[topic].append(value)

        empath_evolution['year'].append(year)

    return pd.DataFrame(empath_evolution)

def prepare_empath_data(df, empath_column, period=None, year_column='release_date', sqrt_scale=True):
    empath_evolution_df = get_empath_evolution(df, empath_column, period, year_column)

    # Melt the DataFrame to have a row for each year and topic
    empath_evolution_df = empath_evolution_df.melt(id_vars=['year'], var_name='topic', value_name='proportion')

    # group similar lexicon categories
    empath_evolution_df['topic'] = empath_evolution_df['topic'].apply(map_topic_to_group, groups=TOPIC_GROUPS)
    empath_evolution_df = empath_evolution_df.groupby(['year', 'topic'], as_index=False).agg({'proportion': 'sum'})

    # Apply square root scaling if wanted
    empath_evolution_df['proportion'] = np.sqrt(empath_evolution_df['proportion']) if sqrt_scale else empath_evolution_df

    # set topic color palette
    unique_topics = empath_evolution_df['topic'].unique()
    topic_colors = {topic: px.colors.qualitative.Plotly[i] for i, topic in enumerate(unique_topics)}

    return empath_evolution_df, topic_colors
