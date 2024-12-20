import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from src.utils.constants import *

COLD_WAR_PERIODS = {
    'Blocs Establishment': (1947, 1953),
    'Major tensions and crises': (1954, 1962),
    'Détente': (1963, 1974),
    'Second Cold War': (1975, 1984),
    'End of the Cold War': (1985, 1991)
}

def plot_eastern_western_archetypes_distrib(east_df, west_df, east_colors, west_colors):
    eastern_movie_eastern_char = east_df[east_df["movie_side"] == 'Eastern']
    western_movie_eastern_char = east_df[east_df["movie_side"] == 'Western']

    eastern_movie_western_char = west_df[west_df["movie_side"] == 'Eastern']
    western_movie_western_char = west_df[west_df["movie_side"] == 'Western']

    # Combine all counts into a single DataFrame
    eastern_archetypes_counts = pd.DataFrame({
        'Eastern Movie': eastern_movie_eastern_char['archetype'].value_counts(),
        'Western Movie': western_movie_eastern_char['archetype'].value_counts()
    }).T

    western_archetypes_counts = pd.DataFrame({
        'Eastern Movie': eastern_movie_western_char['archetype'].value_counts(),
        'Western Movie': western_movie_western_char['archetype'].value_counts()
    }).T

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=["Eastern Characters", "Western Characters"]
    )

    for topic in eastern_archetypes_counts.columns:
        fig.add_trace(go.Bar(
            x=eastern_archetypes_counts.index,
            y=eastern_archetypes_counts[topic],
            name=f"{topic}",
            marker_color=east_colors[topic],
            customdata=eastern_archetypes_counts.index.map(lambda x: topic),
            hovertemplate='Archetype: <b>%{customdata}</b><br>Representatives count: <b>%{y}</b><extra></extra>'
        ), row=1, col=1)

    for topic in western_archetypes_counts.columns:
        fig.add_trace(go.Bar(
            x=western_archetypes_counts.index,
            y=western_archetypes_counts[topic],
            name=f"{topic}",
            marker_color=west_colors[topic],
            customdata=western_archetypes_counts.index.map(lambda x: topic),
            hovertemplate='Archetype: <b>%{customdata}</b><br>Representatives count: <b>%{y}</b><extra></extra>'
        ), row=1, col=2)

    fig.update_layout(
        barmode='stack',
        title_text='Distribution of Eastern and Western Characters Archetypes',
        xaxis_title='Movie Side',
        yaxis_title='Number of Characters',
        legend_title='Dominant Topics',
        height=500, width=1200 
    )

    fig.update_xaxes(title_text="Movie Side", row=1, col=1)
    fig.update_yaxes(title_text="Number of Characters", row=1, col=1)

    fig.update_xaxes(title_text="Movie Side", row=1, col=2)
    fig.update_yaxes(title_text="Number of Characters", row=1, col=2)

    fig.show()
    return fig

def plot_term_frequencies(etf_by_topic, otf_by_topic, colors, topic_dict):
    for topic_id, word_frequencies in etf_by_topic.items():
        words = list(word_frequencies.keys())
        etf_values = np.sqrt(list(word_frequencies.values()))
        otf_values = [np.sqrt(otf_by_topic[word]) for word in words]

        sorted_indices = np.argsort(etf_values)
        words = [words[i] for i in sorted_indices]
        etf_values = [etf_values[i] for i in sorted_indices]
        otf_values = [otf_values[i] for i in sorted_indices]

        fig = go.Figure()

        fig.add_trace(go.Bar(
            y=words,
            x=otf_values,
            orientation='h',
            name='Overall Term Frequency (OTF)',
            marker=dict(color=colors[1], opacity=0.7),
            hovertemplate='Word: <b>%{y}</b><br>sqrt(OTF) = <b>%{x}</b><extra></extra>',
            width=0.55
        ))

        fig.add_trace(go.Bar(
            y=words,
            x=etf_values,
            orientation='h',
            name='Estimated Term Frequency within the topic (ETF)',
            marker=dict(color=colors[0]),
            hovertemplate='Word: <b>%{y}</b><br>sqrt(ETF) = <b>%{x}</b><extra></extra>',
            width=0.55
        ))

        fig.update_layout(
            title=f'Term Frequencies for archetype of {topic_dict[topic_id].lower()}',
            xaxis_title='Frequency (sqrt scale)',
            yaxis_title='Words',
            barmode='overlay',
            legend=dict(
                x=0.95, 
                y=0.2,  
                xanchor='right',
                yanchor='top',
                ),
            height=500,  
            width=1000,  
            margin=dict(l=30, r=30, t=50, b=50) 
        )
        fig.write_html(WEB_EXPORT_FOLDER + f"term_ferquencies_{topic_dict[topic_id].lower()}.html", full_html=True, include_plotlyjs='cdn', config={'responsive': True})
        fig.show()

