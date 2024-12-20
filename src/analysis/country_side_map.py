import pandas as pd
from src.utils.helpers import convert_csv
from ipyleaflet import Map, GeoJSON, Popup, TileLayer, WidgetControl
import requests
from src.utils.constants import *
import ipywidgets as widgets
from ipywidgets import HTML
import json
from src.analysis.intro import compute_side_movie_count_per_country
from src.analysis.country_side_map import *

# Create popup content
def create_popup_content(properties):
    return f"""
    <b>{properties['name']}</b><br>
    Western: {properties['Western']}<br>
    Eastern: {properties['Eastern']}<br>
    None: {properties['None']}
    """

# Function to get a origin point of country
def get_point(geometry):
    if geometry['type'] == 'Polygon':
        return geometry['coordinates'][0][0]
    elif geometry['type'] == 'MultiPolygon':
        return geometry['coordinates'][0][0][0]
    return None

def display_country_side_map(df):
    # Load GeoJSON data for countries
    url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    response = requests.get(url)
    geo_json_data = response.json()

    num_colors = len(COLOR_SCALE)

    # Filter GeoJSON data with represented countries and calculate ratio
    filtered_features = []
    for feature in geo_json_data['features']:
        country_name = feature['properties']['name']
        
        if country_name in df['Country'].values:
            # Get counts for current country
            counts = df[df['Country'] == country_name]
            western_count = int(counts['Western'].values[0])
            eastern_count = int(counts['Eastern'].values[0])
            none_count = int(counts['None'].values[0])
            
            # Determine color
            if (western_count == 0 and eastern_count == 0) or western_count + eastern_count + none_count < 10:
                color = 'rgb(255,255,255)'  # Bright white for no films            
            else:
                total = western_count + eastern_count
                ratio = western_count / total
                color_index = min(int(ratio * num_colors), num_colors - 1)
                color = COLOR_SCALE[color_index]  # Extract the color string from the tuple
            
            # Update feature properties
            feature['properties']['Western'] = western_count
            feature['properties']['Eastern'] = eastern_count
            feature['properties']['None'] = none_count
            feature['properties']['color'] = color
            
            # Add feature
            filtered_features.append(feature)
            
    # Update GeoJSON data
    geo_json_data['features'] = filtered_features

    # Create a map
    center = (20, 0)
    m_side = Map(center=center, zoom=2)

    # Add OpenStreetMap tiles
    osm_layer = TileLayer(url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png")
    m_side.add_layer(osm_layer)

    # Add layer with click event
    geo_json_layer = GeoJSON(
        data=geo_json_data,
        style_callback=lambda feature: {
            'color': feature['properties']['color'],
            'opacity': 1,
            'weight': 1.9,
            'fillOpacity': 0.5
        },
        hover_style={'fillOpacity': 0.3}
    )

    def on_click(event, feature, **kwargs):
        coordinates = get_point(feature['geometry'])
        if coordinates:
            popup_content = create_popup_content(feature['properties'])
            popup = Popup(location=coordinates[::-1], child=widgets.HTML(value=popup_content), close_button=False)
            m_side.add_layer(popup)

    geo_json_layer.on_click(on_click)
    m_side.add_layer(geo_json_layer)

    # Legend of map
    legend_html = """
    <div style="background: white; padding: 5px; border: 1px solid black; border-radius: 3px; font-size: 10px; line-height: 1;">
        <div style="font-weight: bold; text-align: center; margin-bottom: 3px;">Ratio of East. vs. West.-Oriented Films</div>
    """

    legend_labels = [
        "Strongly East.-Orient.",
        "Moderately East.-Orient.",
        "Slightly Eastern-Orient.",
        "Balanced",
        "Slightly West.-Orient.",
        "Moderately West.-Orient.",
        "Strongly West.-Orient."
    ]

    for i, color in enumerate(COLOR_SCALE):
        legend_html += f"""
        <div style="display: flex; align-items: center; margin-bottom: 2px;">
            <div style="width: 12px; height: 12px; background: {color}; border: 1px solid black; margin-right: 2px;"></div>
            <span style="margin: 0; padding: 0;">{legend_labels[i]}</span>
        </div>
        """

    legend_html += """
    </div>
    """

    # Legend widget
    legend_widget = HTML(value=legend_html)
    legend_control = WidgetControl(widget=legend_widget, position='bottomright')
    m_side.add_control(legend_control)

    display(m_side)

    # Save the GeoJSON data to a file
    with open(WEB_EXPORT_FOLDER + "map_country_side.json", "w") as f:
        json.dump(geo_json_data, f)