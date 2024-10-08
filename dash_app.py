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

px.defaults.template = "plotly_dark"
px.defaults.color_continuous_scale = px.colors.sequential.Blackbody


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
datas           = pd.DataFrame(data)
tuples          = [(source,target) for source, target in zip(data['Porque não efetuamos o Pedido?'],data['Sector'])]
datas['tuples'] = tuples

# forms
conc = pd.read_sql_query("SELECT * from forms_conc", db_con)#pd.read_excel('https://docs.google.com/spreadsheets/d/15PU9vOE6deEdFGEPAmeXGAJJBEYMhq4j/edit?usp=share_link&ouid=108398935028018525491&rtpof=true&sd=true', engine='openpyxl')
df   = conc['forms_name'].value_counts().to_frame().reset_index()

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
    #"position": "fixed",
    "top": 0,
    #"right": 0,
    "bottom": 0,
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
        dbc.Col([dcc.Graph(id='output_1')], width=12, style={'backgroundColor': '#b2c5d6', 'padding': '10px'}),
        dbc.Col([dcc.Graph(id='output_9')], width=12, style={'backgroundColor': '#0c2563', 'padding': '10px'}),
        
],) ], fluid=True)


content = html.Div([
    top_kpi_cards,  # KPI cards row
    bottom_charts   # Charts row
], style=CONTENT_STYLE)


radio   = dcc.RadioItems(id='user_choice_1', options=[ {'label': 'Fez o Pedido?', "value": 'Fez o pedido'},
                                                   {'label':'Loja Existe?','value':'Loja Existe'},
                                                   {'label':'Já comprou da TUBOZAN?','value':'Já comprou da TUBOZAN'}],
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

#---------- Figures --------------#

def san_key(data_f,f_frame):
        
        selected = set(data_f.loc[:,f_frame].to_list())
        dt       = datas.query(" `Porque não efetuamos o Pedido?` in @selected ")
        weights  = data_f.set_index(f_frame).to_dict()
        #weights  = dt.loc[:,'Porque não efetuamos o Pedido?'].value_counts()
        # Create a mapping for the unique labels
        labels   = list(set(dt['Sector'].to_list() + dt['Porque não efetuamos o Pedido?'].to_list()))

        # Map sectors and issues to their respective indices
        label_map = {label: i for i, label in enumerate(labels)}
        map_label = {i:label for i, label in enumerate(labels)}
        # Create the Sankey diagram data
        source_indices = [label_map[sector] for sector in dt['Sector']]
        target_indices = [label_map[issue] for issue in dt['Porque não efetuamos o Pedido?']]
        values         = [weights['count'][map_label[target]] for target in target_indices]#[1] * len(source_indices)

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
        fig.update_layout(title_text="Tomada de decisão:<br>Porque não efetuamos o pedido?", font_size=10, template='plotly_dark')
        return fig

    

#---------- LAYOUT --------------#
app.layout = html.Div([
    
    sidebar,
    content
], style={'backgroundColor': '#0c2563'})#'#5485b3'})#'#0c2563'})


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



        color_map = {
                        "Sim": px.colors.qualitative.Plotly[0],
                        "Não": px.colors.qualitative.Plotly[1],
                        "vazio": px.colors.qualitative.Plotly[2],
                    }
        # Adjust marker sizes for bubbles (you can adjust the factor for better visualization)
        bubble_size_factor = 20

        # Group the data by the x-axis value and create a hover text that combines all bubbles for the same x value
        hover_texts = dff.groupby(frame).apply(
            lambda group: "<br>".join([f"{legendd}: {val}, Count: {cnt}" for val, cnt in zip(group[legendd], group['count'])])
        ).reindex(dff[frame])
        
        # Scatter plot trace using go.Scatter with consistent hover and size
        scatter_trace = go.Scatter(
            x=dff[frame],
            y=dff['count'],
            mode='markers',
            marker=dict(
                size=dff['count'] * bubble_size_factor,  # Bubble size
                color=[color_map[val] for val in dff[legendd]],  # Color based on category
                sizemode='area',  # Size bubbles by area for better proportionality
                sizeref=max(dff['count']) / 100,  # Adjust size reference for better scaling
                sizemin=5  # Minimum bubble size
            ),
            text=hover_texts,#[f"{legendd}: {val}<br>Count: {cnt}" for val, cnt in zip(dff[legendd], dff['count'])],  # Custom hover text
            hoverinfo='text',  # Show custom hover info
            showlegend=False
        )
        
        # Pie chart trace using go.Pie with hover and legend control
        pie_trace = go.Pie(
            labels=dff[legendd],
            values=dff['count'],
            hole=0.5,
            marker=dict(colors=[color_map[val] for val in dff[legendd]]),
            textinfo='label+percent',  # Show label and percentage on pie
            hoverinfo='label+value',  # Show category and count on hover
            showlegend=True  # Keep the legend visible for the pie chart
        )
        
        # Add traces to the figure
        figure.add_trace(scatter_trace, row=1, col=1)
        figure.add_trace(pie_trace, row=1, col=2)
        
        # Update layout and background
        figure.update_layout(
            title_text=f"Comparing {frame} -> {legendd}",
            font_size=10,
            template='plotly_dark',  # This sets the dark background
            hovermode="x unified",  # Consistent hover behavior
            #paper_bgcolor="rgba(0, 0, 0, 0)",  # Transparent background
            #plot_bgcolor="rgba(0, 0, 0, 0)",   # Transparent plot background
            legend=dict(
                title=legendd,  # Make the legend title consistent with the category
                x=1.05,  # Place the legend outside of the graph
                y=1
            )
        )
        
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
        dff              = conc.query("`forms_name` == @hovered_category") \
                                [frame].value_counts().reset_index()
        dff.columns      = [frame, 'count']        
        fig              = san_key(dff,frame)
    else:
        dff              = conc[frame].value_counts().reset_index() #without query
        dff.columns      = [frame, 'count']        
        fig              = san_key(dff,frame)
    
    # Return an empty figure if no hover data
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
    
