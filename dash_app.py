'''
 # @ Create Time: 2024-09-23 15:02:41.105417
'''

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import sqlite3 as s
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
import plotly.graph_objects as go


app = Dash(__name__, title="performance", external_stylesheets=[dbc.themes.BOOTSTRAP])

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

# db connect
db_con = s.connect('db_tubozan.db')

# Data
data = {
    'Sector': ['Manager', 'Manager', 'Manager', 'Manager', 'Marketing', 'Marketing', 'Marketing','Vazio'],
    'Porque não efetuamos o Pedido?': ['Preço', 'Atendimento', 'Fidelidade com concorrente', 'Pazo de entrega', 
              'Inicio de Relacionamento', 'Variedade de produtos', 'Qualidade do produto','vazio']
}
datas = pd.DataFrame(data)
tuples = [(source,target) for source, target in zip(data['Porque não efetuamos o Pedido?'],data['Sector'])]
datas['tuples'] = tuples

# forms
conc = pd.read_sql_query("SELECT * from forms_conc", db_con)#pd.read_excel('https://docs.google.com/spreadsheets/d/15PU9vOE6deEdFGEPAmeXGAJJBEYMhq4j/edit?usp=share_link&ouid=108398935028018525491&rtpof=true&sd=true', engine='openpyxl')
df = conc['forms_name'].value_counts().to_frame().reset_index()

# zona branca
zb = pd.read_sql_query("SELECT * from z_b", db_con)

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "10rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


# Top section - KPI cards
top_kpi_cards = dbc.Row(
    [
        dbc.Col(dbc.Card(
            dbc.CardBody([ 
                html.H5("DVG Total", className="card-title"),
                html.H3(id='dvg_tot',children="", className="card-text")
            ])
        ), width=3),
        
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H5("Mucho", className="card-title"),
                html.H3(id='mucho',children='', className="card-text")
            ])
        ), width=3),
        
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H5("Oportunidades", className="card-title"),
                html.H3(id='opp',children='', className="card-text")
            ])
        ), width=3),

        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H5("Enviados", className="card-title"),
                html.H3(id='env',children='', className="card-text"),
                
                          
            ])
        ), width=3),
        
    ],
    #className="mb-4",  # Add some margin at the bottom of the cards
)

# Bottom section - Charts
bottom_charts = dbc.Container([
    dbc.Row([
        dbc.Col([dcc.Graph(
            id='example-graph',
            figure=px.bar(df, x="forms_name", y="count", color='count', color_continuous_scale='Bluered'),
        )], width=12, style={'backgroundColor': '#0c2563', 'padding': '10px'}),
        
    ]),
    dbc.Row([
        dbc.Col([dcc.Graph(id='output_1')], width=6, style={'backgroundColor': '#0c2563', 'padding': '10px'}),
        dbc.Col([dcc.Graph(id='output_9')], width=6, style={'backgroundColor': '#0c2563', 'padding': '10px'}),
        
],) ], fluid=True)


content = html.Div([
    top_kpi_cards,  # KPI cards row
    bottom_charts   # Charts row
], style=CONTENT_STYLE)


radio   = dcc.RadioItems(id='user_choice_1', options=[ {'label': 'Fez o Pedido?', "value": 'Fez o pedido'},
                                                   {'label':'Loja Existe?','value':'Loja Existe'},
                                                   {'label':'Já comprou da TUBOZAN?','value':'Já compou da TUBOZAN'}],
                             value='Fez o pedido?', style={"color": "#0c2563"})


drope   = dcc.Dropdown(id='user_choice_2', options=[ {'label': 'Diferença de Preço', "value": 'Diferença de Preço'},
                                                   {'label':'Qual concorrente?','value':'Qual concorrente?'},
                                                   {'label':'Tamanho','value':'Tamanho'},
                                                   {'label':'Conhece alguma marca do GRUPO DVG','value':'Conhece alguma marca do GRUPO DVG'},
                                                   {'label':'Porque parou de comprar?','value':'Porque parou de comprar?'},
                                                   {'label':'Segmento da Loja','value':'Segmento da Loja'}],value='Diferença de Preço', style={"color": "#0c2563"})

