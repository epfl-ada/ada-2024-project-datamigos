import plotly.io as pio
from src.utils.constants import *

# Custom template
datamigos_template = {
    "layout": {
        "font": {
            "family": "Helvetica Neue"
        },
        "plot_bgcolor": "rgba(0,0,0,0)",   # NEUTRAL-4 background color
        "paper_bgcolor": "rgba(0,0,0,0)",  # NEUTRAL-4 background color
        "colorway": DISTINCT_COLORS,
        "xaxis": {
            "title": {
                "font": {
                    "color": "#333333"
                }
            },
            "tickfont": {
                "color": "#333333"
            }
        },
        "yaxis": {
            "title": {
                "font": {
                    "color": "#333333"
                }
            },
            "tickfont": {
                "color": "#333333"
            }
        },
        "title": {
            "font": {
                "color": "#333333"
            }
        }
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
