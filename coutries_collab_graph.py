from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import networkx as nx
import pandas as pd
import numpy as np
from collections import Counter
from itertools import combinations
from src.utils.helpers import convert_csv, assign_side
from src.constants import DATA_FOLDER_PREPROCESSED

movies = pd.read_csv(DATA_FOLDER_PREPROCESSED + "preprocessed_movies.csv")
convert_csv(movies)

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Interactive Film Production Collaboration Network"),
    dcc.Graph(id='network-graph'),
    
    html.Label("Cold War Threshold (%)"),
    dcc.Slider(
        id='threshold-slider',
        min=0,
        max=50,
        step=1,
        value=19,
        marks={i: str(i) for i in range(5, 51, 5)}
    ),
    
    html.Label("Minimum Films Produced"),
    dcc.Slider(
        id='min-films-slider',
        min=1,
        max=2000,
        step=5,
        value=40,
        marks={i: str(i) for i in range(1, 2001, 50)}
    ),
    
    html.Label("Minimum Collaborations"),
    dcc.Slider(
        id='min-collaborations-slider',
        min=1,
        max=450,
        step=1,
        value=10,
        marks={i: str(i) for i in range(1, 451, 10)}
    )
])


@app.callback(
    Output('network-graph', 'figure'),
    Input('threshold-slider', 'value'),
    Input('min-films-slider', 'value'),
    Input('min-collaborations-slider', 'value')
)
def update_graph(threshold, min_films, min_collab):
    country_film_count = Counter()
    collaboration_count = Counter()
    for countries in movies['countries']:
        country_film_count.update(countries)
        for pair in combinations(countries, 2):
            collaboration_count[tuple(sorted(pair))] += 1

    country_film_count = {k: v for k, v in country_film_count.items() if v > min_films}
    root_film_count = {country: np.sqrt(count) for country, count in country_film_count.items()}
    countries = list(root_film_count.keys())
    
    collaboration_count = {k: v for k, v in collaboration_count.items() if v > min_collab}
    collaboration_count = {k: v for k, v in collaboration_count.items() if k[0] in countries and k[1] in countries}

    country_cold_war_side = assign_side(movies, countries, threshold=threshold)

    G = nx.Graph()
    for country in countries:
        G.add_node(country, side=country_cold_war_side[country], size=root_film_count[country])
    for (c1, c2), count in collaboration_count.items():
        G.add_edge(c1, c2, weight=count)

    pos = nx.spring_layout(G, seed=42, k=10, iterations=100)
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='black'),
        hoverinfo='none',
        mode='lines'
    )

    node_x, node_y, node_colors, node_sizes = [], [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        if G.nodes[node]['side'] == 'Western':
            node_colors.append('blue')
        elif G.nodes[node]['side'] == 'Eastern':
            node_colors.append('red')
        elif G.nodes[node]['side'] == 'Lack of data':
            node_colors.append('lightyellow')
        else:
            node_colors.append('grey')
        node_sizes.append(G.nodes[node]['size'] * 0.5)

    largest_nodes = sorted(G.nodes(data=True), key=lambda x: x[1]['size'], reverse=True)[:2]
    largest_node_names = {node[0] for node in largest_nodes}
    node_labels = [node if node in largest_node_names else "" for node in G.nodes()]

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_labels,
        textposition="top center",
        hoverinfo='text',
        hovertext=[node for node in G.nodes()],
        marker=dict(
            showscale=False,
            colorscale='YlGnBu',
            size=node_sizes,
            color=node_colors
        ),
        textfont=dict(
            family='Arial Black',
            size=11,
            color="black"
        )
    )

    layout = go.Layout(
        showlegend=False,
        hovermode='closest',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False),
        plot_bgcolor='white'
    )

    fig = go.Figure(data=[edge_trace, node_trace], layout=layout)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
