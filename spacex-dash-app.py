import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Read SpaceX launch data into pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv")

# Get min and max payload for RangeSlider
min_payload = spacex_df['PayloadMass'].min()
max_payload = spacex_df['PayloadMass'].max()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center'}),

    # Task 1: Add dropdown
    dcc.Dropdown(id='site-dropdown',
                 options=[{'label': 'All Sites', 'value': 'ALL'}] + 
                         [{'label': site, 'value': site} for site in spacex_df['LaunchSite'].unique()],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True
                ),

    html.Br(),

    # Pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.P("Payload range (Kg):"),

    # Task 3: Add range slider
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                    value=[min_payload, max_payload]),

    # Scatter chart
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# Task 2: Callback to update pie chart
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='Class', 
                     names='LaunchSite', 
                     title='Total Success Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['LaunchSite'] == entered_site]
        fig = px.pie(filtered_df, names='Class',
                     title=f'Total Success vs. Failure for site {entered_site}')
    return fig

# Task 4: Callback to update scatter plot
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_plot(entered_site, payload_range):
    low, high = payload_range
    mask = (spacex_df['PayloadMass'] >= low) & (spacex_df['PayloadMass'] <= high)
    filtered_df = spacex_df[mask]
    
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='PayloadMass', y='Class',
                         color='BoosterVersion',
                         title='Correlation between Payload and Success for all Sites')
    else:
        site_df = filtered_df[filtered_df['LaunchSite'] == entered_site]
        fig = px.scatter(site_df, x='PayloadMass', y='Class',
                         color='BoosterVersion',
                         title=f'Correlation between Payload and Success for site {entered_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=False)
