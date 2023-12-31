Python 3.11.4 (v3.11.4:d2340ef257, Jun  6 2023, 19:15:51) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.
>>> import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output, State

# Load the data using pandas
data = pd.read_csv('/Users/lirui/Desktop/硕博/文凭材料/文憑/IBM-DATA-ANALYST-DATA/Data Visualization with Python/Week '
                   '5/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 24}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            placeholder='Select a report type'
        ),
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': str(year), 'value': year} for year in data['Year'].unique()],
            placeholder='Select year',
            disabled=True
        ),
        html.Button("Show Chart", id='show-chart-button'),
    ]),
    html.Div(id='output-container')
])

@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value'))
def update_input_container(selected_statistics):
    return selected_statistics != 'Yearly Statistics'

@app.callback(
    Output('output-container', 'children'),
    Input('show-chart-button', 'n_clicks'),
    [State('dropdown-statistics', 'value'),
     State('select-year', 'value')])
def update_output_container(n_clicks, selected_statistics, input_year):
    if not n_clicks:
        return []

    if selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'] == input_year]
        
        sales_by_year = yearly_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        fig1 = dcc.Graph(figure=px.line(sales_by_year, x='Year', y='Automobile_Sales', title="Yearly Automobile Sales"))

        sales_by_type = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        fig2 = dcc.Graph(figure=px.line(sales_by_type, x='Vehicle_Type', y='Automobile_Sales', title="Total Monthly Automobile Sales"))

        return html.Div([
            html.Div([fig1], className='chart-item'),
            html.Div([fig2], className='chart-item')
        ])

    elif selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        fig1 = dcc.Graph(figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', title="Average Automobile Sales over Recession Period"))

        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        fig2 = dcc.Graph(figure=px.line(average_sales, x='Vehicle_Type', y='Automobile_Sales', title="Average Number of Vehicles Sold by Vehicle Type"))

        # Chart 3: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        fig3 = dcc.Graph(figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type', title="Total Expenditure Share by Vehicle Type"))

        # Chart 4: Bar chart for the effect of unemployment rate on vehicle type and sales
        unemployment_by_type = recession_data.groupby('Vehicle_Type')['unemployment_rate'].mean().reset_index()
        fig4 = dcc.Graph(figure=px.bar(unemployment_by_type, x='Vehicle_Type', y='unemployment_rate', title="Effect of Unemployment Rate on Vehicle Type and Sales"))

        return html.Div([
            html.Div([fig1], className='chart-item'),
            html.Div([fig2], className='chart-item'),
            html.Div([fig3], className='chart-item'),
            html.Div([fig4], className='chart-item')
        ])

if __name__ == '__main__':
    app.run_server(debug=True)

