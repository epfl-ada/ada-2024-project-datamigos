from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import networkx as nx
import pandas as pd
import numpy as np
from collections import Counter
from itertools import combinations
from src.utils.helpers import convert_csv, assign_side
from utils.constants import DATA_FOLDER_PREPROCESSED

movies = pd.read_csv(DATA_FOLDER_PREPROCESSED + "preprocessed_movies.csv")
convert_csv(movies)

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Interactive Film Production Collaboration Network"),
    dcc.Graph(id='network-graph'),
    
    
    html.Label("Minimum Films Produced"),
    dcc.Slider(
        id='min-films-slider',
        min=1,
        max=350,
        step=5,
        value=40,
        marks={i: str(i) for i in range(0, 351, 50)}
    ),
    
    html.Label("Minimum Collaborations"),
    dcc.Slider(
        id='min-collaborations-slider',
        min=1,
        max=100,
        step=1,
        value=10,
        marks={i: str(i) for i in range(0, 101, 10)}
    )
])


@app.callback(
    Output('network-graph', 'figure'),
    Input('min-films-slider', 'value'),
    Input('min-collaborations-slider', 'value')
)
def update_graph(min_films, min_collab):
    country_film_count = Counter()
    collaboration_count = Counter()

    for countries in movies['countries']:
        country_film_count.update(countries)
        for pair in combinations(countries, 2):
            collaboration_count[tuple(sorted(pair))] += 1

    # Filter by thresholds
    country_film_count = {k: v for k, v in country_film_count.items() if v > min_films}
    root_film_count = {country: np.sqrt(count) for country, count in country_film_count.items()}
    countries = list(root_film_count.keys())

    collaboration_count = {k: v for k, v in collaboration_count.items() if v > min_collab}
    collaboration_count = {k: v for k, v in collaboration_count.items() if k[0] in countries and k[1] in countries}

    country_cold_war_side = assign_side(movies, countries)

    # Create the graph
    G = nx.Graph()
    for country in countries:
        G.add_node(country, side=country_cold_war_side[country], size=root_film_count[country])
    for (c1, c2), count in collaboration_count.items():
        G.add_edge(c1, c2, weight=count)

    # Generate spring layout
    pos = nx.spring_layout(G, seed=42, weight="weight", k=6.0, iterations=100)

    # Prepare edge traces with varying colors, widths, and transparency
    edge_traces = []
    max_collaboration = max(collaboration_count.values())

    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        weight = edge[2]['weight']
        
        # Get the sides of the two nodes involved in the edge
        side_0 = G.nodes[edge[0]]['side']
        side_1 = G.nodes[edge[1]]['side']
        
        # Determine the edge color based on node sides
        if side_0 == side_1:
            if side_0 == 'Western':
                line_color = f'rgba(0, 0, 255, {(weight / max_collaboration) * 5})'  # Blue with transparency
            elif side_0 == 'Eastern':
                line_color = f'rgba(255, 0, 0, {(weight / max_collaboration) * 5})'  # Red with transparency
            else:
                line_color = f'rgba(169, 169, 169, 0.8)'  # Grey for 'None' side
        else:
            # If the nodes are from different sides
            line_color = f'rgba(169, 169, 169, 0.8)'  # Grey for different sides
            if 'Lack of data' in [side_0, side_1]:
                line_color = f'rgba(255, 255, 0, 0.8)'  # Yellow if either node has 'Lack of data'
        
        edge_trace = go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            line=dict(width=weight * 0.01, color=line_color),
            hoverinfo='none',
            mode='lines'
        )
        edge_traces.append(edge_trace)

    # Add all edge traces to the figure
    fig = go.Figure(data=edge_traces)

    # Prepare node traces (as before, unchanged)
    node_x, node_y, node_colors, node_sizes, hover_texts = [], [], [], [], []
    color_mapping = {'Western': 'blue', 'Eastern': 'red', 'None': 'grey', 'Lack of data': 'lightyellow'}

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_colors.append(color_mapping.get(G.nodes[node]['side'], 'black'))
        node_sizes.append(G.nodes[node]['size'] * 0.5)
        hover_texts.append(f"{node} : {round(G.nodes[node]['size']**2)}")

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        hovertext=hover_texts,
        marker=dict(
            size=node_sizes,
            color=node_colors,
            line=dict(width=1, color='black')
        )
    )

    # Add node trace to the figure
    fig.add_trace(node_trace)

    # Set the layout
    layout = go.Layout(
        showlegend=False,
        hovermode='closest',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False),
        plot_bgcolor='white'
    )

    # Update layout and display the figure
    fig.update_layout(layout)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
