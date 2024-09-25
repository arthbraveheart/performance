'''
 # @ Create Time: 2024-09-23 15:02:41.105417
'''

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import sqlite3 as s

from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
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
                html.P("Value: 1000", className="card-text")
            ])
        ), width=3),
        
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H5("Mucho", className="card-title"),
                html.P("Value: 2000", className="card-text")
            ])
        ), width=3),
        
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H5("Oportunidades", className="card-title"),
                html.P("Value: 3000", className="card-text")
            ])
        ), width=3),

        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H5("Enviados", className="card-title"),
                html.P("Value: 4000", className="card-text")
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




sidebar = html.Div(
    [
        html.H3("Performance", className="display-4"),
        html.Hr(),
        html.P(
            "Prospects", className="lead"
        ),
        dbc.Nav(
            [
                
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

# 1 - Callback for hoverData 
@app.callback(
    Output('output_1', 'figure'),
    [Input('example-graph', 'hoverData')]
)
def display_hover_data(hoverData):
    frame = 'Conhece alguma marca do GRUPO DVG'
    legendd = 'Fez o pedido'
    if hoverData:
        hovered_category = hoverData['points'][0]['x']
        dff = conc.query("`forms_name` == @hovered_category") 
        dff = dff.groupby([frame,legendd])[legendd].value_counts().to_frame().reset_index()
                   
        #dff.columns = [frame, 'count']
        
        #figure = px.bar(dff, x=frame, y='count', color = 'count', color_continuous_scale='Bluered')


        figure = px.scatter(dff, x=frame, y="count",
	             size="count", color=legendd,
                   size_max=60)

        
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
        fig.update_layout(title_text="Tomada de decisão", font_size=10)
        return fig
    
    # Return an empty figure if no hover data
    return px.bar(title="Hover over a bar to see details.")


if __name__ == '__main__':
    app.run_server(debug=True)
    
