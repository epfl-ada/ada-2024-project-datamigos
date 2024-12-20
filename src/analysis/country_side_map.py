import pandas as pd
from src.utils.helpers import convert_csv
from ipyleaflet import Map, GeoJSON, Popup, TileLayer, WidgetControl
import requests
from src.utils.constants import *
import ipywidgets as widgets
from ipywidgets import HTML
import json
from analysis.intro import compute_side_movie_count_per_country

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
