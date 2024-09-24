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


conc = pd.read_sql_query("SELECT * from forms_conc", db_con)#pd.read_excel('https://docs.google.com/spreadsheets/d/15PU9vOE6deEdFGEPAmeXGAJJBEYMhq4j/edit?usp=share_link&ouid=108398935028018525491&rtpof=true&sd=true', engine='openpyxl')
df = conc['Nome do Representante'].value_counts().to_frame().reset_index()




app.layout = dbc.Container([
    
    dbc.Row([
        dbc.Col([dcc.Graph(
            id='example-graph',
            figure=px.bar(df, x="Nome do Representante", y="count", color='count', color_continuous_scale='Bluered'),
        ),], width=6, style={'backgroundColor': '#F0F0F0', 'padding': '10px'}),
        dbc.Col([dcc.Graph(id='output_1')], width=6, style={'backgroundColor': '#F0F0F0', 'padding': '10px'}),
        dbc.Col([dcc.Graph(id='output_2')], width=6, style={'backgroundColor': '#F0F0F0', 'padding': '10px'}),
        dbc.Col([dcc.Graph(id='output_3')], width=6, style={'backgroundColor': '#F0F0F0', 'padding': '10px'}),
        dbc.Col([dcc.Graph(id='output_4')], width=6, style={'backgroundColor': '#F0F0F0', 'padding': '10px'}),
        
    ]),
    dbc.Row([
        dbc.Col([dcc.Graph(id='output_5')], width=6, style={'backgroundColor': '#F0F0F0', 'padding': '10px'}),
        dbc.Col([dcc.Graph(id='output_6')], width=6, style={'backgroundColor': '#F0F0F0', 'padding': '10px'}),
        dbc.Col([dcc.Graph(id='output_7')], width=6, style={'backgroundColor': '#F0F0F0', 'padding': '10px'}),
        dbc.Col([dcc.Graph(id='output_8')], width=6, style={'backgroundColor': '#F0F0F0', 'padding': '10px'}),
        dbc.Col([dcc.Graph(id='output_9')], width=6, style={'backgroundColor': '#F0F0F0', 'padding': '10px'}),
        
    ]),


    
])



# 1 - Callback for hoverData 
@app.callback(
    Output('output_1', 'figure'),
    [Input('example-graph', 'hoverData')]
)
def display_hover_data(hoverData):
    frame = 'Porque não efetuamos o Pedido?'
    if hoverData:
        hovered_category = hoverData['points'][0]['x']
        dff = conc.query("`Nome do Representante` == @hovered_category") \
                   [frame].value_counts().reset_index()
        dff.columns = [frame, 'count']
        
        figure = px.bar(dff, y=frame, x='count', color=frame ,color_continuous_scale='Bluered')
        return figure
    
    # Return an empty figure if no hover data
    return px.bar(title="Hover over a bar to see details.")

# 2 - Callback for hoverData 
@app.callback(
    Output('output_2', 'figure'),
    [Input('example-graph', 'hoverData')]
)
def display_hover_data(hoverData):
    frame = 'Conhece alguma marca do GRUPO DVG'
    if hoverData:
        hovered_category = hoverData['points'][0]['x']
        dff = conc.query("`Nome do Representante` == @hovered_category") \
                   [frame].value_counts().reset_index()
        dff.columns = [frame, 'count']
        
        figure = px.bar(dff, x=frame, y='count')
        return figure
    
    # Return an empty figure if no hover data
    return px.bar(title="Hover over a bar to see details.")

# 3 - Callback for hoverData 
@app.callback(
    Output('output_3', 'figure'),
    [Input('example-graph', 'hoverData')]
)
def display_hover_data(hoverData):
    frame = 'Porque parou de comprar?'
    if hoverData:
        hovered_category = hoverData['points'][0]['x']
        dff = conc.query("`Nome do Representante` == @hovered_category") \
                   [frame].value_counts().reset_index()
        dff.columns = [frame, 'count']
        
        figure = px.bar(dff, x=frame, y='count')
        return figure
    
    # Return an empty figure if no hover data
    return px.bar(title="Hover over a bar to see details.")

# 4 - Callback for hoverData 
@app.callback(
    Output('output_4', 'figure'),
    [Input('example-graph', 'hoverData')]
)
def display_hover_data(hoverData):
    frame = 'Já compou da TUBOZAN'
    if hoverData:
        hovered_category = hoverData['points'][0]['x']
        dff = conc.query("`Nome do Representante` == @hovered_category") \
                   [frame].value_counts().reset_index()
        dff.columns = [frame, 'count']
        
        figure = px.bar(dff, x=frame, y='count')
        return figure
    
    # Return an empty figure if no hover data
    return px.bar(title="Hover over a bar to see details.")

# 5 - Callback for hoverData 
@app.callback(
    Output('output_5', 'figure'),
    [Input('example-graph', 'hoverData')]
)
def display_hover_data(hoverData):
    frame = 'Regional do Representante'
    if hoverData:
        hovered_category = hoverData['points'][0]['x']
        dff = conc.query("`Nome do Representante` == @hovered_category") \
                   [frame].value_counts().reset_index()
        dff.columns = [frame, 'count']
        
        figure = px.bar(dff, x=frame, y='count')
        return figure
    
    # Return an empty figure if no hover data
    return px.bar(title="Hover over a bar to see details.")

# 6 - Callback for hoverData 
@app.callback(
    Output('output_6', 'figure'),
    [Input('example-graph', 'hoverData')]
)
def display_hover_data(hoverData):
    frame = 'Fez o pedido'
    if hoverData:
        hovered_category = hoverData['points'][0]['x']
        dff = conc.query("`Nome do Representante` == @hovered_category") \
                   [frame].value_counts().reset_index()
        dff.columns = [frame, 'count']
        
        figure = px.bar(dff, x=frame, y='count')
        return figure
    
    # Return an empty figure if no hover data
    return px.bar(title="Hover over a bar to see details.")

# 7 - Callback for hoverData 
@app.callback(
    Output('output_7', 'figure'),
    [Input('example-graph', 'hoverData')]
)
def display_hover_data(hoverData):
    frame = 'Qual concorrente?'
    if hoverData:
        hovered_category = hoverData['points'][0]['x']
        dff = conc.query("`Nome do Representante` == @hovered_category") \
                   [frame].value_counts().reset_index()
        dff.columns = [frame, 'count']
        
        figure = px.bar(dff, x=frame, y='count')
        return figure
    
    # Return an empty figure if no hover data
    return px.bar(title="Hover over a bar to see details.")

# 8 - Callback for hoverData 
@app.callback(
    Output('output_8', 'figure'),
    [Input('example-graph', 'hoverData')]
)
def display_hover_data(hoverData):
    frame = 'Já compou da TUBOZAN'
    if hoverData:
        hovered_category = hoverData['points'][0]['x']
        dff = conc.query("`Nome do Representante` == @hovered_category") \
                   [frame].value_counts().reset_index()
        dff.columns = [frame, 'count']
        
        figure = px.bar(dff, x=frame, y='count')
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
        dff = conc.query("`Nome do Representante` == @hovered_category") \
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
    