sidebar = html.Div(
    [   #html.Img(src='/private/var/root/Downloads/MUCHO%20LOGO%20positivo%20-%20Copia%20-%20Copia.png'),
        html.H5("Performance", className="display-4", style={"width": "200px"}),
        html.Hr(),
        html.P(
            "Prospects", className="lead"
        ),
        dbc.Nav(
            [
               radio,
               drope, 
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[
          content,
          ], style=CONTENT_STYLE)


app.layout = html.Div([
    
    sidebar,
    content
], style={'backgroundColor': '#0c2563'})


# KPI Cards Callback
@app.callback(
    [Output('dvg_tot', 'children'),
     Output('mucho', 'children'),
     Output('opp', 'children'),
     Output('env', 'children')],
    [Input('example-graph', 'hoverData')]
)
def update_kpi_cards(hoverData):
    cards = ['DVG Total', 'Mucho', 'oportunidades', 'Já passadas']
    
    if hoverData:
        region_dict = {
            'Norte': 'Região Norte',
            'Nordeste': 'Região Nordeste',
            'Sul': 'Região Sul',
            'Minas': 'Região Sudeste',
            'Centro Oeste': 'Região Centro-Oeste',
        }
        hovered_category = region_dict.get(hoverData['points'][0]['x'], 'Região Sudeste')
        dff = zb.query("Regiao == @hovered_category")
        totals = [dff[card].sum() for card in cards]
    else:
        totals = [zb[card].sum() for card in cards]
    
    return [f'{total}' for total in totals] 


# 1 - Callback for hoverData 
@app.callback(
    Output('output_1', 'figure'),
    [Input('example-graph', 'hoverData'), Input('user_choice_1','value'), Input('user_choice_2','value')]
)
def display_hover_data(hoverData, value_1,value_2):
    frame = value_2
    legendd = value_1
    if hoverData:
        hovered_category = hoverData['points'][0]['x']
        dff = conc.query("`forms_name` == @hovered_category") 
        dff = dff.groupby([frame, legendd])[legendd].value_counts().to_frame().reset_index()

        # Create subplots with scatter and pie
        figure = make_subplots(rows=1, cols=2, specs=[[{"type": "scatter"}, {"type": "pie"}]], shared_xaxes=True,
                    shared_yaxes=False, vertical_spacing=0.001)

        # Scatter plot trace
        scatter_fig = px.scatter(dff, x=frame, y="count", size="count", color=legendd, size_max=60)
        for trace in scatter_fig['data']:
            figure.add_trace(trace, row=1, col=1)

        # Pie chart trace
        pie_fig = px.pie(dff, values='count', names=legendd, hole=0.5, title=legendd)
        figure.add_trace(go.Pie(labels=pie_fig['data'][0]['labels'], values=pie_fig['data'][0]['values'], hole=0.5), row=1, col=2)
        figure.update_layout(
                  title=frame)
        return figure
    
    # Return an empty figure if no hover data
    return px.bar(title="Hover over a bar to see details.")


# 9 - Callback for hoverData 
@app.callback(
    Output('output_9', 'figure'),
    [Input('example-graph', 'hoverData')]
)
def display_hover_data(hoverData):
    frame = 'Porque não efetuamos o Pedido?'
    if hoverData:
        hovered_category = hoverData['points'][0]['x']
        dff = conc.query("`forms_name` == @hovered_category") \
                   [frame].value_counts().reset_index()
        dff.columns = [frame, 'count']
        
        selected = set(dff.loc[:,frame].to_list())
        dt     = datas.query(" `Porque não efetuamos o Pedido?` in @selected ")
        
        # Create a mapping for the unique labels
        labels = list(set(dt['Sector'].to_list() + dt['Porque não efetuamos o Pedido?'].to_list()))

        # Map sectors and issues to their respective indices
        label_map = {label: i for i, label in enumerate(labels)}

        # Create the Sankey diagram data
        source_indices = [label_map[sector] for sector in dt['Sector']]
        target_indices = [label_map[issue] for issue in dt['Porque não efetuamos o Pedido?']]

        # Assign default values for the links
        values = [1] * len(source_indices)

        # Create the Sankey chart
        fig = go.Figure(go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
            ),
            link=dict(
                source=source_indices,
                target=target_indices,
                value=values
            )
        ))

        # Set the title and display the figure
        fig.update_layout(title_text="Tomada de decisão:<br>Porque não efetuamos o pedido?", font_size=10)
        return fig
    
    # Return an empty figure if no hover data
    return px.bar(title="Hover over a bar to see details.")



if __name__ == '__main__':
    app.run_server(debug=True)
    
