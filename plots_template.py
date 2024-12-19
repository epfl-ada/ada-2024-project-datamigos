import plotly.io as pio
from src.constants import *

# Custom template
datamigos_template = {
    "layout": {
        "font": {
            "family": "Helvetica Neue"
        },
        "plot_bgcolor": "#F2F2F2",   # NEUTRAL-4 background color
        "colorway": DISTINCT_COLORS,
    },
    "data": {
        "heatmap": [{
            "colorscale": [[i / 6, color] for i, color in enumerate(COLOR_SCALE)]
        }],
        "choropleth": [{
            "colorscale": [[i / 6, color] for i, color in enumerate(COLOR_SCALE)]
        }]
    }
}

pio.templates["datamigos_template"] = datamigos_template
pio.templates.default = "datamigos_template"
