import dash
import copy
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import networkx as nx
from src.utils.collab_viz_helpers import *
from src.utils.helpers import assign_side
from src.utils.constants import *


class StaticGraph:

    def __init__(self, movies_df, min_nb_movies=0, min_nb_collab=0, relevance_nb=10, relevance_diff=10, threshold=19):
        # Compute a dict where each movies is associated to the root of the number
        # of film it has produced, and the dict where each unique tuple of countries is associated
        # with the number of co-production they had
        self.countries, self.root_film_count, self.collaboration_count = compute_counts(movies_df, min_nb_movies, min_nb_collab)

        # Compute a dict of the countries associated to their Cold War Side
        self.country_cold_war_side = assign_side(movies_df, self.countries, relevance_nb, relevance_diff, threshold)

        # Create the graph
        self.graph = nx.Graph()
        for country in self.countries:
            self.graph.add_node(country, side=self.country_cold_war_side[country], size=self.root_film_count[country])
        for (c1, c2), count in self.collaboration_count.items():
            self.graph.add_edge(c1, c2, weight=count)

    def create_figure(self):
        # Will be usefull to adjust thickness and transparency
        max_collaboration = max(self.collaboration_count.values())

        # Generate spring layout
        pos = nx.spring_layout(self.graph, seed=42, weight="weight", k=10, iterations=100)

        # Prepare edge traces with varying colors, widths, and transparency
        edge_traces = []

        for edge in self.graph.edges(data=True):
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            weight = edge[2]['weight']
            
            # Get the Cold War Side of the two nodes involved in the edge
            side_0 = self.graph.nodes[edge[0]]['side']
            side_1 = self.graph.nodes[edge[1]]['side']
            
            # Determine the edge color based on the Cold War Sides
            if side_0 == side_1:
                if side_0 == 'Western':
                    line_color = f'rgba({COLOR_SCALE_RGB["Deep Blue"][0]}, {COLOR_SCALE_RGB["Deep Blue"][1]}, {COLOR_SCALE_RGB["Deep Blue"][2]}, {(weight / max_collaboration) * 5})'
                elif side_0 == 'Eastern':
                    line_color = f'rgba({COLOR_SCALE_RGB["Deep Red"][0]}, {COLOR_SCALE_RGB["Deep Red"][1]}, {COLOR_SCALE_RGB["Deep Red"][2]}, {(weight / max_collaboration) * 5})'
                else:
                    line_color = f'rgba({DISTINCT_COLORS_RGB["Black"][0]}, {DISTINCT_COLORS_RGB["Black"][1]}, {DISTINCT_COLORS_RGB["Black"][2]}, 1)'
            else:
                line_color = f'rgba({DISTINCT_COLORS_RGB["Black"][0]}, {DISTINCT_COLORS_RGB["Black"][1]}, {DISTINCT_COLORS_RGB["Black"][2]}, 1)'
            
            edge_trace = go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                line=dict(width=weight * 0.01, color=line_color),
                hoverinfo='none',
                mode='lines'
            )
            edge_traces.append(edge_trace)

        # Add all edge traces to the figure
        self.fig = go.Figure(data=edge_traces)

        # Prepare node traces
        node_x, node_y, node_colors, node_sizes, hover_texts = [], [], [], [], []

        for node in self.graph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_colors.append(COLOR_MAPPING.get(self.graph.nodes[node]['side']))
            node_sizes.append(self.graph.nodes[node]['size'] * 0.5)
            hover_texts.append(f"{node} : {round(self.graph.nodes[node]['size']**2)}")

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
        self.fig.add_trace(node_trace)

        # Instantiate the layout
        layout = go.Layout(
            showlegend=False,
            hovermode='closest',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False),
            plot_bgcolor="#F2F2F2"
        )

        # Set the layout
        self.fig.update_layout(layout)
        return copy.deepcopy(self.fig)
    
    def plot(self):
        if hasattr(self, 'fig'):
            return self.fig.show()
        else:
            raise("Error: The Figure have not been created yet.")
        
    def get_figure(self):
        if hasattr(self, 'fig'):
            return copy.deepcopy(self.fig)
        else:
            raise("Error: The Figure have not been created yet.")

    def get_countries(self):
        return copy.deepcopy(self.countries)
    
    def get_root_film_count(self):
        return copy.deepcopy(self.root_film_count)
    
    def get_collaboration_count(self):
        return copy.deepcopy(self.collaboration_count)
    
    def get_country_cold_war_side(self):
        return copy.deepcopy(self.country_cold_war_side)
    
    def get_nodes(self):
        return copy.deepcopy(self.graph.nodes)
    
    def get_edges(self):
        return copy.deepcopy(self.graph.edges)


