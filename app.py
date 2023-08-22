from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import numpy as np
import plotly.express as px

dict_cidades = {
    'Belem': './data/station_belem.csv',
    'Curitiba': './data/station_curitiba.csv',
    'Fortaleza': './data/station_fortaleza.csv',
    'Goiania': './data/station_goiania.csv',
    'Macapa': './data/station_macapa.csv',
    'Manaus': './data/station_manaus.csv',
    'Recife': './data/station_recife.csv',
    'Rio de Janeiro': './data/station_rio.csv',
    'Salvador': './data/station_salvador.csv',
    'São Paulo': './data/station_sao_paulo.csv',
    'São Luiz': './data/station_sao_luiz.csv',
    'Vitoria': './data/station_vitoria.csv'
}


df = pd.read_csv(dict_cidades['Salvador'])
df = df.replace(999.90, np.nan)

app = Dash(__name__)

app.layout = html.Div([
    html.Div(className='row', children=[
    dcc.RadioItems(
        options=['Belem',
                 'Curitiba',
                 'Fortaleza',
                 'Goiania',
                 'Macapa',
                 'Manaus',
                 'Recife',
                 'Rio de Janeiro',
                 'Salvador',
                 'São Paulo',
                 'São Luiz',
                 'Vitoria'],
        value='Salvador',
        inline=True,
        id='city-radio')
    ]),
    html.H1(children=f'Temperatura de Cidades Brasileiras durante os anos'),
    
    html.Div(className='row', children=[
        dcc.Dropdown(options=[{'label': 'Janeiro', 'value': 'JAN'},
                    {'label': 'Fevereiro', 'value': 'FEB'},
                    {'label': 'Março', 'value': 'MAR'},
                    {'label': 'Abril', 'value': 'APR'},
                    {'label': 'Maio', 'value': 'MAY'},
                    {'label': 'Junho', 'value': 'JUN'},
                    {'label': 'Julho', 'value': 'JUL'},
                    {'label': 'Agosto', 'value': 'AUG'},
                    {'label': 'Setembro', 'value': 'SEP'},
                    {'label': 'Outubro', 'value': 'OCT'},
                    {'label': 'Novembro', 'value': 'NOV'},
                    {'label': 'Dezembro', 'value': 'DEC'},
                    {'label': 'Verão', 'value': 'D-J-F'},
                    {'label': 'Outono', 'value': 'M-A-M'},
                    {'label': 'Inverno', 'value': 'J-J-A'},
                    {'label': 'Primavera', 'value': 'S-O-N'},
                    {'label': 'Anual', 'value': 'metANN'}],
                    value='JAN',
                    id='month-radio')
    ]),
    dcc.Graph(figure=px.line(df, x='YEAR', y='D-J-F'), id='graph')
])

@callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='city-radio', component_property='value'),
    Input(component_id='month-radio', component_property='value')
)
def update_graph(city_chosen, month_chosen):
    df = pd.read_csv(dict_cidades[city_chosen])
    df = df.replace(999.90, np.nan)
    fig = px.line(df, x='YEAR', y=month_chosen)
    return fig

if __name__ == '__main__':
    app.run(debug=True)
