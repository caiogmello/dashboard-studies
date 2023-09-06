from dash import Dash, html, dcc, callback, Output, Input
import dash
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px


app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    
    dcc.Link(f"{dash.page_registry['pages.compare']['name']}", href=dash.page_registry['pages.compare']['path']),
    html.Br(),
    dcc.Link(f"{dash.page_registry['pages.home']['name']}", href=dash.page_registry['pages.home']['path']),
    
    dash.page_container 
])

if __name__ == '__main__':
    app.run(debug=True)
