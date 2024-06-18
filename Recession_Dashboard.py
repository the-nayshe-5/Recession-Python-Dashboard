# Import required libraries
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
df =  pd.read_csv('historical_automobile_sales.csv')

# Create a dash application
app = dash.Dash(__name__)

# Build dash app layout
app.layout = html.Div(children=[ html.H1('Automobile Sales Statistics Dashboard', 
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 24}),
                                dcc.Dropdown(
                                    id = 'dropdown-statistics',
                                    options = [
                                        {'label' : 'Yearly Statistics', 'value' : 'Yearly Statistics'},
                                        {'label' : 'Recession Period Statistics', 'value' : 'Recession Period Statistics'}
                                    ],
                                    placeholder = 'Select a report type',
                                    value = 'Select Statistics',
                                    style = { 'width' : '80%', 'padding' : '3px', 'font-size' : '20px', 'text-align' : 'center' }
                                ),
                                dcc.Dropdown(
                                    id = 'select-year',
                                    options = [ {'label' : i, 'value' : i} for i in range(1980,2014) ],
                                    placeholder = 'Select year',
                                    value = 'Select year',
                                    style = { 'width' : '80%', 'padding' : '3px', 'font-size' : '20px', 'text-align' : 'center' }
                                ),
                                html.Div([
                                    html.Div(
                                        id = 'output-container',
                                        className = 'chart-grid',
                                        style = { 'display' : 'flex' , 'flex-direction' : 'column'}
                                    )
                                ])
                                ])
                                

    
@app.callback(
    Output(component_id = 'select-year', component_property = 'disabled'),
    Input(component_id = 'dropdown-statistics', component_property = 'value')
)

def update_input_container(stats_value):
    if stats_value == 'Yearly Statistics':
        return False
    else:
        return True

@app.callback(
    Output(component_id = 'output-container', component_property = 'children'),
    [Input(component_id = 'dropdown-statistics', component_property = 'value'), 
     Input(component_id = 'select-year', component_property = 'value')]
)

def update_output_container(stats_value, year_value):
    if stats_value == 'Recession Period Statistics':
        rec_df = df.loc[df['Recession'] == 1]
        #Plot 1 Automobile sales fluctuate over Recession Period (year wise) using line chart
        year_sales = rec_df.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure = px.line(
                year_sales,
                x = 'Year', y = 'Automobile_Sales',
                title = 'Automobile Sales over Recession Period',
                labels = dict(x = 'Year', y = 'Sales')
            )
        )

        #Plot 2 Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart
        veh_sold = rec_df.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure = px.bar(
                veh_sold,
                x = 'Vehicle_Type', y = 'Automobile_Sales',
                title = 'Vehicles Sold by Vehicle Type during Recessions',
                labels = dict(x = 'Vehicle Type', y = 'Sales')
            )
        )

        #Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        tot_exp = rec_df.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        tot_exp['Advertising_Expenditure'] = tot_exp['Advertising_Expenditure']*100/tot_exp['Advertising_Expenditure'].sum()
        R_chart3 = dcc.Graph(
            figure = px.pie(
                tot_exp,
                names = 'Vehicle_Type', values = 'Advertising_Expenditure',
                title = 'Total Expenditure Share by Vehicle Type during Recessions',
                labels = dict(x = 'Vehicle Type', y = 'Expenditure')
            )
        )

        #Plot 4 Develop a Bar chart for the effect of unemployment rate on vehicle type and sales
        unemp_eff = rec_df.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure = px.bar(
                unemp_eff,
                x = 'unemployment_rate', y = 'Automobile_Sales',
                color = 'Vehicle_Type',
                title = 'Total Expenditure Share by Vehicle Type during Recessions',
                labels = {'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
            )
        )

        return [
            html.Div(className = 'chart-item', children = [html.Div(children = R_chart1),html.Div(children = R_chart2)]),
            html.Div(className = 'chart-item', children = [html.Div(children = R_chart3),html.Div(children = R_chart4)])
        ]

    elif (year_value and stats_value == 'Yearly Statistics'):
        year_df = df.loc[df['Year'] == year_value]
        #Plot 1 Yearly Automobile sales using line chart for the whole period.
        year_sales = df.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure = px.line(
                year_sales,
                x = 'Year', y = 'Automobile_Sales',
                title = 'Yearly Autombile Sales',
                labels = dict(x = 'Year', y = 'Sales')
            )
        )

        #Plot 2 Total Monthly Automobile sales using line chart.
        year_sales = year_df.groupby('Month')['Automobile_Sales'].mean().reset_index()
        Y_chart2 = dcc.Graph(
            figure = px.line(
                year_sales,
                x = 'Month', y = 'Automobile_Sales',
                title = 'Total Monthly Automobile Sales',
                labels = dict(x = 'Month', y = 'Sales')
            )
        )

        #Plot 3 Bar chart for average number of vehicles sold during the given year by vehicle type
        veh_sold = year_df.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure = px.bar(
                veh_sold,
                x = 'Vehicle_Type', y = 'Automobile_Sales',
                title = 'Average Vehicles Sold by Vehicle Type in the year {}'.format(year_value),
                labels = dict(x = 'Vehicle Type', y = 'Sales')
            )
        )

        #Plot 4 Total Advertisement Expenditure for each vehicle using pie chart
        tot_exp = year_df.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        tot_exp['Advertising_Expenditure'] = tot_exp['Advertising_Expenditure']*100/tot_exp['Advertising_Expenditure'].sum()
        Y_chart4 = dcc.Graph(
            figure = px.pie(
                tot_exp,
                names = 'Vehicle_Type', values = 'Advertising_Expenditure',
                title = 'Total Advertisment Expenditure for Each Vehicle',
                labels = dict(x = 'Vehicle Type', y = 'Expenditure')
            )
        )

        return [
            html.Div(className = 'chart-item', children = [html.Div(children = Y_chart1), html.Div(children = Y_chart2)],style={'display': 'flex'}),
            html.Div(className = 'chart-item', children = [html.Div(children = Y_chart3), html.Div(children = Y_chart4)],style={'display': 'flex'})
        ]


    
    

# Run the app
if __name__ == '__main__':
    app.run_server()
