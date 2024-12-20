import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from src.utils.constants import *

def compute_lang_distribution(df):
    languages_exploded = df.explode('languages')
    languages_count = languages_exploded['languages'].value_counts().reset_index()
    languages_count.columns = ['language', 'count']
    languages_count = languages_count.sort_values(by='count', ascending=False)

    western_movies = df[df['cold_war_side'] == 'Western']
    western_languages = western_movies.explode('languages')
    western_languages = western_languages[western_languages['languages'] != '']
    western_languages_count = western_languages['languages'].value_counts().reset_index()
    western_languages_count.columns = ['language', 'count']

    eastern_movies = df[df['cold_war_side'] == 'Eastern']
    eastern_languages = eastern_movies.explode('languages')
    eastern_languages = eastern_languages[eastern_languages['languages'] != '']
    eastern_languages = eastern_languages[eastern_languages['languages'] != '??????']
    eastern_languages_count = eastern_languages['languages'].value_counts().reset_index()
    eastern_languages_count.columns = ['language', 'count']

    return languages_count, western_languages_count, eastern_languages_count

def plot_top_languages(df, nb):
    languages_count, _, _ = compute_lang_distribution(df)

    fig = px.bar(languages_count.head(nb), x='language', y='count', labels={'language':'Language', 'count':'Number of Movies'})
    fig.update_yaxes(type="log")
    fig.update_xaxes(tickangle=45)
    fig.update_layout(title_text=f"Top {nb} Languages in Movies", title_x=0.5, title_font_weight='bold', plot_bgcolor="#F2F2F2")
    fig.update_traces(marker_color=NEUTRAL_COLORS[1])

    fig.write_html(WEB_EXPORT_FOLDER + "top_languages.html", full_html=True, include_plotlyjs='cdn', config={'responsive': True})
    fig.show()

def plot_top_lang_per_side(df, nb):
    _, western_languages_count, eastern_languages_count = compute_lang_distribution(df) 

    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'bar'}, {'type': 'bar'}]], subplot_titles=("in Western Bloc Movies", "in Eastern Bloc Movies"))
    fig.add_trace(go.Bar(x=western_languages_count['language'].head(nb), 
                        y=western_languages_count['count'],
                        hovertemplate='%{x}: %{y}<extra></extra>', 
                        marker_color=COLOR_SCALE[6]), row=1, col=1)

    fig.add_trace(go.Bar(x=eastern_languages_count['language'].head(nb),
                        y=eastern_languages_count['count'],
                        hovertemplate='%{x}: %{y}<extra></extra>',
                        marker_color=COLOR_SCALE[0]), row=1, col=2)

    # add log scale to y-axis
    fig.update_yaxes(type="log", row=1, col=1)
    fig.update_yaxes(type="log", row=1, col=2)
    fig.update_xaxes(tickangle=45)
    # add x-axis and y-axis labels (set a common label for both subplots)

    fig.update_xaxes(title_text="Language")
    fig.update_yaxes(title_text="Number of Movies")


    fig.update_layout(title_text=f"Top {nb} Languages", title_x=0.5, title_font_weight='bold', showlegend=False, plot_bgcolor="#F2F2F2")
    # Update the layout for better visualization
    fig.update_layout(
        title_text=f"Top {nb} Languages",
        title_x=0.5,
        title_font_weight='bold', 
        showlegend=False,
        xaxis=dict(title_text='Language'),
        xaxis2=dict(title_text='Language'),
        yaxis=dict(title_text='Number of Movies'),
        yaxis2=dict(title_text='Number of Movies')
    )

    fig.write_html(WEB_EXPORT_FOLDER + "top_languages_per_side.html", full_html=True, include_plotlyjs='cdn', config={'responsive': True})
    fig.show()

def plot_top_lang_side(df, nb, side):
    assert(side == 'Western' or side == 'Eastern')
    _, western_languages_count, eastern_languages_count = compute_lang_distribution(df) 

    if side == 'Western':
        fig = px.bar(western_languages_count.head(nb), x='language', y='count', labels={'language':'Language', 'count':'Number of Movies (log scale)'})
        fig.update_traces(marker_color=COLOR_SCALE[6])
    else:
        fig = px.bar(eastern_languages_count.head(nb), x='language', y='count', labels={'language':'Language', 'count':'Number of Movies (log scale)'})
        fig.update_traces(marker_color=COLOR_SCALE[0])

    fig.update_layout(title_text=f"Top {nb} Languages in {side} Bloc Movies", title_x=0.5, title_font_weight='bold', width=800, plot_bgcolor="#F2F2F2")
    fig.update_yaxes(type="log")
    fig.write_html(WEB_EXPORT_FOLDER + f"top_{side}_languages.html", full_html=True, include_plotlyjs='cdn', config={'responsive': True})
    fig.show()

def plot_top_lang_both_sides(df, nb):
    _, western_languages_count, eastern_languages_count = compute_lang_distribution(df) 

    fig = go.Figure()
    fig.add_trace(go.Bar(x=western_languages_count['language'].head(nb), 
                        y=western_languages_count['count'], 
                        name='Western Bloc Movies',
                        hovertemplate='%{x}: %{y}<extra></extra>',
                        marker_color=COLOR_SCALE[6]))

    fig.add_trace(go.Bar(x=eastern_languages_count['language'].head(nb),
                        y=eastern_languages_count['count'],
                        name='Eastern Bloc Movies',
                        hovertemplate='%{x}: %{y}<extra></extra>',
                        marker_color=COLOR_SCALE[0]))

    fig.update_layout(
        title_text=f"Top {nb} Languages in Western and Eastern Bloc Movies", 
        title_x=0.5, 
        title_font_weight='bold',
        xaxis=dict(title_text='Language'),
        yaxis=dict(title_text='Number of Movies (log scale)'), 
        barmode='group',
        width=950,
        plot_bgcolor="#F2F2F2")

    fig.update_xaxes(tickangle=45)
    fig.update_yaxes(type="log")
    fig.write_html(WEB_EXPORT_FOLDER + "top_east_and_west_lang.html", full_html=True, include_plotlyjs='cdn', config={'responsive': True})
    fig.show()
