from dash import Dash, html, dcc, callback, Output, Input
import dash
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

dash.register_page(__name__, path='/', name="Comparar cidades no mesmo período")

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

layout = html.Div([
    
    html.H1(children='Temperatura de Cidades Brasileiras durante os anos',
            style={'textAlign': 'center', 'fontFamily': 'Arial'}),
    
    html.Div(className='row', children=[
    dcc.Checklist(
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
        id='city-radio',
        labelStyle={'display': 'inline-block'},
        style={'textAlign': 'center', 'fontSize': 20,
                'fontFamily': 'Arial'
               })
    ]),
    
    html.Br(),
    
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
    
    dcc.Graph(figure=px.line(df, x='YEAR', y='D-J-F', color_discrete_sequence=px.colors.qualitative.T10
                             ,title='Gráfico linear da Temperatura de Cidades Brasileiras durante os anos'), id='graph' ),
    
    
    dcc.Graph(figure=px.box(df, y='D-J-F',title='Gráfico BoxPlot da temperatura médiade Cidades Brasileiras durante os anos'), id='box'),
    
    dcc.Graph(figure=px.histogram(df, x='D-J-F',  title='Histograma da temperatura média de Cidades Brasileiras durante os anos'), id='histogram')
    
])

@callback(
    Output(component_id='box', component_property='figure'),
    Output(component_id='graph', component_property='figure'),
    Output(component_id='histogram', component_property='figure'),
    Input(component_id='city-radio', component_property='value'),
    Input(component_id='month-radio', component_property='value'),
    Input(component_id='fill-radio', component_property='value')   
)
def update_graph(city_chosen, month_chosen, fill_chosen):
    
    string = ''
    for i in city_chosen:
        string +=  i + ', '
    string = string[:-2]  
    
    fig_line = px.line(title='Gráfico linear da temperatura de Cidades Brasileiras durante os anos: ' + string) 
    fig_boxplot = px.box(title='Gráfico BoxPlot da temperatura de Cidades Brasileiras durante os anos: ' + string)
    
    histogram_data = []
    
    for i in city_chosen:
    
        df = pd.read_csv(dict_cidades[i])
        df = df.replace(999.90, np.nan)
        
        if fill_chosen == 'Último valor válido':
            df = df.fillna(method='ffill')
        elif fill_chosen == 'Interpolação linear':
            df = df.interpolate(method='linear')
            
        fig_line.add_trace(go.Scatter(x=df['YEAR'], y=df[month_chosen], name=i))
        fig_boxplot.add_trace(go.Box(y=df[month_chosen], name=i))
        histogram_data.append(go.Histogram(x=df[month_chosen], name=i))
        
    fig_histogram = go.Figure(data=histogram_data)

        
    return fig_boxplot, fig_line, fig_histogram

