import pandas as pd
from collections import Counter
from src.utils.constants import *
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from src.analysis.intro import *
from ipyleaflet import Map, TileLayer, GeoJSON, Popup, WidgetControl
from ipywidgets import HTML
import requests
import json

def compute_side_movie_count_per_country(df):
    # Initialize and assign counters
    western_counter = Counter()
    eastern_counter = Counter()
    none_counter = Counter()

    for index, row in df.iterrows():
        countries = row['countries']
        cold_war_side = row['cold_war_side']
        
        for country in countries:
            if cold_war_side == 'Western':
                western_counter[country] += 1
            elif cold_war_side == 'Eastern':
                eastern_counter[country] += 1
            else:
                none_counter[country] += 1

    # Convert to DataFrames
    western_df = pd.DataFrame.from_dict(western_counter, orient='index', columns=['Western']).reset_index()
    eastern_df = pd.DataFrame.from_dict(eastern_counter, orient='index', columns=['Eastern']).reset_index()
    none_df = pd.DataFrame.from_dict(none_counter, orient='index', columns=['None']).reset_index()

    # Merge DataFrames
    country_counts_df = pd.DataFrame.from_dict(Counter([country for sublist in df['countries'] for country in sublist]), orient='index', columns=['Occurrences']).reset_index()
    country_counts_df = country_counts_df.rename(columns={'index': 'Country'})

    country_counts_df = country_counts_df.merge(western_df, how='left', left_on='Country', right_on='index').drop(columns=['index'])
    country_counts_df = country_counts_df.merge(eastern_df, how='left', left_on='Country', right_on='index').drop(columns=['index'])
    country_counts_df = country_counts_df.merge(none_df, how='left', left_on='Country', right_on='index').drop(columns=['index'])

    # Fill NaN values with 0
    country_counts_df = country_counts_df.fillna(0)
    country_counts_df[['Western', 'Eastern', 'None']] = country_counts_df[['Western', 'Eastern', 'None']].astype(int)

    return country_counts_df

def plot_movies_distrib(df):
    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'pie'}, {'type': 'pie'}]], subplot_titles=("Including neutral movies", "Excluding neutral movies"))

    # prepare data for the pie chart
    global_movies_side_count = df['cold_war_side'].value_counts().reset_index()
    global_movies_side_count.columns = ['side', 'count']

    cw_movies_side_count = df[df['cold_war_side'] != 'None']
    cw_movies_side_count = cw_movies_side_count['cold_war_side'].value_counts().reset_index()
    cw_movies_side_count.columns = ['side', 'count']

    # Define colors for the pie chart slices
    colors = {'None': COLOR_SCALE[3], 'Western': COLOR_SCALE[6], 'Eastern': COLOR_SCALE[0]}

    fig.add_trace(go.Pie(labels=global_movies_side_count['side'],
                        values=global_movies_side_count['count'],
                        marker=dict(colors=[colors[side] for side in global_movies_side_count['side']]),
                        hovertemplate='<b>%{label}</b><br>Count: %{value}<br><extra></extra>',
                        name='Side'), row=1, col=1)

    fig.add_trace(go.Pie(labels=cw_movies_side_count['side'],
                        values=cw_movies_side_count['count'],
                        marker=dict(colors=[colors[side] for side in cw_movies_side_count['side']]),
                        hovertemplate='<b>%{label}</b><br>Count: %{value}<br><extra></extra>',
                        name='Side'), row=1, col=2)

    # Adjust the domain of the pie charts to add space between the charts and the titles
    fig.update_traces(domain=dict(x=[0, 0.45], y=[0, 0.95]), row=1, col=1)
    fig.update_traces(domain=dict(x=[0.55, 1], y=[0, 0.95]), row=1, col=2)

    fig.update_layout(title_text="Movies Distribution based on Cold War Side", title_x=0.5, title_font_weight='bold', plot_bgcolor="#F2F2F2")
    fig.write_html(WEB_EXPORT_FOLDER + "movies_distrib.html")
    fig.show()

def plot_movies_distrib_by_year(df):
    year_counts = df.groupby("release_date").size()
    fig = go.Figure(data=[go.Bar(x=year_counts.index, 
                                y=year_counts.values, 
                                width=0.55, 
                                marker_color=COLOR_SCALE[5], 
                                hovertemplate="Year: %{x}<br>No. of movies: %{y}<extra></extra>")])

    fig.update_layout(title="Number of movies by year", xaxis_title="Year", yaxis_title="Number of movies", plot_bgcolor="#F2F2F2")

    fig.update_xaxes(tickangle=-45, tickvals=list(year_counts.index), tickfont=dict(size=8))

    # add some marker to show start of cold war and end of cold war
    fig.add_vline(x=1947, line_dash="dash", line_color=COLOR_SCALE[1])
    fig.add_vline(x=1991, line_dash="dash", line_color=COLOR_SCALE[1])


    fig.add_annotation(
        x=1947, y = 600,
        text="Start of Cold War",
        font=dict(color=COLOR_SCALE[1], size=12),
        showarrow=False,
        yanchor='middle',
        xshift=10, yshift=10,
        textangle=-90  
    )

    fig.add_annotation(
        x=1991, y = 600,
        text="End of Cold War",
        font=dict(color=COLOR_SCALE[1], size=12),
        showarrow=False,
        yanchor='middle',
        xshift=10, yshift=10,
        textangle=-90 
    )

    fig.write_html(WEB_EXPORT_FOLDER + "nb_movies_by_year.html")
    fig.show()

