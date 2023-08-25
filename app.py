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
    
    html.H1(children='Temperatura de Cidades Brasileiras durante os anos',
            style={'textAlign': 'center', 'fontFamily': 'Arial'}),
    
    html.Div(className='row', children=[
    dcc.Dropdown(
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
        value=['Salvador'],
        multi=True,
        id='city-radio',
        style={'textAlign': 'center', 'fontSize': 20,
                'fontFamily': 'Arial',
               })
    ]),
    

    dcc.Graph(figure=px.line(df, x='YEAR', y='D-J-F', color_discrete_sequence=px.colors.qualitative.T10
                             ,title='Gráfico linear da Temperatura de Cidades Brasileiras durante os anos'), id='graph' ),
    
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
                    value='D-J-F',
                    id='month-radio',
                    style={'textAlign': 'center',
                           'fontFamily': 'Arial', 'align': 'center'})
    ]),
    
    html.H3(children='Preenchimento dos valores 999.90: ', style={'textAlign': 'center', 'fontFamily': 'Arial'}),
    
    dcc.RadioItems(options=['NaN', 'Último valor válido', 'Interpolação linear'],
                 value='NaN', id='fill-radio',
                 style={'textAlign': 'center', 'fontFamily': 'Arial', 'align': 'center'},
                 labelStyle={'display': 'inline-block'}),
    
    dcc.Graph(figure=px.box(df, y='D-J-F',title='Gráfico BoxPlot da temperatura médiade Cidades Brasileiras durante os anos'), id='box'),
    
    dcc.Dropdown(
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
        id='city-radio2',
        style={'textAlign': 'center', 'fontSize': 20,
                'fontFamily': 'Arial',
               })
    
])

@callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='city-radio', component_property='value'),
    Input(component_id='month-radio', component_property='value'),
    Input(component_id='fill-radio', component_property='value')   
)
def update_graph(city_chosen, month_chosen, fill_chosen):
    
    string = ''
    for i in city_chosen:
        string +=  i + ', '
    string = string[:-2]  
    
    fig = px.line(title='Gráfico linear da temperatura de Cidades Brasileiras durante os anos: ' + string) 
    
    for i in city_chosen:
    
        df = pd.read_csv(dict_cidades[i])
        df = df.replace(999.90, np.nan)
        
        if fill_chosen == 'Último valor válido':
            df = df.fillna(method='ffill')
        elif fill_chosen == 'Interpolação linear':
            df = df.interpolate(method='linear')
            
        fig.add_trace(px.line(df, x='YEAR', y=month_chosen, color_discrete_sequence=px.colors.qualitative.T10, line_shape='linear').data[0])
        
    return fig

@callback(
    Output(component_id='box', component_property='figure'),
    Input(component_id='city-radio2', component_property='value'),
    Input(component_id='month-radio', component_property='value'),
    Input(component_id='fill-radio', component_property='value')   
)
def update_box(city_chosen, month_chosen, fill_chosen):    
    
    df = pd.read_csv(dict_cidades[city_chosen])
    df = df.replace(999.90, np.nan)
    
    if fill_chosen == 'Último valor válido':
        df = df.fillna(method='ffill')
    elif fill_chosen == 'Interpolação linear':
        df = df.interpolate(method='linear')

    fig = px.box(df, y=month_chosen, title='Gráfico BoxPlot da temperatura de Cidades Brasileiras durante os anos: ' + city_chosen) 

    return fig

if __name__ == '__main__':
    app.run(debug=True)
