from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px

df = pd.read_csv('./data/station_salvador.csv')

app = Dash(__name__)

app.layout = html.Div([
    html.Div(children='Teste com Salvador'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Graph(figure=px.line(df, x='YEAR', y='SEP'))
])

if __name__ == '__main__':
    app.run(debug=True)