def plot_evol_nb_movies(df):
    year_counts = df.groupby("release_date").size()
    movie_side_count = df.groupby(["release_date", "cold_war_side"]).size().unstack()

    fig = go.Figure()

    COLOR_DICT = {
        "Eastern": COLOR_SCALE[0],
        "Western": COLOR_SCALE[6],
        "None": COLOR_SCALE[3]
    }

    for side in movie_side_count.columns:
        fig.add_trace(go.Line(x=movie_side_count.index, 
                                y=movie_side_count[side], 
                                mode="lines", 
                                name=side, 
                                line=dict(width=2, color=COLOR_DICT[side]),
                                hovertemplate="Year: %{x}<br>No. of movies: %{y}<extra></extra>"))
        
    fig.update_layout(title="Evolution of the number of movies per side by year", xaxis_title="Year", yaxis_title="Number of movies", plot_bgcolor="#F2F2F2")
    fig.update_xaxes(tickangle=-45, tickvals=list(year_counts.index), tickfont=dict(size=8))

    # add some marker to show start of cold war and end of cold war
    fig.add_vline(x=1947, line_dash="dash", line_color="black", annotation_text="Start of Cold War")
    fig.add_vline(x=1991, line_dash="dash", line_color="black", annotation_text="End of Cold War")

    fig.write_html(WEB_EXPORT_FOLDER + "evol_nb_movies.html")
    fig.show()

# Function to get a origin point of country
def get_point(geometry):
    if geometry['type'] == 'Polygon':
        return geometry['coordinates'][0][0]
    elif geometry['type'] == 'MultiPolygon':
        return geometry['coordinates'][0][0][0]
    return None

# Linear greyscale color with ratio (0 - 2000 range)
def get_linear_greyscale_color(total):
    if total == 0:
        return 'rgb(255,255,255)'  # White for 0 occurrences
    elif total > 2000:
        return 'rgb(0,0,0)'  # Black for >2000 films
    else:
        grey_value = 255 - int((total / 2000) * 255)
        return f'rgb({grey_value},{grey_value},{grey_value})' # Greyscale

# Create popup content
def create_popup_content(properties):
    return f"""
    <b>{properties['name']}</b><br>
    Number of Films: {properties['Total']}
    """

def display_map_film_nb(df):
    # Load GeoJSON data for countries
    url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    response = requests.get(url)
    geo_json_data = response.json()

    # Calculate the maximum number of films for normalization (we use 2000 as the threshold)
    filtered_features = []
    for feature in geo_json_data['features']:
        country_name = feature['properties']['name']
        
        if country_name in df['Country'].values:
            # Get the number of occurrences for the current country
            counts = df[df['Country'] == country_name]
            total_count = int(counts['Occurrences'].values[0])
            
            # Set color with scale
            color = get_linear_greyscale_color(total_count)
            
            # Update feature properties
            feature['properties']['Total'] = total_count
            feature['properties']['color'] = color
            filtered_features.append(feature)

    # Update GeoJSON data
    geo_json_data['features'] = filtered_features

    # Create a map
    center = (20, 0)
    m_nb = Map(center=center, zoom=2)

    # Add OpenStreetMap tiles
    osm_layer = TileLayer(url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png")
    m_nb.add_layer(osm_layer)

    # Add layer with click event
    geo_json_layer = GeoJSON(
        data=geo_json_data,
        style_callback=lambda feature: {
            'color': feature['properties']['color'],
            'opacity': 1,
            'weight': 1.5,
            'fillOpacity': 0.7
        },
        hover_style={'fillOpacity': 0.3}
    )

    # Popup handling
    def on_click(event, feature, map, **kwargs):
        coordinates = get_point(feature['geometry'])
        if coordinates:
            popup_content = create_popup_content(feature['properties'])
            popup = Popup(location=coordinates[::-1], child=HTML(value=popup_content), close_button=False)
            m_nb.add_layer(popup)

    geo_json_layer.on_click(on_click)
    m_nb.add_layer(geo_json_layer)

    # Legend of map
    legend_html = """
    <div style="background: white; padding: 5px; border: 1px solid black; border-radius: 3px; font-size: 10px; line-height: 1;">
        <div style="font-weight: bold; text-align: center; margin-bottom: 3px;">Number of Films</div>
    """

    legend_colors = [
        ('rgb(255,255,255)', '0'),
        ('rgb(204,204,204)', ''),
        ('rgb(153,153,153)', '1000'),
        ('rgb(102,102,102)', ''),
        ('rgb(51,51,51)', '2000'),
        ('rgb(0,0,0)', '> 2000')
    ]

    for color, label in legend_colors:
        legend_html += f"""
        <div style="display: flex; align-items: center; margin-bottom: 2px;">
            <div style="width: 12px; height: 12px; background: {color}; border: 1px solid black; margin-right: 2px;"></div>
            <span style="margin: 0; padding: 0;">{label}</span>
        </div>
        """

    legend_html += """
    </div>
    """

    # Legend widget
    legend_widget = HTML(value=legend_html)
    legend_control = WidgetControl(widget=legend_widget, position='bottomright')
    m_nb.add_control(legend_control)

    display(m_nb)

    # Save the GeoJSON data for the second map to a file
    with open(WEB_EXPORT_FOLDER + "map_films_nb.json", "w") as f:
        json.dump(geo_json_data, f)