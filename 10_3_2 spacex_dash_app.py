# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
def booster_version_color(booster_version):
    if booster_version == 'B4':
        return 'green'
    elif booster_version == 'B5':
        return 'yellow'
    elif booster_version == 'FT':
        return 'orange'
    elif booster_version == 'v1.0':
        return 'blue'
    elif booster_version == 'v1.1':
        return 'red'

spacex_df['Booster Version Color'] = spacex_df['Booster Version Category'].apply(booster_version_color)
# Create a dash application
app = dash.Dash(__name__)
site_list1 = [
    {'lable': 'All Sites', 'value':'All Sites'},
    {'lable': 'CCAFS LC-40', 'value':'CCAFS_LC_40'},
     {'lable': 'CCAFS SLC-40', 'value':'CCAFS_SLC_40'},
    {'lable': 'KSC LC-39A', 'value':'KSC_LC_39A'},
    {'lable': 'VAFB SLC-4E', 'value':'VAFB_SLC_4E'}]
site_list = ['All Sites', 'CCAFS LC-40', 'CCAFS SLC-40', 'KSC LC-39A', 'VAFB SLC-4E']

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboards',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                html.Br(),
                                html.Br(),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                            options=site_list,
                                             value= 'All Sites',
                                             placeholder = 'Place holder here',
                                             searchable= True,
                                             style={'textAlign':'center','color': '#503D36','font-size':20}

                                            ),
                                html.Br(), 
                                html.Br(),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg)aa:"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,step=1000,
                                                marks={0: '0',2500: '2500',5000: '5000',7500: '7500',},
                                                value=[min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart',component_property='figure'),
              Input(component_id='site-dropdown',component_property='value'))
def get_pie_chart(site_enter):
    filtered_df = spacex_df[spacex_df['class']==1].groupby('Launch Site')['class'].count().reset_index()
    #filtered_df['Percent'] = filtered_df['class'] / filtered_df['class'].sum() * 100
    fig = px.pie(filtered_df, values='class', names='Launch Site', title='title')
    if site_enter == 'All Sites':
        fig = px.pie(filtered_df,values='class',names='Launch Site',title='ALL Sites')
    else:
        #elif site_enter == 'CCAFS LC-40':
        specific_site_df = spacex_df[spacex_df['Launch Site']==site_enter].groupby('class').count().reset_index()
        fig= px.pie(specific_site_df,values='Launch Site',names='class',title=site_enter)

    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
              Input(component_id='site-dropdown',component_property='value'),
              Input(component_id='payload-slider',component_property='value'))
def get_scatter_plot(site_enter,payload_slide):
    payload_slider_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload_slide[0],payload_slide[1])]
    if site_enter == 'All Sites':
        fig1 = px.scatter(payload_slider_df,x='Payload Mass (kg)',y='class',color='Booster Version Category')
    else:
        spacex_slider_df = payload_slider_df[payload_slider_df['Launch Site']==site_enter]
        fig1 = px.scatter(spacex_slider_df,x='Payload Mass (kg)',y='class',color='Booster Version Category')
    return fig1





# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)