class DynamicGraph:
    def __init__(self, movies_df):
        self.app = Dash(__name__)

        self.app.layout = html.Div([
        html.H1("Interactive Film Production Collaboration Network"),
        dcc.Graph(id='network-graph'),
        
        
        html.Label("Minimum Films Produced"),
        dcc.Slider(
            id='min-films-slider',
            min=1,
            max=350,
            step=5,
            value=1,
            marks={i: str(i) for i in range(0, 351, 50)}
        ),
        
        html.Label("Minimum Collaborations"),
        dcc.Slider(
            id='min-collaborations-slider',
            min=1,
            max=100,
            step=1,
            value=0,
            marks={i: str(i) for i in range(0, 101, 10)}
            )
        ])


        @self.app.callback(
            Output('network-graph', 'figure'),
            Input('min-films-slider', 'value'),
            Input('min-collaborations-slider', 'value')
        )
        def update_map(min_films, min_collab):
            graph = StaticGraph(movies_df, min_nb_movies=min_films, min_nb_collab=min_collab)
            return graph.create_figure()
        
    def get_app(self):
        return copy.deepcopy(self.app)
    
    def plot(self):
        return self.app.run(debug=True)


class StaticMap:

    def __init__(self, movies_df, min_nb_movies=0, min_nb_collab=0, relevance_nb=10, relevance_diff=10, threshold=19):
        # Compute a dict where each movies is associated to the root of the number
        # of film it has produced, and the dict where each unique tuple of countries is associated
        # with the number of co-production they had
        self.countries, self.root_film_count, self.collaboration_count = compute_counts(movies_df, min_nb_movies, min_nb_collab)

        # Compute a dict of the countries associated to their Cold War Side
        self.country_cold_war_side = assign_side(movies_df, self.countries, relevance_nb, relevance_diff, threshold)
        
        # Create the graph
        self.graph = nx.Graph()
        for country in self.countries:
            self.graph.add_node(country, side=self.country_cold_war_side[country], size=self.root_film_count[country])
        for (c1, c2), count in self.collaboration_count.items():
            self.graph.add_edge(c1, c2, weight=count)

    def get_countries(self):
        return self.countries
    
    def get_root_film_count(self):
        return self.root_film_count
    
    def get_collaboration_count(self):
        return self.collaboration_count
    
    def get_country_cold_war_side(self):
        return self.country_cold_war_side
    
    def get_nodes(self):
        return self.graph.nodes
    
    def get_edges(self):
        return self.graph.edges
    
    def create_figure(self):
        # Will be usefull to adjust thickness and transparency
        max_collaboration = max(self.collaboration_count.values())

        # Prepare edge traces with varying colors and widths
        edge_lat, edge_lon, edge_colors, edge_widths = [], [], [], []

        for (c1, c2), weight in self.collaboration_count.items():
            if c1 in COUNTRY_COORDS and c2 in COUNTRY_COORDS:
                # Coordinates for edges
                edge_lat.extend([COUNTRY_COORDS[c1][0], COUNTRY_COORDS[c2][0], None])
                edge_lon.extend([COUNTRY_COORDS[c1][1], COUNTRY_COORDS[c2][1], None])

                # Determine color based on the Cold War Side side
                if self.country_cold_war_side.get(c1) == 'Western' and self.country_cold_war_side.get(c2) == 'Western':
                    edge_colors.append(f'rgba({COLOR_SCALE_RGB["Deep Blue"][0]}, {COLOR_SCALE_RGB["Deep Blue"][1]}, {COLOR_SCALE_RGB["Deep Blue"][2]}, {(weight / max_collaboration) * 5})')
                elif self.country_cold_war_side.get(c1) == 'Eastern' and self.country_cold_war_side.get(c2) == 'Eastern':
                    edge_colors.append(f'rgba({COLOR_SCALE_RGB["Deep Red"][0]}, {COLOR_SCALE_RGB["Deep Red"][1]}, {COLOR_SCALE_RGB["Deep Red"][2]}, {(weight / max_collaboration) * 5})')
                else:
                    edge_colors.append(COLOR_MAPPING['None'])

                # Determine edge thickness
                edge_widths.append((weight / max_collaboration) * 5)

        self.fig = go.Figure()

        # Add all edge traces to the figure
        for i, (start_lat, start_lon, color, width) in enumerate(zip(edge_lat[::3], edge_lon[::3], edge_colors, edge_widths)):
            self.fig.add_trace(go.Scattergeo(
                locationmode='ISO-3',
                lat=[edge_lat[i*3], edge_lat[i*3+1], None],
                lon=[edge_lon[i*3], edge_lon[i*3+1], None],
                mode='lines',
                line=dict(width=width, color=color),
                hoverinfo='none'
            ))

        # Prepare node traces
        node_lat, node_lon, node_sizes, node_colors, hover_texts = [], [], [], [], []

        for node in self.graph.nodes():
            node_lat.append(COUNTRY_COORDS[node][0])
            node_lon.append(COUNTRY_COORDS[node][1])
            node_colors.append(COLOR_MAPPING.get(self.graph.nodes[node]['side']))
            node_sizes.append(self.graph.nodes[node]['size'] * 0.5)
            hover_texts.append(f"{node} : {round(self.graph.nodes[node]['size']**2)}")

        # Add node trace to the figure
        self.fig.add_trace(go.Scattergeo(
            locationmode='ISO-3',
            lat=node_lat,
            lon=node_lon,
            mode='markers',
            marker=dict(
                size=node_sizes,
                color=node_colors,
                line=dict(width=0.5, color='black')
            ),
            hoverinfo='text',
            hovertext=hover_texts
        ))

        # Set the layout
        self.fig.update_layout(
            showlegend=False,
            geo=dict(
                projection_type='natural earth',
                showland=True,
                landcolor="#F2F2F2",
                showcountries=True,
            )
        )

        return copy.deepcopy(self.fig)

    def plot(self):
        if hasattr(self, 'fig'):
            return self.fig.show()
        else:
            raise("Error: The Figure have not been created yet.")
        
    def get_figure(self):
        if hasattr(self, 'fig'):
            return copy.deepcopy(self.fig)
        else:
            raise("Error: The Figure have not been created yet.")

    def get_countries(self):
        return copy.deepcopy(self.countries)
    
    def get_root_film_count(self):
        return copy.deepcopy(self.root_film_count)
    
    def get_collaboration_count(self):
        return copy.deepcopy(self.collaboration_count)
    
    def get_country_cold_war_side(self):
        return copy.deepcopy(self.country_cold_war_side)
    
    def get_nodes(self):
        return copy.deepcopy(self.graph.nodes)
    
    def get_edges(self):
        return copy.deepcopy(self.graph.edges)
    

