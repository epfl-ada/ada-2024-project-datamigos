import plotly.io as pio
from src.constants import *

# Colors
color_scale_red_blue = [
    "#BD0032",  #Deep Red - East Side
    "#F7514B",  #Red
    "#FEB3A6",  #Light Red
    "#F2F2F2",  #Neutral Middle
    "#A0CBE8",  #Light Blue
    "#5C8DB8",  #Blue
    "#1C5EA9"   #Deep Blue - West Side
]

distinct_colors = [
    "#1F6B5D",
    "#06DD95",
    "#98E144",
    "#FFE989",
    "#F1AB79",
    "#4BAE9A",
    "#7FB112",
    "#F0FE41",
    "#FAC82B",
    "#F58634"
]

# Custom template
datamigos_template = {
    "layout": {
        "font": {
            "family": "Helvetica Neue"
        },
        "plot_bgcolor": "#F2F2F2",   # NEUTRAL-4 background color
        "colorway": distinct_colors,
    },
    "data": {
        "heatmap": [{
            "colorscale": [[i / 6, color] for i, color in enumerate(color_scale_red_blue)]
        }],
        "choropleth": [{
            "colorscale": [[i / 6, color] for i, color in enumerate(color_scale_red_blue)]
        }]
    }
}

pio.templates["datamigos_template"] = datamigos_template
pio.templates.default = "datamigos_template"