def plot_empath_evolution(empath_df, topic_colors, title_end='Across Years'):
    fig = go.Figure()
    # Map colors
    empath_df['color'] = empath_df['topic'].map(topic_colors)

    fig = px.line(
        empath_df,
        x='year',
        y='proportion',
        color='topic',
        color_discrete_map=topic_colors
    )
    
    fig.update_layout(
        width = 900,
        height = 500,
        xaxis_title="Movie Release Year",
        yaxis_title="Frequency of a Category",
        legend_title="Categories",
        title={
            "text": f"Changing Themes in Character Representation {title_end}",
            "x": 0.43,
            "xanchor": "center",
            "font": {"size": 20, "family": "Arial", "weight": "bold"}
        },
        margin=dict(l=50, r=50, t=50, b=50)
    )
    fig.show()
    return fig

def plot_empath_distrib_by_year(empath_df, topic_colors, year):
    fig = go.Figure()
    grouped_year_data = empath_df[empath_df['year'] == year].groupby('topic', as_index=False).agg({'proportion': 'sum'})

    fig.add_trace(go.Bar(
        x=grouped_year_data['topic'],
        y=grouped_year_data['proportion'],
        name=f"Year {year}",
        marker=dict(color=[topic_colors[topic] for topic in grouped_year_data['topic']])
    ))
    
    fig.update_layout(
        title={
            "text": f"Characters' Empath Features Distribution for Year {year}",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20, "family": "Arial", "weight": "bold"}
        },
        xaxis_title="Empath Topics", 
        yaxis_title="Proportion",
        legend_title="Year",
        barmode="group", 
        width = 800, height=400
    )

    fig.update_xaxes(tickfont=dict(size=9.5))
    fig.show()
    return fig

def assign_period(row, periods=COLD_WAR_PERIODS):
    for period, (start, end) in periods.items():
        if start <= row['release_date'] <= end:
            return period
    return 'Unknown'
    
def plot_nb_characters_per_side_per_period(character_df, periods=COLD_WAR_PERIODS):
    character_df['period'] = character_df.apply(assign_period, axis=1)
    
    char_count = \
        character_df.groupby(['period', 'release_date', 'character_side']).size().reset_index(name='char_count')
    char_count = char_count[char_count['period'] != 'Unknown']

    # Filter data for Eastern and Western separately
    eastern_char_count = char_count[char_count['character_side'] == 'Eastern']
    western_char_count = char_count[char_count['character_side'] == 'Western']

    fig = go.Figure()

    fig.add_trace(go.Box(
        y=eastern_char_count['char_count'],
        x=eastern_char_count['period'],
        name='Eastern',
        marker_color='#DD3C32'
    ))

    fig.add_trace(go.Box(
        y=western_char_count['char_count'],
        x=western_char_count['period'],
        name='Western',
        marker_color='#0F89E6'
    ))

    fig.update_layout(
        title='Number of Characters Representing Each Side for Different Cold War Periods',
        legend_title='Character Side',
        xaxis=dict(
            title='Period',
            categoryorder='array',  # Fix the category order for x-axis
            categoryarray=list(COLD_WAR_PERIODS.keys()), 
            tickfont=dict(size=10)
        ),
        yaxis_title='Number of Characters',
        boxmode='group',
        boxgap=0.4,
        height=500, width=900
    )

    fig.show()