class DynamicMap:

    def __init__(self, movies_df):
        self.app = dash.Dash(__name__)

        self.app.layout = html.Div([
            html.H1('Film Production Collaboration Network'),
            
            html.Div([
                html.Label('Minimum Films Produced:'),
                dcc.Slider(
                    id='min-films-slider',
                    min=1,
                    max=350,
                    step=1,
                    value=1,
                    marks={i: str(i) for i in range(0, 351, 50)},
                ),
            ]),
            
            html.Div([
                html.Label('Minimum Collaboration Count:'),
                dcc.Slider(
                    id='min-collab-slider',
                    min=1,
                    max=100,
                    step=1,
                    value=0,
                    marks={i: str(i) for i in range(0, 101, 10)},
                ),
            ]),

            dcc.Graph(id='film-network-map'),
        ])

        @self.app.callback(
            dash.dependencies.Output('film-network-map', 'figure'),
            [
                dash.dependencies.Input('min-films-slider', 'value'),
                dash.dependencies.Input('min-collab-slider', 'value'),
            ]
        )
        def update_map(min_films, min_collab):
            map = StaticMap(movies_df, min_nb_movies=min_films, min_nb_collab=min_collab)
            return map.create_figure()
    
    def get_app(self):
        return copy.deepcopy(self.app)
    
    def plot(self):
        return self.app.run(debug=True)